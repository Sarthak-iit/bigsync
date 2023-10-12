import React from 'react';
import { BarChart } from '@mui/x-charts/BarChart';


function MyBarChart({values,xData}) {
    const xAxis = [{ scaleType: 'band', data:xData ,categoryGapRatio: 0.5}];
    const series = [{ data: values }];
    return (
        <BarChart
        
            xAxis={xAxis}
            series={series}
            width={500}
            height={300}
        />
    );
}

export default MyBarChart;
