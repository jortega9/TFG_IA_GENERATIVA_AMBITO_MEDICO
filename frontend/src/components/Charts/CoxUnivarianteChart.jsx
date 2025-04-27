import React from 'react';
import ReactApexChart from 'react-apexcharts';

const CoxUnivarianteChart = ({ data }) => {

    const colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
        '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5',
        '#393b79', '#637939', '#8c6d31', '#843c39', '#7b4173',
        '#3182bd', '#6baed6', '#9ecae1', '#e6550d', '#fd8d3c',
        '#fdae6b', '#31a354', '#74c476', '#a1d99b', '#756bb1',
        '#9e9ac8', '#bcbddc', '#636363', '#969696', '#bdbdbd'
    ];

    const seriesHR = [
        {
            name: 'Hazard Ratio (HR)',
            data: data.map(item => item.HR)
        }
    ];

    const optionsHR = {
        chart: {
            type: 'bar',
            height: 300,
        },
        dataLabels: {
            enabled: false
        },
        plotOptions: {
            bar: {
                horizontal: true,
                barHeight: '60%',
                distributed: true,
            }
        },
        xaxis: {
            categories: data.map(item => item.variable),
            title: {
                text: 'Cociente de Riesgos (HR)'
            }
        },
        tooltip: {
            y: {
                formatter: (val, { series, seriesIndex, dataPointIndex }) => {
                const item = data[dataPointIndex];
                return `HR: ${item.HR} (IC 95%: ${item.ci_lower} - ${item.ci_upper})`;
                }
            },
            custom: ({ series, seriesIndex, dataPointIndex, w }) => {
                const item = data[dataPointIndex];
                return `<div style="padding: 8px; background: white; border: 1px solid #ccc;">
                        <strong>${item.variable}</strong><br/>
                        HR: ${item.HR}<br/>
                        IC 95%: ${item.ci_lower} - ${item.ci_upper}
                        </div>`;
            }
        },
        annotations: {
            xaxis: [
                {
                    x: 1,
                    borderColor: '#775DD0',
                    label: {
                        style: {
                            color: '#fff',
                            background: '#775DD0'
                        },
                        text: 'HR = 1'
                    }
                }
            ]
        },
        colors: colors,
    };

    const seriesP = [
        {
            name: 'Valor p',
            data: data.map(item => item.p)
        }
    ];

    const optionsP = {
        chart: {
            type: 'bar',
            height: 300,
        },
        dataLabels: {
            enabled: false
        },
        plotOptions: {
            bar: {
                horizontal: true,
                columnWidth: '60%',
                distributed: true,
            }
        },
        xaxis: {
            categories: data.map(item => item.variable),
            title: {
                text: 'Variable'
            }
        },
        yaxis: {
            title: {
                text: 'P-valor'
            }
        },
        tooltip: {
            y: {
                formatter: (val) => `p: ${val}`
            }
        },
        annotations: {
            yaxis: []
        },
        colors: colors,
    };

    return (
        <div style={{ display: 'flex', justifyContent: 'space-around', alignItems: 'center', flexDirection: 'row', width: '100%', flexWrap: 'wrap' }}>
            <div>
                <h4 style={{ textAlign: 'center', color: '#4D7AFF' }}>Cociente de Riesgos (HR)</h4>
                <ReactApexChart options={optionsHR} series={seriesHR} type="bar" height={350} width={350} />
            </div>
            <div>
                <h4 style={{ textAlign: 'center', color: '#4D7AFF' }}>P-Valor</h4>
                <ReactApexChart options={optionsP} series={seriesP} type="bar" height={350} width={350} />
            </div>
        </div>
    );
}

export default CoxUnivarianteChart;
