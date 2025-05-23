import React, { useState } from 'react';
import { Box, Button, Typography, Tooltip, CircularProgress } from '@mui/material';
import { Snackbar, Alert } from '@mui/material';
import ThemeToggle from './ThemeToggle';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import * as XLSX from 'xlsx';
import mammoth from 'mammoth';

const DropFiles = ({ setIsDataPrepared }) => {
    const [fileData, setFileData] = useState([]);
    const [text, setText] = useState("");
    const [files, setFiles] = useState([]);
    const [preparingData, setPreparingData] = useState(false);
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [openErrorSnackbar, setOpenErrorSnackbar] = useState(false);
    const [errorFileNames, setErrorFileNames] = useState([]);

    const addFiles = (acceptedFiles) => {
        setFiles((prevFiles) => [...prevFiles, ...acceptedFiles]);
        console.log(acceptedFiles);
    };

    const getFileNameWithoutExtension = (fileName) => {
        const lastDotIndex = fileName.lastIndexOf('.');
        return lastDotIndex !== -1 ? fileName.substring(0, lastDotIndex) : fileName;
    };

    /**
     * Copiar archivos proporcionados por el usuario a la carpeta de trabajo.
     * 
     * @param {*} event 
     * @returns 
     */
    const handleFileUpload = async (event) => {
        const uploadedFiles = event.target.files;
        if (!uploadedFiles || uploadedFiles.length === 0) return;
        
        const validExtensions = ['.xlsx', '.json'];
        const newFiles = Array.from(uploadedFiles);

        const validFiles = [];
        const errorFiles = [];

        newFiles.forEach((file) => {
            const extension = file.name.slice(file.name.lastIndexOf('.')).toLowerCase();
            
            if(validExtensions.includes(extension)) {
                validFiles.push(file);
            }
            else {
                errorFiles.push({name: file.name, error: "Formato no válido"});
            }
        
        });

        if (errorFiles.length > 0){
            setErrorFileNames(errorFiles.map(file => file.name));
            setOpenErrorSnackbar(true);
        }

        if (validFiles.length === 0) return;

        addFiles(validFiles);
    
        const formData = new FormData();
        validFiles.forEach((file) => {
            formData.append('files', file);
        });
    
        console.log('Archivos subidos:', validFiles);
    
        const response = await fetch('http://127.0.0.1:8000/ai/copyDocs', {
            method: 'POST',
            body: formData
        });
    
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
    
        const result = await response.json();
        setFileData(result.paths)
        console.log("Respuesta del servidor:", result);
    };

    /**
     * Preparar los datos para proporcionarselos al modelo.
     * 
     * @returns 
     */
    const handlePrepareData = async () => {
        const excelFile = fileData.find((file) => file.includes('.xlsx'));
        const masterFile = fileData.find((file) => file.includes('.json'));
        setPreparingData(true);
    
        if (!excelFile || !masterFile) {
            console.error("Archivos necesarios no encontrados.");
            return;
        }
        
        const requestData = {
            master_path: masterFile,
            excel_path: excelFile
        };

        console.log("Request Data:", requestData);
    
        try {
            const response = await fetch('http://127.0.0.1:8000/ai/prepare-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });
    
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            
            const result = await response.json();
            console.log("Respuesta del servidor:", result);
            setIsDataPrepared(true);
            setOpenSnackbar(true);
        } catch (error) {
            console.error("Error al realizar la petición:", error);
        }
        finally {
            setPreparingData(false);
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
            flexDirection: 'column'
            }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: '10%' }}>
                    <Typography sx={{ color: '#4D7AFF', fontSize: '0.9rem' }}>
                        <strong>CARGAR BBDD Y ARCHIVO MAESTRO</strong>
                    </Typography>
                    {/* <ThemeToggle /> */}
                </Box>

                <Box sx={{
                    border: '2px dashed gray',
                    padding: 4,
                    textAlign: 'center',
                    borderRadius: 2,
                    backgroundColor: '#F5f5f5',
                    flexGrow: 1,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: files.length > 0 ? 'flex-start' : 'center',
                    overflow: 'hidden'
                }}>
                    {files.length === 0 && (
                        <Typography variant="h5" color="gray" sx={{ padding: '20px' }}>
                            Arrastra tus archivos aquí o haz clic para seleccionarlos (.xlsx y .json)
                        </Typography>
                    )}

                    {files.length > 0 && (
                        <>
                            <Typography variant="h6" sx={{ paddingBottom: '20px', color:"#4D7AFF" }}><strong>Archivos seleccionados:</strong></Typography>
                            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                                {files.map((file, index) => {
                                    const fileName = getFileNameWithoutExtension(file.name);
                                    return (
                                        <Box key={index} sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                                            <InsertDriveFileIcon sx={{ fontSize: 40, color: '#4D7AFF' }} />
                                            <Tooltip title={fileName} arrow>
                                                <Typography variant="body2" noWrap sx={{
                                                    maxWidth: '100px',
                                                    textAlign: 'center',
                                                    overflow: 'hidden',
                                                    textOverflow: 'ellipsis',
                                                    whiteSpace: 'nowrap',
                                                    color: '#333333'
                                                }}>
                                                    {fileName}
                                                </Typography>
                                            </Tooltip>
                                        </Box>
                                    );
                                })}
                            </Box>
                        </>
                    )}

                    {files.length < 2 ? (
                        <Button
                            variant="contained"
                            component="label"
                            sx={{ backgroundColor: '#4D7AFF', fontSize: '1.1rem', marginTop: 6, alignSelf: 'center' }}
                        >
                            Buscar Archivos
                            <input
                                type="file"
                                hidden
                                multiple
                                onChange={handleFileUpload}
                            />
                        </Button>
                    ) : ( 
                        <>
                            {
                                preparingData ? (
                                    <Box sx={{
                                        display: 'flex',
                                        flexDirection: 'column',
                                        alignItems: 'center',
                                        marginTop: 6
                                    }}>
                                        <CircularProgress sx={{ color: '#4D7AFF', mb: 2 }} />
                                        <Typography variant="body1" sx={{ color: '#4D7AFF' }}>
                                        Preparando datos...
                                        </Typography>
                                    </Box>
                                ) : (
                                    <Button
                                    variant="contained"
                                    sx={{ backgroundColor: '#4D7AFF', fontSize: '1.1rem', marginTop: 6, alignSelf: 'center' }}
                                    onClick={handlePrepareData}
                                    >
                                        Preparar Datos
                                    </Button>   
                                )
                            }                 
                        </>
                    )}
                </Box>
            </Box>

            <Snackbar open={openSnackbar} autoHideDuration={4000} onClose={() => setOpenSnackbar(false)} anchorOrigin={{ vertical: 'top', horizontal: 'center' }}            >
                <Alert onClose={() => setOpenSnackbar(false)} severity="success" sx={{ width: '100%' }}>
                    Datos de la base de datos y archivo maestro preparados.
                </Alert>
            </Snackbar>

            <Snackbar open={openErrorSnackbar} autoHideDuration={4000} onClose={() => setOpenErrorSnackbar(false)} anchorOrigin={{ vertical: 'top', horizontal: 'center' }}            >
                <Alert onClose={() => setOpenErrorSnackbar(false)} severity="error" sx={{ width: '100%' }}>
                    Formato no valido en: {errorFileNames.join(', ')}
                </Alert>
            </Snackbar>
        </>
        
    );
};

export default DropFiles;