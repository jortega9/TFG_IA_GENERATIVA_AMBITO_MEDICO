import React, { useState } from 'react';
import DropFiles from '../DropFiles';
import ProcessDescData from '../Statistics/ProcessDescData';
import ProcessAdvData from '../Statistics/ProcessAdvData';
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

    const [descNumVars, setDescnumVars] = useState([]);
    const [descNumCsv, setDescNumCsv] = useState('');
    const [descCatVars, setDescCatVars] = useState([]);
    const [descCatCsv, setDescCatCsv] = useState('');

    const [csvMannWhitneyPath, setCsvMannWhitneyPath] = useState("");
    const [csvTStudentPath, setCsvTStudentPath] = useState("");

    const [csvChiPath, setCsvChiPath] = useState("");
    const [csvFisherPath, setCsvFisherPath] = useState("");
    const [groupVariable, setGroupVariable] = useState("");
    const [validKeys, setValidKeys] = useState([]);

    const [isDataPrepared, setIsDataPrepared] = useState(false);
    const [isDescDataProcessed, setIsDescDataProcessed] = useState(false);
    const [isAdvDataProcessed, setIsAdvDataProcessed] = useState(false);

    const getStepContent = (step) => {
        switch (step) {
            case 0:
                return <DropFiles setIsDataPrepared={setIsDataPrepared}/>;
            case 1:
                return <ProcessDescData
                setIsDataProcessed={setIsDescDataProcessed}
                setDescnumVars={setDescnumVars}
                setDescNumCsv={setDescNumCsv}
                setDescCatVars={setDescCatVars}
                setDescCatCsv={setDescCatCsv}
            />;
            case 2:
                return <DescStatistics1 descNumCsv={descNumCsv}/>;
            case 3:
                return <DescStatistics2 descNumCsv={descNumCsv}/>;
            case 4:
                return <DescStatistics3 descCatCsv={descCatCsv}/>;
            case 5:
                return <ProcessAdvData 
                setIsDataProcessed={setIsAdvDataProcessed}
                setGroupVariable={setGroupVariable}
                setValidKeys={setValidKeys}
                setCsvMannWhitneyPath={setCsvMannWhitneyPath}
                setCsvTStudentPath={setCsvTStudentPath}
                setCsvChiPath={setCsvChiPath}
                setCsvFisherPath={setCsvFisherPath}
            />;
            case 6:
                return <AdvancedStatistics1
                groupVariable={groupVariable}
                csvMannWhitneyPath={csvMannWhitneyPath}
                csvTStudentPath={csvTStudentPath}
                csvChiPath={csvChiPath}
                csvFisherPath={csvFisherPath}

                />;
            case 7:
                return <AdvancedStatistics2 />;
            case 8:
                return <AdvancedStatistics3 />;
            case 9:
                return <AdvancedStatistics4 />;
            default:
                return <p>Error: Paso desconocido</p>;
            }
    };

    const isStepValid = () => {
        switch (currentStep) {
            case 0:
                return isDataPrepared;
                // return true;
            case 1:
                return isDescDataProcessed;
                // return true;
            case 2:
                return true;
            case 3:
                return true;
            case 4:
                return true;
            case 5:
                return isAdvDataProcessed;
            case 6:
                return true;
            case 7:
                return true;
            case 8:
                return true;
            case 9:
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
