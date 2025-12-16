from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List
from firebase_admin import firestore
from utils.db import db

router = APIRouter(prefix="/api/sales", tags=["sales"])

# --- Pydantic Models ---

class SaleItem(BaseModel):
    """Individual item in a sale"""
    product_id: str = Field(..., description="Product document ID")
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., gt=0, description="Quantity must be greater than 0")
    unit_price: float = Field(..., gt=0, description="Unit price must be greater than 0")

class ManualSaleCreate(BaseModel):
    """Schema for creating a manual sale"""
    customer_name: Optional[str] = Field(None, description="Customer name (optional)")
    items: List[SaleItem] = Field(..., min_length=1, description="List of items sold")
    payment_method: Optional[str] = Field("Cash", description="Payment method")
    notes: Optional[str] = Field(None, description="Additional notes")

class SaleResponse(BaseModel):
    """Schema for sale response"""
    id: str
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    items: List[dict]
    total_amount: float
    status: str
    payment_method: str
    source: str  # "chatbot" or "manual"
    notes: Optional[str] = None
    timestamp: Optional[str] = None

# --- API Endpoints ---

@router.post("/manual", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
async def create_manual_sale(sale: ManualSaleCreate):
    """
    Create a manual sale entry and decrement inventory.
    
    This endpoint is used when sales happen outside the chatbot (in-person, phone, etc.)
    """
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not established"
        )
    
    try:
        # Calculate total amount
        total_amount = sum(item.quantity * item.unit_price for item in sale.items)
        
        # Prepare sale data
        sale_data = {
            "customer_name": sale.customer_name,
            "items": [item.model_dump() for item in sale.items],
            "total_amount": total_amount,
            "status": "Confirmed",
            "payment_method": sale.payment_method or "Cash",
            "source": "manual",  # Mark as manual entry
            "notes": sale.notes,
            "timestamp": firestore.SERVER_TIMESTAMP
        }
        
        # Use batch write for atomicity (sale + inventory update)
        batch = db.batch()
        
        # 1. Create sale record
        sales_ref = db.collection("sales")
        new_sale_doc = sales_ref.document()
        batch.set(new_sale_doc, sale_data)
        
        # 2. Decrement inventory for each item
        products_ref = db.collection("products")
        for item in sale.items:
            product_doc_ref = products_ref.document(item.product_id)
            
            # Verify product exists and has enough stock
            product_doc = product_doc_ref.get()
            if not product_doc.exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product {item.product_id} not found"
                )
            
            product_data = product_doc.to_dict()
            current_stock = product_data.get("stock_count", 0)
            
            if current_stock < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for {item.name}. Available: {current_stock}, Requested: {item.quantity}"
                )
            
            # Decrement stock
            batch.update(product_doc_ref, {
                "stock_count": firestore.Increment(-item.quantity)
            })
        
        # Commit the batch
        batch.commit()
        
        # Fetch created sale
        created_doc = new_sale_doc.get()
        created_data = created_doc.to_dict()
        
        return SaleResponse(
            id=new_sale_doc.id,
            **{k: v for k, v in created_data.items() if k != "timestamp"},
            timestamp=str(created_data.get("timestamp")) if created_data.get("timestamp") else None
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating manual sale: {str(e)}"
        )


@router.get("/", response_model=List[SaleResponse])
async def list_sales(
    source: Optional[str] = None,
    limit: int = 100
):
    """
    List all sales with optional filtering.
    
    - **source**: Filter by source ("chatbot" or "manual")
    - **limit**: Maximum number of sales to return (default: 100)
    """
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not established"
        )
    
    try:
        sales_ref = db.collection("sales")
        query = sales_ref.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(limit)
        
        # Apply source filter if provided
        if source:
            query = query.where("source", "==", source)
        
        docs = query.stream()
        
        sales = []
        for doc in docs:
            sale_data = doc.to_dict()
            
            # Add source field if it doesn't exist (for backward compatibility with chatbot sales)
            if "source" not in sale_data:
                sale_data["source"] = "chatbot"
            
            sales.append(SaleResponse(
                id=doc.id,
                **{k: v for k, v in sale_data.items() if k != "timestamp"},
                timestamp=str(sale_data.get("timestamp")) if sale_data.get("timestamp") else None
            ))
        
        return sales
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching sales: {str(e)}"
        )


@router.get("/{sale_id}", response_model=SaleResponse)
async def get_sale(sale_id: str):
    """
    Get a single sale by ID.
    """
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not established"
        )
    
    try:
        doc_ref = db.collection("sales").document(sale_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sale with ID {sale_id} not found"
            )
        
        sale_data = doc.to_dict()
        
        # Add source field if it doesn't exist
        if "source" not in sale_data:
            sale_data["source"] = "chatbot"
        
        return SaleResponse(
            id=doc.id,
            **{k: v for k, v in sale_data.items() if k != "timestamp"},
            timestamp=str(sale_data.get("timestamp")) if sale_data.get("timestamp") else None
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching sale: {str(e)}"
        )
