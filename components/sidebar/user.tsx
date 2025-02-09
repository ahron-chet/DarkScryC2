"use client";

import { useSession, signOut } from "next-auth/react";
import React, { useEffect, useState } from "react";

export default function UserDropdown() {
  const [full_name, set_full_name] = useState("Loading...");
  const [user_role, set_user_role] = useState("Loading...");

  const handleSignOut = async () => {
    await signOut();
  };

  useEffect(() => {
    fetch("/api/me")
      .then((res) => {
        if (!res.ok) throw new Error("Not authenticated");
        return res.json();
      })
      .then((data) => {
        set_full_name(`${data.first_name || "Unknown"} ${data.last_name || ""}`);
        set_user_role(data.role);
      })
      .catch(() => set_full_name("Unknown"));
  }, []);

  return (
    <div className="user-info dropdown dropup">
      {/* This "h6" triggers the dropdown (Bootstrap logic) */}
      <h6 className="dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
        {full_name}
      </h6>

      <small>{user_role}</small>

      <ul className="dropdown-menu dropdown-menu-dark">
        <li>
          <a className="dropdown-item" href="#">
            <i className="bi bi-gear"></i> Settings
          </a>
        </li>
        <li>
          <a className="dropdown-item" href="#">
            <i className="bi bi-person"></i> Profile
          </a>
        </li>
        <li>
          {/* Convert sign out from a link to a button or an <a> with onClick */}
          <button
            type="button"
            className="dropdown-item"
            onClick={handleSignOut}
          >
            <i className="bi bi-box-arrow-right"></i> Sign out
          </button>
        </li>
      </ul>
    </div>
  );
}
