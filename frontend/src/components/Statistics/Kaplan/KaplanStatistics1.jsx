import React, { useState, useEffect } from 'react';
import {
    Box,
    Button,
    Typography,
    ToggleButton,
    ToggleButtonGroup,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    CircularProgress
} from '@mui/material';
import { Variable } from 'lucide-react';

import kaplan_meier_plot from "../../../../../data/processed/kaplan_meier/kaplan_meier_plot.png"

const KaplanStatistics1 = ({csvKaplanPath, imagesKaplanPath}) => {
    const [procesando, setProcesando] = useState(false);
    const [loading, setLoading] = useState(false);

    const [medianSurvivalTime, setMedianSurvivalTime] = useState([]);
    const [nObservations, setNObservations] = useState([]);

    const handleExecuteData = async () => {  
        setProcesando(true);
        setLoading(true);

        try {
            console.log("csvKaplanPath: ", csvKaplanPath, " imagesKaplanPath:", imagesKaplanPath);
            const response = await fetch('http://127.0.0.1:8000/ai/kaplanStatistics1', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    excel_path: csvKaplanPath
                }),
            });
    
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
    
            const result = await response.json();
            console.log("Ejecutar kaplanStatistics1:", result);

            const msArray = [];
            const nObsArray = [];
            for (const variable in result.result) {
                const { median_survival_time, n_observations } = result.result[variable];
                msArray.push({ variable, valor: median_survival_time });
                nObsArray.push({ variable, valor: n_observations });
            }
            setMedianSurvivalTime(msArray);
            setNObservations(nObsArray);
            

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
                    <strong> KAPLAN MEIER GENERAL. </strong>
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
                                {medianSurvivalTime.length === 0 ? (
                                    <Box sx={{ textAlign: 'center', mt: 4 }}>
                                        <Typography elevation={2} sx={{ padding: 3, borderRadius: 2, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f5f5f5', color: '#4D7AFF' }}>
                                            <strong>No hay datos disponibles para realizar el análisis general de Kaplan Meier.</strong>
                                        </Typography>
                                    </Box>
                                ) : (
                                    <>
                                        <TableContainer component={Paper} sx={{ boxShadow: 2, borderRadius: 2 }}>
                                            <Table size="small" sx={{ minWidth: 600, border: '1px solid #e0e0e0' }}>
                                                <TableHead>
                                                    <TableRow sx={{ backgroundColor: '#f1f5ff' }}>
                                                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Variable</TableCell>
                                                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Tiempo Medio de Supervivencia</TableCell>
                                                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Número Observaciones</TableCell>
                                                    </TableRow>
                                                </TableHead>
                                                <TableBody>
                                                    {medianSurvivalTime.map((item, idx) => {

                                                        return (
                                                            <TableRow
                                                                key={idx}
                                                                hover
                                                                sx={{
                                                                    backgroundColor: '#d9f2d9',
                                                                    '&:hover': {
                                                                        backgroundColor: '#d9f2d9',
                                                                    },
                                                                }}
                                                            >
                                                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>{item.variable}</TableCell>
                                                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>
                                                                    {medianSurvivalTime[idx]?.valor ?? '-'}
                                                                </TableCell>
                                                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>
                                                                    {nObservations[idx]?.valor ?? '-'}
                                                                </TableCell>
                                                            </TableRow>
                                                        );
                                                    })}
                                                </TableBody>
                                            </Table>
                                        </TableContainer>
                                        <Box sx={{ textAlign: 'center', mt: 4 }}>
                                            <img
                                                src={kaplan_meier_plot}
                                                alt="Kaplan Meier Plot"
                                                style={{
                                                    width: '400px', // o cualquier ancho que te guste
                                                    height: 'auto',
                                                    borderRadius: '8px',
                                                    boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)'
                                                }}
                                            />
                                        </Box>

                                    </>
                                )}
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
                    OBTENER KAPLAN MEIER GENERAL
                </Button>
            )}
            </Box>
    );
};

export default KaplanStatistics1;