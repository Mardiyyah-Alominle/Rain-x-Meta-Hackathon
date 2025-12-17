from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime, timedelta
from firebase_admin import firestore
from utils.db import db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

# --- Pydantic Models ---

class DashboardStats(BaseModel):
    """Dashboard statistics response"""
    total_sales: int
    total_revenue: float
    total_products: int
    low_stock_products: int
    out_of_stock_products: int
    recent_sales: List[Dict[str, Any]]
    sales_trend: List[Dict[str, Any]]  # Last 7 days
    top_products: List[Dict[str, Any]]

# --- API Endpoints ---

@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats():
    """
    Get comprehensive dashboard statistics including:
    - Total sales count
    - Total revenue
    - Product inventory stats
    - Recent sales
    - Sales trend (last 7 days)
    - Top selling products
    """
    if db is None:
        logger.error("Database connection is None - Firebase not initialized")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not established. Please check Firebase configuration and environment variables."
        )
    
    logger.info("Fetching dashboard analytics...")
    
    try:
        # 1. Get total sales and revenue
        sales_ref = db.collection("sales")
        all_sales = list(sales_ref.stream())
        
        total_sales = len(all_sales)
        total_revenue = sum(sale.to_dict().get("total_amount", 0) for sale in all_sales)
        
        # 2. Get product statistics
        products_ref = db.collection("products")
        all_products = list(products_ref.stream())
        
        total_products = len(all_products)
        low_stock_products = 0
        out_of_stock_products = 0
        low_stock_threshold = 10
        
        for product in all_products:
            stock = product.to_dict().get("stock_count", 0)
            if stock == 0:
                out_of_stock_products += 1
            elif stock <= low_stock_threshold:
                low_stock_products += 1
        
        # 3. Get recent sales (last 10)
        recent_sales_query = sales_ref.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(10)
        recent_sales_docs = recent_sales_query.stream()
        
        recent_sales = []
        for sale in recent_sales_docs:
            sale_data = sale.to_dict()
            recent_sales.append({
                "id": sale.id,
                "customer_name": sale_data.get("customer_name", sale_data.get("customer_id", "Unknown")),
                "total_amount": sale_data.get("total_amount", 0),
                "items_count": len(sale_data.get("items", [])),
                "source": sale_data.get("source", "chatbot"),
                "timestamp": str(sale_data.get("timestamp")) if sale_data.get("timestamp") else None
            })
        
        # 4. Calculate sales trend (last 7 days)
        sales_trend = []
        today = datetime.now()
        
        for i in range(6, -1, -1):  # Last 7 days
            day = today - timedelta(days=i)
            day_start = datetime(day.year, day.month, day.day)
            day_end = day_start + timedelta(days=1)
            
            # Count sales for this day
            day_sales = [
                sale for sale in all_sales
                if sale.to_dict().get("timestamp") and
                day_start <= sale.to_dict()["timestamp"] < day_end
            ]
            
            day_revenue = sum(sale.to_dict().get("total_amount", 0) for sale in day_sales)
            
            sales_trend.append({
                "date": day.strftime("%Y-%m-%d"),
                "day": day.strftime("%a"),
                "sales_count": len(day_sales),
                "revenue": round(day_revenue, 2)
            })
        
        # 5. Calculate top selling products
        product_sales_count = {}
        
        for sale in all_sales:
            items = sale.to_dict().get("items", [])
            for item in items:
                product_id = item.get("product_id")
                if product_id:
                    if product_id not in product_sales_count:
                        product_sales_count[product_id] = {
                            "product_id": product_id,
                            "name": item.get("name", "Unknown"),
                            "quantity_sold": 0,
                            "revenue": 0
                        }
                    product_sales_count[product_id]["quantity_sold"] += item.get("quantity", 0)
                    product_sales_count[product_id]["revenue"] += item.get("quantity", 0) * item.get("unit_price", 0)
        
        # Sort by quantity sold and get top 5
        top_products = sorted(
            product_sales_count.values(),
            key=lambda x: x["quantity_sold"],
            reverse=True
        )[:5]
        
        # Round revenue values
        for product in top_products:
            product["revenue"] = round(product["revenue"], 2)
        
        return DashboardStats(
            total_sales=total_sales,
            total_revenue=round(total_revenue, 2),
            total_products=total_products,
            low_stock_products=low_stock_products,
            out_of_stock_products=out_of_stock_products,
            recent_sales=recent_sales,
            sales_trend=sales_trend,
            top_products=top_products
        )
    
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching dashboard stats: {str(e)}"
        )
