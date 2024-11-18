import React, { useState } from 'react';
import '../styles/chat.css';
import AsistenteIcon from '../../public/assets/AsistenteIcon.png';
import { Button } from '@mui/material';
import AccountButton from './AccountButton';
import { useNavigate } from 'react-router-dom';


function AppHeader() {
    const navigate = useNavigate();

    const handleUroloBot = () => {
        navigate('/');
    }

    return (
        <>
            <header className="app-header">
            <div className="avatar">
                <img src={AsistenteIcon} alt="Bot avatar" className="avatar-image"/>
            </div>
            <Button variant="text" sx={{color:'white', fontSize:'20px'}} onClick={handleUroloBot}><strong>UroloBot</strong></Button>
            <AccountButton/>

            </header>
        </>
    );
}

export default AppHeader;
