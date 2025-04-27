import React from 'react';
import ReactApexChart from 'react-apexcharts';

const coloresBase = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
    '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5',
    '#393b79', '#637939', '#8c6d31', '#843c39', '#7b4173',
    '#3182bd', '#6baed6', '#9ecae1', '#e6550d', '#fd8d3c',
    '#fdae6b', '#31a354', '#74c476', '#a1d99b', '#756bb1',
    '#9e9ac8', '#bcbddc', '#636363', '#969696', '#bdbdbd'
];

const ChiSquaredChart = ({ table, data }) => {
    const categories = table.map(item => item.variable);
    const dataSeries = data.map(item => item.valor);

    const options = {
        chart: {
            type: 'bar',
            height: 350,
            toolbar: { show: false }
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '55%',
                endingShape: 'rounded',
                distributed: true // ✅ aplica un color por categoría
            }
        },
        dataLabels: {
            enabled: false
        },
        xaxis: {
            categories,
            title: {
                text: 'Variables',
                style: { fontWeight: 600 }
            },
            labels: {
                rotate: -45
            }
        },
        yaxis: {
            title: {
                text: 'P Value',
                style: { fontWeight: 600 }
            }
        },
        colors: coloresBase, // ✅ aplica tus colores personalizados
        tooltip: {
            y: {
                formatter: (val) => val.toFixed(2)
            }
        },
        legend: {
            show: false
        }
    };

    const series = [
        {
            name: 'Chi²',
            data: dataSeries
        }
    ];

    return (
        <div id="chart">
            <ReactApexChart
                options={options}
                series={series}
                type="bar"
                height={400}
                width={800}
            />
        </div>
    );
};

export default ChiSquaredChart;
