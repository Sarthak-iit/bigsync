import React, { useEffect } from 'react';
import Plot from 'react-plotly.js';

const PlotlyPlot = (props) => {
  console.log(props.props)
  const [ xData, yData,xLabel,yLabel,title ] = props.props;
  console.log('title',title)
    // if (!xData || !yData || xData.length !== yData.length) {
    //   return;
    // }

    return (
        <Plot
          data={[
      {
        x: xData,
        y: yData,
        mode: 'lines',
      },
    ]}
          layout={ {width: 1000, height: 450,title: title,
          xaxis: {
          title: xLabel,
        },
        yaxis: {
          title: yLabel,
        }
          } }
        />
      )}

    // Clean up the chart when the component unmounts
    

export default PlotlyPlot;
