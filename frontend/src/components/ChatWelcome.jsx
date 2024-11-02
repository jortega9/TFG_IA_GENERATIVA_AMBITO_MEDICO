import React from 'react';
import '../styles/ChatWelcome.css'; // Asegúrate de crear y ajustar este archivo CSS
import ThemeToggle from './ThemeToggle';

const ChatWelcome = () => {
  return (
    <div className="chat-placeholder">
      <div className="chat-placeholder-header">
        <h2 className="chat-placeholder-title">Bienvenido a Urolobot</h2>
        <ThemeToggle />
      </div>
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

    </div>
  );
};

export default ChatWelcome;
