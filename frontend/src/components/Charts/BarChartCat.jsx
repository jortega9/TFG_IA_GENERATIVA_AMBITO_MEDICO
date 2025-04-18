import React from 'react';
import Chart from 'react-apexcharts';

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

const BarChartCat = ({ data, title, variable, height = 300, width = 480 }) => {
    const categorias = data.map(item => item.variable);
    const nombresBase = categorias.map(c => c.split('_')[0]);

    // Buscar punto de corte a partir de la mitad donde cambia el grupo base
    const findSplitIndex = () => {
        const mid = Math.floor(categorias.length / 2);
        for (let i = mid; i < categorias.length; i++) {
            const prev = categorias[i - 1].split('_')[0];
            const current = categorias[i].split('_')[0];
            if (prev !== current) return i;
        }
        return mid;
    };

    const splitIndex = findSplitIndex();

    // Dividir data y categorías
    const dataFirstHalf = data.slice(0, splitIndex);
    const dataSecondHalf = data.slice(splitIndex);

    // Función para crear options y series para cada mitad
    const createChartProps = (subset, subtitle) => {
        const cats = subset.map(item => item.variable);
        const bases = cats.map(c => c.split('_')[0]);

        // Asignar colores por nombre base
        const colorMap = {};
        let colorIndex = 0;
        bases.forEach(nombre => {
            if (!colorMap[nombre]) {
                colorMap[nombre] = coloresBase[colorIndex % coloresBase.length];
                colorIndex++;
            }
        });

        const colors = bases.map(nombre => colorMap[nombre]);

        return {
            options: {
                chart: {
                    type: 'bar',
                },
                plotOptions: {
                    bar: {
                        borderRadius: 4,
                        horizontal: false,
                        columnWidth: '50%',
                        distributed: true,
                    }
                },
                colors: colors,
                dataLabels: {
                    enabled: false
                },
                xaxis: {
                    categories: cats,
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
                    text: `${title} (${subtitle})`,
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
            },
            series: [{
                name: 'Media',
                data: subset.map(item => item.valor)
            }]
        };
    };

    const chart1 = createChartProps(dataFirstHalf, 'Primera parte');
    const chart2 = createChartProps(dataSecondHalf, 'Segunda parte');

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
            <Chart options={chart1.options} series={chart1.series} type="bar" height={height} width={width} />
            <Chart options={chart2.options} series={chart2.series} type="bar" height={height} width={width} />
        </div>
    );
};

export default BarChartCat;
