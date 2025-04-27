import React, { useEffect, useState } from 'react';
import {
    Box, Typography, Table, TableBody, TableCell,
    TableContainer, TableHead, TableRow, Paper
} from '@mui/material';

// import masterData from '../../../../../data/processed/master.json'; 

const KaplanVariableCard = ({ variableName, plotImage, csvKaplanPath, onLoaded }) => {
    const [data, setData] = useState([]);
    const [masterData, setMasterData] = useState({});

    const fetchMasterData = async () => {
        try {
            const response = await fetch('http://localhost:5173/master/master.json');
            if (!response.ok) {
            throw new Error('Archivo master.json no encontrado');
            }
            const data = await response.json();
            setMasterData(data);
        } catch (error) {
            console.error('Error cargando master.json:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleExecuteData = async () => {
        try {
            fetchMasterData();
            const response = await fetch('http://127.0.0.1:8000/ai/kaplanStatisticsVars', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    excel_path: csvKaplanPath,
                    name: variableName,
                }),
            });

            const result = await response.json();
            const entries = [];

            for (const variable in result.result) {
                const { group, median_survival_time, n_patients } = result.result[variable];
                entries.push({ variable, group, median_survival_time, n_patients });
            }

            setData(entries);
        } catch (error) {
            console.error(`Error al procesar ${variableName}:`, error);
        } finally {
            onLoaded();
        }
    };

    useEffect(() => {
        handleExecuteData();
    }, []);

    return (
        <Box sx={{ my: 1 }}>
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold', fontSize: '18px', color: '#4D7AFF' }}>
                Kaplan Meier {variableName} :
            </Typography>

            {data.length > 0 && (
                <TableContainer component={Paper} sx={{ boxShadow: 2, borderRadius: 2 }}>
                    <Table size="small">
                        <TableHead>
                            <TableRow>
                                <TableCell align="center"><strong>Variable</strong></TableCell>
                                <TableCell align="center"><strong>Grupo</strong></TableCell>
                                <TableCell align="center"><strong>Tiempo Medio</strong></TableCell>
                                <TableCell align="center"><strong>Pacientes</strong></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                        {data.map((item, idx) => {
                            const masterVariable = masterData[item.variable.split('_')[0]];
                            console.log(item.variable);
                            console.log(item.variable.split('_')[0])
                            console.log(masterVariable);
                            const valorDescripcion =
                                masterVariable && masterVariable.valores[item.group]
                                    ? masterVariable.valores[item.group]
                                    : item.group;
                            
                            console.log(item.group);
                            console.log(valorDescripcion);

                            return (
                                <TableRow
                                    key={idx}
                                    sx={{
                                        '&:hover': { backgroundColor: '#f1f1f1' },
                                    }}
                                >
                                    <TableCell align="center">{item.variable}</TableCell>
                                    <TableCell align="center">{valorDescripcion}</TableCell>
                                    <TableCell align="center">{item.median_survival_time}</TableCell>
                                    <TableCell align="center">{item.n_patients}</TableCell>
                                </TableRow>
                            );
                        })}
                        </TableBody>
                    </Table>
                </TableContainer>
            )}

            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
                <img src={plotImage} alt={`Kaplan ${variableName}`} style={{
                    width: '400px',
                    borderRadius: 8,
                    boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
                }} />
            </Box>
        </Box>
    );
};

export default KaplanVariableCard;
