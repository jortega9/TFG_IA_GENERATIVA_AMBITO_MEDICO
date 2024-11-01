import React from "react";
import { Navigate } from "react-router-dom";
import TobiChat from "./TobiChat";

function ProtectedRoute() {
    const user = sessionStorage.getItem('user');
    const userJSON = user ? JSON.parse(user) : null;

    return userJSON ? (
        <TobiChat/>
    ) : (
        <Navigate to="/login" replace />
    );
}

export default ProtectedRoute;