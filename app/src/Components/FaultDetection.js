import React, { useState } from 'react';
import GLOBAL from '../GLOBAL';
import Plot from '../utils/plot_FD';
import { useNavigate } from 'react-router-dom';

import {
  Container,
  Typography,
  TextField,
  Button,
  Box,
  CircularProgress,
  Paper,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  FormLabel
} from '@mui/material';

const serverAddress = GLOBAL.serverAddress;

const FaultDetection = () => {
  const [samplingRate, setSamplingRate] = useState('');
  const [threshold, setThreshold] = useState('');
  const [file, setFile] = useState(null);
  const [analysisType, setAnalysisType] = useState('sample-to-sample');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [plotData, setPlotData] = useState(null);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const uploadedFile = e.target.files[0];
    setFile(uploadedFile);
  };

  const sendToServer = async () => {
    setLoading(true);
    const analysisTypeValue = analysisType === "sample-to-sample" ? 0.0 : 1.0;
    const formData = new FormData();
    formData.append('samplingRate', samplingRate);
    formData.append('threshold', threshold);
    formData.append('file', file);
    formData.append('analysisTypeValue', analysisTypeValue);

    try {
        const response = await fetch(serverAddress + 'v2/FD', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            setResponse('Error occurred while processing the request.');
            return;
        }

        const serverData = await response.json();
        if (serverData.error) {
            setResponse(`Error: ${serverData.error}`);
        } else if (serverData.status === "Fault detected") {
            setResponse(`Fault detected between ${serverData.fault_start} s and ${serverData.fault_end} s`);
            setPlotData({
              domain: serverData.domain, 
              IA: serverData.IA,
              IB: serverData.IB,
              IC: serverData.IC,
            });
        } else {
          setResponse("No fault detected.");
          setPlotData({
            domain: serverData.domain, 
            IA: serverData.IA,
            IB: serverData.IB,
            IC: serverData.IC,
          });
        }
    } catch (error) {
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
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Paper elevation={4} 
            sx={{ p: 4, 
                  borderRadius: 2, 
                  backgroundColor: "#f9f9f9",
                  maxWidth: "500px",
                  mx: "auto", }}>
        <Typography variant="h4" component="h2" gutterBottom textAlign="center">
          Fault Detector
        </Typography>

        <form onSubmit={handleSubmit}>
          <Box mb={2}>
            <TextField
              label="Sampling Rate"
              type="number"
              value={samplingRate}
              onChange={(e) => setSamplingRate(e.target.value)}
              fullWidth
              required
              variant="outlined"
            />
          </Box>

          <Box mb={2}>
            <TextField
              label="Threshold"
              type="number"
              value={threshold}
              onChange={(e) => setThreshold(e.target.value)}
              fullWidth
              required
              variant="outlined"
            />
          </Box>

          <Box mb={2}>
            <FormControl component="fieldset">
              <FormLabel component="legend">Analysis Type</FormLabel>
              <RadioGroup
                row
                value={analysisType}
                onChange={(e) => setAnalysisType(e.target.value)}
              >
                <FormControlLabel
                  value="sample-to-sample"
                  control={<Radio />}
                  label="Sample-to-Sample"
                />
                <FormControlLabel
                  value="cycle-to-cycle"
                  control={<Radio />}
                  label="Cycle-to-Cycle"
                />
              </RadioGroup>
            </FormControl>
          </Box>

          <Box mb={2} display="flex" justifyContent="center">
            <Button variant="contained" component="label">
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
              sx={{ width: 200,
                backgroundColor: loading ? "#fff" : "#4050b5",
                color: loading ? "#4050b5" : "#fff",
                border: "2px solid #4050b5",
                "&:hover": { backgroundColor: loading ? "#ffffff" : "#303a8e" },
                "&.Mui-disabled": { backgroundColor: "#ffffff", borderColor: "#4050b5" },
               }}
            >
              {loading ? <CircularProgress size={24} sx={{ color: "#4050b5" }} /> : "Detect Fault"}
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
        <Paper elevation={3} sx={{ mt: 4, p: 3, textAlign: "center", maxWidth: "520px", mx: "auto" }}>
          <Typography variant="h6">Analysis Result</Typography>
          <Typography variant="body1">
            <strong>{response}</strong>
          </Typography>
        </Paper>
      )}

      {response.includes("Fault detected") && (
        <Paper elevation={3} sx={{ mt: 2, p: 2, textAlign: "center", maxWidth: 400, mx: "auto" }}>
          <Typography variant="body1" mb={1}>
            Ready to classify the detected fault?
          </Typography>
          <Button variant="contained" onClick={() => navigate("/faultclassification")}>
            Go to Fault Classification
          </Button>
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
            style={{ width: "700px", height: "80vh", minHeight: "600px" }}
          />
        </Paper>
      )}
      {}
    </Container>
  );
};

export default FaultDetection;