import React, { useState, useEffect } from 'react';
import AppHeader from '../components/AppHeader';
import '../styles/AccountPage.css';
import { useNavigate } from 'react-router-dom';

function AccountPage() {
    const [userInfo, setUserInfo] = useState({});

    const navigate = useNavigate();

    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(true);
    const [dataObtained, setDataObteined] = useState(false);

    useEffect(() => {
        const getInfo = async () => {
            if (dataObtained) return; // Si ya se obtuvieron los datos, no vuelve a cargarlos
            try {
                const token = localStorage.getItem('token');
                const response = await fetch('http://127.0.0.1:8000/auth/info', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });

                const data = await response.json();
                setUserInfo(data);
                setDataObteined(true); 
            } catch (error) {
                console.error("Error al obtener la información del usuario: ", error);
                alert("Hubo un problema al cargar la información del usuario.");
            } finally {
                setLoading(false);
            }
        };

        getInfo();
    }, [dataObtained]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setUserInfo((prevInfo) => ({
            ...prevInfo,
            [name]: value,
        }));
    };

    async function saveUser(){
        try{

            const token = localStorage.getItem('token');
            const response = await fetch('http://127.0.0.1:8000/auth/update', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    name: userInfo.name,
                    username: userInfo.username,
                    email: userInfo.email,
                })
            });

            console.log("Usuario actualizado con éxito");
            return true;
        }
        catch(error){
            console.error("Error al realizar el saveUser: ", error);
        }
    }

    const handleSave = async (e) => {
        try {
            await saveUser();
            console.log("Operación de guardado completada");
        } catch (error) {
            alert("Hubo un problema al actualizar el usuario. Inténtalo de nuevo.");
        }
    };

    async function deleteUser(){
        try{
            const token = localStorage.getItem('token');
            const response = await fetch('http://127.0.0.1:8000/auth/delete', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
            });

            console.log("Usuario eliminado con éxito");
            return true;
        }
        catch(error){
            console.error("Error al realizar el deleteUser: ", error);
        }
    }

    const handleDeleteUser = async (e) => {
        try {
            e.preventDefault();
            await deleteUser();
            navigate('/login');
        } catch (error) {
            alert("Hubo un problema al actualizar el usuario. Inténtalo de nuevo.");
        }
        
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div className="app-container">
            <AppHeader />
            <div style={{ maxWidth: '400px', margin: '0 auto' }}>
                <h2 className='account-title'>Información de Cuenta</h2>
                
                <div>
                    <label className='account-items'>Nombre Completo:</label>
                    <input
                        type="text"
                        name="name"
                        value={userInfo.name}
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
                        type="text"
                        name="email"
                        value={userInfo.email}
                        onChange={handleChange}
                        style={{ width: '100%', marginBottom: '10px', padding: '8px' }}
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
