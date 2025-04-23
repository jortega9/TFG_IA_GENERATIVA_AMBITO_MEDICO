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
import { Button } from '@mui/material';

import bilat2_kaplan_meier_plot from '../../../../data/processed/kaplan_meier/bilat2_kaplan_meier_plot.png';
import capras_kaplan_meier_plot from '../../../../data/processed/kaplan_meier/capras_kaplan_meier_plot.png';
import extracap_kaplan_meier_plot from '../../../../data/processed/kaplan_meier/extracap_kaplan_meier_plot.png';
import gleason1_kaplan_meier_plot from '../../../../data/processed/kaplan_meier/gleason1_kaplan_meier_plot.png';
import gleason2_kaplan_meier_plot from '../../../../data/processed/kaplan_meier/gleason2_kaplan_meier_plot.png';
import hereda_kaplan_meier_plot from '../../../../data/processed/kaplan_meier/hereda_kaplan_meier_plot.png';
import kaplan_meier_plot from '../../../../data/processed/kaplan_meier/kaplan_meier_plot.png';
import localiz_kaplan_meier_plot from '../../../../data/processed/kaplan_meier/localiz_kaplan_meier_plot.png';
import margen_kaplan_meier_plot from '../../../../data/processed/kaplan_meier/margen_kaplan_meier_plot.png';
import multifoc_kaplan_meier_plot from '../../../../data/processed/kaplan_meier/multifoc_kaplan_meier_plot.png';
import pinag_kaplan_meier_plot from '../../../../data/processed/kaplan_meier/pinag_kaplan_meier_plot.png';
import ra_estroma_kaplan_meier_plot from '../../../../data/processed/kaplan_meier/ra_estroma_kaplan_meier_plot.png';
import rtpadyu_kaplan_meier_plot from '../../../../data/processed/kaplan_meier/rtpadyu_kaplan_meier_plot.png';
import tnm2_kaplan_meier_plot from '../../../../data/processed/kaplan_meier/tnm2_kaplan_meier_plot.png';
import vvss_kaplan_meier_plot from '../../../../data/processed/kaplan_meier/vvss_kaplan_meier_plot.png';


const Report = () => {
    const steps = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27"];
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
                setImagesKaplanPath={setImagesKaplanPath}
                setCsvKaplanPath={setCsvKaplanPath}
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
                return <KaplanStatisticsVars key="bilat2" csvKaplanPath={csvKaplanPath} nameVar="bilat2" plotK={bilat2_kaplan_meier_plot} plotS={bilat2_kaplan_meier_plot} />;
            case 15:
                return <KaplanStatisticsVars key="capras" csvKaplanPath={csvKaplanPath} nameVar="capras" plotK={capras_kaplan_meier_plot} plotS={capras_kaplan_meier_plot} />;
            case 16:
                return <KaplanStatisticsVars key="extracap" csvKaplanPath={csvKaplanPath} nameVar="extracap" plotK={extracap_kaplan_meier_plot} plotS={extracap_kaplan_meier_plot} />;
            case 17:
                return <KaplanStatisticsVars key="gleason1" csvKaplanPath={csvKaplanPath} nameVar="gleason1" plotK={gleason1_kaplan_meier_plot} plotS={gleason1_kaplan_meier_plot} />;
            case 18:
                return <KaplanStatisticsVars key="gleason2" csvKaplanPath={csvKaplanPath} nameVar="gleason2" plotK={gleason2_kaplan_meier_plot} plotS={gleason2_kaplan_meier_plot} />;
            case 19:
                return <KaplanStatisticsVars key="hereda" csvKaplanPath={csvKaplanPath} nameVar="hereda" plotK={hereda_kaplan_meier_plot} plotS={hereda_kaplan_meier_plot} />;
            case 20:
                return <KaplanStatisticsVars key="localiz" csvKaplanPath={csvKaplanPath} nameVar="localiz" plotK={localiz_kaplan_meier_plot} plotS={localiz_kaplan_meier_plot} />;
            case 21:
                return <KaplanStatisticsVars key="margen" csvKaplanPath={csvKaplanPath} nameVar="margen" plotK={margen_kaplan_meier_plot} plotS={margen_kaplan_meier_plot} />;
            case 22:
                return <KaplanStatisticsVars key="multifoc" csvKaplanPath={csvKaplanPath} nameVar="multifoc" plotK={multifoc_kaplan_meier_plot} plotS={multifoc_kaplan_meier_plot} />;
            case 23:
                return <KaplanStatisticsVars key="pinag" csvKaplanPath={csvKaplanPath} nameVar="pinag" plotK={pinag_kaplan_meier_plot} plotS={pinag_kaplan_meier_plot} />;
            case 24:
                return <KaplanStatisticsVars key="ra_estroma" csvKaplanPath={csvKaplanPath} nameVar="ra_estroma" plotK={ra_estroma_kaplan_meier_plot} plotS={ra_estroma_kaplan_meier_plot} />;
            case 25:
                return <KaplanStatisticsVars key="rtpadyu" csvKaplanPath={csvKaplanPath} nameVar="rtpadyu" plotK={rtpadyu_kaplan_meier_plot} plotS={rtpadyu_kaplan_meier_plot} />;
            case 26:
                return <KaplanStatisticsVars key="tnm2" csvKaplanPath={csvKaplanPath} nameVar="tnm2" plotK={tnm2_kaplan_meier_plot} plotS={tnm2_kaplan_meier_plot} />;
            case 27:
                return <KaplanStatisticsVars key="vvss" csvKaplanPath={csvKaplanPath} nameVar="vvss" plotK={vvss_kaplan_meier_plot} plotS={vvss_kaplan_meier_plot} />;                
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
                return true;
            case 13:
                return true;
            case 14:
                return true;
            case 15:
                return true;
            case 16:
                return true;
            case 17:
                return true;
            case 18:
                return true;
            case 19:
                return true;
            case 20:
                return true;
            case 21:
                return true;
            case 22:
                return true;
            case 23:
                return true;
            case 24:
                return true;
            case 25:
                return true;
            case 26:
                return true;
            case 27:
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
