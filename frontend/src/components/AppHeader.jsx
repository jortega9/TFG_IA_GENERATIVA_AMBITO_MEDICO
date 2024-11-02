import React, { useState } from 'react';
import '../styles/chat.css';
import AsistenteIcon from '../../public/assets/AsistenteIcon.png';
import { Button } from '@mui/material';
import AccountButton from './AccountButton';


function AppHeader() {

    return (
        <>
            <header className="app-header">
            <div className="avatar">
                <img src={AsistenteIcon} alt="Bot avatar" className="avatar-image"/>
            </div>
            <h1>UroloBot</h1>
            <AccountButton/>

            </header>
        </>
    );
}

export default AppHeader;
