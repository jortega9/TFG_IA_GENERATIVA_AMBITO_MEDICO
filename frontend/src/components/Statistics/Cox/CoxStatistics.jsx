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
    CircularProgress,
    Divider
} from '@mui/material';

import CoxUnivarianteChart from '../../Charts/CoxUnivarianteChart';

/**
 * Visualización de los resultados del análisis de supervivencia con el modelo de regresión de Cox univariante.
 * 
 * @param {*} param0 
 * @returns 
 */
const CoxStatistics = ({ csvCoxPath }) => {

    const [data, setData] = useState([]);

    /**
     * Función para obtener los resultados del análisis de supervivencia con el modelo de regresión de Cox univariante.
     */
    const handleExecuteData = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/ai/coxStatistics', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    excel_path: csvCoxPath,
                }),
            });

            const result = await response.json();
            const entries = [];

            for (const variable in result.result) {
                const { coef, HR, p, ci_lower, ci_upper } = result.result[variable];
                entries.push({ variable, coef, HR, p, ci_lower, ci_upper });
            }

            setData(entries);
        } catch (error) {
            console.error(`Error al procesar ${variableName}:`, error);
        }
    };

    useEffect(() => {
        handleExecuteData();
    }, []);

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
                    <strong>ANÁLISIS DE SUPERVIVENCIA CON MODELO DE REGRESIÓN DE COX UNIVARIANTE. </strong>
                </Typography>
                {/* <ThemeToggle /> */}
            </Box>
            <>
                <Box sx={{ backgroundColor: '#f5f5f5', borderRadius: 1, padding: 2, marginTop: 2, flexGrow: 1, overflowY: 'auto' }}>
                    <Box sx={{ my: 1 }}>
                        {data.length > 0 && (
                            <>     
                                <TableContainer component={Paper} sx={{ boxShadow: 2, borderRadius: 2 }}>
                                    <Table size="small">
                                        <TableHead>
                                            <TableRow>
                                                <TableCell align="center"><strong>Variable</strong></TableCell>
                                                <TableCell align="center"><strong>Coeficiente</strong></TableCell>
                                                <TableCell align="center"><strong>Cociente de Riesgos (HR)</strong></TableCell>
                                                <TableCell align="center"><strong>P-Valor</strong></TableCell>
                                                <TableCell align="center"><strong>Intervalo de Confianza Inferior (95%)</strong></TableCell>
                                                <TableCell align="center"><strong>Intervalo de Confianza Superior (95%)</strong></TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {data.map((item, idx) => (
                                                <TableRow key={idx} sx={{ '&:hover': { backgroundColor: '#f1f1f1' } }}>
                                                <TableCell align="center">{item.variable}</TableCell>
                                                <TableCell align="center">{item.coef}</TableCell>
                                                <TableCell align="center">{item.HR}</TableCell>
                                                <TableCell align="center">{item.p}</TableCell>
                                                <TableCell align="center">{item.ci_lower}</TableCell>
                                                <TableCell align="center">{item.ci_upper}</TableCell>
                                                </TableRow>
                                            ))}
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', mt: 2 }}>
                                    <CoxUnivarianteChart data={data} />
                                </Box>
                            </>
                        )}
                    </Box>

                </Box>
            </>
        </Box>
    );
};

export default CoxStatistics;