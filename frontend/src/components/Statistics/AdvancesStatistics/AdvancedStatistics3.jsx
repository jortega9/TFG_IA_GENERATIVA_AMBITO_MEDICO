import React, { useState } from 'react';
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
    Paper
} from '@mui/material';
import ThemeToggle from '../../ThemeToggle';

import ChiSquaredChart from '../../Charts/ChiSquaredChart';

//TODO MannWhitney

const AdvStatistics3 = ({csvMannWhitneyPath}) => {
    const [procesando, setProcesando] = useState(false);
    const [loading, setLoading] = useState(false);
    const [nCasos, setNCasos] = useState([]);
    const [nControles, setNControles] = useState([]);
    const [pValue, setPValue] = useState([]);
    const [significative, setSignificative] = useState([]);

    const handleAdv3 = async () => {
        setProcesando(true);
        setLoading(true);

        try {
            console.log("csvMannWhitneyPath:", csvMannWhitneyPath);
            const response = await fetch('http://127.0.0.1:8000/ai/advStatistics3', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    excel_path: csvMannWhitneyPath
                }),
            });

            if (!response.ok) {
                throw new Error(`Error en la solicitud: ${response.statusText}`);
            }

            const data = await response.json();
            const nCasosArray = [];
            const nControlesArray = [];
            const pValueArray = [];
            const significativoArray = [];

            for (const variable in data.result) {
                const { n_casos, n_controles, p_value, significativo } = data.result[variable];
                nCasosArray.push({ variable, valor: n_casos });
                nControlesArray.push({ variable, valor: n_controles });
                pValueArray.push({ variable, valor: p_value });
                significativoArray.push({ variable, valor: significativo });
            }

            setNCasos(nCasosArray);
            setNControles(nControlesArray);
            setPValue(pValueArray);
            setSignificative(significativoArray);

        } catch (error) {
            console.error("Error al ejecutar el adv1:", error);
        } finally {
            setLoading(false);
        }
    };
    
    

    return (
        <Box sx={{ backgroundColor: 'white', borderRadius: 2, padding: 2, boxShadow: 1, width: '100%', height: '70vh', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: '10%' }}>
                <Typography sx={{ color: '#4D7AFF', fontSize: '0.9rem' }}>
                    <strong>ANÁLISIS NUMÉRICO MANN WHITNEY</strong>
                </Typography>
                {/* <ThemeToggle /> */}
            </Box>

            {procesando ? (
                <>
                    <Box sx={{ backgroundColor: '#f5f5f5', borderRadius: 1, padding: 2, marginTop: 2, flexGrow: 1, overflowY: 'auto' }}>
                        {loading ? (
                            <Typography><strong>Realizando Análisis Numérico Mann Whitney</strong></Typography>
                        ) : (
                            <>
                                {nCasos.length === 0 ? (
                                    <Box sx={{ textAlign: 'center', mt: 4 }}>
                                        <Typography elevation={2} sx={{ padding: 3, borderRadius: 2, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f5f5f5', color: '#4D7AFF' }}>
                                            <strong>No hay datos disponibles para realizar el análisis categórico de Mann Whitney.</strong>
                                        </Typography>
                                    </Box>
                                ) : (
                                    <>
                                        <TableContainer component={Paper} sx={{ boxShadow: 2, borderRadius: 2 }}>
                                            <Table size="small" sx={{ minWidth: 600, border: '1px solid #e0e0e0' }}>
                                                <TableHead>
                                                    <TableRow sx={{ backgroundColor: '#f1f5ff' }}>
                                                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Variable</TableCell>
                                                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Número Casos</TableCell>
                                                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Número Controles</TableCell>
                                                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>P Value</TableCell>
                                                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Significativo</TableCell>
                                                    </TableRow>
                                                </TableHead>
                                                <TableBody>
                                                    {nCasos.map((item, idx) => {
                                                        const isSignificative = significative[idx]?.valor === true;

                                                        return (
                                                            <TableRow
                                                                key={idx}
                                                                hover
                                                                sx={{
                                                                    backgroundColor: isSignificative ? '#e6f7e6' : 'inherit',
                                                                    '&:hover': {
                                                                        backgroundColor: isSignificative ? '#d9f2d9' : '#f9f9f9',
                                                                    },
                                                                }}
                                                            >
                                                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>{item.variable}</TableCell>
                                                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>
                                                                    {nCasos[idx]?.valor ?? '-'}
                                                                </TableCell>
                                                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>
                                                                    {nControles[idx]?.valor ?? '-'}
                                                                </TableCell>
                                                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>
                                                                    {pValue[idx]?.valor ?? '-'}
                                                                </TableCell>
                                                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>
                                                                    {significative[idx]?.valor != null ? (significative[idx].valor ? 'Sí' : 'No') : '-'}
                                                                </TableCell>
                                                            </TableRow>
                                                        );
                                                    })}
                                                </TableBody>
                                            </Table>
                                        </TableContainer>
                                        <Box sx={{ display: 'flex', justifyContent: 'center', marginTop: 2 }}>
                                            <ChiSquaredChart table={nCasos} data={pValue} />
                                        </Box>
                                    </>
                                )}
                            </>

                        )}
                    </Box>

                </>
            ) : (
                <Button
                    variant="contained"
                    sx={{ backgroundColor: '#4D7AFF', fontSize: '1.1rem', marginTop: 16, alignSelf: 'center' }}
                    onClick={handleAdv3}
                >
                    Realizar Análisis Numérico Mann Whitney
                </Button>
            )}
        </Box>
    );
};

export default AdvStatistics3;
