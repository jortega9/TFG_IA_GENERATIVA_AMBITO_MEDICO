import React, { useState } from 'react';
import { Box, Button, Typography } from '@mui/material';
import { useDropzone } from 'react-dropzone';
import ThemeToggle from '../ThemeToggle';

const ReportSummary = () => {
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
            <h2>ReportSummary</h2>
            
            
        </Box>
    )
}

export default ReportSummary;