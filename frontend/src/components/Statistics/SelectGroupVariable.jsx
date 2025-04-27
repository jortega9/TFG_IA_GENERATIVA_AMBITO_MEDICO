import React, { useState, useEffect } from 'react';
import { Box, Button, Typography, ToggleButton, ToggleButtonGroup, CircularProgress, TextField  } from '@mui/material';
import { Circle } from '@mui/icons-material';
import ThemeToggle from '../ThemeToggle';
import { Snackbar, Alert } from '@mui/material';

const SelectGroupVariable = ({setIsGroupIdentified}) => {
    const [razonamiento, setRazonamiento] = useState('');
    const [procesando, setProcesando] = useState(false);
    const [loading, setLoading] = useState(false);
    const [groupV, setGroupV] = useState('');
    const [jsonPath, setJsonPath] = useState('');
    const [validKeys, setValidKeys] = useState([]);
    const [openSnackbar, setOpenSnackbar] = useState(false);  

    const handleConfirmGroupVariable = async () => {
        const payload = {
            group_variable: groupV,
            valid_keys: validKeys
        };

        try {
            setLoading(true);
            const saveResponse = await fetch('http://127.0.0.1:8000/ai/save-config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    payload,
                    jsonPath
                })
            });

            if (!saveResponse.ok) {
                throw new Error('Error al guardar el archivo JSON');
            }

            console.log('Archivo JSON actualizado correctamente');

            const response = await fetch('http://127.0.0.1:8000/ai/categorize-variables', {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }

            const result = await response.json();
            setIsGroupIdentified(true);
            console.log("Ejecutar categorize-variables:", result);

            setOpenSnackbar(true);

        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleExecuteData = async () => {  
        setProcesando(true);
        setLoading(true);

        try {
            const response = await fetch('http://127.0.0.1:8000/ai/identify-group-variable', {
                method: 'POST',
            });
    
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
    
            const result = await response.json();
            console.log("Ejecutar group identify:", result);

            const explanation = result.result.explanation;
            setRazonamiento(explanation);
            setGroupV(result.result.results.ret.group_variable);
            setJsonPath(result.result.results.json_path);
            setValidKeys(result.result.results.ret.valid_keys);

            console.log("Ejecutar group identify:", result);
        } catch (error) {
            console.error("Error al ejecutar el group identify:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
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
                        <strong> IDENTIFICACIÓN DE VARIABLE DE GRUPO Y CATEGORIZACIÓN VARIABLES. </strong>
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
                            Categorizando variables...
                            </Typography>
                        </Box>
                        ) : (
                                <>
                                    <Typography variant="h6" sx={{ marginBottom: 1, color: '#388E3C' }}>
                                        Variable de Grupo Identificada:
                                    </Typography>

                                    <TextField
                                        value={groupV}
                                        onChange={(e) => setGroupV(e.target.value)}
                                        variant="outlined"
                                        fullWidth
                                        sx={{ marginBottom: 3 }}
                                    />

                                    <Typography variant="body2" sx={{ color: '#333', textAlign: 'left', marginBottom: 1 }}>
                                        Claves Válidas:
                                    </Typography>

                                    <TextField
                                        value={validKeys.join(', ')}
                                        onChange={(e) => setValidKeys(e.target.value.split(',').map(val => val.trim()))}
                                        variant="outlined"
                                        fullWidth
                                        multiline
                                        sx={{ marginBottom: 3 }}
                                    />

                                    <Button
                                        variant="contained"
                                        sx={{ backgroundColor: '#4D7AFF', fontSize: '1.1rem', marginTop: 1, alignSelf: 'center' }}
                                        onClick={handleConfirmGroupVariable}
                                    >
                                        Confirmar Variable de Grupo
                                    </Button>
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
                        Identificar Variable de grupo y Categorizar Variables
                    </Button>
                )}
            </Box>

            <Snackbar open={openSnackbar} autoHideDuration={4000} onClose={() => setOpenSnackbar(false)} anchorOrigin={{ vertical: 'top', horizontal: 'center' }}            >
                <Alert onClose={() => setOpenSnackbar(false)} severity="success" sx={{ width: '100%' }}>
                    Variable de grupo identificada y variables categorizadas correctamente.
                </Alert>
            </Snackbar>

        </>

    );
};

export default SelectGroupVariable;