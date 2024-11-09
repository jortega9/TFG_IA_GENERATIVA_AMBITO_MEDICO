import React, { useState } from 'react';
import AppHeader from '../components/AppHeader';
import '../styles/AccountPage.css';
import { useNavigate } from 'react-router-dom';

function AccountPage() {
    const [userInfo, setUserInfo] = useState({
        fullName: 'Jorge Ortega',
        username: 'jor123',
        email: 'jorge@example.com',
        password: '1234',
    });

    const navigate = useNavigate();

    const [showPassword, setShowPassword] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setUserInfo((prevInfo) => ({
            ...prevInfo,
            [name]: value,
        }));
    };

    const handleSave = () => {
        console.log('Información guardada:', userInfo);
        alert('Información guardada con éxito');
    };

    const handleDeleteUser = () => {
        console.log('Usuario eliminado:', userInfo);
        alert('Usuario eliminado con éxito');
        navigate('/login');
    }

    return (
        <div className="app-container">
            <AppHeader />
            <div style={{ maxWidth: '400px', margin: '0 auto' }}>
                <h2 className='account-title'>Información de Cuenta</h2>
                
                <div>
                    <label className='account-items'>Nombre Completo:</label>
                    <input
                        type="text"
                        name="fullName"
                        value={userInfo.fullName}
                        onChange={handleChange}
                        style={{ width: '100%', marginBottom: '10px', padding: '8px' }}
                    />
                </div>

                <div>
                    <label className='account-items'>Username:</label>
                    <input
                        type="text"
                        name="username"
                        value={userInfo.username}
                        onChange={handleChange}
                        style={{ width: '100%', marginBottom: '10px', padding: '8px' }}
                    />
                </div>

                <div>
                    <label className='account-items'>Correo Electrónico:</label>
                    <input
                        type="email"
                        name="email"
                        value={userInfo.email}
                        readOnly
                        style={{ width: '100%', marginBottom: '10px', padding: '8px', backgroundColor: '#d3d3d3' }}
                    />
                </div>

                <div style={{ position: 'relative' }}>
                    <label className='account-items'>Contraseña:</label>
                    <input
                        type={showPassword ? 'text' : 'password'}
                        name="password"
                        value={userInfo.password}
                        readOnly
                        style={{ width: '100%', marginBottom: '10px', padding: '8px', backgroundColor: '#d3d3d3' }}
                    />
                    <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        style={{
                            position: 'absolute',
                            left: '96%',
                            top: '45px',
                            background: 'none',
                            border: 'none',
                            cursor: 'pointer',
                        }}
                    >
                        {showPassword ? '🔓' : '🔒'}
                    </button>
                </div>

                <button
                    onClick={handleSave}
                    style={{
                        width: '108%',
                        padding: '10px',
                        backgroundColor: '#4CAF50',
                        color: 'white',
                        border: 'none',
                        cursor: 'pointer',
                        fontSize: '16px',
                        marginTop: '10px',
                    }}
                >
                    Guardar
                </button>
                <button
                    onClick={handleDeleteUser}
                    style={{
                        width: '108%',
                        padding: '10px',
                        backgroundColor: '#f44336',
                        color: 'white',
                        border: 'none',
                        cursor: 'pointer',
                        fontSize: '16px',
                        marginTop: '10px',
                    }}
                >
                    Eliminar Usuario
                </button>
            </div>
        </div>
    );
}

export default AccountPage;
