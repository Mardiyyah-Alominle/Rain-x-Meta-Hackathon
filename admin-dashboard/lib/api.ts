import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Product API
export const productAPI = {
    getAll: async (params?: { category?: string; low_stock?: number }) => {
        const response = await apiClient.get('/api/products', { params });
        return response.data;
    },

    getById: async (id: string) => {
        const response = await apiClient.get(`/api/products/${id}`);
        return response.data;
    },

    create: async (data: {
        name: string;
        selling_price: number;
        stock_count: number;
        image_url: string;
        description?: string;
        category?: string;
        sku?: string;
    }) => {
        const response = await apiClient.post('/api/products', data);
        return response.data;
    },

    update: async (id: string, data: Partial<{
        name: string;
        selling_price: number;
        stock_count: number;
        image_url: string;
        description?: string;
        category?: string;
        sku?: string;
    }>) => {
        const response = await apiClient.put(`/api/products/${id}`, data);
        return response.data;
    },

    delete: async (id: string) => {
        await apiClient.delete(`/api/products/${id}`);
    },
};

// Sales API
export const salesAPI = {
    getAll: async (params?: { source?: string; limit?: number }) => {
        const response = await apiClient.get('/api/sales', { params });
        return response.data;
    },

    getById: async (id: string) => {
        const response = await apiClient.get(`/api/sales/${id}`);
        return response.data;
    },

    createManual: async (data: {
        customer_name?: string;
        items: Array<{
            product_id: string;
            name: string;
            quantity: number;
            unit_price: number;
        }>;
        payment_method?: string;
        notes?: string;
    }) => {
        const response = await apiClient.post('/api/sales/manual', data);
        return response.data;
    },
};

// Analytics API
export const analyticsAPI = {
    getDashboard: async () => {
        const response = await apiClient.get('/api/analytics/dashboard');
        return response.data;
    },
};

export default apiClient;
