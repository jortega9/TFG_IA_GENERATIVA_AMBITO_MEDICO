import React, { useState } from 'react';
import { Button, Menu, MenuItem } from '@mui/material';
import { FiUser } from 'react-icons/fi';
import { useNavigate } from 'react-router-dom';

function AccountButton() {
    const [menu, setMenu] = useState(null);
    const open = Boolean(menu);

    const navigate = useNavigate();

    const handleClick = (event) => {
        setMenu(event.currentTarget);
    };

    const handleClose = () => {
        setMenu(null);
    };

    const handleAccount = () => {
        navigate('/account');
    };

    const handleChangePsw = () => {
        navigate('/passwd');
    };

    function getToken() {
        return localStorage.getItem('token');
    }

    async function logoutUser(){
        try{
            const token = getToken();

            const response = await fetch('http://127.0.0.1:8000/auth/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({})
            });
            if(response.ok){
                localStorage.removeItem('token');
            }
            const user = await response.json();
            return user; 

        }
        catch(error){
            console.error("Error al realizar el loginUser: ", error);
        }
    }

    const handleLogout = async (e) => {
        e.preventDefault();

        const user = await logoutUser({});

        if (user) {
            navigate('/login');
        }
    };

    return (
        <>
            <Button
                variant="contained"
                sx={{
                    backgroundColor: 'white',
                    color: 'grey',
                    borderRadius: '50%',
                    padding: '5px',
                    border: '2px solid grey',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    minWidth: '40px',
                    minHeight: '40px',
                    '&:hover': {
                        backgroundColor: '#f5f5f5',
                    },
                }}
                onClick={handleClick}
            >
                <FiUser size={20} />
            </Button>

            <Menu
                anchorEl={menu}
                open={open}
                onClose={handleClose}
                sx={{
                    '& .MuiPaper-root': { // background del menu
                        backgroundColor: 'grey',
                        border: '1px solid #333333',
                        color: 'white',
                    },
                    '& .MuiMenuItem-root': { //textos del menu
                        color: 'white',
                        '&:hover': {
                            backgroundColor: '#666666',
                        },
                    },
                }}
            >
                <MenuItem onClick={handleAccount}>Mi Cuenta</MenuItem>
                <MenuItem onClick={handleChangePsw}>Cambiar Contraseña</MenuItem>
                <MenuItem onClick={handleLogout}>Cerrar Sesión</MenuItem>
            </Menu>

        </>
    );
}

export default AccountButton;
