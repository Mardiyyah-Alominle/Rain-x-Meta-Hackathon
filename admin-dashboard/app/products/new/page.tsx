"use client";

import { productAPI } from "@/lib/api";
import { ProductForm } from "@/components/product-form";

export default function NewProductPage() {
    const handleSubmit = async (data: any) => {
        await productAPI.create(data);
    };

    return (
        <div className="p-8 space-y-6">
            <h1 className="text-3xl font-bold">Add New Product</h1>
            <ProductForm onSubmit={handleSubmit} submitLabel="Create Product" />
        </div>
    );
}
