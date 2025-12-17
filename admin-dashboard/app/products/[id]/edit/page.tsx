"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { productAPI } from "@/lib/api";
import { Product } from "@/lib/types";
import { ProductForm } from "@/components/product-form";
import { Skeleton } from "@/components/ui/skeleton";

// Required for static export with dynamic routes
export function generateStaticParams() {
    return [];
}

export default function EditProductPage() {
    const params = useParams();
    const productId = params.id as string;
    const [product, setProduct] = useState<Product | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (productId) {
            loadProduct();
        }
    }, [productId]);

    const loadProduct = async () => {
        try {
            setLoading(true);
            const data = await productAPI.getById(productId);
            setProduct(data);
            setError(null);
        } catch (err: any) {
            setError(err.message || "Failed to load product");
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (data: any) => {
        await productAPI.update(productId, data);
    };

    if (loading) {
        return (
            <div className="p-8 space-y-6 h-auto">
                <Skeleton className="h-8 w-48" />
                <Skeleton className="h-96 w-full" />
            </div>
        );
    }

    if (error || !product) {
        return (
            <div className="p-8">
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                    <p className="text-red-800">Error: {error || "Product not found"}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="p-8 space-y-6">
            <h1 className="text-3xl font-bold">Edit Product</h1>
            <ProductForm
                product={product}
                onSubmit={handleSubmit}
                submitLabel="Update Product"
            />
        </div>
    );
}
