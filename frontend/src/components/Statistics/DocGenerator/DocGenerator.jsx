import React, { useState, useEffect } from 'react';
import {
    Box,
    Button,
    Typography,
    CircularProgress,
} from '@mui/material';

/**
 *  Componente para generar el informe PDF, acceder a él y descargar el archivo ZIP con los resultados del proceso.
 * 
 * @param {*} param0 
 * @returns 
 */
const DocGenerator = ({ csvCoxPath }) => {
    const [pdfPath, setPdfPath] = useState([]);
    const [loadingZip, setLoadingZip] = useState(false);

    /**
     * Función para descargar el archivo ZIP generado por el backend
     */
    const handleDownloadZip = async () => {
        try {
            setLoadingZip(true);

            const response = await fetch('http://127.0.0.1:8000/ai/download-zip', {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error('Error descargando el archivo');
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'statistics.zip');
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Error al descargar el archivo:', error);
        } finally {
            setLoadingZip(false);
        }
    };

    /**
     * Función para generar el documento PDF a partir de los resultados obtenidos
     */
    const handleExecuteData = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/ai/documentGenerator', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    excel_path: csvCoxPath,
                }),
            });

            const result = await response.json();
            setPdfPath(result.result);
        } catch (error) {
            console.error('Error al procesar docgenerator:', error);
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
                    <strong>GENERAR INFORME.</strong>
                </Typography>
            </Box>
            <>
                <Box sx={{
                    backgroundColor: '#f5f5f5',
                    borderRadius: 1,
                    padding: 2,
                    marginTop: 2,
                    flexGrow: 1,
                    overflow: 'hidden',
                    display: 'flex',
                    flexDirection: 'column'
                }}>
                    <Box sx={{ flexGrow: 1, overflow: 'hidden' }}>
                        {pdfPath.length > 0 ? (
                            <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                                <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%', alignItems: 'center', justifyContent: 'center', gap: 2 }}>
                                    <Typography variant="h6" sx={{ color: '#4D7AFF', textAlign: 'center' }}>
                                        <strong>Informe generado</strong>
                                    </Typography>
                                    {loadingZip ? (
                                        <Box sx={{
                                            display: 'flex',
                                            flexDirection: 'column',
                                            alignItems: 'center',
                                            marginTop: 6
                                        }}>
                                            <CircularProgress sx={{ color: '#4D7AFF', mb: 2 }} />
                                            <Typography variant="body1" sx={{ color: '#4D7AFF' }}>
                                                Descargando statistics.zip...
                                            </Typography>
                                        </Box>
                                    ) : (
                                        <div style={{ display: 'flex', gap: '10px', flexDirection: 'row', justifyContent: 'center' }}>
                                            <Button
                                                variant="contained"
                                                color="primary"
                                                onClick={() => window.open(pdfPath, '_blank')}
                                            >
                                                Abrir PDF
                                            </Button>
                                            <Button
                                                variant="contained"
                                                color="primary"
                                                onClick={handleDownloadZip}
                                            >
                                                Descargar Zip
                                            </Button>
                                        </div>
                                    )}
                                </Box>
                            </Box>
                        ) : (
                            <Box sx={{
                                display: 'flex',
                                flexDirection: 'column',
                                alignItems: 'center',
                                marginTop: 6
                            }}>
                                <CircularProgress sx={{ color: '#4D7AFF', mb: 2 }} />
                                <Typography variant="body1" sx={{ color: '#4D7AFF' }}>
                                    Generando Informe...
                                </Typography>
                            </Box>
                        )}
                    </Box>
                </Box>
            </>
        </Box>
    );
};

export default DocGenerator;
