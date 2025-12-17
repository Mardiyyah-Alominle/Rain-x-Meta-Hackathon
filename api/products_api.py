from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from firebase_admin import firestore
from utils.db import db
from api.auth import verify_api_key

router = APIRouter(prefix="/api/products", tags=["products"])

# --- Pydantic Models for Request/Response ---

class ProductCreate(BaseModel):
    """Schema for creating a new product"""
    name: str = Field(..., min_length=1, description="Product name")
    selling_price: float = Field(..., gt=0, description="Selling price must be greater than 0")
    stock_count: int = Field(..., ge=0, description="Stock count must be non-negative")
    image_url: str = Field(..., description="Product image URL from UploadThing")
    description: Optional[str] = Field(None, description="Product description")
    category: Optional[str] = Field(None, description="Product category")
    sku: Optional[str] = Field(None, description="Stock Keeping Unit")

class ProductUpdate(BaseModel):
    """Schema for updating an existing product"""
    name: Optional[str] = Field(None, min_length=1)
    selling_price: Optional[float] = Field(None, gt=0)
    stock_count: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    sku: Optional[str] = None

class ProductResponse(BaseModel):
    """Schema for product response"""
    id: str
    name: str
    selling_price: float
    stock_count: int
    image_url: str
    description: Optional[str] = None
    category: Optional[str] = None
    sku: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

# --- API Endpoints ---

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_api_key)])
async def create_product(product: ProductCreate):
    """
    Create a new product in the Firebase Firestore database.
    """
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not established"
        )
    
    try:
        # Prepare product data
        product_data = product.model_dump()
        product_data["created_at"] = firestore.SERVER_TIMESTAMP
        product_data["updated_at"] = firestore.SERVER_TIMESTAMP
        
        # Add to Firestore
        products_ref = db.collection("products")
        doc_ref = products_ref.add(product_data)
        
        # Get the created document ID
        product_id = doc_ref[1].id
        
        # Fetch the created document to return with timestamps
        created_doc = products_ref.document(product_id).get()
        created_data = created_doc.to_dict()
        
        return ProductResponse(
            id=product_id,
            **{k: v for k, v in created_data.items() if k != "created_at" and k != "updated_at"},
            created_at=str(created_data.get("created_at")),
            updated_at=str(created_data.get("updated_at"))
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating product: {str(e)}"
        )


@router.get("/", response_model=List[ProductResponse], dependencies=[Depends(verify_api_key)])
async def list_products(
    category: Optional[str] = None,
    low_stock: Optional[int] = None
):
    """
    List all products with optional filtering.
    
    - **category**: Filter by product category
    - **low_stock**: Filter products with stock less than or equal to this value
    """
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not established"
        )
    
    try:
        products_ref = db.collection("products")
        query = products_ref
        
        # Apply filters if provided
        if category:
            query = query.where("category", "==", category)
        
        if low_stock is not None:
            query = query.where("stock_count", "<=", low_stock)
        
        # Execute query
        docs = query.stream()
        
        products = []
        for doc in docs:
            product_data = doc.to_dict()
            products.append(ProductResponse(
                id=doc.id,
                **{k: v for k, v in product_data.items() if k != "created_at" and k != "updated_at"},
                created_at=str(product_data.get("created_at")) if product_data.get("created_at") else None,
                updated_at=str(product_data.get("updated_at")) if product_data.get("updated_at") else None
            ))
        
        return products
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching products: {str(e)}"
        )


@router.get("/{product_id}", response_model=ProductResponse, dependencies=[Depends(verify_api_key)])
async def get_product(product_id: str):
    """
    Get a single product by ID.
    """
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not established"
        )
    
    try:
        doc_ref = db.collection("products").document(product_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found"
            )
        
        product_data = doc.to_dict()
        return ProductResponse(
            id=doc.id,
            **{k: v for k, v in product_data.items() if k != "created_at" and k != "updated_at"},
            created_at=str(product_data.get("created_at")) if product_data.get("created_at") else None,
            updated_at=str(product_data.get("updated_at")) if product_data.get("updated_at") else None
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching product: {str(e)}"
        )


@router.put("/{product_id}", response_model=ProductResponse, dependencies=[Depends(verify_api_key)])
async def update_product(product_id: str, product: ProductUpdate):
    """
    Update an existing product.
    """
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not established"
        )
    
    try:
        doc_ref = db.collection("products").document(product_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found"
            )
        
        # Prepare update data (only include fields that were provided)
        update_data = {k: v for k, v in product.model_dump().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        # Add updated timestamp
        update_data["updated_at"] = firestore.SERVER_TIMESTAMP
        
        # Update the document
        doc_ref.update(update_data)
        
        # Fetch updated document
        updated_doc = doc_ref.get()
        updated_data = updated_doc.to_dict()
        
        return ProductResponse(
            id=product_id,
            **{k: v for k, v in updated_data.items() if k != "created_at" and k != "updated_at"},
            created_at=str(updated_data.get("created_at")) if updated_data.get("created_at") else None,
            updated_at=str(updated_data.get("updated_at")) if updated_data.get("updated_at") else None
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating product: {str(e)}"
        )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_api_key)])
async def delete_product(product_id: str):
    """
    Delete a product by ID.
    """
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not established"
        )
    
    try:
        doc_ref = db.collection("products").document(product_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found"
            )
        
        # Delete the document
        doc_ref.delete()
        
        return None
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting product: {str(e)}"
        )
