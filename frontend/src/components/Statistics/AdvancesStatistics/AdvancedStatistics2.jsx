import React, { useState, useEffect } from 'react';
import {
    Box,
    Typography,
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


/**
 * Visualización de los resultados del análisis categórico de Fisher
 * 
 * @param {*} param0 
 * @returns 
 */
const AdvStatistics2 = ({ csvFisherPath }) => {
    const [procesando, setProcesando] = useState(false);
    const [loading, setLoading] = useState(false);
    const [table, setTable] = useState([]);
    const [statistics, setStatistics] = useState([]);
    const [pValue, setPValue] = useState([]);
    const [significative, setSignificative] = useState([]);

    /**
     * Función para obtener los resultados del análisis categórico Fisher
     */
    const handleAdv2 = async () => {
        setProcesando(true);
        setLoading(true);

        try {
            const response = await fetch('http://127.0.0.1:8000/ai/advStatistics2', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    excel_path: csvFisherPath
                }),
            });

            if (!response.ok) {
                throw new Error(`Error en la solicitud: ${response.statusText}`);
            }

            const data = await response.json();
            const tablaArray = [];
            const statArray = [];
            const pValueArray = [];
            const significativoArray = [];

            for (const variable in data.result) {
                const { tabla, stat, p_value, significativo } = data.result[variable];
                tablaArray.push({ variable, valor: tabla });
                statArray.push({ variable, valor: stat });
                pValueArray.push({ variable, valor: p_value });
                significativoArray.push({ variable, valor: significativo });
            }

            setTable(tablaArray);
            setStatistics(statArray);
            setPValue(pValueArray);
            setSignificative(significativoArray);

        } catch (error) {
            console.error("Error al ejecutar el adv2:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        handleAdv2();
    }, []);

    return (
        <Box sx={{ backgroundColor: 'white', borderRadius: 2, padding: 2, boxShadow: 1, width: '100%', height: '70vh', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: '10%' }}>
                <Typography sx={{ color: '#4D7AFF', fontSize: '0.9rem' }}>
                    <strong>ANÁLISIS CATEGÓRICO FISHER</strong>
                </Typography>
            </Box>

            <Box sx={{ backgroundColor: '#f5f5f5', borderRadius: 1, padding: 2, marginTop: 2, flexGrow: 1, overflowY: 'auto' }}>
                {loading ? (
                    <Typography><strong>Realizando análisis categórico Fisher...</strong></Typography>
                ) : (
                    <>
                        {table.length === 0 ? (
                            <Box sx={{ textAlign: 'center', mt: 4 }}>
                                <Typography elevation={2} sx={{ padding: 3, borderRadius: 2, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f5f5f5', color: '#4D7AFF' }}>
                                    <strong>No hay datos disponibles para realizar el análisis categórico de Fisher.</strong>
                                </Typography>
                            </Box>
                        ) : (
                            <>
                                <TableContainer component={Paper} sx={{ boxShadow: 2, borderRadius: 2 }}>
                                    <Table size="small" sx={{ minWidth: 600, border: '1px solid #e0e0e0' }}>
                                        <TableHead>
                                            <TableRow sx={{ backgroundColor: '#f1f5ff' }}>
                                                <TableCell align="center" sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Variable</TableCell>
                                                <TableCell align="center" sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Fisher</TableCell>
                                                <TableCell align="center" sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>P-Valor</TableCell>
                                                <TableCell align="center" sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Significativo</TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {table.map((item, idx) => {
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
                                                        <TableCell align="center" sx={{ border: '1px solid #e0e0e0' }}>{item.variable}</TableCell>
                                                        <TableCell align="center" sx={{ border: '1px solid #e0e0e0' }}>
                                                            {statistics[idx]?.valor ?? '-'}
                                                        </TableCell>
                                                        <TableCell align="center" sx={{ border: '1px solid #e0e0e0' }}>
                                                            {pValue[idx]?.valor ?? '-'}
                                                        </TableCell>
                                                        <TableCell align="center" sx={{ border: '1px solid #e0e0e0' }}>
                                                            {significative[idx]?.valor != null ? (significative[idx].valor ? 'Sí' : 'No') : '-'}
                                                        </TableCell>
                                                    </TableRow>
                                                );
                                            })}
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                                <Box sx={{ display: 'flex', justifyContent: 'center', marginTop: 2 }}>
                                    <ChiSquaredChart table={table} data={pValue} />
                                </Box>
                            </>
                        )}
                    </>
                )}
            </Box>
        </Box>
    );
};

export default AdvStatistics2;
