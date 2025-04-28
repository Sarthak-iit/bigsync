import React, { useState } from 'react';
import { 
  Button, 
  TextField, 
  Grid, 
  Typography, 
  Alert, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow, 
  Paper,
  Tabs,
  Tab,
  Box
} from '@mui/material';
import LinearBuffer from './Loading'; // Assuming you have a loading bar component
import { useLocation, useNavigate } from "react-router-dom";

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function GSLF() {
  const location = useLocation();
  // State variables for the file, acceleration factor, result, and loading status
  const [selectedFile, setSelectedFile] = useState(location.state?.selectedFile || null);
  const [accelerationFactor, setAccelerationFactor] = useState(1.0);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [activeTab, setActiveTab] = useState(0);
  
  const navigate = useNavigate();
  const handleBackButton = () => {
    navigate("/powerflow", { state: { selectedFile } });
  };
  
  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
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
      const response = await fetch("http://localhost:8080/v2/gslf", {
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
      
      {loading && <LinearBuffer />}
      
      {result && (
        <div style={{ marginTop: "20px" }}>
          <Typography variant="h6">Results:</Typography>
          
          <Grid container spacing={2} style={{ marginTop: "10px" }}>
            <Grid item xs={12}>
              <Typography variant="body1">
                Convergence achieved in {result.iterations || "N/A"} iterations
              </Typography>
              <Typography variant="body1">
                Maximum mismatch: {result.max_mismatch || "N/A"}
              </Typography>
            </Grid>
          </Grid>
          
          <Box sx={{ borderBottom: 1, borderColor: 'divider', marginTop: "20px" }}>
            <Tabs value={activeTab} onChange={handleTabChange} aria-label="result tabs">
              <Tab label="Bus Results" />
              <Tab label="Line Results" />
            </Tabs>
          </Box>
          
          <TabPanel value={activeTab} index={0}>
            {result.final_voltages && (
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Bus Number</TableCell>
                      <TableCell>Voltage (Magnitude)</TableCell>
                      <TableCell>Voltage (Angle)</TableCell>
                      <TableCell>Real Power (MW)</TableCell>
                      <TableCell>Reactive Power (MVAr)</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {result.final_voltages.map((voltage, index) => (
                      <TableRow key={index}>
                        <TableCell>{index + 1}</TableCell>
                        <TableCell>{voltage.magnitude.toFixed(4)}</TableCell>
                        <TableCell>{voltage.angle.toFixed(4)}</TableCell>
                        <TableCell>{voltage.real_power.toFixed(4)}</TableCell>
                        <TableCell>{voltage.complex_power.toFixed(4)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </TabPanel>
          
          <TabPanel value={activeTab} index={1}>
            {result.line_flow_results && (
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>From Bus</TableCell>
                      <TableCell>To Bus</TableCell>
                      <TableCell>P From (MW)</TableCell>
                      <TableCell>Q From (MVAr)</TableCell>
                      <TableCell>P To (MW)</TableCell>
                      <TableCell>Q To (MVAr)</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {result.line_flow_results.map((line, index) => (
                      <TableRow key={index}>
                        <TableCell>{line.from_bus}</TableCell>
                        <TableCell>{line.to_bus}</TableCell>
                        <TableCell>{line.P_from.toFixed(4)}</TableCell>
                        <TableCell>{line.Q_from.toFixed(4)}</TableCell>
                        <TableCell>{line.P_to.toFixed(4)}</TableCell>
                        <TableCell>{line.Q_to.toFixed(4)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </TabPanel>
        </div>
      )}
    </div>
  );
}

export default GSLF;
