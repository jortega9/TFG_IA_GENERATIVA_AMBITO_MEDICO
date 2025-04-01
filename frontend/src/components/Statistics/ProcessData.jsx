import React, { useState, useEffect } from 'react';
import { Box, Button, Typography, ToggleButton, ToggleButtonGroup } from '@mui/material';
import { Circle } from '@mui/icons-material';
import ThemeToggle from '../ThemeToggle';

const ProcessData = () => {
    const [respuesta, setRespuesta] = useState([]);
    const [texto, setTexto] = useState('');
    const [procesando, setProcesando] = useState(false);
    const [loading, setLoading] = useState(false);
    const [mostrar, setMostrar] = useState('respuesta');
    const [message, setMessage] = useState('');
    const [isOK, setIsOK] = useState(false);

    const parseString = (input) => {
        const keywords = ["Pensamiento:", "Ejecuta:", "Observacion:", "Resultado:"];
        const result = [];
        let currentKeyword = null;
        let currentContent = "";
    
        const regex = new RegExp(`(${keywords.join('|')})`, 'g');
        const parts = input.split(regex).filter(Boolean);
    
        parts.forEach(part => {
        const keyword = keywords.find(kw => part.startsWith(kw));
        if (keyword) {
            if (currentKeyword) {
            result.push({ tipo: currentKeyword, contenido: currentContent.trim() });
            }
            currentKeyword = keyword.replace(':', '');
            currentContent = part.replace(keyword, '').trim();
        } else if (currentKeyword) {
            currentContent += ' ' + part.trim();
        }
        });
    
        if (currentKeyword) {
        result.push({ tipo: currentKeyword, contenido: currentContent.trim() });
        }
    
        return result;
    };
    
    const getColor = (tipo) => {
        switch (tipo) {
        case 'Pensamiento': return '#1976D2';
        case 'Ejecuta': return '#388E3C';
        case 'Observacion': return '#D32F2F';
        default: return '#333';
        }
    };
    
    const renderMensaje = (mensaje, index) => (
        <Box key={index} sx={{ display: 'flex', alignItems: 'center', marginBottom: 1 }}>
        <Circle sx={{ fontSize: 12, color: getColor(mensaje.tipo), marginRight: 1 }} />
        <Typography variant="body2" sx={{ color: '#333', wordBreak: 'break-word', textAlign: 'left' }}>
            <strong>{mensaje.tipo}:</strong> {mensaje.contenido}
        </Typography>

        </Box>
    );

    const handleExecuteData = async () => {  
        setProcesando(true);
        setLoading(true);

        try {
            const response = await fetch('http://127.0.0.1:8000/ai/testExecuteData', {
                method: 'POST',
            });
    
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
    
            const result = await response.json();
            const resultText = result.result.razonamiento.join(' ');
            const resultVars = result.result.resultado;
            console.log(resultVars);
            setTexto(resultText);
            setRespuesta(parseString(resultText));
            setMessage(resultVars.message);
            setIsOK(resultVars.isOK);
    
            console.log("Ejecutar Procesado:", result);
        } catch (error) {
            console.error("Error al ejecutar el procesado:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box sx={{
            backgroundColor: 'white',
            borderRadius: 2,
            padding: 2,
            boxShadow: 1,
            width: '100%',
            height: "64vh",
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden'
        }}>
            <Box sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
            }}>

                <Typography sx={{ color: '#4D7AFF', fontSize: '1rem' }}>
                    <strong> PROCESANDO DATOS DE BBDD Y MAESTRO. </strong>
                </Typography>
                <ThemeToggle />
            </Box>

            {procesando ? (
                <>
                <ToggleButtonGroup
                    value={mostrar}
                    exclusive
                    onChange={(e, val) => val && setMostrar(val)}
                    sx={{ marginTop: 1, height: 15 }}
                >
                    <ToggleButton value="razonamiento">Razonamiento</ToggleButton>
                    <ToggleButton value="respuesta">Respuesta</ToggleButton>
                </ToggleButtonGroup>

                <Box sx={{ backgroundColor: '#f5f5f5', borderRadius: 1, padding: 2, marginTop: 2, flexGrow: 1, overflowY: 'auto' }}>
                    {loading ? (
                    <Typography><strong>Procesando datos...</strong></Typography>
                    ) : (
                    mostrar === 'razonamiento' ? (
                        respuesta.map(renderMensaje)
                    ) : (
                        <>
                            {
                                isOK ? (
                                    <Typography variant="body1" ><strong>{message}</strong></Typography>
                                ) : (
                                    <>
                                        <Typography variant="body1" ><strong>{message}</strong></Typography>
                                        <TextField
                                            label="Por favor, responda la pregunta"
                                            variant="outlined"
                                            fullWidth
                                            margin="normal"
                                        />
                                    </>
                                )
                            }
                        </>
                    )
                    )}
                </Box>
                </>
            ) : (
                <Button
                    variant="contained"
                    sx={{ backgroundColor: '#4D7AFF', fontSize: '1.1rem', marginTop: 16, alignSelf: 'center' }}
                    onClick={handleExecuteData}
                >
                    Procesar Datos  
                </Button>
            )}
            </Box>
    );
};

export default ProcessData;