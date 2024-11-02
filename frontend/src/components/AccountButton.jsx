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

    const handleLogout = () => {
        navigate('/login');
    };

    return (
        <>
            <Button
                variant="contained"
                sx={{
                    backgroundColor: 'white',
                    color: 'grey',
                    borderRadius: '50%',
                    padding: '10px',
                    border: '2px solid grey',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    minWidth: '48px',
                    minHeight: '48px',
                    '&:hover': {
                        backgroundColor: '#f5f5f5',
                    },
                }}
                onClick={handleClick}
            >
                <FiUser size={24} />
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
