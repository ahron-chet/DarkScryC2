"use client"; // This ensures the component runs on the client side

import { logout } from "@/lib/authClient";

export default function LogoutButton() {
  return (
    <button onClick={() => logout()} className="btn btn-danger">
      Sign Out
    </button>
  );
}
