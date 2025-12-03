import AppNav from "./appnav.tsx";
import React from "react";
import { AuthenticatedRoute } from "../allauth_auth/routing.jsx";

const sidebarNavItems = [
  {
    title: "Home",
    href: "/",
  },
  {
    title: "Profile",
    href: "/dashboard/profile",
  },
  {
    title: "Employee App",
    href: "/dashboard/employees",
  },
  {
    title: "Navigation Demo",
    href: "/dashboard/navigation/tab1",
    fuzzyMatchActivePath: "/dashboard/navigation/",
  },
  {
    title: "Logout",
    href: "/account/logout",
  },
]

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen flex-col md:flex-row md:overflow-hidden container">
      <div className="w-full flex-none md:w-64">
        <AppNav items={sidebarNavItems}/>
      </div>
      <div className="w-full p-6 md:overflow-y-auto md:p-12">
        <AuthenticatedRoute>
          {children}
        </AuthenticatedRoute>
      </div>
    </div>
  );
}
