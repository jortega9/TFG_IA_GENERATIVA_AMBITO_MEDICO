import React from 'react';
import '../styles/ChatWelcome.css';
import ThemeToggle from './ThemeToggle';
import { Box, Button, Typography } from '@mui/material';

const ChatWelcome = () => {
  return (
      <Box sx={{
        backgroundColor: 'white',
        borderRadius: 2,
        padding: 2,
        boxShadow: 1,
        width: '100%',
        height: "70vh",
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden'
    }}>
      <Box sx={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',               
      }}>
          <Typography sx={{ color: '#4D7AFF', fontSize: '1.5rem' }}>
              <strong>Bienvenido a Urolobot</strong>
          </Typography>
          {/* <ThemeToggle /> */}
        </Box> 
        <div className="chat-placeholder-content">
          <p className="chat-placeholder-text">
            Bienvenido al panel clínico asistido por IA. Desde aquí puede acceder al asistente virtual de IA, y generar documentos de manera automatizada basados en resultados estadísticos.
          </p>
          <ul className="chat-placeholder-list">
            <li>Acceda al asistente virtual basado en IA.</li>
            <li>Genere documentos basados en resultados estadísticos sobre una base de datos.</li>
          </ul>
          <p className="chat-placeholder-note">
            Este sistema está diseñado para apoyar la labor médica e investigadora, garantizando confidencialidad y rigurosidad científica en cada paso del proceso.
          </p>
        </div>

    </Box>
  );
};

export default ChatWelcome;
