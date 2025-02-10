import React, { useState } from 'react';
import DropFiles from '../DropFiles';
import StatisticAnalysis from '../StatisticAnalysis';
import ReportSummary from '../ReportSummary';
import { Button } from '@mui/material';

const Report = () => {
    const steps = ["1", "2", "3"];
    const [currentStep, setCurrentStep] = useState(0);
    const [files, setFiles] = useState([]);

    const addFiles = (acceptedFiles) => {
        setFiles((prevFiles) => [...prevFiles, ...acceptedFiles]);
        console.log(acceptedFiles);
    };

    const getStepContent = (step) => {
        switch (step) {
            case 0:
                return <DropFiles files={files} addFiles={addFiles} />;
            case 1:
                return <StatisticAnalysis/>;
            case 2:
                return <ReportSummary/>;
            default:
                return <p>Error: Paso desconocido</p>;
            }
    };

    const isStepValid = () => {
        switch (currentStep) {
            case 0:
                return files.length === 2;
            case 1:
                return true;
            case 2:
                return true;
            default:
                return false;
        }
    };


    const nextStep = () => {
        if (isStepValid() && currentStep < steps.length - 1) setCurrentStep(currentStep + 1);
    };

    const prevStep = () => {
        if (currentStep > 0) setCurrentStep(currentStep - 1);
    };

    return (
        <div style={{ width: "100%", height: "100%"}}>
            <div style={{ width: "100%", height: "100%", textAlign: "center" }}>
                {getStepContent(currentStep)}
                <Button onClick={prevStep} disabled={currentStep === 0}>
                Atrás
                </Button>
                <Button onClick={nextStep} disabled={!isStepValid()}>
                Siguiente
                </Button>
            </div>
        </div>
    );
};

export default Report;
