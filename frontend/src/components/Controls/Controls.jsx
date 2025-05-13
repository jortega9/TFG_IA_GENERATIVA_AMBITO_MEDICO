import "./Controls.css";
import { Accordion, AccordionDetails, AccordionSummary, FormControlLabel, FormGroup, Checkbox } from '@mui/material';
import { React, useState } from 'react';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import GroupsIcon from '@mui/icons-material/Groups';
import SummarizeIcon from '@mui/icons-material/Summarize';

function Controls({ onChatAccessChange, onReportAccessChange }) {
    const [isChatAccessible, setIsChatAccessible] = useState(false);
    const [isReportAccessible, setIsReportAccessible] = useState(false);

    /**
     * Activar funcionalidad de chat
     * 
     * @param {*} event 
     */
    const handleCheckboxChat = (event) => {
        const isChecked = event.target.checked;
        setIsChatAccessible(isChecked);
        onChatAccessChange(isChecked);
    };

    /**
     * Activar funcionalidad de genración de informes
     * 
     * @param {*} event 
     */
    const handleCheckboxReport = (event) => {
        const isChecked = event.target.checked;
        setIsReportAccessible(isChecked);
        onReportAccessChange(isChecked);
    };

    return (
        <div className="controls-container">
            <Accordion className="accordion-box">
                <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel1-content" id="panel1-header">
                    <div className="accordion-title">
                        <GroupsIcon className="icon" />
                        <h4 className="title">Asistente IA</h4>
                    </div>
                </AccordionSummary>
                <AccordionDetails>
                    <FormGroup>
                        <div className="checkbox-group">
                            <FormControlLabel control={<Checkbox color="success" onChange={handleCheckboxChat} id='chat'/>} label="Acceder al Chat" />
                        </div>
                    </FormGroup>
                </AccordionDetails>
            </Accordion>
            <Accordion className="accordion-box">
                <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel2-content" id="panel2-header">
                    <div className="accordion-title">
                        <SummarizeIcon className="icon" />
                        <h4 className="title">Informes</h4>
                    </div>
                </AccordionSummary>
                <AccordionDetails>
                    <FormGroup>
                        <div className="checkbox-group">
                            <FormControlLabel control={<Checkbox color="success" onChange={handleCheckboxReport} id='report'/>} label="Generador de Informes" />
                        </div>
                    </FormGroup>
                </AccordionDetails>
            </Accordion>
        </div>
    );
}

export default Controls;
