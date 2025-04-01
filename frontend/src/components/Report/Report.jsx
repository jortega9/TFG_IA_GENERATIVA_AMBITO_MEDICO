import React, { useState } from 'react';
import DropFiles from '../DropFiles';
import ProcessData from '../Statistics/ProcessData';
import DescStatistics1 from '../Statistics/DescStatistics/DescStatistics1';
import DescStatistics2 from '../Statistics/DescStatistics/DescStatistics2';
import DescStatistics3 from '../Statistics/DescStatistics/DescStatistics3';
import AdvancedStatistics1 from '../Statistics/AdvancesStatistics/AdvancedStatistics1';
import AdvancedStatistics2 from '../Statistics/AdvancesStatistics/AdvancedStatistics2';
import AdvancedStatistics3 from '../Statistics/AdvancesStatistics/AdvancedStatistics3';
import AdvancedStatistics4 from '../Statistics/AdvancesStatistics/AdvancedStatistics4';
import { Button } from '@mui/material';

const Report = () => {
    const steps = ["1", "2", "3", "4", "5", "6", "7", "8"];
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
                return <ProcessData />;
            case 2:
                return <DescStatistics1 />;
            case 3:
                return <DescStatistics2 />;
            case 4:
                return <DescStatistics3 />;
            case 5:
                return <AdvancedStatistics1 />;
            case 6:
                return <AdvancedStatistics2 />;
            case 7:
                return <AdvancedStatistics3 />;
            case 8:
                return <AdvancedStatistics4 />;
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
            case 3:
                return true;
            case 4:
                return true;
            case 5:
                return true;
            case 6:
                return true;
            case 7:
                return true;
            case 8:
                return false;
            default:
                return false;
        }
    };


    const nextStep = () => {
        if (isStepValid() && currentStep < steps.length){
            setCurrentStep(currentStep + 1);
            console.log(currentStep);
        } 

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
