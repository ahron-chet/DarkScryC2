"use client"; // This ensures the component runs on the client side

import { signOut } from "next-auth/react";

export default function LogoutButton() {
  return (
    <button onClick={() => signOut()} className="btn btn-danger">
      Sign Out
    </button>
  );
}
