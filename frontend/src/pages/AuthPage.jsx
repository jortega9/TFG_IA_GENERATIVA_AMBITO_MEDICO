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
    const [successMsg, setSuccessMsg] = useState('');
    const [isLogin, setIsLogin] = useState(true);
    const navigate = useNavigate();

    function setUser(user) {
        sessionStorage.setItem('user', JSON.stringify(user));
    }

    /**
     * Comprobar si el usuario existe en la base de datos.
     * 
     * @param {*} identifier 
     * @returns 
     */
    const checkUserExistence = async (identifier) => {
        try{
            const response = await fetch('http://127.0.0.1:8000/auth/user-exist', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify({ identifier })
            });

            const userExist = await response.json();
            return userExist.user_exists;

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
        setSuccessMsg('');
    }

    /**
     * 
     * Realizar el inicio de sesión del usuario.
     * 
     * @param {*} info 
     * @returns 
     */
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
            const user = await response.json();
            if (response.ok) {
                localStorage.setItem('token', user.access_token);
                return user;
            } else {
                throw new Error(user.detail || "Error en el login");
            }

        }
        catch(error){
            console.error("Error al realizar el loginUser: ", error);
            setErrorMsg("Error al iniciar sesión. Por favor, revisa tu email y contraseña.");
        }
    }

    const handleLogin = async (e) => {
        e.preventDefault();

        const user = await loginUser({
            email: email,
            password: password,
        });

        if (user) {
            navigate('/Urolobot');
        }
    };

    /**
     * Comprobar si es un email válido
     * 
     * @param {*} email 
     * @returns 
     */
    function isValidEmail(email) {
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailPattern.test(email);
    }

    /**
     * Comprobar información de registro de un usuario nuevo y realizar el registro.
     * 
     * @param {*} e 
     * @returns 
     */
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

        const newUser = await registerUser(name, email, password);
        setSuccessMsg("Usuario registrado con éxito. Por favor, inicia sesión.");
    }

    /**
     * Realizar el registro de un usuario nuevo.
     * 
     * @param {*} name 
     * @param {*} email 
     * @param {*} password 
     * @returns 
     */
    async function registerUser(name, email, password){
        try{
            const response = await fetch('http://127.0.0.1:8000/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password
                })
            });
            const user = await response.json();
            if (response.ok) {
                return user;
            } else {
                throw new Error(user.detail || "Error en el registro");
            }
        }
        catch(error){
            console.error("Error al realizar el registerUser: ", error);
            setErrorMsg("Error al registrarse. Por favor, verifica los datos introducidos.");
            setSuccessMsg('');
        }
    };

    return (
        <Box className="auth-page-container">
            <div className="avatar-login">
                <img src={AsistenteIcon} alt="Bot avatar" className="avatar-image" />
            </div>
            <Typography variant="h4" className="title">
                {isLogin ? 'Iniciar Sesión en UroloBot' : 'Regístrate en UroloBot'}
            </Typography>
    
            {isLogin ? (
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
                {successMsg && <p className="success-message"><strong>{successMsg}</strong></p>}
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
