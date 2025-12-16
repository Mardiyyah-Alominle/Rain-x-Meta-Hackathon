"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
    LayoutDashboard,
    Package,
    ShoppingCart,
    PlusCircle,
    Bot,
} from "lucide-react";
import {
    Sidebar,
    SidebarContent,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    SidebarHeader,
} from "@/components/ui/sidebar";

const menuItems = [
    {
        title: "Dashboard",
        icon: LayoutDashboard,
        href: "/",
    },
    {
        title: "Products",
        icon: Package,
        href: "/products",
    },
    {
        title: "Add Product",
        icon: PlusCircle,
        href: "/products/new",
    },
    {
        title: "Sales",
        icon: ShoppingCart,
        href: "/sales",
    },
    {
        title: "Record Sale",
        icon: PlusCircle,
        href: "/sales/new",
    },
];

export function AppSidebar() {
    const pathname = usePathname();

    return (
        <Sidebar>
            <SidebarHeader className="border-b px-6 py-4">
                <div className="flex items-center gap-2">
                    <Bot className="h-6 w-6" />
                    <div>
                        <h2 className="text-lg font-semibold">AestheticBot</h2>
                        <p className="text-xs text-muted-foreground">Admin Dashboard</p>
                    </div>
                </div>
            </SidebarHeader>
            <SidebarContent>
                <SidebarGroup>
                    <SidebarGroupLabel>Navigation</SidebarGroupLabel>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            {menuItems.map((item) => (
                                <SidebarMenuItem key={item.href}>
                                    <SidebarMenuButton
                                        asChild
                                        isActive={pathname === item.href}
                                    >
                                        <Link href={item.href}>
                                            <item.icon className="h-4 w-4" />
                                            <span>{item.title}</span>
                                        </Link>
                                    </SidebarMenuButton>
                                </SidebarMenuItem>
                            ))}
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>
            </SidebarContent>
        </Sidebar>
    );
}
