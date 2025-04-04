import React, { useState } from "react";
import { IUser } from "@/lib/useUserApi";
import useUserApi from "@/lib/useUserApi";
import { signOut } from "next-auth/react";


interface UserProfileModalProps {
    user: IUser;
    onClose: () => void;
}

export default function UserProfileModal({
    user,
    onClose
}: UserProfileModalProps) {
    const [showChangePasswordModal, setShowChangePasswordModal] = useState(false);
    const { deleteUser } = useUserApi();

    async function handleDeleteAccount() {
        if (!user.user_id) return;
        if (!confirm("Are you sure you want to delete this account?")) return;
        // await deleteUser(user.user_id);
        onClose();
        signOut();
    }

    return (
        <>
            {/* MAIN USER-PROFILE MODAL */}
            <div
                className="modal fade show user-profile-modal"
                style={{ display: "block" }}
                role="dialog"
            >
                <div className="modal-dialog modal-dialog-centered modal-md">
                    <div className="modal-content">
                        {/* HEADER */}
                        <div className="modal-header border-0">
                            <h5 className="modal-title">User Information</h5>
                            <button
                                type="button"
                                className="btn-close"
                                aria-label="Close"
                                onClick={onClose}
                            />
                        </div>

                        {/* BODY */}
                        <div className="modal-body">
                            {/* AVATAR + NAME/ROLE */}
                            <div className="d-flex align-items-center mb-4">
                                <img
                                    src="https://cdn-icons-png.flaticon.com/512/149/149071.png"
                                    alt="User Avatar"
                                    className="rounded-circle me-3"
                                    style={{ width: "64px", height: "64px", objectFit: "cover" }}
                                />
                                <div>
                                    <h4 className="mb-1">
                                        {user.first_name ?? "Unknown"} {user.last_name ?? ""}
                                    </h4>
                                    <span className="badge bg-primary">{user.role ?? "N/A"}</span>
                                </div>
                            </div>

                            {/* PERSONAL INFO */}
                            <section className="mb-4">
                                <h6 className="fw-bold mb-3">Personal Info</h6>
                                <div className="row g-3">
                                    <div className="col-md-6">
                                        <label className="form-label">First Name</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            value={user.first_name ?? ""}
                                            readOnly
                                        />
                                    </div>
                                    <div className="col-md-6">
                                        <label className="form-label">Last Name</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            value={user.last_name ?? ""}
                                            readOnly
                                        />
                                    </div>
                                    <div className="col-md-6">
                                        <label className="form-label">Email</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            value={user.email ?? ""}
                                            readOnly
                                        />
                                    </div>
                                    <div className="col-md-6">
                                        <label className="form-label">Country</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            value={user.country ?? ""}
                                            readOnly
                                        />
                                    </div>

                                    <div className="col-md-6">
                                        <label className="form-label">Password</label>
                                        <input
                                            type="password"
                                            className="form-control"
                                            value={user.password ? user.password : "********"}
                                            readOnly
                                        />
                                    </div>
                                    <div className="col-md-6 d-flex align-items-end">
                                        <button
                                            type="button"
                                            className="btn btn-link p-0 text-decoration-none"
                                            onClick={() => setShowChangePasswordModal(true)}
                                        >
                                            <i className="bi bi-key me-1"></i> Change Password
                                        </button>
                                    </div>
                                </div>
                            </section>

                            {/* COMPANY DETAILS */}
                            <section className="mb-4">
                                <h6 className="fw-bold mb-3">Company Details</h6>
                                <div className="row g-3">
                                    <div className="col-md-6">
                                        <label className="form-label">Company Name</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            value={user.company_name ?? ""}
                                            readOnly
                                        />
                                    </div>
                                    <div className="col-md-6">
                                        <label className="form-label">Industry</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            value={user.industry ?? ""}
                                            readOnly
                                        />
                                    </div>
                                </div>
                            </section>

                            {/* LICENSE EXPIRATION */}
                            <section>
                                <h6 className="fw-bold mb-3">License Expiration</h6>
                                <div className="row g-3">
                                    <div className="col-md-6">
                                        <label className="form-label">Expiration Date</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            // Example only
                                            value={"2026-06-15 00:00:00"}
                                            readOnly
                                        />
                                    </div>
                                </div>
                            </section>
                        </div>

                        {/* FOOTER */}
                        <div className="modal-footer border-0">
                            <button
                                type="button"
                                className="btn btn-outline-secondary me-auto"
                                onClick={() => { signOut() }}
                            >
                                Sign Out
                            </button>
                            <button type="button" className="btn btn-secondary" onClick={onClose}>
                                Close
                            </button>
                            <button
                                type="button"
                                className="btn btn-danger"
                                onClick={handleDeleteAccount}
                            >
                                Delete Account
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* BACKDROP + SUB-MODAL for Change Password */}
            {showChangePasswordModal && (
                <>
                    <div
                        className="modal-backdrop fade show"
                        style={{ zIndex: 1055 }}
                    />
                    <ChangePasswordModal user={user} onClose={() => setShowChangePasswordModal(false)} />
                </>
            )}
        </>
    );
}

/* 
   Sub-modal: uses useUserApi() directly to update the user’s password.
   Also shows a Bootstrap spinner while loading.
*/
function ChangePasswordModal({
    user,
    onClose,
}: {
    user: IUser;
    onClose: () => void;
}) {
    const { updateUser } = useUserApi();
    const [newPassword, setNewPassword] = useState("");
    const [confirmPass, setConfirmPass] = useState("");
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    async function handleSubmit() {
        setError(null);
        if (!newPassword || !confirmPass) {
            setError("Please fill in both fields.");
            return;
        }
        if (newPassword !== confirmPass) {
            setError("Passwords do not match.");
            return;
        }

        try {
            setLoading(true);
            if (user.user_id) {
                await updateUser(user.user_id, { password: newPassword });
            }
            onClose();
        } catch (err) {
            setError("Error updating password. Please try again.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div
            className="modal fade show"
            role="dialog"
            style={{ display: "block", zIndex: 1060 }}
            aria-modal="true"
        >
            <div className="modal-dialog modal-dialog-centered">
                <div className="modal-content">
                    {/* HEADER */}
                    <div className="modal-header">
                        <h5 className="modal-title">Change Password</h5>
                        <button
                            type="button"
                            className="btn-close"
                            aria-label="Close"
                            onClick={onClose}
                        />
                    </div>

                    {/* BODY */}
                    <div className="modal-body">
                        {loading ? (
                            <ModalLoader />
                        ) : (
                            <>
                                <div className="mb-3">
                                    <label className="form-label">New Password</label>
                                    <input
                                        type="password"
                                        className="form-control"
                                        value={newPassword}
                                        onChange={(e) => setNewPassword(e.target.value)}
                                    />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Confirm New Password</label>
                                    <input
                                        type="password"
                                        className="form-control"
                                        value={confirmPass}
                                        onChange={(e) => setConfirmPass(e.target.value)}
                                    />
                                </div>
                                {error && <div className="alert alert-danger">{error}</div>}
                            </>
                        )}
                    </div>

                    {/* FOOTER - hidden when loading */}
                    {!loading && (
                        <div className="modal-footer">
                            <button type="button" className="btn btn-secondary" onClick={onClose}>
                                Cancel
                            </button>
                            <button type="button" className="btn btn-primary" onClick={handleSubmit}>
                                Save Password
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

/**
 * A simple function that returns a standard Bootstrap spinner.
 * We name it "modal-loader" class, but it's just a spinner with some optional styling.
 */
function ModalLoader() {
    return (
        <div className="modal-loader d-flex justify-content-center align-items-center py-4">
            <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">Loading...</span>
            </div>
        </div>
    );
}
