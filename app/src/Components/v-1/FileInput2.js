import React from 'react';
import { Button, Typography } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

function FileInput(props) {
  const [selectedFile, setSelectedFile] = props.props;

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    console.log('File selected:', file);
    setSelectedFile(file); // Store the selected file in the context
  };

  return (
    <div>
      <input
        type="file"
        id="fileInput"
        accept=".csv, .xlsx, .xls" // Allow CSV and Excel files
        onChange={handleFileChange}
        style={{ display: 'none' }}
      />
      <label htmlFor="fileInput">
        <Button
          variant="outlined"
          component="span"
          startIcon={<CloudUploadIcon />}
          sx={{ margin: 2 }}
        >
          Import File
        </Button>
      </label>
      {selectedFile && (
        <Typography variant="body1">
          Selected File: {selectedFile.name}
        </Typography>
      )}
    </div>
  );
}

export default FileInput;
