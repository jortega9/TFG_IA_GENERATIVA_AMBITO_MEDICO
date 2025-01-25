import "./Controls.css";
import { Accordion, AccordionDetails, AccordionSummary, Box, FormControlLabel, FormGroup, Checkbox } from '@mui/material';
import {React, useState} from 'react';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import GroupsIcon from '@mui/icons-material/Groups';
import SummarizeIcon from '@mui/icons-material/Summarize';


function Controls({ onChatAccessChange, onReportAccessChange }) {
    const [isChatAccessible, setIsChatAccessible] = useState(false);
    const [isReportAccessible, setIsReportAccessible] = useState(false);

    const handleCheckboxChat = (event) => {
        const isChecked = event.target.checked;
        setIsChatAccessible(isChecked);
        onChatAccessChange(isChecked);
    };

    const handleCheckboxReport = (event) => {
        const isChecked = event.target.checked;
        setIsReportAccessible(isChecked);
        onReportAccessChange(isChecked);
    };

    return (
        <Box sx={{flexGRow:1, height: "100%", width:"100%", overflow: 'auto' }}>
            <Accordion className="accordion-box points">
                <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel1-content" id="panel1-header">
                    <div className="accordion-title">
                        <GroupsIcon fontsize='large'/>
                        <h4 style={{margin: 0}}>Consultas</h4>
                    </div>
                </AccordionSummary>
                <AccordionDetails>
                    <FormGroup>
                        <div className="puntos-context">
                            <div className="checkbox-column">
                                <FormControlLabel control={<Checkbox color="success" onChange={handleCheckboxChat} id='chat'/>} label="Acceder al Chat " />
                            </div>
                        </div>
                    </FormGroup>
                </AccordionDetails>
            </Accordion>
            <Accordion className="accordion-box points">
                <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel1-content" id="panel1-header">
                    <div className="accordion-title">
                        <SummarizeIcon fontsize='large'/>
                        <h4 style={{margin: 0}}>Informes</h4>
                    </div>
                </AccordionSummary>
                <AccordionDetails>
                    <FormGroup>
                        <div className="puntos-context">
                            <div className="checkbox-column">
                                <FormControlLabel control={<Checkbox color="success" onChange={handleCheckboxReport} id='report'/>} label="Generador de Informes " />
                            </div>
                        </div>
                    </FormGroup>
                </AccordionDetails>
            </Accordion>
        </Box>
    )
}

export default Controls;