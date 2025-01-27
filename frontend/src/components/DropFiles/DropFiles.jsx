import React, { useState } from 'react';
import { Box, Button, Typography } from '@mui/material';
import { useDropzone } from 'react-dropzone';
import ThemeToggle from '../ThemeToggle';

const DropFiles = () => {
    const [files, setFiles] = useState([]);

    const addFiles = (acceptedFiles) => {
        setFiles((prevFiles) => [...prevFiles, ...acceptedFiles]);
    };

    return (
        <Box sx={{
            backgroundColor: 'white',
            borderRadius: 2,
            padding: 4,
            boxShadow: 1,
            width: '721px',
            height: "292px",
        }}>
            <Box sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: 3,
            }}>
                <Typography variant="h4" component="h2" sx={{ color: '#4D7AFF' }}><strong>Generador de Informes</strong></Typography>
                <ThemeToggle />
            </Box>
            <Box sx={{
                border: '2px dashed gray',
                padding: 4,
                textAlign: 'center',
                borderRadius: 2,
                backgroundColor: '#F5f5f5',
            }}>
                <div style={{ cursor: 'pointer', padding: '30px' }}>
                    <Typography variant="h5" color="textSecondary">
                        Arrastra tus archivos aquí o haz clic para seleccionarlos
                    </Typography>
                </div>
                <Button
                    variant="contained"
                    component="label"
                    sx={{ marginTop: 3, backgroundColor: '#4D7AFF', fontSize: '1.1rem' }}
                >
                    Buscar Archivos
                    <input
                        type="file"
                        hidden
                        multiple
                        onChange={(e) => addFiles([...e.target.files])}
                    />
                </Button>

                {files.length > 0 && (
                    <Box mt={3}>
                        <Typography variant="h6">Archivos seleccionados:</Typography>
                        <ul>
                            {files.map((file, index) => (
                                <li key={index}>{file.name}</li>
                            ))}
                        </ul>
                    </Box>
                )}
            </Box>
            
        </Box>
    )
}

export default DropFiles;