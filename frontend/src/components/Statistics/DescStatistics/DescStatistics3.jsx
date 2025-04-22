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

import masterData from '../../../../../data/processed/master.json'; 

import BarChartCat from '../../Charts/BarChartCat';
import BarChartIC95 from '../../Charts/BarChartIC95';

const DescStatistics3 = ({ descCatCsv }) => {
    const [procesando, setProcesando] = useState(false);
    const [loading, setLoading] = useState(false);
    const [frecuencias, setFrecuencias] = useState([]);
    const [ic95, setIc95] = useState([]);
    const [nPruebas, setNPruebas] = useState([]);
    const [valores, setValores] = useState([]);
    const [mostrar, setMostrar] = useState('frecuencias');

    const handleDesc3 = async () => {
        setProcesando(true);
        setLoading(true);

        try {
            const response = await fetch('http://127.0.0.1:8000/ai/descStatistics3', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    excel_path: descCatCsv,
                }),
            });

            if (!response.ok) {
                throw new Error(`Error en la solicitud: ${response.statusText}`);
            }

            const data = await response.json();
            const frecuenciasArray = [];
            const ic95Array = [];
            const nArray = [];
            const valoresArray = [];

            for (const variable in data.result) {
                const { valor, n, porcentaje, ic_95_inf, ic_95_sup} = data.result[variable];
                valoresArray.push({ variable, valor });
                nArray.push({ variable, valor: n });
                frecuenciasArray.push({ variable, valor: porcentaje });
                ic95Array.push({ variable, valorI: ic_95_inf, valorS: ic_95_sup });
            }

            setNPruebas(nArray);
            setFrecuencias(frecuenciasArray);
            setIc95(ic95Array);
            setValores(valoresArray);


        } catch (error) {
            console.error("Error al ejecutar el desc3:", error);
        } finally {
            setLoading(false);
        }
    };

    const renderTable = (data, label, nArray, valores) => (
        <TableContainer component={Paper} sx={{ boxShadow: 2, borderRadius: 2 }}>
            <Table size="small" sx={{ minWidth: 300, border: '1px solid #e0e0e0' }}>
                <TableHead>
                    <TableRow sx={{ backgroundColor: '#f1f5ff' }}>
                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Variable</TableCell>
                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Valor</TableCell>
                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>N</TableCell>
                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>{label}</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {data.map((item, idx) => {
                        const nItem = nArray.find(n => n.variable === item.variable);
                        const valoresItem = valores.find(v => v.variable === item.variable);
                        const masterVariable = masterData[item.variable.split('_')[0]];

                        console.log('masterVariable', masterVariable);

                        const valorDescripcion =
                            masterVariable && masterVariable.valores[valoresItem?.valor]
                                ? masterVariable.valores[valoresItem.valor]
                                : valoresItem?.valor;
                        
                        return (
                            <TableRow
                                key={idx}
                                hover
                                sx={{ '&:hover': { backgroundColor: '#f9f9f9' } }}
                            >
                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>{item.variable}</TableCell>
                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>{valorDescripcion}</TableCell>
                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>{nItem ? nItem.valor : '-'}</TableCell>
                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>{item.valor}</TableCell>
                            </TableRow>
                        );
                    })}
                </TableBody>
            </Table>
        </TableContainer>
    );
    

    const renderTableIC95 = (data, nArray, valores) => (
        <TableContainer component={Paper} sx={{ boxShadow: 2, borderRadius: 2 }}>
            <Table size="small" sx={{ minWidth: 300, border: '1px solid #e0e0e0' }}>
                <TableHead>
                    <TableRow sx={{ backgroundColor: '#f1f5ff' }}>
                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Variable</TableCell>
                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Valor</TableCell>
                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>N</TableCell>
                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Intervalo Confianza Inferior 95%</TableCell>
                        <TableCell sx={{ fontWeight: 'bold', border: '1px solid #ccc' }}>Intervalo Confianza Superior 95%</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {data.map((item, idx) => {
                        const nItem = nArray.find(n => n.variable === item.variable);
                        const valoresItem = valores.find(v => v.variable === item.variable);

                        console.log("variable:" + item.variable)
                        const masterVariable = masterData[item.variable.split('_')[0]];

                        console.log('masterVariable', masterVariable);

                        const valorDescripcion =
                            masterVariable && masterVariable.valores[valoresItem?.valor]
                                ? masterVariable.valores[valoresItem.valor]
                                : valoresItem?.valor;
                        
                        return (
                            <TableRow
                                key={idx}
                                hover
                                sx={{ '&:hover': { backgroundColor: '#f9f9f9' } }}
                            >
                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>{item.variable}</TableCell>
                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>{valorDescripcion}</TableCell>
                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>{nItem ? nItem.valor : '-'}</TableCell>
                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>{item.valorI}</TableCell>
                                <TableCell sx={{ border: '1px solid #e0e0e0' }}>{item.valorS}</TableCell>
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
                    <strong>PORCENTAJES CON INTERVALOS DE CONFIANZA AL 95% Y FRECUENCIAS ABSOLUTAS (VARIABLES CUALITATIVAS).</strong>
                </Typography>
                {/* <ThemeToggle /> */}
            </Box>

            {procesando ? (
                <>
                <ToggleButtonGroup
                    value={mostrar}
                    exclusive
                    onChange={(e, val) => val && setMostrar(val)}
                    sx={{ marginTop: 1, height: 15 }}
                >
                    <ToggleButton value="frecuencias">Frecuencias</ToggleButton>
                    <ToggleButton value="ic95inf">Intervalo Confianza 95%</ToggleButton>
                </ToggleButtonGroup>

                <Box sx={{ backgroundColor: '#f5f5f5', borderRadius: 1, padding: 2, marginTop: 2, flexGrow: 1, overflowY: 'auto' }}>
                    {loading ? (
                    <Typography><strong>Calculando porcentajes con intervalos de confianza al 95% y freecuencias absolutas de las variables cualitativas...</strong></Typography>
                    ) : (
                        <>
                            {mostrar === 'frecuencias' ? (
                                <>
                                    {renderTable(frecuencias, 'Frecuencias Absolutas', nPruebas, valores)}
                                    <Box mt={4} sx={{ display: 'flex', justifyContent: 'space-around' }}>
                                        <BarChartCat data={frecuencias} categories={valores.map(v => `${v.variable}`)} title='Frecuencias de Variables Categóricas' variable='Frecuencias' height={400} width={850} />
                                    </Box>
                                </>
                            ) : (
                                <>
                                    {renderTableIC95(ic95, nPruebas, valores)}
                                    <Box mt={4} sx={{ display: 'flex', justifyContent: 'space-around' }}>
                                        <BarChartIC95 data={ic95} categories={valores.map(v => `${v.variable}`)} title='Intervalos de Confianza 95% Variables Numéricas' variable='IC 95'/>
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
                    onClick={handleDesc3}
                >
                    Calcular Porcentajes y Frecuencias Absolutas
                </Button>
            )}
            </Box>
        );
};

export default DescStatistics3;