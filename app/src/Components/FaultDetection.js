import React, { useState } from 'react';
import GLOBAL from '../GLOBAL';
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
        } else {
            setResponse("No fault detected.");
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
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Paper elevation={4} sx={{ p: 4, borderRadius: 2, backgroundColor: "#f9f9f9" }}>
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
              sx={{ width: 200 }}
            >
              {loading ? <CircularProgress size={24} /> : "Detect Fault"}
            </Button>
          </Box>
        </form>
      </Paper>

      {response && (
        <Paper elevation={3} sx={{ mt: 4, p: 3, textAlign: "center" }}>
          <Typography variant="h6">Analysis Result</Typography>
          <Typography variant="body1">
            <strong>{response}</strong>
          </Typography>
        </Paper>
      )}
    </Container>
  );
};

export default FaultDetection;