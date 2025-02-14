"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect } from "react";

import UserDropdown from "components/sidebar/UserDropdown";
import { side_bar_effect } from "lib/custome_effects"


export default function Sidebar() {
  const pathname = usePathname();
  // A small helper to decide if a link is active
  function isActive(href: string) {
    // e.g., if the path starts with "/dashboard" or is exactly "/dashboard"
    return pathname === href || pathname.startsWith(href);
  }
  useEffect(() => {
    (async () => {
      const products = await side_bar_effect();
    })()
  }, [])

  return (
    <nav id="sidebarMenu" className="sidebar">
      <div className="sidebar-content d-flex flex-column">
        {/* LOGO AREA */}
        <div className="logo-area">
          <img
            src="/images/logo.png"
            alt="DarkSCRY Logo"
            className="logo-img"
          />
          {/* TOGGLE BUTTON (optionally wire this up to a state hook) */}
          <button className="toggle-btn" id="toggleSidebar">
            <i className="bi bi-list"></i>
          </button>
        </div>
        {/* SEARCH BAR */}
        <div className="sidebar-search">
          <i className="bi bi-search"></i>
          <input type="text" placeholder="Search..." />
        </div>
        {/* NAV LINKS */}
        <div className="nav-list">
          <ul className="nav flex-column mb-auto">

            {/* Dashboard */}
            <li className="nav-item" id="dashboard">
              <Link
                href="/dashboard"
                className={`nav-link ${isActive("/dashboard") ? "active" : ""}`}
              >
                <i className="bi bi-speedometer2"></i>
                <span>Dashboard</span>
              </Link>
            </li>

            {/* Alerts */}
            <li className="nav-item" id="alerts">
              <Link
                href="/alerts"
                className={`nav-link ${isActive("/alerts") ? "active" : ""}`}
              >
                <i className="bi bi-exclamation-triangle"></i>
                <span>Alerts</span>
              </Link>
            </li>

            {/* Clients */}
            <li className="nav-item" id="clients">
              <Link
                href="/clients"
                className={`nav-link ${isActive("/clients") ? "active" : ""}`}
              >
                <i className="bi bi-laptop"></i>
                <span>Clients</span>
              </Link>
            </li>

            {/* Assets (Submenu) */}
            <li className="nav-item" id="assets">
              <a
                href="#assetsSubmenu"
                className="nav-link d-flex justify-content-between align-items-center"
                data-bs-toggle="collapse"
              >
                <div>
                  <i className="bi bi-box-seam"></i>
                  <span>Assets</span>
                </div>
                <i className="bi bi-chevron-down"></i>
              </a>
              <ul className="submenu collapse list-unstyled" id="assetsSubmenu">
                <li>
                  <Link href="/assets/discovery" className="nav-link">
                    Discovery
                  </Link>
                </li>
                <li>
                  <Link href="/assets/asm" className="nav-link">
                    ASM
                  </Link>
                </li>
              </ul>
            </li>

            {/* Integrations */}
            <li className="nav-item" id="integrations">
              <Link
                href="/integrations"
                className={`nav-link ${
                  isActive("/integrations") ? "active" : ""
                }`}
              >
                <i className="bi bi-puzzle"></i>
                <span>Integrations</span>
              </Link>
            </li>

            {/* Accounts */}
            <li className="nav-item" id="accounts">
              <Link
                href="/accounts"
                className={`nav-link ${isActive("/accounts") ? "active" : ""}`}
              >
                <i className="bi bi-people"></i>
                <span>Accounts</span>
              </Link>
            </li>
          </ul>
        </div>
        {/* USER SECTION */}
        <div className="user-section" id="side-bar-user-section">
          
          <div className="profile-pic-container">
            <img
              src="https://cdn-icons-png.flaticon.com/512/149/149071.png"
              alt="User"
              className="profile-pic"
            />
          </div>
          <UserDropdown />
        </div>
      </div>
    </nav>
  );
}
