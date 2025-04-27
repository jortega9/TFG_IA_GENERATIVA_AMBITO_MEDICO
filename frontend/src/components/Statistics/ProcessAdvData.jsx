import React, { useState, useEffect } from 'react';
import { Box, Button, Typography, ToggleButton, ToggleButtonGroup, CircularProgress   } from '@mui/material';
import ThemeToggle from '../ThemeToggle';

const ProcessAdvData = ({setIsDataProcessed, setCsvMannWhitneyPath, setCsvTStudentPath, setCsvChiPath, setCsvFisherPath, setCsvSignificantPath, setImagesKaplanPath, setCsvKaplanPath, setCsvCoxPath }) => {
    const [procesando, setProcesando] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleExecuteData = async () => {  
        setProcesando(true);
        setLoading(true);

        try {
            const response = await fetch('http://127.0.0.1:8000/ai/executeDataAdv', {
                method: 'POST',
            });
    
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
    
            const result = await response.json();
            console.log("Ejecutar Procesado Adv:", result);


            setCsvChiPath(result.result.chi.results.csv_chi_path);
            setCsvFisherPath(result.result.fisher.results.csv_fisher_path);
            setCsvMannWhitneyPath(result.result.mann.results.csv_mann_path);
            setCsvTStudentPath(result.result.tStudent.results.csv_t_student);
            setCsvSignificantPath(result.result.significant.results.csv_path);
            setImagesKaplanPath(result.result.kaplan.results.images_path);
            setCsvKaplanPath(result.result.kaplan.results.data_path);
            setCsvCoxPath(result.result.cox.results.cox_univariante)

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
                    <strong> PROCESANDO DATOS COMPARATIVOS. </strong>
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
                            Procesando los datos...
                            </Typography>
                        </Box>
                        ) : (
                            <>
                                <Typography elevation={2} sx={{ padding: 3, borderRadius: 2, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f5f5f5', color: '#4D7AFF' }}>
                                    <strong>Datos procesados correctamente.</strong>
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
                    Procesar Datos Comparativos
                </Button>
            )}
            </Box>
    );
};

export default ProcessAdvData;