import React, { useState, useEffect } from 'react';
import {
    Box,
    Button,
    Typography,
    ToggleButton,
    ToggleButtonGroup,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    CircularProgress,
    Divider
} from '@mui/material';

import KaplanVariableCard from './KaplanVariableCard';

// import bilat2_kaplan_meier_plot from '../../../../../data/processed/kaplan_meier/bilat2_kaplan_meier_plot.png';
// import capras_kaplan_meier_plot from '../../../../../data/processed/kaplan_meier/capras_kaplan_meier_plot.png';
// import extracap_kaplan_meier_plot from '../../../../../data/processed/kaplan_meier/extracap_kaplan_meier_plot.png';
// import gleason1_kaplan_meier_plot from '../../../../../data/processed/kaplan_meier/gleason1_kaplan_meier_plot.png';
// import gleason2_kaplan_meier_plot from '../../../../../data/processed/kaplan_meier/gleason2_kaplan_meier_plot.png';
// import hereda_kaplan_meier_plot from '../../../../../data/processed/kaplan_meier/hereda_kaplan_meier_plot.png';
// import localiz_kaplan_meier_plot from '../../../../../data/processed/kaplan_meier/localiz_kaplan_meier_plot.png';
// import margen_kaplan_meier_plot from '../../../../../data/processed/kaplan_meier/margen_kaplan_meier_plot.png';
// import multifoc_kaplan_meier_plot from '../../../../../data/processed/kaplan_meier/multifoc_kaplan_meier_plot.png';
// import pinag_kaplan_meier_plot from '../../../../../data/processed/kaplan_meier/pinag_kaplan_meier_plot.png';
// import ra_estroma_kaplan_meier_plot from '../../../../../data/processed/kaplan_meier/ra_estroma_kaplan_meier_plot.png';
// import rtpadyu_kaplan_meier_plot from '../../../../../data/processed/kaplan_meier/rtpadyu_kaplan_meier_plot.png';
// import tnm2_kaplan_meier_plot from '../../../../../data/processed/kaplan_meier/tnm2_kaplan_meier_plot.png';
// import vvss_kaplan_meier_plot from '../../../../../data/processed/kaplan_meier/vvss_kaplan_meier_plot.png';


const kaplanVars = [
    { name: "bilat2", plot: "bilat2_kaplan_meier_plot.png" },
    { name: "capras", plot: "capras_kaplan_meier_plot.png" },
    { name: "extracap", plot: "extracap_kaplan_meier_plot.png" },
    { name: "gleason1", plot: "gleason1_kaplan_meier_plot.png" },
    { name: "gleason2", plot: "gleason2_kaplan_meier_plot.png" },
    { name: "hereda", plot: "hereda_kaplan_meier_plot.png" },
    { name: "localiz", plot: "localiz_kaplan_meier_plot.png" },
    { name: "margen", plot: "margen_kaplan_meier_plot.png" },
    { name: "multifoc", plot: "multifoc_kaplan_meier_plot.png" },
    { name: "pinag", plot: "pinag_kaplan_meier_plot.png" },
    { name: "ra_estroma", plot: "ra_estroma_kaplan_meier_plot.png" },
    { name: "rtpadyu", plot: "rtpadyu_kaplan_meier_plot.png" },
    { name: "tnm2", plot: "tnm2_kaplan_meier_plot.png" },
    { name: "vvss", plot: "vvss_kaplan_meier_plot.png" },
];

const KaplanStatisticsVars = ({ csvKaplanPath }) => {
    const [loadedCount, setLoadedCount] = useState(0);

    const total = kaplanVars.length;
    const allLoaded = loadedCount === total - 1;

    const handleCardLoaded = () => {
        setLoadedCount((prev) => prev + 1);
    };

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
                    <strong> ANÁLISIS DE KAPLAN MEIER EN FUNCIÓN DE CADA VARIABLE. </strong>
                </Typography>
                {/* <ThemeToggle /> */}
            </Box>
            <>
                <Box sx={{ backgroundColor: '#f5f5f5', borderRadius: 1, padding: 2, marginTop: 2, flexGrow: 1, overflowY: 'auto' }}>
                    {kaplanVars.map(({ name, plot }, index) => (
                        <Box key={name}>
                            <KaplanVariableCard
                                key={name}
                                variableName={name}
                                plotImage={`http://127.0.0.1:8000/ai/kaplan-image/${plot}`}
                                csvKaplanPath={csvKaplanPath}
                                onLoaded={handleCardLoaded}
                            />
                            {index < kaplanVars.length - 1 && (
                                <Divider sx={{ my: 4, borderColor: '#e0e0e0'}} />
                            )}
                        </Box>
                    ))}
                </Box>
            </>
        </Box>
    );
};

export default KaplanStatisticsVars;