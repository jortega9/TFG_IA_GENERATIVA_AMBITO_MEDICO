import React, { useState } from 'react';
import { Box, Button, Typography } from '@mui/material';
import ThemeToggle from '../../ThemeToggle';

const DescStatistics1 = () => {
    const [respuesta, setRespuesta] = useState('Aquí se mostrará la respuesta generada.');

    return (
        <Box sx={{
            backgroundColor: 'white',
            borderRadius: 2,
            padding: 2,
            boxShadow: 1,
            width: '100%',
            height: "64vh",
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden'
        }}>
            <Box sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',               
            }}>
                <Typography sx={{ color: '#4D7AFF', fontSize: '1.5rem' }}>
                    <strong>Generador de Informes</strong>
                </Typography>
                <ThemeToggle />
            </Box>            
            <Box sx={{
                backgroundColor: '#f5f5f5',
                borderRadius: 1,
                padding: 2,
                flexGrow: 1,
                overflowY: "scroll",
                overflowX: "hidden",
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                marginBottom: 1,
                marginTop: 1
            }}>
                <div style={{ padding: 3 }}>
                    <Typography variant="body1" sx={{ color: '#333', wordBreak: 'break-word' }}>
                        <strong>Determinar Media y Desviación Típica siguiendo una Distribución Normal. (Variables Númericas)</strong>
                    </Typography>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', padding: 2, alignItems: 'flex-start', width: '100%' }}>
                    <Typography variant="body1" sx={{ color: '#333' }}>
                        {respuesta}
                    </Typography>
                    <Typography variant="body1" sx={{ color: '#333' }}>
                        {respuesta}
                    </Typography>
                    <Typography variant="body1" sx={{ color: '#333' }}>
                        {respuesta}
                    </Typography>
                    <Typography variant="body1" sx={{ color: '#333' }}>
                        {respuesta}
                    </Typography>
                    <Typography variant="body1" sx={{ color: '#333' }}>
                        {respuesta}
                    </Typography>
                    <Typography variant="body1" sx={{ color: '#333' }}>
                        {respuesta}
                    </Typography>
                    <Typography variant="body1" sx={{ color: '#333' }}>
                        {respuesta}
                    </Typography>
                    <Typography variant="body1" sx={{ color: '#333' }}>
                        {respuesta}
                    </Typography>
                    <Typography variant="body1" sx={{ color: '#333' }}>
                        {respuesta}
                    </Typography>
                    <Typography variant="body1" sx={{ color: '#333' }}>
                        {respuesta}
                    </Typography>
                    <Typography variant="body1" sx={{ color: '#333' }}>
                        {respuesta}
                    </Typography>
                    <Typography variant="body1" sx={{ color: '#333' }}>
                        {respuesta}
                    </Typography>
                    <Typography variant="body1" sx={{ color: '#333' }}>
                        {respuesta}
                    </Typography>
                    <Typography variant="body1" sx={{ color: '#333' }}>
                        {respuesta}
                    </Typography>
                </div>
            </Box>
        </Box>
    );
};

export default DescStatistics1;
