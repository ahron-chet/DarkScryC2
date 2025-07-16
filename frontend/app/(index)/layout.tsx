"use client";

import Sidebar from "@/components/Sidebar";
import useRequireAuth from "@/lib/hooks/useRequireAuth";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import "animate.css/animate.css";
import "./../../style/components.Sidebar.css";
import Script from 'next/script';

export default function WithSidebarLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  useRequireAuth();
  return (
    <>
      <Script
        src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
        strategy="afterInteractive"
      />
      <Sidebar />
      <main className="main-content">{children}</main>
    </>
  );
}
