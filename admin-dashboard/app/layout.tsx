import type { Metadata } from "next";
import "./globals.css";
import { AppSidebar } from "@/components/app-sidebar";
import { SidebarProvider } from "@/components/ui/sidebar";

export const metadata: Metadata = {
  title: "Imran Store Admin",
  description: "Admin dashboard for Imran Store - Clothing and Footwear",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">
        <SidebarProvider>
          <div className="flex min-h-screen w-full">
            <AppSidebar />
            <main className="flex-1 overflow-y-auto bg-gray-50">
              {children}
            </main>
          </div>
        </SidebarProvider>
      </body>
    </html>
  );
}
