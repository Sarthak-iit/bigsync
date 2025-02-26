import React, { useState } from 'react';
import { Button, TextField, Grid, Typography, Alert, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import GLOBAL from '../GLOBAL'; // Assuming this contains the serverAddress
import LinearBuffer from './Loading'; // Assuming you have a loading bar component
import { useLocation, useNavigate } from "react-router-dom";

const serverAddress = GLOBAL.serverAddress;

function GSFL() {
  const location = useLocation();
  // State variables for the file, acceleration factor, result, and loading status
  const [selectedFile, setSelectedFile] = useState(location.state?.selectedFile || null);
  const [file, setFile] = useState(null);
  const [accelerationFactor, setAccelerationFactor] = useState(1.0);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const navigate = useNavigate();

  const handleBackButton = () => {
    navigate("/powerflow", { state: { selectedFile } });
  };

  // Handle file upload
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      // Reset the file input field to allow re-upload of the same file
      event.target.value = null;
    }
  };

  // Handle acceleration factor change
  const handleAccelerationChange = (event) => {
    setAccelerationFactor(event.target.value);
  };

  // Handle form submission
  const handleSubmit = async (event) => {
    if (!selectedFile) {
      setErrorMessage("Please upload a file.");
      return;
    }
    event.preventDefault();
    const formData = new FormData();
    formData.append("file", selectedFile);  // Ensure this has a valid file
    formData.append("acceleration_factor", accelerationFactor);  // Ensure this is a number

    try {
      setLoading(true); // Start loading
      const response = await fetch("http://localhost:8080/v2/gsfl", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log(data); // Log the data for debugging
      setResult(data.result); // Update the result with the full response
      setErrorMessage(null); // Clear any previous error messages
    } catch (error) {
      console.error("Error uploading file:", error);
      setErrorMessage("Error uploading file: " + error.message);
      setResult(null); // Clear results on error
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <Typography variant="h4">Gauss-Seidel Power Flow Solver</Typography>
      {errorMessage && <Alert severity="error">{errorMessage}</Alert>}
      <Grid container spacing={2} style={{ marginTop: "10px" }}>
        <Grid item xs={12}>
          {selectedFile ? (
            <Typography variant="subtitle1" color="textSecondary">
              Uploaded File: {selectedFile.name}
            </Typography>
          ) : (
            <TextField
              type="file"
              onChange={handleFileChange}
              inputProps={{
                accept:
                  ".csv, application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
              }}
              fullWidth
            />
          )}
        </Grid>
        <Grid item xs={12}>
            <TextField
              type="number"
              label="Acceleration Factor"
              value={accelerationFactor}
              onChange={handleAccelerationChange}
              fullWidth
              variant="outlined"
            />
        </Grid>
        <Grid item>
          <Button 
            variant="contained" 
            color="primary"
            onClick={handleSubmit}>
            Submit
          </Button>
        </Grid>
        <Grid item>
          <Button 
            variant="contained" 
            color="primary"
            onClick={handleBackButton}>
            Back
          </Button>
        </Grid>
      </Grid>
      {/* <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              type="file"
              onChange={handleFileChange}
              inputProps={{ accept: '.csv, application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }} // Accept CSV and Excel files
              fullWidth
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              type="number"
              label="Acceleration Factor"
              value={accelerationFactor}
              onChange={handleAccelerationChange}
              fullWidth
              variant="outlined"
            />
          </Grid>
          
        </Grid>
      </form> */}
      {loading && <LinearBuffer />}
      {result && result.final_voltages && (
        <div>
          <Typography variant="h6">Results:</Typography>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Bus Number</TableCell> {/* Added Bus Number Header */}
                  <TableCell>Voltage (Magnitude)</TableCell>
                  <TableCell>Voltage (Angle)</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {result.final_voltages.map((voltage, index) => (
                  <TableRow key={index}>
                    <TableCell>{index + 1}</TableCell> {/* Bus Number as index + 1 */}
                    <TableCell>{voltage.magnitude}</TableCell>
                    <TableCell>{voltage.angle}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </div>
      )}
    </div>
  );
}

export default GSFL;
