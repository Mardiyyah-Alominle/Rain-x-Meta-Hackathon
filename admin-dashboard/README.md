# Imran Store Admin Dashboard

A modern, full-stack admin dashboard for managing Imran Store - a clothing and footwear e-commerce platform.

## 🚀 Features

- **Product Management**: Create, edit, and delete products with images
- **Sales Tracking**: Record manual sales and view all transactions
- **Analytics Dashboard**: Real-time stats, sales trends, and top products
- **Beautiful UI**: Built with Next.js and shadcn/ui components
- **Firebase Integration**: Seamlessly integrated with existing chatbot database

## 📋 Prerequisites

- Node.js 18+ and npm
- Python 3.8+ (for backend)
- Firebase Firestore configured
- FastAPI backend running on `localhost:8000`

## 🛠️ Installation

```bash
# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the dashboard.

## 🏗️ Build

```bash
# Create production build
npm run build

# Start production server
npm start
```

## 📁 Project Structure

```
admin-dashboard/
├── app/                    # Next.js App Router pages
│   ├── page.tsx           # Dashboard home
│   ├── products/          # Product management
│   └── sales/             # Sales management
├── components/            # React components
│   ├── ui/               # shadcn/ui components
│   ├── app-sidebar.tsx   # Navigation sidebar
│   └── product-form.tsx  # Product form
└── lib/                  # Utilities
    ├── api.ts            # API client
    └── types.ts          # TypeScript types
```

## 🔧 Configuration

### Environment Variables

- `NEXT_PUBLIC_API_URL`: FastAPI backend URL (default: `http://localhost:8000`)

### Next.js Config

The `next.config.ts` is configured to allow external images from any domain for product images.

## 📖 Usage

### Starting the Backend

```bash
# From the project root
cd ..
uvicorn api.index:app --reload --port 8000
```

### Starting the Frontend

```bash
# From admin-dashboard directory
npm run dev
```

### Adding Products

1. Navigate to "Products" → "Add Product"
2. Fill in product details
3. Enter image URL (or upload when UploadThing is integrated)
4. Click "Create Product"

### Recording Manual Sales

1. Navigate to "Sales" → "Record Sale"
2. Add items from product dropdown
3. Set quantities and prices
4. Enter customer info (optional)
5. Click "Record Sale"

## 🎨 Tech Stack

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Charts**: Recharts
- **HTTP Client**: Axios
- **Icons**: Lucide React

## 🔗 API Endpoints

The dashboard communicates with these FastAPI endpoints:

- `GET /api/products` - List products
- `POST /api/products` - Create product
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product
- `GET /api/sales` - List sales
- `POST /api/sales/manual` - Create manual sale
- `GET /api/analytics/dashboard` - Dashboard stats

## 📝 License

MIT

## 👥 Contributing

Contributions are welcome! Please open an issue or submit a pull request.
