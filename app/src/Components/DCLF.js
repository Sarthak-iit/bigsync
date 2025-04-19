import React, { useState } from 'react';
import {
  Box, Button, Grid, Typography, Alert, Tabs, Tab, CircularProgress,
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TextField
} from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';
import GLOBAL from '../GLOBAL';

const serverAddress = GLOBAL.serverAddress;

function DCLF() {
  const location = useLocation();
  const navigate = useNavigate();
  
  const [selectedFile, setSelectedFile] = useState(location.state?.selectedFile || null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [tab, setTab] = useState(0);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      event.target.value = null;
    }
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      setErrorMessage("Please upload a file.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const res = await fetch(`http://localhost:8080/v2/dclf`, {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      setResult(data.result);
      setErrorMessage(null);
    } catch (error) {
      setErrorMessage("Failed to fetch: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom>DC Load Flow Solver</Typography>

      {errorMessage && <Alert severity="error" sx={{ mb: 2 }}>{errorMessage}</Alert>}

      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <Button variant="outlined" component="label" fullWidth>
            {selectedFile ? selectedFile.name : "Upload File"}
            <input type="file" hidden onChange={handleFileChange} accept=".csv,.xlsx" />
          </Button>
        </Grid>
        <Grid item xs={6} md={3}>
          <Button variant="contained" fullWidth onClick={handleSubmit}>Submit</Button>
        </Grid>
        <Grid item xs={6} md={3}>
          <Button variant="contained" color="secondary" fullWidth onClick={() => navigate("/powerflow", { state: { selectedFile } })}>Back</Button>
        </Grid>
      </Grid>

      {loading && (
        <Box mt={4} display="flex" justifyContent="center">
          <CircularProgress />
        </Box>
      )}

      {result && (
        <Box mt={5}>
          <Tabs value={tab} onChange={(e, newValue) => setTab(newValue)} centered>
            <Tab label="Bus Results" />
            <Tab label="Line Results" />
          </Tabs>

          {tab === 0 && (
            <TableContainer component={Paper} sx={{ mt: 2 }}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Bus</TableCell>
                    <TableCell>Angle (°)</TableCell>
                    <TableCell>Real Power</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {result.final_voltages.map((bus, index) => (
                    <TableRow key={index}>
                      <TableCell>{index + 1}</TableCell>
                      <TableCell>{bus.angle.toFixed(4)}</TableCell>
                      <TableCell>{bus.real_power.toFixed(4)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}

          {tab === 1 && (
            <TableContainer component={Paper} sx={{ mt: 2 }}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>From</TableCell>
                    <TableCell>To</TableCell>
                    <TableCell>P_from</TableCell>
                    <TableCell>P_to</TableCell>
                    <TableCell>Losses</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {result.line_flow_results.map((line, index) => (
                    <TableRow key={index}>
                      <TableCell>{line.from_bus}</TableCell>
                      <TableCell>{line.to_bus}</TableCell>
                      <TableCell>{line.P_from.toFixed(4)}</TableCell>
                      <TableCell>{line.P_to.toFixed(4)}</TableCell>
                      <TableCell>{line.P_losses.toFixed(4)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </Box>
      )}
    </Box>
  );
}

export default DCLF;
