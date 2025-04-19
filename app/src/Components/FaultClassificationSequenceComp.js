import React, { useState } from 'react';
import GLOBAL from '../GLOBAL';
import Plot from '../utils/plot';
import {
  Container,
  Typography,
  TextField,
  Button,
  Box,
  CircularProgress,
  Paper,
} from '@mui/material';

const serverAddress = GLOBAL.serverAddress;

const FaultAnalyzer = () => {
  const [totalTime, setTotalTime] = useState('');
  const [faultTimeInstant, setFaultTimeInstant] = useState('');
  const [faultDuration, setFaultDuration] = useState('');
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [plotData, setPlotData] = useState(null);

  const handleFileChange = (e) => {
    const uploadedFile = e.target.files[0];
    setFile(uploadedFile);
  };

  const sendToServer = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append('totalTime', totalTime);
    formData.append('faultTimeInstant', faultTimeInstant);
    formData.append('faultDuration', faultDuration);
    formData.append('file', file);


    try {
      const response = await fetch(serverAddress + 'v2/FCSQ', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        console.error('Error:', response.status);
        setResponse('Error occurred while processing the request.');
        return;
      }

      const serverData = await response.json();
      setResponse(serverData.result);
      setPlotData({
        domain: serverData.domain, 
        I0m: serverData.I0m,
        I1m: serverData.I1m,
        I2m: serverData.I2m,
        Iam: serverData.Iam,
        Ibm: serverData.Ibm,
        Icm: serverData.Icm,
        I0a: serverData.I0a,
        I1a: serverData.I1a,
        I2a: serverData.I2a,
        Iaa: serverData.Iaa,
        Iba: serverData.Iba,
        Ica: serverData.Ica,
      });

    } catch (error) {
      console.error('Error:', error);
      setResponse('Error occurred while fetching the request.');
    } finally {
      setLoading(false);
    }
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    if (loading) return;
    await sendToServer();
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      {/* Form Container */}
      <Paper
        elevation={4}
        sx={{
          p: 4,
          borderRadius: 2,
          boxShadow: 4,
          backgroundColor: "#f9f9f9",
          maxWidth: "500px",
          mx: "auto", // Centering the form
        }}
      >
        <Typography variant="h4" component="h2" gutterBottom textAlign="center">
          Fault Analyzer
        </Typography>
  
        <form onSubmit={handleSubmit}>
          <Box mb={2}>
            <TextField
              label="Total Time"
              type="number"
              value={totalTime}
              onChange={(e) => setTotalTime(e.target.value)}
              fullWidth
              required
              variant="outlined"
            />
          </Box>
  
          <Box mb={2}>
            <TextField
              label="Fault Time Instant"
              type="number"
              value={faultTimeInstant}
              onChange={(e) => setFaultTimeInstant(e.target.value)}
              fullWidth
              required
              variant="outlined"
            />
          </Box>
  
          <Box mb={2}>
            <TextField
              label="Fault Duration"
              type="number"
              value={faultDuration}
              onChange={(e) => setFaultDuration(e.target.value)}
              fullWidth
              required
              variant="outlined"
            />
          </Box>
  
          <Box mb={2} display="flex" justifyContent="center">
            <Button variant="contained" component="label" sx={{ width: 200, border: "2px solid #4050b5", }}>
              Upload File
              <input type="file" accept=".xlsx, .xls" hidden onChange={handleFileChange} required />
            </Button>
          </Box>
  
          {file && (
            <Typography variant="body2" mb={3} color="textSecondary" textAlign="center">
              Uploaded: <strong>{file.name}</strong>
            </Typography>
          )}
  
          <Box display="flex" justifyContent="center">
            <Button
              type="submit"
              variant="contained"
              disabled={loading}
              sx={{
                width: 200,
                backgroundColor: loading ? "#fff" : "#4050b5",
                color: loading ? "#4050b5" : "#fff",
                border: "2px solid #4050b5",
                "&:hover": { backgroundColor: loading ? "#ffffff" : "#303a8e" },
                "&.Mui-disabled": { backgroundColor: "#ffffff", borderColor: "#4050b5" },
              }}
            >
              {loading ? <CircularProgress size={24} sx={{ color: "#4050b5" }} /> : "Analyze Fault"}
            </Button>
          </Box>
  
          {loading && (
            <Typography mt={3} textAlign="center">
              Algorithm running in the background, please wait...
            </Typography>
          )}
        </form>
      </Paper>
  
      {/* Result Container */}
      {response && (
        <Paper
          elevation={3}
          sx={{mt: 4, p: 3, textAlign: "center", maxWidth: "520px", mx: "auto" }}
        >
          <Typography variant="h6">Analysis Result</Typography>
          <Typography variant="body1">
            <strong>{response}</strong>
          </Typography>
        </Paper>
      )}
  
      {/* Plot Container */}
      {plotData && (
        <Paper elevation={4} sx={{ marginBottom: 50, mt: 4, p: 3 }}>
          <Typography variant="h6" textAlign="center" mb={2}>
            Fault Analysis Plot
          </Typography>
          <Plot
            data={plotData}
            layout={{
              title: "Fault Current Analysis",
              xaxis: { title: "Time (s)", showgrid: true },
              yaxis: { title: "Current Magnitude", showgrid: true },
              plot_bgcolor: "#f8f9fa",
              paper_bgcolor: "#ffffff",
              margin: { t: 40, b: 50, l: 50, r: 50 },
            }}
            useResizeHandler
            style={{ margin: "50px", width: "100%", height: "500px" }}
          />
        </Paper>
      )}
      {}
    </Container>
  );
  
  
};

export default FaultAnalyzer;
