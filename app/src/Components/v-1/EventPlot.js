// import { LineChart } from '@mui/x-charts/LineChart';
// import Slider from '@mui/material/Slider';
// import Box from '@mui/material/Box';
// import Alert from '@mui/material/Alert';
// import { useState } from 'react';
// export default function EventPlot(props) {
//     const minDistance = 5;
//     let eventData = props.props.eventData;
//     let r = props.props.r;
//     const x_data = eventData[1];
//     const y_data = eventData[0];
//     console.log(x_data, y_data)
//     const a = x_data.length / 100;
//     const labels = {
//         0:['frequency','time'],
//         1:['ROCOF','time'],
//         2:['frequency','time'],
//         3:['frequency','time'],
//         4:['Power[dB]','frequency']
//     }
//     // function valuetext(value) {
//     //     return `${(x_data[0] + (x_data[x_data.length - 1] - x_data[0]) / (x_data.length / a) * value).toFixed(3)}`;
//     // }
//     // const [value, setValue] = useState([0, 100]);
//     // const [y, setY] = useState(y_data)
//     // const [x, setX] = useState(x_data)

//     // const handleChangeSlider = (event, newValue, activeThumb) => {
//     //     if (!Array.isArray(newValue)) {
//     //         return;
//     //     }
//     //     if (newValue[1] - newValue[0] <= minDistance) {
//     //         if (activeThumb === 0) {
//     //             const clamped = Math.min(newValue[0], 100 - minDistance);
//     //             setValue([clamped, clamped + minDistance]);
//     //             setX(x_data.slice(Number(value[0] * a), Number(value[1]) * a))
//     //             setY(y_data.slice(Number(value[0] * a), Number(value[1]) * a))
//     //         } else {
//     //             const clamped = Math.max(newValue[1], minDistance);
//     //             setValue([clamped - minDistance, clamped]);
//     //             setX(x_data.slice(Number(value[0] * a), Number(value[1]) * a))
//     //             setY(y_data.slice(Number(value[0] * a), Number(value[1]) * a))
//     //         }
//     //     }
//     //     else {
//     //         setValue(newValue);
//     //         setX(x_data.slice(Number(value[0] * a), Number(value[1]) * a))
//     //         setY(y_data.slice(Number(value[0] * a), Number(value[1]) * a))
//     //     }


//     return (
        
//         <Box >
//             <Box display="flex"
//                 flexDirection="column"  // Center vertically
//                 alignItems="center"      // Center horizontally
//                 maxHeight={'100vh'}>
//                 {eventData[1].length === 0 && <Alert variant="filled" severity="warning">This event is not detected</Alert>}
//                 {eventData[1].length !== 0 &&
//                     <Box>
//                         <LineChart
//                             xAxis={[{ data: eventData[1], label: labels[r][1] }]}
//                             series={[
//                                 {
//                                     curve: "linear",
//                                     data: eventData[0],
//                                     label: labels[r][0]
//                                     // color: graphToggleColor, label: graphToggleLabel
//                                 },
//                             ]}
//                         />
//                         <Box sx={{ width: 300 }}>
//                             {/* <Slider
//                                 value={value}
//                                 onChange={handleChangeSlider}
//                                 valueLabelDisplay="auto"
//                                 valueLabelFormat={valuetext}
//                                 getAriaValueText={valuetext}
//                                 disableSwap
//                             /> */}
//                         </Box>
//                     </Box>

//                 }

//             </Box>
//         </Box>
//         // </Paper>
//     );
// }