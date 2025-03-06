import React, { useState, useEffect } from 'react';
import { Box, Typography } from '@mui/material';
import { Circle } from '@mui/icons-material';
import ThemeToggle from '../ThemeToggle';

const ProcessData = () => {
    const [respuesta, setRespuesta] = useState([]);

    const texto = `
        Pensamiento: Primero, necesito cargar el dataset desde el archivo Excel para comenzar el proceso de limpieza.
        Ejecuta: read_excel
        Observacion: Parece que no se ha cargado ningún dato del archivo Excel. Necesito verificar si el archivo se encuentra en la ruta especificada.
        Ejecuta: read_master
        Observacion: No he podido cargar el archivo maestro, lo que puede indicar que no tengo acceso a los archivos o que no existen disponibles.
        Pensamiento: Debo asegurarme de que los archivos estén disponibles antes de continuar.
        Pensamiento: Podría intentar cargar el dataset nuevamente para verificar si hay un problema específico con la ruta.
        Ejecuta: read_excel
        Observacion: No he podido cargar el dataset desde el archivo Excel en ninguno de los intentos. Esto sugiere que puede haber un problema con la disponibilidad del archivo o su formato.
        Pensamiento: Dado que no puedo proceder con la carga del dataset, necesito una confirmación sobre su disponibilidad o una alternativa.
    `.trim();

    const parseString = (input) => {
        const keywords = ["Pensamiento:", "Ejecuta:", "Observacion:", "Resultado:"];
        const result = [];
        let currentKeyword = null;
        let currentContent = "";

        const lines = input.split('\n').map(line => line.trim());
        lines.forEach(line => {
            const keyword = keywords.find(kw => line.startsWith(kw));
            if (keyword) {
                if (currentKeyword) {
                    result.push({ tipo: currentKeyword, contenido: currentContent.trim() });
                }
                currentKeyword = keyword.replace(':', '');
                currentContent = line.replace(keyword, '').trim();
            } else if (currentKeyword) {
                currentContent += ' ' + line.trim();
            }
        });

        if (currentKeyword) {
            result.push({ tipo: currentKeyword, contenido: currentContent.trim() });
        }

        return result;
    };

    useEffect(() => {
        const parsedData = parseString(texto);
        console.log(parsedData);
        setRespuesta(parsedData);
    }, []);

    const getColor = (tipo) => {
        switch (tipo) {
            case 'Pensamiento': return '#1976D2';
            case 'Ejecuta': return '#388E3C';
            case 'Observacion': return '#D32F2F';
            default: return '#333';
        }
    };

    const renderMensaje = (mensaje, index) => (
        <Box key={index} sx={{ display: 'flex', alignItems: 'center', marginBottom: 1, width: '100%' }}>
            <Circle sx={{ fontSize: 12, color: getColor(mensaje.tipo), marginRight: 1 }} />
            <Typography
                variant="body2"
                sx={{ color: '#333', textAlign: 'left', wordBreak: 'break-word' }}
            >
                <strong>{mensaje.tipo}:</strong> {mensaje.contenido}
            </Typography>
        </Box>
    );

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
                alignItems: 'flex-start',
                marginBottom: 1,
                marginTop: 1
            }}>
                <Typography variant="body1" sx={{ color: '#333', paddingBottom: 2 }}>
                    <strong> Se están procesando los datos de los documentos subidos. </strong>
                </Typography>

                {respuesta.map((mensaje, index) => renderMensaje(mensaje, index))}
            </Box>
        </Box>
    );
};

export default ProcessData;
