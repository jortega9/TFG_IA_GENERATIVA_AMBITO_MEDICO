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
import KaplanStatistics1 from '../Statistics/Kaplan/KaplanStatistics1';
import KaplanStatisticsVars from '../Statistics/Kaplan/KaplanStatisticsVars';
import CoxStatistics from '../Statistics/Cox/CoxStatistics';
import DocGenerator from '../Statistics/DocGenerator/DocGenerator';
import { Button } from '@mui/material';

const Report = () => {
    const steps = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"];
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

    const [csvKaplanPath, setCsvKaplanPath] = useState("");
    const [imagesKaplanPath, setImagesKaplanPath] = useState("");
    const [csvCoxPath, setCsvCoxPath] = useState("");

    const [isDataPrepared, setIsDataPrepared] = useState(false);
    const [isDescDataProcessed, setIsDescDataProcessed] = useState(false);
    const [isAdvDataProcessed, setIsAdvDataProcessed] = useState(false);
    const [isGroupIdentified, setIsGroupIdentified] = useState(false);
    const [isTimeIdentified, setIsTimeIdentified] = useState(false);

    /**
     * Obtener el contenido de la sección actual durante el proceso de generación del informe
     * 
     * @param {*} step 
     * @returns 
     */
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
                setImagesKaplanPath={setImagesKaplanPath}
                setCsvKaplanPath={setCsvKaplanPath}
                setCsvCoxPath={setCsvCoxPath}
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
            case 13:
                return <KaplanStatistics1 csvKaplanPath={csvKaplanPath} imagesKaplanPath={imagesKaplanPath}/>;
            case 14:
                return <KaplanStatisticsVars csvKaplanPath={csvKaplanPath} />
            case 15:
                return <CoxStatistics csvCoxPath={csvCoxPath} />
            case 16:
                return <DocGenerator />
            default:
                return <p>Error: Paso desconocido</p>;
            }
    };

    /**
     * Comprobar si el paso actual es válido para avanzar en el proceso de generación del informe
     * 
     * @returns 
     */
    const isStepValid = () => {
        switch (currentStep) {
            case 0:
                return isDataPrepared;
            case 1:
                return isGroupIdentified;
            case 2:
                return isDescDataProcessed;
            case 3:
                return true;
            case 4:
                return true;
            case 5:
                return true;
            case 6:
                return isTimeIdentified;
            case 7:
                return isAdvDataProcessed;
            case 8:
                return true;
            case 9:
                return true;
            case 10:
                return true;
            case 11:
                return true;
            case 12:
                return true;
            case 13:
                return true;
            case 14:
                return true;
            case 15:
                return true;
            case 16:
                return false;
            default:
                return false;
        }
    };

    /**
     * Comprobar si el paso actual es válido para volver atras en el proceso de generación del informe
     * 
     * @returns 
     */
    const isBackStepValid = () => {
        switch (currentStep) {
            case 0:
                return false;
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
                return true;
            case 9:
                return true;
            case 10:
                return true;
            case 11:
                return true;
            case 12:
                return true;
            case 13:
                return true;
            case 14:
                return true;
            case 15:
                return true;
            case 16:
                return false;
            default:
                return false;
        }
    };

    /**
     * Avanzar al siguiente paso en el proceso de generación del informe
     */
    const nextStep = () => {
        if (isStepValid() && currentStep < steps.length){
            setCurrentStep(currentStep + 1);
            console.log(currentStep);
        } 

    };

    /**
     * Volver al paso anterior en el proceso de generación del informe
     */
    const prevStep = () => {
        if (currentStep > 0) setCurrentStep(currentStep - 1);
    };

    return (
        <div style={{ width: "100%", height: "100%"}}>
            <div style={{ width: "100%", height: "100%", textAlign: "center" }}>
                {getStepContent(currentStep)}
                <Button onClick={prevStep} disabled={!isBackStepValid()}>
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
