import React from 'react';
import '../styles/ChatWelcome.css'; // Asegúrate de crear y ajustar este archivo CSS
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
          Bienvenido a su panel de pacientes. Seleccione un chat para comenzar a revisar o inicie una nueva consulta con un paciente.
        </p>
        <ul className="chat-placeholder-list">
          <li>Revise los síntomas detallados proporcionados por los pacientes.</li>
          <li>Consulte el historial médico relevante y notas anteriores.</li>
          <li>Proporcione orientación médica precisa y planifique el seguimiento necesario.</li>
        </ul>
        <p className="chat-placeholder-note">
          La información proporcionada es confidencial y se debe tratar con el más alto nivel de profesionalismo médico.
        </p>
      </div>
    </Box>
  );
};

export default ChatWelcome;
