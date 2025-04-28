import React, { useState} from "react";
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
  CircularProgress,
} from "@mui/material";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";

function ContingencyAnalysis() {
  const location = useLocation();
  const [selectedFile, setSelectedFile] = useState(location.state?.selectedFile || null);
  const [losfResults, setLosfResults] = useState(null);
  const [gosfResults, setGosfResults] = useState(null);
  const [outageLine, setOutageLine] = useState("");
  const [outageGen, setOutageGen] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const navigate = useNavigate();

  const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    setSelectedFile(file);
    setLosfResults(null); // Clear results when a new file is uploaded
    setGosfResults(null); // Clear results when a new file is uploaded

    // Reset the file input field to allow re-upload of the same file
    event.target.value = null;
  }
};


  const handleBackButton = () => {
    navigate("/powerflow", { state: { selectedFile } });
  };

  const handleSubmit = async (endpoint) => {
    if (!selectedFile) {
      setErrorMessage("Please upload a file.");
      return;
    }

    if (endpoint === "losf" && !outageLine) {
      setErrorMessage("Please provide an outage line number for LOSF.");
      return;
    }

    if (endpoint === "gosf" && !outageGen) {
      setErrorMessage("Please provide an outage generator number for GOSF.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("outageLine", outageLine);  // Ensure this is a number
    formData.append("outageGen", outageGen);  // Ensure this is a number

    try {
      setLoading(true);
      setErrorMessage(null);
      const url =
        endpoint === "losf"
          ? `http://localhost:8080/v2/${endpoint}`
          : `http://localhost:8080/v2/${endpoint}`;

      const response = await axios.post(url, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (endpoint === "losf") {
        setLosfResults(response.data.losf_results);
        setGosfResults(null);
      } else if (endpoint === "gosf") {
        setGosfResults(response.data.gosf_results);
        setLosfResults(null);
      }
    } catch (error) {
      console.error("Error:", error);
      setErrorMessage("An error occurred while processing the request.");
      setLosfResults(null);
      setGosfResults(null);
    } finally {
      setLoading(false);
    }
  };

  const renderTable = (data, title, type) => (
    <div style={{ marginTop: "20px" }}>
      <Typography variant="h6">{title}</Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Line No.</TableCell>
              <TableCell>Original Pline</TableCell>
              <TableCell>{type === "losf" ? "LOSF" : "GOSF"}</TableCell>
              <TableCell>P Calculated</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((row, index) => (
              <TableRow key={index}>
                <TableCell>{row.line_no}</TableCell>
                <TableCell>{row.orig_pline}</TableCell>
                <TableCell>{type === "losf" ? row.losf : row.gosf}</TableCell>
                <TableCell>{row.p_calc}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );

  return (
    <div style={{ padding: "20px" }}>
      <Grid item xs={12} paddingBottom={"10px"} >
          <Button 
            variant="contained" 
            color="primary"
            onClick={handleBackButton}>
            Back
          </Button>
        </Grid>
      <Typography variant="h4">Contingency Analysis</Typography>
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
        <Grid item xs={6}>
          <TextField
            label="Outage Line Number (LOSF)"
            type="number"
            value={outageLine}
            onChange={(e) => setOutageLine(e.target.value)}
            fullWidth
          />
        </Grid>
        <Grid item xs={6}>
          <TextField
            label="Outage Generator Number (GOSF)"
            type="number"
            value={outageGen}
            onChange={(e) => setOutageGen(e.target.value)}
            fullWidth
          />
        </Grid>
        <Grid item xs={6}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => handleSubmit("losf")}
            fullWidth
          >
            Calculate LOSF
          </Button>
        </Grid>
        <Grid item xs={6}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => handleSubmit("gosf")}
            fullWidth
          >
            Calculate GOSF
          </Button>
        </Grid>
      </Grid>
      {loading && (
        <div style={{ marginTop: "20px", textAlign: "center" }}>
          <CircularProgress />
        </div>
      )}
      {losfResults && renderTable(losfResults, "Line Outage Sensitivity Factor (LOSF) Results", "losf")}
      {gosfResults && renderTable(gosfResults, "Generator Outage Sensitivity Factor (GOSF) Results", "gosf")}
    </div>
  );
}

export default ContingencyAnalysis;
