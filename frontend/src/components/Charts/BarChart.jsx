import React from 'react';
import Chart from 'react-apexcharts';

const BarChart = ({ data, title, variable }) => {
    const series = [{
        name: 'Media',
        data: data.map(item => item.valor),
    }];

    const options = {
        chart: {
            type: 'bar',

        },
        plotOptions: {
            bar: {
                borderRadius: 4,
                horizontal: false, // ← Cambiado a vertical
                columnWidth: '50%',
            }
        },
        dataLabels: {
            enabled: false
        },
        xaxis: {
            categories: data.map(item => item.variable),
            title: {
                text: 'Variables',
                style: { fontSize: '12px' }
            },
            labels: {
                rotate: -45,
                style: { fontSize: '12px' }
            }
        },
        yaxis: {
            title: {
                text: variable,
                style: { fontSize: '12px' }
            }
        },
        title: {
            text: title,
            align: 'center',
            style: {
                fontSize: '14px'
            }
        },
        tooltip: {
            y: {
                formatter: val => val.toFixed(2)
            }
        }
    };

    return <Chart options={options} series={series} type="bar" height={300} width={480} />;
};

export default BarChart;
