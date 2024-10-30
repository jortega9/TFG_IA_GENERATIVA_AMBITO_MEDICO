import React, { useState } from 'react';
import { TextField, Button, Typography, Box } from '@mui/material';
import { json, useNavigate } from 'react-router-dom';
import AsistenteIcon from '../../public/assets/AsistenteIcon.png';
import './AuthPage.css'; // Importa el archivo CSS

const AuthPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMsg, setErrorMsg] = useState('');
    const [isLogIn, setIsLogIn] = useState(true);
    const navigate = useNavigate();

    function setUser(user) {
        sessionStorage.setItem('user', JSON.stringify(user));
    }

    const checkUserExistence = async (email) => {
        try{
            const response = await fetch('/api/login/user-exist', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Accept': 'application/json',
                },
                body: JSON.stringify({ email })
              });

            const userExist = await response.json();
            return userExist;

        }
        catch(error){
            console.error("Error comprobando la existencia del usuario:", error);
            return;
        }
    }

    async function loginUser(info){
        try{
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify(info)
            })
            if(response.status === 401){
                setErrorMsg("Usuario o Contraseña incrrectos");
                return null;
            }
            if(response.status === 500){
                setErrorMsg("Error de servidor");
                return null;
            }
            if(response.status === 404){
                setErrorMsg("Error de conexión, servidor no encontrado");
                return null;
            }
            const user = await response.json();
            return user; 

        }
        catch(error){
            console.error("Error al realizar el loginUser: ", error);
        }
    }

    const handleLogin = async (e) => {
        e.preventDefault();

        const user = await loginUser({
            email: email,
            password: password,
        });

        if (email) {
            setUser(user);
            navigate('/Tobichat');
        }
    };

    const handleRegisterRedirect = () => {
        navigate('/register');
    };

    return (
        <Box className="auth-page-container">
            <div className="avatar-login">
                <img src={AsistenteIcon} alt="Bot avatar" className="avatar-image" />
            </div>
            <Typography variant="h4" className="title">
                UroloBot
            </Typography>
            <div className="input-container">
                <TextField
                    className="input-user"
                    label="Correo Electrónico"
                    type="email"
                    variant="outlined"
                    fullWidth
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <TextField
                    className="input-user"
                    label="Contraseña"
                    type="password"
                    variant="outlined"
                    fullWidth
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                {errorMsg && <p className='error-mesage'>{errorMsg}</p>}
                <Button
                    variant="contained"
                    fullWidth
                    onClick={handleLogin}
                    className="login-button"
                >
                    Iniciar Sesión
                </Button>
            </div>
            <Typography variant="body2" className="register-prompt">
                ¿No tienes cuenta?{' '}
                <Button variant="text" onClick={handleRegisterRedirect} className="register-button">
                    Regístrate
                </Button>
            </Typography>
        </Box>
    );
};

export default AuthPage;
