// import React, { useState, useEffect } from 'react';
// import { useNavigate,useLocation } from 'react-router-dom';
// import { Button, Typography, Box, Alert } from '@mui/material';
// import CloudUploadIcon from '@mui/icons-material/CloudUpload';
// import csvToServer from '../../utils/v1/csvToServer'
// import PlotlyPlot from '../PlotV2';
// import LinearBuffer from '../Loading';
// import DiscreteSlider from '../Slider';
// import classifyEvent from '../../utils/v1/classifyEvent';

// // url 
// const serverAddress = 'http://localhost:5000/';

// function DetectEvent() {
//   const navigate = useNavigate();
//   const location = useLocation();
//   // for buffering 
//   const [isLoading, setIsLoading] = useState(false);
//   const [buttonText, setButtonText] = useState("Send to server")
//   // for user input of window size 
//   const [windowSize, setWindowSize] = useState(2);

//   // State to store the selected file
//   const [selectedFile, setSelectedFile] = useState(null);

//   // For plotting data from server
//   const [plotData, setPlotData] = useState(null);
  

//   // This variable used for checking anything sent to server or not
//   // If not sent then any Alert(server error etc.) should not apper
//   const [sentToServer, setSentToServer] = useState(false);
//   const [sd_th, setSd_th] = useState(0.025); // State variable to store the sd_th
//   // Function to send file to server
//   const sendToServer = async (e) => {

//     // set loading to true
//     setIsLoading(true);
//     // set sent to server to true
//     setSentToServer(true);

//     // get fault data from server using async function csv to server
//     const faultData = await csvToServer(selectedFile, serverAddress+'/v1/detect-event', windowSize,sd_th );
//     // server return faultdata if fault is there and fault:none of fault is not there
//     if (faultData) {
//       setPlotData(faultData);
//       console.log(faultData)
      
//       // load for 3 more seconds after getting data from server
//       setTimeout(() => { setIsLoading(false);setButtonText("Classify event"); }, 3000);
      
//     }
//     else {
//       // if faultdata is not there that means some server error
//       setPlotData(null);
//       setTimeout(() => { setIsLoading(false); }, 3000);

//     }
//   }
//   // Function to handle file selection
//   const handleFileChange = (event) => {
//     const file = event.target.files[0];
//     setSelectedFile(file);

//   };


//   // 

//   const classifyEventOnClick = async()=>{
//     // set loading to true
//     setIsLoading(true);
//     const data = await classifyEvent(selectedFile,serverAddress+'/v1/classify-event');
//     if (data) {
//       // load for 3 more seconds after getting data from server
//       setTimeout(() => { setIsLoading(false);
//         navigate('/classify-event', {
//           state: data,
//         });
//       }, 3000);
      
      
//     }
//     else {
//       // navigate('/classify', {
//       //   state: data,
//       // });

//     }
//   }
//   /* 1. A box containing file input will always be there
//   2. If there is a file selected then a button with text 
//   sent to server and a slider to choose window size will appear
//   3. After selecting window size and clicking button, loading will appear
//   4. Nothing will happen till loading is there
//   5. After completion of loading, 3 cases can be there
//     (a) faultData is not set means nothing came from server, in that 
//   */ 
//   return (
//     <Box>
//       <Box component="center" sx={{ p: 1, border: '1px dashed grey', margin: 2 }}>
//         <input
//           type="file"
//           id="fileInput"
//           accept=".csv"
//           onChange={handleFileChange}
//           style={{ display: 'none' }}
//         />
//         <label htmlFor="fileInput">
//           <Button
//             variant="outlined"
//             component="span"
//             startIcon={<CloudUploadIcon />}
//             sx={{ margin: 2 }}
//           >
//             Upload File
//           </Button>
//         </label>
//         {selectedFile && (
//           <Typography variant="body1">
//             Selected File: {selectedFile.name}
//           </Typography>
//         )}
//         {selectedFile && (
//           <DiscreteSlider prop={[sd_th, setSd_th,[0.1,1,0.05],"ROCOF Standard deviation threshold",0.025]} />
//         )}
//         {selectedFile && (
//           <DiscreteSlider prop={[windowSize, setWindowSize,[10,200,10],"Window Size",2]} />
//         )}

//         {selectedFile && windowSize && !plotData && sd_th &&(
//           <Button variant="contained" sx={{ margin: 2 }} onClick={sendToServer}>{buttonText}</Button>
//         )}
//         {selectedFile && windowSize && plotData &&(
//           <Button variant="contained" sx={{ margin: 2 }} onClick={classifyEventOnClick}>{buttonText}</Button>
//         )}
//       </Box>
//       {isLoading && <LinearBuffer />}
//       {sentToServer && !isLoading && !plotData && <Alert variant="filled" severity="error">Internal Server error</Alert>}
//       {sentToServer && !isLoading && plotData && !plotData["fault"] && <Alert variant="filled" severity="success">No fault detected in uploaded data.</Alert>}
//       {sentToServer && !isLoading && plotData && plotData["fault"] && (<Box component="center" >
//         <PlotlyPlot props={[plotData.time,plotData.freq,'Time','Frequency','Faulty data']} ></PlotlyPlot>
//       </Box>)}
//     </Box>
//   );
// }



// export default DetectEvent;
