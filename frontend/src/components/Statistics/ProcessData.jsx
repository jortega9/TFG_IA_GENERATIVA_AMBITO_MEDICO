import React, { useState, useEffect } from 'react';
import { Box, Typography, Button, CircularProgress } from '@mui/material';
import { Circle } from '@mui/icons-material';
import ThemeToggle from '../ThemeToggle';

const ProcessData = () => {
    const [respuesta, setRespuesta] = useState([]);
    const [texto, setTexto] = useState('');
    const [procesando, setProcesando] = useState(false);
    const [loading, setLoading] = useState(false);

    const parseString = (input) => {
        const keywords = ["Pensamiento:", "Ejecuta:", "Observacion:", "Resultado:"];
        const result = [];
        let currentKeyword = null;
        let currentContent = "";
    
        // Crear una expresión regular que detecte las palabras clave
        const regex = new RegExp(`(${keywords.join('|')})`, 'g');
    
        // Dividir el texto por las palabras clave, manteniendo las palabras clave en el resultado
        const parts = input.split(regex).filter(Boolean);
    
        parts.forEach(part => {
            const keyword = keywords.find(kw => part.startsWith(kw));
            if (keyword) {
                if (currentKeyword) {
                    result.push({
                        tipo: currentKeyword,
                        contenido: currentContent.trim()
                    });
                }
                currentKeyword = keyword.replace(':', '');
                currentContent = part.replace(keyword, '').trim();
            } else if (currentKeyword) {
                currentContent += ' ' + part.trim();
            }
        });
    
        if (currentKeyword) {
            result.push({
                tipo: currentKeyword,
                contenido: currentContent.trim()
            });
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
        <Box key={index} sx={{ display: 'flex', alignItems: 'center', marginBottom: 1, width: '100%' }}>
            <Circle sx={{ fontSize: 12, color: getColor(mensaje.tipo), marginRight: 1 }} />
            <Typography
                variant="body2"
                sx={{ color: '#333', textAlign: 'left', wordBreak: 'break-word' }}
            >
                <strong>{mensaje.tipo}:</strong> {mensaje.contenido}
            </Typography>
        </Box>
    );

    const handleExecuteData = async () => {  
        setProcesando(true);
        setLoading(true);

        try {
            const response = await fetch('http://127.0.0.1:8000/ai/executeData', {
                method: 'POST',
            });
    
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
    
            const result = await response.json();
            const resultText = result.result.join(' ');
            setTexto(resultText);
            setRespuesta(parseString(resultText));
    
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
                <Box sx={{
                    backgroundColor: '#f5f5f5',
                    borderRadius: 1,
                    padding: 2,
                    flexGrow: 1,
                    overflowY: "scroll",
                    overflowX: "hidden",
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'flex-start',
                    marginBottom: 1,
                    marginTop: 1
                }}>
                    {loading ? (
                        <Typography variant="body1" sx={{ color: '#333', paddingBottom: 2 }}>
                            <strong> Cargando datos... </strong>
                        </Typography>
                    ) : (
                        <>
                            <Typography variant="body1" sx={{ color: '#333', paddingBottom: 2 }}>
                                <strong> Se están procesando los datos de los documentos subidos. </strong>
                            </Typography>
                            {respuesta.map((mensaje, index) => renderMensaje(mensaje, index))}
                        </>
                    )}
                </Box>
            ) : (
                <Button
                    variant="contained"
                    sx={{ backgroundColor: '#4D7AFF', fontSize: '1.1rem', marginTop: 16, alignSelf: 'center' }}
                    onClick={handleExecuteData}
                >
                    Ejecutar Procesado
                </Button>
            )}
        </Box>
    );
};

export default ProcessData;