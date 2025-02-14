"use client";

import React, { useEffect, useState } from "react";
import { useSession, signOut } from "next-auth/react";
import useUserApi, { IUser } from "lib/useUserApi";
import UserProfileModal from "./ProfileModal";

export default function UserDropdown() {
  const [fullName, setFullName] = useState("Loading...");
  const [userRole, setUserRole] = useState("Loading...");
  const [userId, setUserId] = useState<string | null>(null);
  const [userData, setUserData] = useState<IUser | null>(null);
  const [showProfile, setShowProfile] = useState(false);

  const { getUser } = useUserApi();

  const { data: session, status } = useSession()
  // Sign-out logic
  const handleSignOut = async () => {
    await signOut();
  };

  // 1) Fetch /api/me to get the user_id
  useEffect(() => {
    if (!session?.user.accessToken){
      return;
    }
    fetch("/api/me")
      .then((res) => {
        if (!res.ok) throw new Error("Not authenticated");
        return res.json();
      })
      .then((data) => {
        if (data.user_id) {
          setUserId(data.user_id);
        }
        // For quick display in the dropdown:
        const firstName = data.first_name || "Unknown";
        const lastName = data.last_name || "";
        setFullName(`${firstName} ${lastName}`);
        setUserRole(data.role || "Unknown");
      })
      .catch(() => {
        setFullName("Unknown");
        setUserRole("Unknown");
      });
  }, [session?.user.accessToken]);

  // 2) If we have a user_id, load the user from the API
  useEffect(() => {
    if (userId) {
      getUser(userId)
        .then((fetchedUser) => setUserData(fetchedUser))
        .catch((err) => console.error("Failed to get user data", err));
    }
  }, [userId]);

  return (
    <>
      {/* Conditionally render the profile modal when showProfile is true */}
      {showProfile && userData && (
        <UserProfileModal user={userData} onClose={() => setShowProfile(false)} />
      )}

      <div className="user-info dropdown dropup">
        {/* The name triggers the dropdown */}
        <h6
          className="dropdown-toggle"
          data-bs-toggle="dropdown"
          aria-expanded="false"
          style={{ cursor: "pointer" }}
        >
          {fullName}
        </h6>
        <small>{userRole}</small>

        <ul className="dropdown-menu dropdown-menu-dark">
          <li>
            <a className="dropdown-item" href="#">
              <i className="bi bi-gear"></i> Settings
            </a>
          </li>
          <li>
            <a
              className="dropdown-item"
              href="#"
              onClick={() => {
                setShowProfile(true);
              }}
            >
              <i className="bi bi-person"></i> Profile
            </a>
          </li>
          <li>
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
    </>
  );
}
