import React, { useState } from 'react';
import { Box, Button, Typography, ToggleButton, ToggleButtonGroup } from '@mui/material';
import ThemeToggle from '../../ThemeToggle';
import { Circle } from '@mui/icons-material';

const DescStatistics2 = () => {
    const [respuesta, setRespuesta] = useState([]);
    const [texto, setTexto] = useState('');
    const [procesando, setProcesando] = useState(false);
    const [loading, setLoading] = useState(false);
    const [mediana, setMediana] = useState([]);
    const [rangoI, setRangoI] = useState([]);
    const [mostrar, setMostrar] = useState('respuesta');

    const handleDesc2 = async () => {
        setProcesando(true);
        setLoading(true);

        try {
            console.log("Ejecutar Desc2");
        } catch (error) {
        console.error("Error al ejecutar el desc2:", error);
        } finally {
        setLoading(false);
        }
    };

    return (
        <Box sx={{ backgroundColor: 'white', borderRadius: 2, padding: 2, boxShadow: 1, width: '100%', height: '70vh', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: '10%' }}>
                <Typography sx={{ color: '#4D7AFF', fontSize: '0.9rem' }}>
                    <strong>DETERMINANDO MEDIANA Y RANGO INTERCUARTÍLICO SIN SEGUIR UNA DISTRIBUCIÓN NORMAL (VARIABLES NUMÉRICAS).</strong>
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
                    <Typography><strong>Calculando mediana y rango intercuartílico de las variables númericas...</strong></Typography>
                    ) : (
                    mostrar === 'razonamiento' ? (
                        respuesta.map(renderMensaje)
                    ) : (
                        <>
                        <Typography variant="body1"><strong>Mediana:</strong></Typography>
                        {mediana.map((item, idx) => (
                            <Typography key={`mediana-${idx}`}>{item.variable}: {item.valor}</Typography>
                        ))}
                        <Typography variant="body1" sx={{ marginTop: 2 }}><strong>Rango Intercuartílico:</strong></Typography>
                        {rangoI.map((item, idx) => (
                            <Typography key={`rangI-${idx}`}>{item.variable}: {item.valor}</Typography>
                        ))}
                        </>
                    )
                    )}
                </Box>
                </>
            ) : (
                <Button
                    variant="contained"
                    sx={{ backgroundColor: '#4D7AFF', fontSize: '1.1rem', marginTop: 16, alignSelf: 'center' }}
                    onClick={handleDesc2}
                >
                    Calcular Mediana y Rango Intercuartílico
                </Button>
            )}
            </Box>
        );
};

export default DescStatistics2;
