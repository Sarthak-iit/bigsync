import React from 'react';
import { Container, Typography, Button, Box } from '@mui/material';

const companyNameStyles = {
  fontFamily: 'Arial, sans-serif',
  fontWeight: 'bold',
  marginBottom: '16px',
  transition: 'transform 0.5s ease', // Add a smooth transition
};

const imageStyles = {
  width: '200px',
  height: 'auto',
  transition: 'transform 0.5s ease', // Add a smooth transition
};

const LandingPage = () => {
  // Function to trigger animation on hover
  const handleMouseEnter = () => {
    const logo = document.getElementById('logo');
    const image = document.getElementById('image');
    logo.style.transform = 'scale(1.1)'; // Scale up by 10%
    image.style.transform = 'scale(1.1)'; // Scale up by 10%
  };

  // Function to reset animation when mouse leaves
  const handleMouseLeave = () => {
    const logo = document.getElementById('logo');
    const image = document.getElementById('image');
    logo.style.transform = 'scale(1)';
    image.style.transform = 'scale(1)';
  };

  return (
    <Container maxWidth="sm">
      <Box mt={4} textAlign="center">
        {/* Your logo */}
        <img
          src="/logo.png"
          alt="Logo"
          style={imageStyles}
          id="image"
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
        />
      </Box>
      <Box mt={2} textAlign="center">
        <Typography style={companyNameStyles} variant="h2" id="logo">
          Big Sync
        </Typography>
      </Box>
      <Box mt={4} textAlign="center">
        {/* Buttons */}
        <Button variant="contained" color="primary" size="large" href="/check">
          Check
        </Button>
        <Button
          href="/history"
          variant="outlined"
          color="primary"
          size="large"
          style={{ marginLeft: '16px' }}
        >
          History
        </Button>
      </Box>
    </Container>
  );
};

export default LandingPage;
