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
  const [selectedDataset, setSelectedDataset] = useState("I0m");
  const [dataType, setDataType] = useState("Magnitude"); // "Magnitude" or "Angle"

  // Define colors for different datasets
  const datasetColors = {
    I0m: "rgba(0, 0, 255, 1)", // Blue
    I1m: "rgba(0, 128, 0, 1)", // Green
    I2m: "rgba(255, 0, 0, 1)", // Red
    Iam: "rgba(180, 0, 0, 1)", // Dark Red
    Ibm: "rgba(255, 215, 0, 1)", // Yellow
    Icm: "rgba(100, 100, 255, 1)", // Light Blue
  };

  const datasetOptions = {
    I0m: data.I0m, I0a: data.I0a,
    I1m: data.I1m, I1a: data.I1a,
    I2m: data.I2m, I2a: data.I2a,
    Iam: data.Iam, Iaa: data.Iaa,
    Ibm: data.Ibm, Iba: data.Iba,
    Icm: data.Icm, Ica: data.Ica,
  };

  const handleDatasetChange = (event) => {
    setSelectedDataset(event.target.value);
  };

  const handleDataTypeChange = (event) => {
    setDataType(event.target.value);
  };

  const selectedKey = dataType === "Magnitude" ? selectedDataset : selectedDataset.replace("m", "a");
  
  const chartData = {
    labels: data.domain, // X-axis values
    datasets: [
      {
        label: `${selectedDataset} (${dataType})`,
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
        title: { display: true, text: dataType === "Magnitude" ? "Current Magnitude" : "Current Angle (Degrees)", font: { size: 14 } },
        grid: { color: "#ddd", borderDash: [5, 5] },
      },
    },
  };

  return (
    <div style={{ maxWidth: "800px", margin: "auto", padding: "20px", backgroundColor: "#fff", borderRadius: "10px", boxShadow: "0px 4px 10px rgba(0,0,0,0.1)" }}>
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
          <optgroup label="Sequence Components">
            <option value="I0m">I0m (Zero-Sequence)</option>
            <option value="I1m">I1m (Positive-Sequence)</option>
            <option value="I2m">I2m (Negative-Sequence)</option>
          </optgroup>
          <optgroup label="Phase Currents">
            <option value="Iam">Iam (Phase-A)</option>
            <option value="Ibm">Ibm (Phase-B)</option>
            <option value="Icm">Icm (Phase-C)</option>
          </optgroup>
        </select>

        {/* Data Type Selection (Magnitude/Angle) */}
        <select
          onChange={handleDataTypeChange}
          value={dataType}
          style={{
            padding: "8px",
            fontSize: "16px",
            borderRadius: "5px",
            border: "1px solid #ccc",
            background: "#f8f8f8",
            cursor: "pointer",
          }}
        >
          <option value="Magnitude">Magnitude</option>
          <option value="Angle">Angle</option>
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
