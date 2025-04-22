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

//TODO Significativas

const AdvStatistics5 = ({csvSignificantPath}) => {
    const [procesando, setProcesando] = useState(false);
    const [loading, setLoading] = useState(false);
    const [type, setType] = useState([]);
    const [testApplied, setTestApplied] = useState([]);
    const [value, setValue] = useState([]);

    const handleAdv5 = async () => {
        setProcesando(true);
        setLoading(true);
        // variable,tipo,test_aplicado,valor

        try {
            console.log("csvSignificantPath:", csvSignificantPath);
            const response = await fetch('http://127.0.0.1:8000/ai/advStatistics5', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    excel_path: csvSignificantPath
                }),
            });

            if (!response.ok) {
                throw new Error(`Error en la solicitud: ${response.statusText}`);
            }

            const data = await response.json();
            const tipoArray = [];
            const testAplicadoArray = [];
            const valorArray = [];

            for (const variable in data.result) {
                const { tipo, test_aplicado, valor } = data.result[variable];
                tipoArray.push({ variable, valor: tipo });
                testAplicadoArray.push({ variable, valor: test_aplicado });
                valorArray.push({ variable, valor: valor });
            }

            setType(tipoArray);
            setTestApplied(testAplicadoArray);
            setValue(valorArray);

        } catch (error) {
            console.error("Error al ejecutar el adv5:", error);
        } finally {
            setLoading(false);
        }
    };
    
    

    return (
        <Box sx={{ backgroundColor: 'white', borderRadius: 2, padding: 2, boxShadow: 1, width: '100%', height: '70vh', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: '10%' }}>
                <Typography sx={{ color: '#4D7AFF', fontSize: '0.9rem' }}>
                    <strong>VARIABLES SIGNIFICATIVAS</strong>
                </Typography>
                {/* <ThemeToggle /> */}
            </Box>

            {procesando ? (
                <>
                    <Box sx={{ backgroundColor: '#f5f5f5', borderRadius: 1, padding: 2, marginTop: 2, flexGrow: 1, overflowY: 'auto' }}>
                        {loading ? (
                            <Typography><strong>Determinando Variables Significativas</strong></Typography>
                        ) : (
                            <>
                                {type.length === 0 ? (
                                    <Box sx={{ textAlign: 'center', mt: 4 }}>
                                        <Typography elevation={2} sx={{ padding: 3, borderRadius: 2, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f5f5f5', color: '#4D7AFF' }}>
                                            <strong>No hay variables significativas.</strong>
                                        </Typography>
                                    </Box>
                                ) : (
                                    <>
                                        <TableContainer component={Paper} sx={{ boxShadow: 2, borderRadius: 2 }}>
                                            <Table size="small" sx={{ minWidth: 600, border: '1px solid #e0e0e0' }}>
                                                <TableHead>
                                                    <TableRow sx={{ backgroundColor: '#f1f5ff' }}>
                                                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Variable</TableCell>
                                                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Tipo</TableCell>
                                                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Test Aplicado</TableCell>
                                                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Valor</TableCell>
                                                    </TableRow>
                                                </TableHead>
                                                <TableBody>
                                                    {type.map((item, idx) => {

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
                                                                    {type[idx]?.valor ?? '-'}
                                                                </TableCell>
                                                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>
                                                                    {testApplied[idx]?.valor ?? '-'}
                                                                </TableCell>
                                                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>
                                                                    {value[idx]?.valor ?? '-'}
                                                                </TableCell>
                                                            </TableRow>
                                                        );
                                                    })}
                                                </TableBody>
                                            </Table>
                                        </TableContainer>
                                        <Box sx={{ display: 'flex', justifyContent: 'center', marginTop: 2 }}>
                                            <ChiSquaredChart table={testApplied} data={value} />
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
                    onClick={handleAdv5}
                >
                    Determinar Variables Significativas
                </Button>
            )}
        </Box>
    );
};

export default AdvStatistics5;
