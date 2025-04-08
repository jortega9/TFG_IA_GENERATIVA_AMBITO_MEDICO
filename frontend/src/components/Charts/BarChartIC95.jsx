import React from 'react';
import Chart from 'react-apexcharts';

const BarChartIC95 = ({ data, categories, title, variable }) => {
    const findSplitIndex = () => {
        const mid = Math.floor(categories.length / 2);
        for (let i = mid; i < categories.length; i++) {
            const prevGroup = categories[i - 1].split('_')[0];
            const currentGroup = categories[i].split('_')[0];
            if (prevGroup !== currentGroup) {
                return i;
            }
        }
        return mid;
    };

    const splitIndex = findSplitIndex();

    const dataFirstHalf = data.slice(0, splitIndex);
    const dataSecondHalf = data.slice(splitIndex);

    const categoriesFirstHalf = categories.slice(0, splitIndex);
    const categoriesSecondHalf = categories.slice(splitIndex);

    const createSeries = (subset) => [
        {
            name: 'Inferior',
            data: subset.map(item => item.valorI),
        },
        {
            name: 'Superior',
            data: subset.map(item => item.valorS),
        }
    ];

    const createOptions = (subsetCategories, subtitle) => ({
        chart: {
            type: 'bar',
        },
        plotOptions: {
            bar: {
                borderRadius: 4,
                horizontal: false,
                columnWidth: '50%',
            }
        },
        dataLabels: {
            enabled: false
        },
        xaxis: {
            categories: subsetCategories,
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
            position: 'top'
        }
    });

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
            <Chart
                options={createOptions(categoriesFirstHalf, 'Primera parte')}
                series={createSeries(dataFirstHalf)}
                type="bar"
                height={400}
                width={800}
            />
            <Chart
                options={createOptions(categoriesSecondHalf, 'Segunda parte')}
                series={createSeries(dataSecondHalf)}
                type="bar"
                height={400}
                width={800}
            />
        </div>
    );
};

export default BarChartIC95;
