import React, { useState, useEffect } from 'react';
import {
    Box,
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

import BarChartNum from '../../Charts/BarChartNum';
import PieChart from '../../Charts/PieChart';

const DescStatistics2 = ({ descNumCsv }) => {
    const [procesando, setProcesando] = useState(false);
    const [loading, setLoading] = useState(false);
    const [mediana, setMediana] = useState([]);
    const [rangoI, setRangoI] = useState([]);
    const [mostrar, setMostrar] = useState('mediana');
    const [nPruebas, setNPruebas] = useState([]);

    const handleDesc2 = async () => {
        setProcesando(true);
        setLoading(true);

        try {
            const response = await fetch('http://127.0.0.1:8000/ai/descStatistics2', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    excel_path: descNumCsv,
                }),
            });

            if (!response.ok) {
                throw new Error(`Error en la solicitud: ${response.statusText}`);
            }

            const data = await response.json();
            const medianasArray = [];
            const rangoIArray = [];
            const nArray = [];

            for (const variable in data.result) {
                const { n, mediana, rangoI } = data.result[variable];
                nArray.push({ variable, valor: n });
                medianasArray.push({ variable, valor: mediana });
                rangoIArray.push({ variable, valor: rangoI });
            }

            setNPruebas(nArray);
            setMediana(medianasArray);
            setRangoI(rangoIArray);

        } catch (error) {
            console.error("Error al ejecutar el desc2:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        handleDesc2();
    }, []);

    const renderTable = (data, label, nArray) => (
        <TableContainer component={Paper} sx={{ boxShadow: 2, borderRadius: 2 }}>
            <Table size="small" sx={{ minWidth: 300, border: '1px solid #e0e0e0' }}>
                <TableHead>
                    <TableRow sx={{ backgroundColor: '#f1f5ff' }}>
                        <TableCell align="center" sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Variable</TableCell>
                        <TableCell align="center" sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>N</TableCell>
                        <TableCell align="center" sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>{label}</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {data.map((item, idx) => {
                        const nItem = nArray.find(n => n.variable === item.variable);
                        return (
                            <TableRow
                                key={idx}
                                hover
                                sx={{ '&:hover': { backgroundColor: '#f9f9f9' } }}
                            >
                                <TableCell align="center" sx={{ border: '1px solid #e0e0e0' }}>{item.variable}</TableCell>
                                <TableCell align="center" sx={{ border: '1px solid #e0e0e0' }}>{nItem ? nItem.valor : '-'}</TableCell>
                                <TableCell align="center" sx={{ border: '1px solid #e0e0e0' }}>{item.valor}</TableCell>
                            </TableRow>
                        );
                    })}
                </TableBody>
            </Table>
        </TableContainer>
    );

    return (
        <Box sx={{ backgroundColor: 'white', borderRadius: 2, padding: 2, boxShadow: 1, width: '100%', height: '70vh', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: '10%' }}>
                <Typography sx={{ color: '#4D7AFF', fontSize: '0.9rem' }}>
                    <strong>DETERMINANDO MEDIANA Y RANGO INTERCUARTÍLICO SIN SEGUIR UNA DISTRIBUCIÓN NORMAL (VARIABLES NUMÉRICAS).</strong>
                </Typography>
            </Box>

            <ToggleButtonGroup
                value={mostrar}
                exclusive
                onChange={(e, val) => val && setMostrar(val)}
                sx={{ marginTop: 1, height: 15 }}
            >
                <ToggleButton value="mediana">Mediana</ToggleButton>
                <ToggleButton value="rangoI">Rango Intercuartílico</ToggleButton>
            </ToggleButtonGroup>

            <Box sx={{ backgroundColor: '#f5f5f5', borderRadius: 1, padding: 2, marginTop: 2, flexGrow: 1, overflowY: 'auto' }}>
                {loading ? (
                    <Typography><strong>Calculando mediana y rango intercuartílico de las variables numéricas...</strong></Typography>
                ) : (
                    mostrar === 'mediana' ? (
                        <>
                            {renderTable(mediana, 'Mediana', nPruebas)}
                            <Box mt={4} sx={{ display: 'flex', justifyContent: 'space-around' }}>
                                <BarChartNum data={mediana} title='Medianas de Variables Numéricas' variable='Medianas' />
                                <PieChart data={mediana} title='Distribución de Medianas' />
                            </Box>
                        </>
                    ) : (
                        <>
                            {renderTable(rangoI, 'Rango Intercuartílico', nPruebas)}
                            <Box mt={4} sx={{ display: 'flex', justifyContent: 'space-around' }}>
                                <BarChartNum data={rangoI} title='Rangos Intercuartílicos de Variables Numéricas' variable='Rango Intercuartílico'/>
                                <PieChart data={rangoI} title='Distribución de Rangos Intercuartílicos' />
                            </Box>
                        </>
                    )
                )}
            </Box>
        </Box>
    );
};

export default DescStatistics2;
