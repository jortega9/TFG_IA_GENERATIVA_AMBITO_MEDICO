import React, { useState } from 'react';
import { Box, Button, Typography } from '@mui/material';
import { useDropzone } from 'react-dropzone';
import ThemeToggle from '../ThemeToggle';

const StatisticAnalysis = () => {
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
            width: '50rem',
            height: "18rem",
        }}>
            <Box sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: 3,
            }}>
                <Typography sx={{ color: '#4D7AFF', fontSize: '1.5rem' }}>
                    <strong>Generador de Informes</strong>
                </Typography>
                <ThemeToggle />
            </Box>
            <h2>StatisticAnalysis</h2>
            
        </Box>
    )
}

export default StatisticAnalysis;