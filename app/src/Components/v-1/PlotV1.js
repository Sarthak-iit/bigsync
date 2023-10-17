// import { useState } from 'react';
// import { LineChart } from '@mui/x-charts/LineChart';
// import Slider from '@mui/material/Slider';
// import Box from '@mui/material/Box';
// import Alert from '@mui/material/Alert';
// import ToggleButton from '@mui/material/ToggleButton';
// import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';

// export default function Chart(props) {
//     const minDistance = 5;
//     const x_data = props.data.time;
//     const y_data = [props.data.freq,props.data.rocof];
//     const a = x_data.length / 100;
//     function valuetext(value) {
//         return `${(x_data[0] + (x_data[x_data.length - 1] - x_data[0]) / (x_data.length / a) * value).toFixed(3)} sec`;

//     }
    
//     const graphToggleLabel = ["Frequency","ROCOF"]
//     const graphToggleColor = ["orange","purple"]
//     const [plotType, setPlotType] = useState(0);
//     const [value, setValue] = useState([0, 100]);
//     const [y, setY] = useState(y_data[plotType])
//     const [x, setX] = useState(x_data)
//     console.log(x.length,y.length)

    
//     const handleChangeToggle = (event, whatToPlot) => {
//         if(whatToPlot !== 0 && !whatToPlot){return}
//         console.log(whatToPlot)
//         setPlotType(whatToPlot);
//         setX(x_data.slice(Number(value[0] * a), Number(value[1]) * a))
//         setY(y_data[whatToPlot].slice(Number(value[0] * a), Number(value[1]) * a))
//     };
//     const handleChangeSlider = (event, newValue, activeThumb) => {
//         if (!Array.isArray(newValue)) {
//             return;
//         }
//         if (newValue[1] - newValue[0] <= minDistance) {
//             if (activeThumb === 0) {
//                 const clamped = Math.min(newValue[0], 100 - minDistance);
//                 setValue([clamped, clamped + minDistance]);
//                 setX(x_data.slice(Number(value[0] * a), Number(value[1]) * a))
//                 setY(y_data[plotType].slice(Number(value[0] * a), Number(value[1]) * a))
//                 // setFA(fault_area.slice(Number(value[0] * a), Number(value[1]) * a))
//             } else {
//                 const clamped = Math.max(newValue[1], minDistance);
//                 setValue([clamped - minDistance, clamped]);
//                 setX(x_data.slice(Number(value[0] * a), Number(value[1]) * a))
//                 setY(y_data[plotType].slice(Number(value[0] * a), Number(value[1]) * a))
//                 // setFA(fault_area.slice(Number(value[0] * a), Number(value[1]) * a))
//             }
//         }
//         else {
//             setValue(newValue);
//             setX(x_data.slice(Number(value[0] * a), Number(value[1]) * a))
//             setY(y_data[plotType].slice(Number(value[0] * a), Number(value[1]) * a))
//             console.log('hihi',Number(value[0] * a), Number(value[1]) * a)
//         }

//     };
//     return (
//         // <Paper elevation={10}>
//         <Box>
//             <Alert variant="filled" severity="warning">Fault detected in following data.</Alert>
//             <Box>
//                 <LineChart
//                     xAxis={[{ data: x, label: 'time' }]}
//                     series={[
//                         {
//                             curve: "linear",
//                             data: y,
//                             color: graphToggleColor[plotType], label: graphToggleLabel[plotType]
//                         },
//                     ]}
//                     width={1000}
//                     height={300}
//                 />
//             </Box>
//             <Box sx={{ width: 300 }}>
//                 <Slider
//                     value={value}
//                     onChange={handleChangeSlider}
//                     valueLabelDisplay="auto"
//                     valueLabelFormat={valuetext}
//                     getAriaValueText={valuetext}
//                     disableSwap
//                 />
//             </Box>
//             <ToggleButtonGroup
//                 color="primary"
//                 value={plotType}
//                 exclusive
//                 onChange={handleChangeToggle}
//                 aria-label="WhatToPlot"
//             >
//                 <ToggleButton value={0}>Freq</ToggleButton>
//                 <ToggleButton value={1}>Rocof</ToggleButton>
//             </ToggleButtonGroup>
//         </Box>
//         // </Paper>
//     );
// }