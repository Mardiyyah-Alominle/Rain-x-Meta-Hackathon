export interface Product {
    id: string;
    name: string;
    selling_price: number;
    stock_count: number;
    image_url: string;
    description?: string;
    category?: string;
    sku?: string;
    created_at?: string;
    updated_at?: string;
}

export interface SaleItem {
    product_id: string;
    name: string;
    quantity: number;
    unit_price: number;
}

export interface Sale {
    id: string;
    customer_id?: string;
    customer_name?: string;
    items: SaleItem[];
    total_amount: number;
    status: string;
    payment_method: string;
    source: 'chatbot' | 'manual';
    notes?: string;
    timestamp?: string;
}

export interface DashboardStats {
    total_sales: number;
    total_revenue: number;
    total_products: number;
    low_stock_products: number;
    out_of_stock_products: number;
    recent_sales: Array<{
        id: string;
        customer_name: string;
        total_amount: number;
        items_count: number;
        source: string;
        timestamp?: string;
    }>;
    sales_trend: Array<{
        date: string;
        day: string;
        sales_count: number;
        revenue: number;
    }>;
    top_products: Array<{
        product_id: string;
        name: string;
        quantity_sold: number;
        revenue: number;
    }>;
}
