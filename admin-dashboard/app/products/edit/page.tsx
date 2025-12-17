import { Suspense } from "react";
import EditProductClient from "./client";

export default function EditProductPage() {
    return (
        <Suspense fallback={
            <div className="p-8 space-y-6 h-auto">
                <div className="h-8 w-48 bg-gray-200 animate-pulse rounded" />
                <div className="h-96 w-full bg-gray-200 animate-pulse rounded" />
            </div>
        }>
            <EditProductClient />
        </Suspense>
    );
}
