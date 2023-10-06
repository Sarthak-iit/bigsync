import React from 'react';
import Plot from 'react-plotly.js';
const getInnermostValue = (arr) => arr.reduce((acc, val) => (Array.isArray(val) ? getInnermostValue(val) : val), arr);

const AnalysePlot = (props) => {
  const [xData, yDatas, data, property] = props.props;
  console.log('yDatas',yDatas)
  console.log('xData',xData);
  const toPlot = yDatas.map((yData, i) => ({
    x:xData,
    y: data[yData]?data[yData][property].map(dataPoint => dataPoint):[],
    type: 'scatter',
    mode: 'lines+points',
    name: getInnermostValue(yDatas[i]), // Set the legend as yDatas[i]
  }));

  return (
    <Plot
      data={toPlot}
      layout={{
        width: 1000, height: 450,
        xaxis: {
          title: 'Time',
        },
        yaxis: {
          title: property,
        },
      }}
    />
  );
};

export default AnalysePlot;
