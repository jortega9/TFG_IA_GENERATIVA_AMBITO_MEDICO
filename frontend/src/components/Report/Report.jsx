import React, { useState } from 'react';
import DropFiles from '../DropFiles';
import SelectGroupVariable from '../Statistics/SelectGroupVariable';
import SelectTimeVariable from '../Statistics/SelectTimeVariable';
import ProcessDescData from '../Statistics/ProcessDescData';
import ProcessAdvData from '../Statistics/ProcessAdvData';
import DescStatistics1 from '../Statistics/DescStatistics/DescStatistics1';
import DescStatistics2 from '../Statistics/DescStatistics/DescStatistics2';
import DescStatistics3 from '../Statistics/DescStatistics/DescStatistics3';
import AdvancedStatistics1 from '../Statistics/AdvancesStatistics/AdvancedStatistics1';
import AdvancedStatistics2 from '../Statistics/AdvancesStatistics/AdvancedStatistics2';
import AdvancedStatistics3 from '../Statistics/AdvancesStatistics/AdvancedStatistics3';
import AdvancedStatistics4 from '../Statistics/AdvancesStatistics/AdvancedStatistics4';
import AdvancedStatistics5 from '../Statistics/AdvancesStatistics/AdvancedStatistics5';
import { Button } from '@mui/material';

const Report = () => {
    const steps = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"];
    const [currentStep, setCurrentStep] = useState(0);

    const [descNumVars, setDescnumVars] = useState([]);
    const [descNumCsv, setDescNumCsv] = useState('');
    const [descCatVars, setDescCatVars] = useState([]);
    const [descCatCsv, setDescCatCsv] = useState('');

    const [csvMannWhitneyPath, setCsvMannWhitneyPath] = useState("");
    const [csvTStudentPath, setCsvTStudentPath] = useState("");

    const [csvChiPath, setCsvChiPath] = useState("");
    const [csvFisherPath, setCsvFisherPath] = useState("");
    const [csvSignificantPath, setCsvSignificantPath] = useState("");

    const [isDataPrepared, setIsDataPrepared] = useState(false);
    const [isDescDataProcessed, setIsDescDataProcessed] = useState(false);
    const [isAdvDataProcessed, setIsAdvDataProcessed] = useState(false);
    const [isGroupIdentified, setIsGroupIdentified] = useState(false);
    const [isTimeIdentified, setIsTimeIdentified] = useState(false);

    const getStepContent = (step) => {
        switch (step) {
            case 0:
                return <DropFiles setIsDataPrepared={setIsDataPrepared}/>;
            case 1:
                return <SelectGroupVariable setIsGroupIdentified={setIsGroupIdentified}/>;
            case 2:
                return <ProcessDescData
                setIsDataProcessed={setIsDescDataProcessed}
                setDescnumVars={setDescnumVars}
                setDescNumCsv={setDescNumCsv}
                setDescCatVars={setDescCatVars}
                setDescCatCsv={setDescCatCsv}
            />;
            case 3:
                return <DescStatistics1 descNumCsv={descNumCsv}/>;
            case 4:
                return <DescStatistics2 descNumCsv={descNumCsv}/>;
            case 5:
                return <DescStatistics3 descCatCsv={descCatCsv}/>;
            case 6:
                return <SelectTimeVariable setIsTimeIdentified={setIsTimeIdentified} />;
            case 7:
                return <ProcessAdvData 
                setIsDataProcessed={setIsAdvDataProcessed}
                setCsvMannWhitneyPath={setCsvMannWhitneyPath}
                setCsvTStudentPath={setCsvTStudentPath}
                setCsvChiPath={setCsvChiPath}
                setCsvFisherPath={setCsvFisherPath}
                setCsvSignificantPath={setCsvSignificantPath}
            />;
            case 8:
                return <AdvancedStatistics1 csvChiPath={csvChiPath} />;
            case 9:
                return <AdvancedStatistics2 csvFisherPath={csvFisherPath}/>;
            case 10:
                return <AdvancedStatistics3 csvMannWhitneyPath={csvMannWhitneyPath}/>;
            case 11:
                return <AdvancedStatistics4 csvTStudentPath={csvTStudentPath}/>;
            case 12:
                return <AdvancedStatistics5 csvSignificantPath={csvSignificantPath}/>;
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
                return isGroupIdentified;
                // return true;
            case 2:
                return isDescDataProcessed;
                // return true;
            case 3:
                return true;
            case 4:
                return true;
            case 5:
                return true;
            case 6:
                return isTimeIdentified;
            case 7:
                return true;
            case 8:
                return true;
            case 9:
                return true;
            case 10:
                return true;
            case 11:
                return true;
            case 12:
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
