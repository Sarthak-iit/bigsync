import React, { useState } from "react";
import { Container, Typography, Button, Box } from "@mui/material";
import FileInput from "./v-1/FileInput2";
import { useLocation, useNavigate } from "react-router-dom";

const buttonStyle = {
  marginTop: "10px",
  width: "30vw",
};

const imageStyles = {
  width: '200px',
  height: 'auto',
  transition: 'transform 0.5s ease', // Add a smooth transition
};

const PowerFlowAnalysis = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState(location.state?.selectedFile || null);

  const handleGaussSeidelButton = () => {
    navigate("/gauss", { state: { selectedFile } });
  };

  const handleNewtonRaphsonButton = () => {
    navigate("/newton", { state: { selectedFile } });
  };

  const handleFastDecoupledButton = () => {
    navigate("/fdlf", { state: { selectedFile } });
  };

  const handleContingencyButton = () => {
    navigate("/contingency", { state: { selectedFile } });
  };

  const handleDCButton = () => {
    navigate("/dclf", { state: { selectedFile } });
  };

  return (
    <Container maxWidth="medium">
      <Box mt={4} textAlign="center">
        <img
          src="/logo.png"
          alt="Logo"
          id="image"
          style={imageStyles}
        />
      </Box>
      <Box mt={2} textAlign="center">
        <Typography variant="h2" id="logo">
          Power Flow Analysis
        </Typography>
      </Box>
      <Box mt={4} textAlign="center">
        <FileInput
            props={[selectedFile, setSelectedFile]}
            inputProps={{
              accept: '.xls, .xlsx, application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            }}
          />
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
          {selectedFile && <Button
                      style={buttonStyle}
                      variant="contained"
                      color="primary"
                      size="large"
                      onClick={handleGaussSeidelButton}
                    >
                      Gauss-Seidel Load Flow
                    </Button>}
          {selectedFile && <Button
                      style={buttonStyle}
                      variant="contained"
                      color="primary"
                      size="large"
                      onClick={handleNewtonRaphsonButton}
                      disabled={!selectedFile}
                    >
                      Newton-Raphson Load Flow
                    </Button>}
          {selectedFile && <Button
                      style={buttonStyle}
                      variant="contained"
                      color="primary"
                      size="large"
                      onClick={handleFastDecoupledButton}
                      disabled={!selectedFile}
                    >
                      Fast Decoupled Load Flow
                    </Button>}
          {selectedFile && <Button
                      style={buttonStyle}
                      variant="contained"
                      color="primary"
                      size="large"
                      onClick={handleDCButton}
                      disabled={!selectedFile}
                    >
                      DC Load Flow
                    </Button>}
          {selectedFile && <Button
                      style={buttonStyle}
                      variant="contained"
                      color="primary"
                      size="large"
                      onClick={handleContingencyButton}
                      disabled={!selectedFile}
                    >
                      Contingency Analysis
                    </Button>}
        </div>
      </Box>
    </Container>
  );
};

export default PowerFlowAnalysis;
