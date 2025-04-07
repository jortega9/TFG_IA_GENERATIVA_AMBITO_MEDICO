import React, { useState, useEffect } from 'react';
import { Box, Button, Typography, ToggleButton, ToggleButtonGroup, CircularProgress   } from '@mui/material';
import { Circle } from '@mui/icons-material';
import ThemeToggle from '../ThemeToggle';

const ProcessData = ({setIsDataProcessed, setDescnumVars, setDescNumCsv, setDescCatVars, setDescCatCsv, }) => {
    const [numRazonamiento, setNumRazonamiento] = useState('');
    const [catRazonamiento, setCatRazonamiento] = useState('');
    const [procesando, setProcesando] = useState(false);
    const [loading, setLoading] = useState(false);
    const [mostrar, setMostrar] = useState('numerico');

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
            console.log("Ejecutar Procesado:", result);

            const numericText = result.result.numeric.explanation;
            const numericResults = result.result.numeric.results;
            const categoricalText = result.result.categorical.explanation;
            const categoricalResults = result.result.categorical.results;

            const numericVars = numericResults.variables;
            const numericCsv = numericResults.csv_path;
            const categoricalVars = categoricalResults.variables;
            const categoricalCsv = categoricalResults.csv_path;

            setNumRazonamiento(numericText);
            setCatRazonamiento(categoricalText);
            setDescnumVars(numericVars);
            setDescNumCsv(numericCsv);
            setDescCatVars(categoricalVars);
            setDescCatCsv(categoricalCsv);        

            console.log("Ejecutar Procesado:", result);
            setIsDataProcessed(true);
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
            height: "70vh",
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden'
        }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: '10%' }}>
                <Typography sx={{ color: '#4D7AFF', fontSize: '0.9rem' }}>
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
                    <ToggleButton value="numerico">Vars Numéricas</ToggleButton>
                    <ToggleButton value="categorico">Vars Categóricas </ToggleButton>
                </ToggleButtonGroup>

                <Box sx={{ backgroundColor: '#f5f5f5', borderRadius: 1, padding: 2, marginTop: 2, flexGrow: 1, overflowY: 'auto' }}>
                    {loading ? (
                    <Box sx={{
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        marginTop: 6
                    }}>
                        <CircularProgress sx={{ color: '#4D7AFF', mb: 2 }} />
                        <Typography variant="body1" sx={{ color: '#4D7AFF' }}>
                        Procesando los datos...
                        </Typography>
                    </Box>
                    ) : (
                        mostrar === 'numerico' ? (
                            <>
                                <Typography variant="h6" sx={{ marginBottom: 2, color: '#1976D2' }}>
                                    Razonamiento Variables Numéricas
                                </Typography>
                                <Typography variant="body2" sx={{ color: '#333', wordBreak: 'break-word', textAlign: 'left' }}>
                                    <strong>Observación:</strong> {numRazonamiento}
                                </Typography>
                            </>
                        ) : (
                            <>
                                <Typography variant="h6" sx={{ marginBottom: 2, color: '#388E3C' }}>
                                    Razonamiento Variables Categóricas
                                </Typography>
                                <Typography variant="body2" sx={{ color: '#333', wordBreak: 'break-word', textAlign: 'left' }}>
                                    <strong>Observación:</strong> {catRazonamiento}
                                </Typography>
                            </>
                        )
                    )
                    }
                </Box>
                </>
            ) : (
                <Button
                    variant="contained"
                    sx={{ backgroundColor: '#4D7AFF', fontSize: '1.1rem', marginTop: 16, alignSelf: 'center' }}
                    onClick={handleExecuteData}
                >
                    Procesar Datos Descriptivos
                </Button>
            )}
            </Box>
    );
};

export default ProcessData;