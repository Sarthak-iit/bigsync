import React from 'react';
import { useState } from 'react';
import { Container, Typography, Button, Box } from '@mui/material';
import FileInput from './v-1/FileInput'
import { useNavigate } from 'react-router-dom';
import parseCSV from '../utils/parseCSV';
import formatData from '../utils/formatData';
import LinearBuffer from './Loading'

const imageStyles = {
  width: '200px',
  height: 'auto',
  transition: 'transform 0.5s ease', // Add a smooth transition
};

const LandingPage = () => {
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState();
  const [isLoading, setisLoading] = useState(false);
  const [subLnData, setSubLnData] = useState({});
  const [data, setData] = useState([]);
  const [time, setTime] = useState([]);
  const handleAnalyseButton = async () => {
    if (selectedFile) {
      setisLoading(true);
      try {
        var data = await parseCSV(selectedFile);
        var time;
        [time, data] = await formatData(data);
        setData(data);
        setTime(time);
        const sub = Object.keys(data);
        const subLnData = {};
        for (const item of sub) {
          const parts = item.split(':');
          const subKey = `Sub:${parts[1]}`;
          const lnValue = parts[2] + ':' + parts[3];
          if (!subLnData[subKey]) {
            subLnData[subKey] = [];
          }
          subLnData[subKey].push(lnValue);
        }
        setSubLnData(subLnData);
        setTimeout(() => {
          setisLoading(false);

          navigate('/analyse', {
            state: [subLnData, data, time],
          });
        }, 3000)


      } catch (error) {
        console.error('Error:', error);
      }
    };



  }
  return (
    <Container maxWidth="sm">
      <Box mt={4} textAlign="center">
        {/* Your logo */}
        <img
          src="/logo.png"
          alt="Logo"
          id="image"
          style={imageStyles}
        />
      </Box>
      <Box mt={2} textAlign="center">
        <Typography variant="h2" id="logo">
          Big Sync
        </Typography>
      </Box>
      <Box mt={4} textAlign="center">
        <FileInput props={[selectedFile, setSelectedFile]} />

        {selectedFile && !isLoading && <Button
          variant="contained"
          color="primary"
          size="large"
          onClick={handleAnalyseButton}
          style={{ marginLeft: '16px' }}
        >
          Start Analysis
        </Button>}
        <Box margin={5}>
          {isLoading && <LinearBuffer mt={5} />}
        </Box>


      </Box>
    </Container>
  );
};

export default LandingPage;

