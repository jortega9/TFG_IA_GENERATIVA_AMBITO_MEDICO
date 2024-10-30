import React, { useState } from 'react';
import { TextField, Button, Typography, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import AsistenteIcon from '../../public/assets/AsistenteIcon.png';
import './AuthPage.css'; // Importa el archivo CSS

const AuthPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const hardcodedEmail = 'jorge.amato@example.com';

    function setUser(user) {
        sessionStorage.setItem('user', JSON.stringify(user));
    }

    const handleLogin = async (e) => {
        e.preventDefault();

        const user = {
            email: email,
            password: password,
        };

        if (email === hardcodedEmail && password === '12345') {
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
