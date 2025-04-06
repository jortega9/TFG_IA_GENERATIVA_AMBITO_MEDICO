import React from 'react';
import Chart from 'react-apexcharts';

const PieChart = ({ data, title}) => {
    const series = data.map(item => item.valor);
    const labels = data.map(item => item.variable);

    const chartColors = generateColors(data.length);

    function generateColors(count) {
        return Array.from({ length: count }, (_, i) => {
            const hue = Math.round((360 / count) * i);
            return `hsl(${hue}, 65%, 55%)`;
        });
    }

    const options = {
        chart: {
            type: 'pie',
        },
        labels: labels,
        colors: chartColors,
        title: {
            text: title,
            align: 'center',
            style: {
                fontSize: '14px'
            }
        },
        legend: {
            position: 'bottom',
        },
        tooltip: {
            y: {
                formatter: val => val.toFixed(2)
            }
        },
        dataLabels: {
            style: {
                fontSize: '11px'
            }
        }
    };

    return <Chart options={options} series={series} type="pie" height={300} width={400} />;
};

export default PieChart;
