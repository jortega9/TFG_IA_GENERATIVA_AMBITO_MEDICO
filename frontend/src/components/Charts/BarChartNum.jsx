import React from 'react';
import Chart from 'react-apexcharts';

// Función para generar una paleta de colores (puedes ampliarla)
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


const BarChartNum = ({ data, title, variable, height = 300, width = 480 }) => {

    const dataFiltrada = data.filter(item => !item.variable.toLowerCase().includes('nhis'));
    // Extrae nombres base (sin número)
    const categorias = dataFiltrada.map(item => item.variable);
    const nombresBase = categorias.map(c => c.split('_')[0]);

    // Asigna un color a cada nombre base
    const colorMap = {};
    let colorIndex = 0;
    nombresBase.forEach(nombre => {
        if (!colorMap[nombre]) {
            colorMap[nombre] = coloresBase[colorIndex % coloresBase.length];
            colorIndex++;
        }
    });

    // Mapea los colores a cada categoría
    const coloresPorBarra = nombresBase.map(nombre => colorMap[nombre]);

    const series = [{
        name: 'Media',
        data: dataFiltrada.map(item => item.valor),
    }];

    const options = {
        chart: {
            type: 'bar',
        },
        plotOptions: {
            bar: {
                borderRadius: 4,
                horizontal: false,
                columnWidth: '50%',
                distributed: true, // Necesario para colores individuales por barra
            }
        },
        colors: coloresPorBarra,
        dataLabels: {
            enabled: false
        },
        xaxis: {
            categories: categorias,
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
        },
        legend: {
            show: false
        }
    };

    return <Chart options={options} series={series} type="bar" height={height} width={width} />;
};

export default BarChartNum;
