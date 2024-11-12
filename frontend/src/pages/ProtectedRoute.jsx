import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
    const [userJSON, setUserJSON] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const getActiveUser = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://127.0.0.1:8000/auth/active', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.ok) {
                const user = await response.json();
                setUserJSON(user);
            } else {
                setUserJSON(null);
            }
        } catch (error) {
            console.error('Error verificando autenticación', error);
            setUserJSON(null);
        } finally {
            setLoading(false);
        }
        };

        getActiveUser();
    }, []);

    if (loading) return <div>Loading...</div>;

    if (!userJSON) return <Navigate to="/login" replace />;

    return children;
};

export default ProtectedRoute;
