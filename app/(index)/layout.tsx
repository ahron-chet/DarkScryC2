"use client";

import Sidebar from "@/components/Sidebar";
import Script from "next/script";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import "animate.css/animate.css";
import "./../../style/components.Sidebar.css";
import { SessionProvider } from "next-auth/react";
import "bootstrap/dist/js/bootstrap.bundle.min.js";

export default function WithSidebarLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <SessionProvider refetchInterval={0} refetchOnWindowFocus={false}>
      {/* <Script
        src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
        strategy="afterInteractive"
      /> */}
      <Sidebar />
      <main className="main-content">{children}</main>
    </SessionProvider>
  );
}
