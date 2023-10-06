import React, { useEffect, useRef } from 'react';
import { Chart } from 'chart.js/auto';

const LineChartWithZoom = (props) => {
  const [xData, yData] = props.props;
  const chartRef = useRef(null);
  const chartInstanceRef = useRef(null);

  useEffect(() => {
    if (!xData || !yData || xData.length !== yData.length) {
      return;
    }

    if (chartInstanceRef.current) {
      chartInstanceRef.current.destroy();
    }

    const ctx = chartRef.current.getContext('2d');

    const data = {
      labels: xData.map((x, index) => index.toString()),
      datasets: [
        {
          label: 'My Dataset',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
          data: yData,
        },
      ],
    };

    const config = {
      type: 'line',
      data: data,
      options: {
        scales: {
          x: {
            type: 'category',
          },
        },
        interaction: {
          mode: 'xy',
          axis: 'xy',
          zoom: {
            wheel: {
              enabled: true,
            },
            pinch: {
              enabled: true,
            },
            mode: 'xy',
          },
        },
      },
    };

    const newChartInstance = new Chart(ctx, config);
    chartInstanceRef.current = newChartInstance;

  }, [xData, yData]);

  return (
    <div>
      <canvas ref={chartRef} />
    </div>
  );
};

export default LineChartWithZoom;
