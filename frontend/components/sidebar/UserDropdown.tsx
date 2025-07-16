"use client";

import React, { useEffect, useState } from "react";
import JWT from "jsonwebtoken";
import useUserApi, { IUser } from "lib/useUserApi";
import UserProfileModal from "./ProfileModal";
import { getAccessToken, logout } from "@/lib/authClient";

export default function UserDropdown() {
  const [fullName, setFullName] = useState("Loading...");
  const [userRole, setUserRole] = useState("Loading...");
  const [userId, setUserId] = useState<string | null>(null);
  const [userData, setUserData] = useState<IUser | null>(null);
  const [showProfile, setShowProfile] = useState(false);

  const { getUser } = useUserApi();
  const handleSignOut = () => {
    logout();
  };

  // 1) Decode token to get user_id
  useEffect(() => {
    const token = getAccessToken();
    if (!token) return;
    const decoded = JWT.decode(token) as { sub?: string } | null;
    if (decoded && decoded.sub) {
      setUserId(decoded.sub);
    }
  }, []);

  // 2) If we have a user_id, load the user from the API
  useEffect(() => {
    if (userId) {
      getUser(userId)
        .then((fetchedUser) => {
          setUserData(fetchedUser);
          const firstName = fetchedUser.first_name || "Unknown";
          const lastName = fetchedUser.last_name || "";
          setFullName(`${firstName} ${lastName}`);
          setUserRole(fetchedUser.role || "Unknown");
        })
        .catch((err) => {
          console.error("Failed to get user data", err);
          setFullName("Unknown");
          setUserRole("Unknown");
        });
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
