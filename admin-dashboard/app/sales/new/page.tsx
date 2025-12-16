"use client";

import { useState, useEffect, FormEvent } from "react";
import { useRouter } from "next/navigation";
import { productAPI, salesAPI } from "@/lib/api";
import { Product } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Trash2, Plus } from "lucide-react";

interface SaleItem {
    product_id: string;
    name: string;
    quantity: number;
    unit_price: number;
}

export default function NewSalePage() {
    const router = useRouter();
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(false);
    const [items, setItems] = useState<SaleItem[]>([]);
    const [customerName, setCustomerName] = useState("");
    const [paymentMethod, setPaymentMethod] = useState("Cash");
    const [notes, setNotes] = useState("");

    useEffect(() => {
        loadProducts();
    }, []);

    const loadProducts = async () => {
        try {
            const data = await productAPI.getAll();
            setProducts(data);
        } catch (err) {
            alert("Failed to load products");
        }
    };

    const addItem = () => {
        if (products.length === 0) {
            alert("No products available. Please add products first.");
            return;
        }

        const firstProduct = products[0];
        setItems([
            ...items,
            {
                product_id: firstProduct.id,
                name: firstProduct.name,
                quantity: 1,
                unit_price: firstProduct.selling_price,
            },
        ]);
    };

    const removeItem = (index: number) => {
        setItems(items.filter((_, i) => i !== index));
    };

    const updateItem = (index: number, field: keyof SaleItem, value: any) => {
        const newItems = [...items];

        if (field === "product_id") {
            const product = products.find((p) => p.id === value);
            if (product) {
                newItems[index] = {
                    ...newItems[index],
                    product_id: product.id,
                    name: product.name,
                    unit_price: product.selling_price,
                };
            }
        } else {
            newItems[index] = { ...newItems[index], [field]: value };
        }

        setItems(newItems);
    };

    const calculateTotal = () => {
        return items.reduce((sum, item) => sum + item.quantity * item.unit_price, 0);
    };

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();

        if (items.length === 0) {
            alert("Please add at least one item");
            return;
        }

        try {
            setLoading(true);

            await salesAPI.createManual({
                customer_name: customerName || undefined,
                items,
                payment_method: paymentMethod,
                notes: notes || undefined,
            });

            router.push("/sales");
        } catch (err: any) {
            alert("Error: " + (err.response?.data?.detail || err.message || "Failed to create sale"));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-8 space-y-6">
            <h1 className="text-3xl font-bold">Record Manual Sale</h1>

            <form onSubmit={handleSubmit} className="space-y-6">
                {/* Customer Information */}
                <Card>
                    <CardHeader>
                        <CardTitle>Customer Information</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="grid gap-4 md:grid-cols-2">
                            <div className="space-y-2">
                                <Label htmlFor="customer_name">Customer Name (Optional)</Label>
                                <Input
                                    id="customer_name"
                                    value={customerName}
                                    onChange={(e) => setCustomerName(e.target.value)}
                                    placeholder="e.g., John Doe"
                                />
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="payment_method">Payment Method</Label>
                                <Select value={paymentMethod} onValueChange={setPaymentMethod}>
                                    <SelectTrigger>
                                        <SelectValue />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="Cash">Cash</SelectItem>
                                        <SelectItem value="Bank Transfer">Bank Transfer</SelectItem>
                                        <SelectItem value="Card">Card</SelectItem>
                                        <SelectItem value="Mobile Money">Mobile Money</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="notes">Notes (Optional)</Label>
                            <Textarea
                                id="notes"
                                value={notes}
                                onChange={(e) => setNotes(e.target.value)}
                                placeholder="Additional notes about this sale..."
                                rows={3}
                            />
                        </div>
                    </CardContent>
                </Card>

                {/* Items */}
                <Card>
                    <CardHeader>
                        <div className="flex items-center justify-between">
                            <CardTitle>Items</CardTitle>
                            <Button type="button" onClick={addItem} size="sm">
                                <Plus className="mr-2 h-4 w-4" />
                                Add Item
                            </Button>
                        </div>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        {items.length === 0 ? (
                            <p className="text-center text-muted-foreground py-8">
                                No items added yet. Click "Add Item" to get started.
                            </p>
                        ) : (
                            items.map((item, index) => (
                                <div
                                    key={index}
                                    className="grid gap-4 md:grid-cols-12 items-end border-b pb-4"
                                >
                                    <div className="space-y-2 md:col-span-5">
                                        <Label>Product</Label>
                                        <Select
                                            value={item.product_id}
                                            onValueChange={(value) => updateItem(index, "product_id", value)}
                                        >
                                            <SelectTrigger>
                                                <SelectValue />
                                            </SelectTrigger>
                                            <SelectContent>
                                                {products.map((product) => (
                                                    <SelectItem key={product.id} value={product.id}>
                                                        {product.name} (₦{product.selling_price}) - Stock: {product.stock_count}
                                                    </SelectItem>
                                                ))}
                                            </SelectContent>
                                        </Select>
                                    </div>

                                    <div className="space-y-2 md:col-span-2">
                                        <Label>Quantity</Label>
                                        <Input
                                            type="number"
                                            min="1"
                                            value={item.quantity}
                                            onChange={(e) =>
                                                updateItem(index, "quantity", parseInt(e.target.value) || 1)
                                            }
                                        />
                                    </div>

                                    <div className="space-y-2 md:col-span-2">
                                        <Label>Unit Price (₦)</Label>
                                        <Input
                                            type="number"
                                            step="0.01"
                                            value={item.unit_price}
                                            onChange={(e) =>
                                                updateItem(index, "unit_price", parseFloat(e.target.value) || 0)
                                            }
                                        />
                                    </div>

                                    <div className="space-y-2 md:col-span-2">
                                        <Label>Subtotal</Label>
                                        <div className="font-semibold text-lg">
                                            ₦{(item.quantity * item.unit_price).toLocaleString()}
                                        </div>
                                    </div>

                                    <div className="md:col-span-1">
                                        <Button
                                            type="button"
                                            variant="outline"
                                            size="icon"
                                            onClick={() => removeItem(index)}
                                        >
                                            <Trash2 className="h-4 w-4 text-red-600" />
                                        </Button>
                                    </div>
                                </div>
                            ))
                        )}

                        {items.length > 0 && (
                            <div className="flex justify-end pt-4 border-t">
                                <div className="text-right">
                                    <p className="text-sm text-muted-foreground">Total Amount</p>
                                    <p className="text-2xl font-bold">
                                        ₦{calculateTotal().toLocaleString()}
                                    </p>
                                </div>
                            </div>
                        )}
                    </CardContent>
                </Card>

                {/* Submit */}
                <div className="flex gap-4">
                    <Button type="submit" disabled={loading || items.length === 0}>
                        {loading ? "Recording Sale..." : "Record Sale"}
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
            </form>
        </div>
    );
}
