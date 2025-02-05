import React, { useState } from 'react';
import DropFiles from '../DropFiles/DropFiles';
import StatisticAnalysis from '../StatisticAnalysis/StatisticAnalysis';
import ReportSummary from '../ReportSummary/ReportSummary';
import { Button } from '@mui/material';

const Report = () => {
    const steps = ["1", "2", "3"];

    const getStepContent = (step) => {
        switch (step) {
            case 0:
                return <DropFiles/>;
            case 1:
                return <StatisticAnalysis/>;
            case 2:
                return <ReportSummary/>;
            default:
                return <p>Error: Paso desconocido</p>;
            }
    };

    const [currentStep, setCurrentStep] = useState(0);

    const nextStep = () => {
        if (currentStep < steps.length - 1) setCurrentStep(currentStep + 1);
    };

    const prevStep = () => {
        if (currentStep > 0) setCurrentStep(currentStep - 1);
    };

    return (
        <div style={{ width: "100%", margin: "auto", marginTop: "50px" }}>
            <div style={{ width: "100%", marginTop: "20px", textAlign: "center" }}>
                {getStepContent(currentStep)}
                <Button onClick={prevStep} disabled={currentStep === 0}>
                Atrás
                </Button>
                <Button onClick={nextStep} disabled={currentStep === steps.length - 1}>
                Siguiente
                </Button>
            </div>
        </div>
    );
};

export default Report;
