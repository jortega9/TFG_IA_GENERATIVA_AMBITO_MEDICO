import React, { useState } from 'react';
import '../styles/chat.css'; // Asegúrate de que el CSS esté vinculado
import AsistenteIcon from '../../public/assets/AsistenteIcon.png';
import { Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';


function AppHeader() {

    const navigate = useNavigate();

    const handleLogout = () => {
        const user = {
            email: "",
            password: ""
        };
        sessionStorage.setItem('user', JSON.stringify(user));
        navigate('/login');
    };

    return (
        <>
            <header className="app-header">
            <div className="avatar">
                <img src={AsistenteIcon} alt="Bot avatar" className="avatar-image" />
            </div>
            <h1>UroloBot</h1>
            <Button
                variant="contained"
                color="primary"
                sx={{
                    backgroundColor: 'grey',
                    color: 'white',         
                    borderRadius: '50px',   
                    padding: '10px 20px', 
                    '&:hover': { 
                    backgroundColor: 'darkgrey',
                    },
                }}
                onClick={handleLogout}
                >
                Log Out
            </Button>
            </header>
        </>
    );
}

export default AppHeader;
