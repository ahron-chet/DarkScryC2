import React from 'react';

interface LoadingProps {
    text: string;
}

export default function Loading({ text }: LoadingProps) {
    return (
        <div className="card bg-dark text-white" style={{ borderRadius: 16 }}>
            <div className="card-body">
                <div className="d-flex align-items-center gap-2 text-secondary">
                    <div className="spinner-border spinner-border-sm" role="status"></div>
                    <span>{text}</span>
                </div>
            </div>
        </div>
    );
}

