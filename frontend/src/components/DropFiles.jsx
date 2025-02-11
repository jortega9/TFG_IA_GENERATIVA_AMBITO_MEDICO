import React, { useState } from 'react';
import { Box, Button, Typography, Tooltip } from '@mui/material';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import ThemeToggle from './ThemeToggle';

const DropFiles = ({ files, addFiles }) => {

    const getFileNameWithoutExtension = (fileName) => {
        const lastDotIndex = fileName.lastIndexOf('.');
        return lastDotIndex !== -1 ? fileName.substring(0, lastDotIndex) : fileName;
    };

    return (
        <Box sx={{
            backgroundColor: 'white',
            borderRadius: 2,
            padding: 2,
            boxShadow: 1,
            width: '100%',
            height: "64vh",
            display: 'flex',
            flexDirection: 'column'
        }}>
            {/* Títulos y botón */}
            <Box sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: 2,
            }}>
                <Typography sx={{ color: '#4D7AFF', fontSize: '1.5rem' }}>
                    <strong>Generador de Informes</strong>
                </Typography>
                <ThemeToggle />
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
                {/* Mensaje solo si no hay archivos */}
                {files.length === 0 && (
                    <Typography variant="h5" color="gray" sx={{ padding: '20px' }}>
                        Arrastra tus archivos aquí o haz clic para seleccionarlos
                    </Typography>
                )}

                {/* Mostrar archivos con icono y nombre sin extensión */}
                {files.length > 0 && (
                    <>
                        <Typography variant="h6" sx={{ paddingBottom: '20px', color:"#333333" }}>Archivos seleccionados:</Typography>
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
                        onChange={(e) => addFiles([...e.target.files])}
                    />
                </Button>
            </Box>
        </Box>
    );
};

export default DropFiles;
