import React, { useState } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const Plot = ({ data }) => {
  const [selectedDataset, setSelectedDataset] = useState("IA");

  // Define colors for different datasets
  const datasetColors = {
    IA: "rgba(0, 0, 255, 1)", // Blue
    IB: "rgba(0, 128, 0, 1)", // Green
    IC: "rgba(180, 0, 0, 1)", // Red
  };

  const datasetOptions = {
    IA : data.IA,
    IB : data.IB,
    IC : data.IC,
  };

  const handleDatasetChange = (event) => {
    setSelectedDataset(event.target.value);
  };

  const selectedKey = selectedDataset;

  const chartData = {
    labels: data.domain, // X-axis values
    datasets: [
      {
        label: `${selectedDataset}`,
        data: datasetOptions[selectedKey],
        borderColor: datasetColors[selectedDataset], // Color as per mapping
        backgroundColor: datasetColors[selectedDataset].replace("1)", "0.2)"), // Transparent fill
        borderWidth: 2,
        fill: false, // No fill under the line
        tension: 0, // Straight lines (no smoothness)
        pointRadius: 3,
        pointBackgroundColor: datasetColors[selectedDataset],
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: "top",
        labels: {
          font: { size: 14 },
          color: "#333",
        },
      },
      tooltip: {
        backgroundColor: "#fff",
        titleColor: "#333",
        bodyColor: "#666",
        borderWidth: 1,
        borderColor: "#ddd",
        cornerRadius: 5,
      },
    },
    scales: {
      x: {
        title: { display: true, text: "Time (s)", font: { size: 14 } },
        grid: { display: false },
      },
      y: {
        title: { display: true, text: "Current", font: { size: 14 } },
        grid: { color: "#ddd", borderDash: [5, 5] },
      },
    },
  };

  return (
    <div style={{ maxWidth: "1000px", margin: "auto", padding: "20px", backgroundColor: "#fff", borderRadius: "10px", boxShadow: "0px 8px 30px rgba(0, 0, 0, 0.15)"  }}>
      <h2 style={{ textAlign: "center", color: "#333" }}>Fault Current Analysis</h2>

      {/* Styled Dataset Dropdown */}
      <div style={{ display: "flex", justifyContent: "center", gap: "10px", marginBottom: "10px" }}>
        {/* Dataset Selection */}
        <select
          onChange={handleDatasetChange}
          value={selectedDataset}
          style={{
            padding: "8px",
            fontSize: "16px",
            borderRadius: "5px",
            border: "1px solid #ccc",
            background: "#f8f8f8",
            cursor: "pointer",
          }}
        >
          <optgroup label="Phase Currents">
            <option value="IA">IA (Phase-A)</option>
            <option value="IB">IB (Phase-B)</option>
            <option value="IC">IC (Phase-C)</option>
          </optgroup>
        </select>

      </div>

      {/* Line Chart */}
      <div style={{ height: "400px" }}>
        <Line data={chartData} options={options} />
      </div>
    </div>
  );
};

export default Plot;
