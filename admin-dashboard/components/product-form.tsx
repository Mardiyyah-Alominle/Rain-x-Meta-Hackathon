"use client";

import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import { Product } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface ProductFormProps {
    product?: Product;
    onSubmit: (data: any) => Promise<void>;
    submitLabel: string;
}

export function ProductForm({ product, onSubmit, submitLabel }: ProductFormProps) {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        name: product?.name || "",
        selling_price: product?.selling_price || "",
        stock_count: product?.stock_count || "",
        image_url: product?.image_url || "",
        description: product?.description || "",
        category: product?.category || "",
        sku: product?.sku || "",
    });

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();

        try {
            setLoading(true);

            // Validate required fields
            if (!formData.name || !formData.selling_price || !formData.stock_count || !formData.image_url) {
                alert("Please fill in all required fields");
                return;
            }

            const submitData = {
                name: formData.name,
                selling_price: parseFloat(formData.selling_price as string),
                stock_count: parseInt(formData.stock_count as string),
                image_url: formData.image_url,
                ...(formData.description && { description: formData.description }),
                ...(formData.category && { category: formData.category }),
                ...(formData.sku && { sku: formData.sku }),
            };

            await onSubmit(submitData);
            router.push("/products");
        } catch (err: any) {
            alert("Error: " + (err.message || "Failed to save product"));
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <Card>
                <CardHeader>
                    <CardTitle>Product Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="grid gap-4 md:grid-cols-2">
                        <div className="space-y-2">
                            <Label htmlFor="name">
                                Product Name <span className="text-red-500">*</span>
                            </Label>
                            <Input
                                id="name"
                                value={formData.name}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                placeholder="e.g., Sage Tote Bag"
                                required
                            />
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="sku">SKU (Optional)</Label>
                            <Input
                                id="sku"
                                value={formData.sku}
                                onChange={(e) => setFormData({ ...formData, sku: e.target.value })}
                                placeholder="e.g., STB-001"
                            />
                        </div>
                    </div>

                    <div className="grid gap-4 md:grid-cols-2">
                        <div className="space-y-2">
                            <Label htmlFor="selling_price">
                                Selling Price (₦) <span className="text-red-500">*</span>
                            </Label>
                            <Input
                                id="selling_price"
                                type="number"
                                step="0.01"
                                value={formData.selling_price}
                                onChange={(e) => setFormData({ ...formData, selling_price: e.target.value })}
                                placeholder="e.g., 2500"
                                required
                            />
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="stock_count">
                                Stock Count <span className="text-red-500">*</span>
                            </Label>
                            <Input
                                id="stock_count"
                                type="number"
                                value={formData.stock_count}
                                onChange={(e) => setFormData({ ...formData, stock_count: e.target.value })}
                                placeholder="e.g., 50"
                                required
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="category">Category (Optional)</Label>
                        <Input
                            id="category"
                            value={formData.category}
                            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                            placeholder="e.g., Bags, Accessories"
                        />
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="image_url">
                            Image URL <span className="text-red-500">*</span>
                        </Label>
                        <Input
                            id="image_url"
                            type="url"
                            value={formData.image_url}
                            onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                            placeholder="https://example.com/image.jpg"
                            required
                        />
                        <p className="text-xs text-muted-foreground">
                            Enter a direct URL to the product image
                        </p>
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="description">Description (Optional)</Label>
                        <Textarea
                            id="description"
                            value={formData.description}
                            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                            placeholder="Product description..."
                            rows={4}
                        />
                    </div>

                    <div className="flex gap-4 pt-4">
                        <Button type="submit" disabled={loading}>
                            {loading ? "Saving..." : submitLabel}
                        </Button>
                        <Button
                            type="button"
                            variant="outline"
                            onClick={() => router.back()}
                            disabled={loading}
                        >
                            Cancel
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </form>
    );
}
