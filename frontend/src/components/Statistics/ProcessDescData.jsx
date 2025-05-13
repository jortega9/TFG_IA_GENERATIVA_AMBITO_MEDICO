import React, { useState, useEffect } from 'react';
import { Box, Button, Typography, ToggleButton, ToggleButtonGroup, CircularProgress   } from '@mui/material';
import { Circle } from '@mui/icons-material';
import ThemeToggle from '../ThemeToggle';

/**
 *  Visualización del proceso de analisis descriptivos para variables numericas y categóricas
 * 
 * @param {*} param0 
 * @returns 
 */
const ProcessDescData = ({setIsDataProcessed, setDescnumVars, setDescNumCsv, setDescCatVars, setDescCatCsv, }) => {
    const [numRazonamiento, setNumRazonamiento] = useState('');
    const [catRazonamiento, setCatRazonamiento] = useState('');
    const [procesando, setProcesando] = useState(false);
    const [loading, setLoading] = useState(false);
    const [mostrar, setMostrar] = useState('numerico');

    /**
     * Función para comenzar el proceso de ejecución de los análisis descriptivos para las variables numéricas y categóricas.
     */
    const handleExecuteData = async () => {  
        setProcesando(true);
        setLoading(true);

        try {
            const response = await fetch('http://127.0.0.1:8000/ai/executeDataDesc', {
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
                {/* <ThemeToggle /> */}
            </Box>

            {procesando ? (
                <>
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
                            Procesando los datos descriptivos...
                            </Typography>
                        </Box>
                        ) : (
                            <>
                                <Typography elevation={2} sx={{ padding: 3, borderRadius: 2, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f5f5f5', color: '#4D7AFF' }}>
                                    <strong>Datos descriptivos procesados correctamente.</strong>
                                </Typography>
                            </>
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

export default ProcessDescData;