"use client";

import { useEffect, useState } from "react";
import { salesAPI } from "@/lib/api";
import { Sale } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { ShoppingCart, Bot, User } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";

export default function SalesPage() {
    const [sales, setSales] = useState<Sale[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        loadSales();
    }, []);

    const loadSales = async () => {
        try {
            setLoading(true);
            const data = await salesAPI.getAll();
            setSales(data);
            setError(null);
        } catch (err: any) {
            setError(err.message || "Failed to load sales");
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="p-8 space-y-6">
                <Skeleton className="h-8 w-32" />
                <Card>
                    <CardHeader>
                        <Skeleton className="h-6 w-48" />
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {[1, 2, 3].map((i) => (
                                <Skeleton key={i} className="h-16 w-full" />
                            ))}
                        </div>
                    </CardContent>
                </Card>
            </div>
        );
    }

    if (error) {
        return (
            <div className="p-8">
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                    <p className="text-red-800">Error: {error}</p>
                    <button
                        onClick={loadSales}
                        className="mt-2 text-sm text-red-600 hover:text-red-800 underline"
                    >
                        Retry
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="p-8 space-y-6">
            <h1 className="text-3xl font-bold">Sales</h1>

            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <ShoppingCart className="h-5 w-5" />
                        All Sales ({sales.length})
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    {sales.length === 0 ? (
                        <div className="text-center py-12">
                            <ShoppingCart className="mx-auto h-12 w-12 text-gray-400" />
                            <h3 className="mt-4 text-lg font-medium">No sales yet</h3>
                            <p className="mt-2 text-sm text-muted-foreground">
                                Sales will appear here once customers start purchasing
                            </p>
                        </div>
                    ) : (
                        <div className="rounded-md border">
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead>Date</TableHead>
                                        <TableHead>Customer</TableHead>
                                        <TableHead>Items</TableHead>
                                        <TableHead>Total</TableHead>
                                        <TableHead>Payment</TableHead>
                                        <TableHead>Source</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {sales.map((sale) => (
                                        <TableRow key={sale.id}>
                                            <TableCell>
                                                {sale.timestamp
                                                    ? new Date(sale.timestamp).toLocaleDateString()
                                                    : "-"}
                                            </TableCell>
                                            <TableCell>
                                                {sale.customer_name || sale.customer_id || "Unknown"}
                                            </TableCell>
                                            <TableCell>
                                                <div className="space-y-1">
                                                    {sale.items.map((item, idx) => (
                                                        <div key={idx} className="text-sm">
                                                            {item.name} x{item.quantity}
                                                        </div>
                                                    ))}
                                                </div>
                                            </TableCell>
                                            <TableCell className="font-semibold">
                                                ₦{sale.total_amount.toLocaleString()}
                                            </TableCell>
                                            <TableCell>{sale.payment_method || "-"}</TableCell>
                                            <TableCell>
                                                <div className="flex items-center gap-1">
                                                    {sale.source === "chatbot" ? (
                                                        <>
                                                            <Bot className="h-4 w-4 text-blue-600" />
                                                            <span className="text-sm">Chatbot</span>
                                                        </>
                                                    ) : (
                                                        <>
                                                            <User className="h-4 w-4 text-green-600" />
                                                            <span className="text-sm">Manual</span>
                                                        </>
                                                    )}
                                                </div>
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
