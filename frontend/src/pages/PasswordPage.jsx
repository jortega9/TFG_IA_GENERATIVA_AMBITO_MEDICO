import React, { useState, useEffect } from 'react';
import AppHeader from '../components/AppHeader';
import { useNavigate } from 'react-router-dom';
import CloseIcon from '@mui/icons-material/Close';
import IconButton from '@mui/material/IconButton';

function PasswordPage() {
    const [userInfo, setUserInfo] = useState({
        email: '',
        password: '',
        password2: '',
    });

    const [errorMsg, setErrorMsg] = useState('');
    const [successMsg, setSuccessMsg] = useState('');

    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setUserInfo((prevInfo) => ({
            ...prevInfo,
            [name]: value,
        }));
    };

    const handleClose = () => {
        navigate('/');
    };

    /**
     * Realizar comprobaciones de nueva contraseña y cambiar la contraseña del usuario.
     * 
     * @returns 
     */
    async function changePswd(){
        try{

            setErrorMsg('');
            const token = localStorage.getItem('token');
            const thisUser = await fetch('http://127.0.0.1:8000/auth/active', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });
            
            const thisUserJSON = await thisUser.json();
            console.log(thisUserJSON.email);
            if(thisUserJSON.email !== userInfo.email){
                setErrorMsg("El correo electrónico no coincide con el usuario activo");
                return false;
            }

            if(userInfo.password !== userInfo.password2){
                setErrorMsg("Las contraseñas no coinciden");
                return false;
            }

            const response = await fetch('http://127.0.0.1:8000/auth/updatePwd', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    email: userInfo.email,
                    password: userInfo.password,
                })
            });
            
            console.log("Contraseña actualizada con éxito");
            return true;
        }
        catch(error){
            console.error("Error al realizar el change password: ", error);
        }
    }

    const handlePswdChange = async (e) => {
        try {
            let change = await changePswd();
            if(change){
                setSuccessMsg("Contraseña actualizada con éxito");
                console.log("Operación de cambio de contraseña completada");
            }
        } catch (error) {
            alert("Hubo un problema al actualizar el usuario. Inténtalo de nuevo.");
        }
    };

    return (
        <div className="app-container">
            <AppHeader />
            <div style={{  display: 'flex', direction: 'rtl',}}>
                <IconButton
                aria-label="close"
                onClick={handleClose}
                style={{ color: '#555' }}
                >
                    <CloseIcon />
                </IconButton>
            </div>
            <div style={{ maxWidth: '400px', margin: '0 auto' }}>
                <h2 className='account-title'>Cambiar Contraseña</h2>
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
                    <label className='account-items'>Nueva Contraseña:</label>
                    <input
                        type= 'password'
                        name="password"
                        value={userInfo.password}
                        onChange={handleChange}
                        style={{ width: '100%', marginBottom: '10px', padding: '8px' }}
                    />
                </div>

                <div style={{ position: 'relative' }}>
                    <label className='account-items'>Repetir Contraseña:</label>
                    <input
                        type='password'
                        name="password2"
                        value={userInfo.password2}
                        onChange={handleChange}
                        style={{ width: '100%', marginBottom: '10px', padding: '8px' }}
                    />
                </div>

                {errorMsg && <p className="error-message">{errorMsg}</p>}
                {successMsg && <p className="success-message"><strong>{successMsg}</strong></p>}

                <button
                    onClick={handlePswdChange}
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
                    Restaurar Contraseña
                </button>
            </div>
        </div>
    );
}

export default PasswordPage;
