import React, { useState } from 'react';
import { TextField, Button, Typography, Box } from '@mui/material';
import { json, useNavigate } from 'react-router-dom';
import AsistenteIcon from '../../public/assets/AsistenteIcon.png';
import '../styles/AuthPage.css';

const AuthPage = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [errorMsg, setErrorMsg] = useState('');
    const [isLogin, setIsLogin] = useState(true);
    const navigate = useNavigate();

    function setUser(user) {
        sessionStorage.setItem('user', JSON.stringify(user));
    }

    const checkUserExistence = async (email) => {
        try{
            const response = await fetch('http://127.0.0.1:8000/login/user-exist', {
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

    function clearInputs() {
        setName('');
        setEmail('');
        setPassword('');
        setConfirmPassword('');
        setErrorMsg('');
    }

    async function loginUser(info){
        try{
            console.log(info);
            console.log("antes del fetch");
            const response = await fetch('http://127.0.0.1:8000/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    identifier: info.email,
                    password: info.password
                })
            });
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

        if (user) {
            setUser(user);
            navigate('/Tobichat');
        }
    };

    function isValidEmail(email) {
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailPattern.test(email);
    }

    const handleRegister = async (e) => {
        e.preventDefault();
        setErrorMsg('');
        
        if(!isValidEmail(email)) {
            setErrorMsg('El email no es válido. Por favor, introduce otro email.');
            return;
        }

        if( password !== confirmPassword){
            setErrorMsg('Contraseñas diferentes');
            return;
        }

        const existUser = await checkUserExistence(email);
        if(existUser){
            setErrorMsg("Usuario ya registrado.");
            return;
        }

        const newUser = await createNewUser(name, email, password);
        setSuccessMsg("Se ha registrado con éxito.");
    }

    return (
        <Box className="auth-page-container">
            <div className="avatar-login">
                <img src={AsistenteIcon} alt="Bot avatar" className="avatar-image" />
            </div>
            <Typography variant="h4" className="title">
                {isLogin ? 'Iniciar Sesión en UroloBot' : 'Regístrate en UroloBot'}
            </Typography>
    
            {isLogin ? (
                // Formulario de Inicio de Sesión
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
                {errorMsg && <p className="error-message">{errorMsg}</p>}
                <Button
                    variant="contained"
                    fullWidth
                    onClick={handleLogin}
                    className="login-button"
                >
                    Iniciar Sesión
                </Button>
                <div className='centered-text'>
                    <Typography variant="body2" className="change-prompt">
                        ¿No tienes cuenta?{' '}
                        <Button variant="text" 
                            onClick={() => {
                                setIsLogin(false);
                                clearInputs();
                            }}
                            className="change-button"
                        >
                        Regístrate
                        </Button>
                    </Typography>
                </div>
                </div>
            ) : (
                // Formulario de Registro
                <div className="input-container">
                <TextField
                    className="input-user"
                    label="Nombre"
                    type="text"
                    variant="outlined"
                    fullWidth
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
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
                <TextField
                    className="input-user"
                    label="Confirmar Contraseña"
                    type="password"
                    variant="outlined"
                    fullWidth
                    required
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                />
                {errorMsg && <p className="error-message">{errorMsg}</p>}
                <Button
                    variant="contained"
                    fullWidth
                    onClick={handleRegister}
                    className="register-button"
                >
                    Registrarse
                </Button>
                <div className='centered-text'>
                    <Typography variant="body2" className="change-prompt">
                        ¿Ya tienes cuenta?{' '}
                        <Button variant="text" 
                            onClick={() => {
                                setIsLogin(true);
                                clearInputs();
                            }}
                            className="change-button"
                        >
                        Iniciar Sesión
                        </Button>
                    </Typography>
                </div>
                </div>
            )}
            </Box>
        );
    }

export default AuthPage;
