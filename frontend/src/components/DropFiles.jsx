import React, { useState } from 'react';
import { Box, Button, Typography, Tooltip } from '@mui/material';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import * as XLSX from 'xlsx';
import mammoth from 'mammoth';

const DropFiles = ({ files, addFiles }) => {
    const [fileData, setFileData] = useState(null);

    const getFileNameWithoutExtension = (fileName) => {
        const lastDotIndex = fileName.lastIndexOf('.');
        return lastDotIndex !== -1 ? fileName.substring(0, lastDotIndex) : fileName;
    };

    const convertTextToDictionary = (value) => {
        const lines = value.split("\n").map(line => line.trim()).filter(line => line.length > 0);
    
        const data = { sections: [] };
        let currentSection = null;
    
        lines.forEach(line => {
            if (line.startsWith("# ")) {  // Nueva sección
                currentSection = { title: line.substring(2), variables: [] };
                data.sections.push(currentSection);
            } else if (line.startsWith("/ ")) {  // Nueva variable
                if (currentSection) {
                    currentSection.variables.push({ name: line.substring(2), description: [] });
                }
            } else if (line.startsWith("? ")) {  // Descripción de variable
                if (currentSection && currentSection.variables.length > 0) {
                    currentSection.variables[currentSection.variables.length - 1].description.push(line.substring(2));
                }
            }
        });
    
        return data;  // Retorna el diccionario directamente
    };

    const handleFileUpload = (event) => {
        const uploadedFiles = event.target.files;
        if (!uploadedFiles || uploadedFiles.length === 0) return;
    
        const newFiles = Array.from(uploadedFiles);
        addFiles(newFiles);
    
        newFiles.forEach((file) => {
            if (file.name.endsWith('.xlsx')) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const data = new Uint8Array(e.target.result);
                    const workbook = XLSX.read(data, { type: "array" });
                    const firstSheet = workbook.SheetNames[0];
                    const sheetData = XLSX.utils.sheet_to_json(workbook.Sheets[firstSheet]);
    
                    console.log("Contenido del archivo XLSX:", sheetData);
                    setFileData(sheetData);
                };
                reader.readAsArrayBuffer(file);
            } 
            else if (file.name.endsWith('.docx')) {
                console.log("Archivo Word:", file);
            
                const reader = new FileReader();
                reader.onload = async (e) => {
                    try {
                        const arrayBuffer = e.target.result;
                        const result = await mammoth.extractRawText({ arrayBuffer });
                        
                        const jsonValue = convertTextToDictionary(result.value);
                        console.log("JSON generado:", jsonValue);
                        setFileData(jsonValue);
            
                    } catch (error) {
                        console.error("Error al leer el archivo .docx:", error);
                    }
                };
                reader.readAsArrayBuffer(file);
            }
        });
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
            <Typography sx={{ color: '#4D7AFF', fontSize: '1.5rem' }}>
                <strong>Generador de Informes</strong>
            </Typography>

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
                        Arrastra tus archivos aquí o haz clic para seleccionarlos
                    </Typography>
                )}

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
                        onChange={handleFileUpload}
                    />
                </Button>
            </Box>
        </Box>
    );
};

export default DropFiles;
