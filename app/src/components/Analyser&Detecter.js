/* eslint-disable no-useless-concat */
import React, { useState, useEffect } from 'react';
import { Checkbox, Grid, Typography, Button, Divider, Alert, TextField } from '@mui/material';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import { useLocation } from 'react-router-dom';
import AnalysePlot from './Plot_Analyse&Detect';
import PlotlyPlot from './PlotV2';
import { useNavigate } from 'react-router-dom';
import DiscreteSlider from './Slider';
import dataToServer from '../utils/dataToServer'
import classifyEventData from '../utils/classifyEventV2';
import AlertDialog from './ErrorAlert'
import ThresholdForm from './ThresholdForm';
const serverAddress = 'http://localhost:5000/';
function Analyser() {

    // ------------ Getting csv Data -----------------//
    const navigate = useNavigate();
    const location = useLocation();
    const [subLnData, data, time] = location.state || [null, null, null];

    // -------------- Making state variables ------------//
    const [selectedSub, setSelectedSub] = useState(null);
    const [selectedLine, setSelectedLine] = useState(null);
    const [property, setProperty] = React.useState('F');
    const [faultData, setfaultData] = React.useState(null);
    const [mode, setMode] = React.useState(null);
    const [sd_th, setSd_th] = useState(0.025);
    const [windowSize, setWindowSize] = useState(2);
    const [buttonText, setButtonText] = useState("Detect event")
    const [plotData, setPlotData] = useState([[], []]);
    const [islandingEventData, setislandingEventData] = React.useState(null);
    const [err_message, setErr_message] = React.useState(null);
    const [reaadyToCheckEvents, setReadyToCheckEvents] = React.useState(false);
    const [thresholdValues, setThresholdValues] = useState({
        stepChange: 0.1,
        oscillatoryEvent: 5,
        impulseEvent: 2,
        islandingEvent: 0.1,
    });

    let p1 = ['F', 'VM', 'VA', 'IM', 'IA']
    let p2 = ['Frequency', 'Voltage Magnitude', 'Voltage Angle', 'Current Magnitude', 'Current Angle']

    // --------------- handeling Button functions ------------------ // 

    const handleDetectFaultButton = () => {
        console.log('Mode set to detect-event')
        setButtonText('Send To Server');
        setMode(0);
 
    }
    const appendDataSetToPlot = () => {
        if (selectedSub && selectedLine && property) {
            let temp = [];
            plotData.forEach((d) => {
                if (d.length !== 0) {
                    temp.push([d]);
                }
            })
            temp.push([`${selectedSub}` + ':' + `${selectedLine}`]);
            console.log('temp', temp);
            setPlotData(temp);
            setislandingEventData(temp);
            setMode(1);
        } 
        else { 
            return;  
        }
    }
    const resetPlotData = () => {
        setPlotData([[], []]);
        setislandingEventData([[], []])
    }
    const sendToServer = async (e) => {
        console.log(selectedSub, selectedLine)
        const serverData = await dataToServer([time, data[`${selectedSub}` + ':' + `${selectedLine}`][property]], serverAddress + 'v2/detect-event', windowSize, sd_th);
        console.log('serverData', serverData);
        if (serverData.error) {
            if (serverData.error.message) {
                console.log(serverData.error)
                setErr_message(serverData.error.message);
            }
            else {
                setErr_message(serverData.error.message);
            }

            return
        }
        // server return faultdata if fault is there and fault:none of fault is not there
        if (serverData) {
            setfaultData(serverData);
            setPlotData([[], []]);
            setButtonText('Classify event');
            setMode(2);
        }
        else {

            setfaultData(null);
        }
    }
    const handleClassifyEvent = async (e) => {

        const classifiedData = await classifyEventData([time, data[`${selectedSub}` + ':' + `${selectedLine}`][property], thresholdValues], serverAddress + 'v2/classify-event');
        console.log('classifiedData',classifiedData)
        if(classifiedData.error){
            setErr_message(classifiedData.error.message);
        }
        else{

            navigate('/classify-event', {
                state: classifiedData,
            })

        }
    }
    const handleClassifyIslandingEvent = async (e) => {
        console.log('islandingEventData')
        let array = []
        islandingEventData.forEach((d) => {
            array.push(data[d]['F'])
        })
        const serverData = await dataToServer([time, array, thresholdValues], serverAddress + 'v2/detect-islanding-event', windowSize, sd_th);
        if (serverData) {

            navigate('/classify-event', {
                state: serverData,
            })

        }
        else {


        }
    }

    // --------------- useeffect -----------------------------------------------------//

    useEffect(() => {
        resetPlotData();
    }, [property])
    useEffect(() => {
        console.log('mode->0')
        setMode(0);
        setfaultData(null);
        setButtonText('Detect Event');
    }, [property, selectedLine, selectedSub])

    if (!data) {
        return null;
    }

    // if (selectedSub && selectedLine && property) { console.log(selectedSub, selectedLine, property) }
    // ---------------------------------------------------------//

    return (
        <Grid container justifyContent={'space-between'} margin={1} width={'99%'}>
            {!data && <Alert severity="error">No Data found to analyze !!</Alert>}
            {err_message && <AlertDialog props={[err_message, setErr_message]} />}
            <Grid container item xs={1.5} direction='column' alignContent={'flex-start'}>
                <Grid >
                    <Grid item xs={2} direction='column' justifyContent={'center'} alignItems={'center'}>
                        <Typography variant="h6">Substations</Typography>
                        <FormGroup>
                            {Object.keys(subLnData).map((subKey) => (
                                <FormControlLabel
                                    key={subKey}
                                    control={
                                        <Checkbox
                                            checked={selectedSub === subKey}
                                            onChange={() => { setSelectedSub(subKey); setSelectedLine(null) }}
                                            size="caption"
                                        />
                                    }
                                    label={subKey}
                                />
                            ))}
                        </FormGroup>
                    </Grid>
                    <Grid item xs={6}>
                        {selectedSub && (
                            <div>
                                <Typography variant="h6">{selectedSub}:Lines</Typography>
                                <FormGroup>
                                    {subLnData[selectedSub].map((line) => (
                                        <FormControlLabel
                                            key={line}
                                            control=
                                            {<Checkbox size="caption" checked={selectedLine === line}
                                                onChange={() => setSelectedLine(line)} />}
                                            label={line}

                                        />
                                    ))}
                                </FormGroup>
                            </div>
                        )}
                    </Grid>
                </Grid>
                <Divider></Divider>
                <Button variant="contained" size='small' onClick={appendDataSetToPlot}>Add</Button>

            </Grid>
            <Grid >
                <Grid >

                    {(!faultData || (mode === 0)) && <AnalysePlot props={[time ? time : [], plotData, data, property]} />}
                    {(faultData && mode && mode !== 0) && <PlotlyPlot props={[faultData.time ? faultData.time : [], faultData.freq ? faultData.freq : [], 'Time', 'Frequency', faultData["fault"] ? "Fault Detected in " + `${selectedSub}` + ':' + `${selectedLine}` : "No fault detected in " + `${selectedSub}` + ':' + `${selectedLine}`]} />}
                </Grid>
                <Grid container margin={2} direction={'column'} justifyContent={'center'} alignItems={'center'}>
                    {mode === 0 && selectedSub && selectedLine && property === 'F' && plotData[0] && plotData[0].length > 0 && <Button variant="contained" onClick={handleDetectFaultButton}>{buttonText}</Button>}
                    {mode === 1 && selectedSub && selectedLine && property === 'F' && (
                        <Button variant="contained" sx={{ margin: 2 }} onClick={sendToServer}>{buttonText}</Button>
                    )}
                    {reaadyToCheckEvents && mode === 2 && selectedSub && selectedLine && property === 'F' && (
                        <Button variant="contained" sx={{ margin: 2 }} onClick={handleClassifyEvent}>{buttonText}</Button>
                    )}
                    {reaadyToCheckEvents && mode === 2 && selectedSub && selectedLine && property === 'F' && islandingEventData[0] && islandingEventData[0].length > 0 && (
                        <Button variant="contained" sx={{ margin: 2 }} onClick={handleClassifyIslandingEvent}>{'Detect islanding event '}</Button>
                    )}

                    {data && mode === 1 && property === 'F' && (
                        <DiscreteSlider prop={[sd_th, setSd_th, [0.1, 1, 0.05], "ROCOF Standard deviation threshold", 0.025]} />
                    )}
                    {data && mode === 1 && property === 'F' && (
                        <DiscreteSlider prop={[windowSize, setWindowSize, [10, 200, 10], "Window Size", 2]} />
                    )}
                </Grid>


            </Grid>
            <Grid>
                <Typography variant="h6">Properties</Typography>
                <FormGroup>
                    {Object.keys(p1).map((p, i) => (
                        <FormControlLabel
                            key={p}
                            control={
                                <Checkbox
                                    checked={property === p1[i]}
                                    onChange={() => { setProperty(p1[i]) }}
                                    size="caption"
                                />
                            }
                            label={p2[i]}
                        />
                    ))}
                </FormGroup>
                <Button variant="contained" size='small' onClick={resetPlotData}>Reset plot data</Button>
                <Grid container direction={'column'} marginTop={10}>
                    {mode === 2 && selectedSub && selectedLine && property === 'F' && <Typography variant="h6">Threshold values</Typography>}
                    {mode === 2 && selectedSub && selectedLine && property === 'F' &&
                        <ThresholdForm  values={thresholdValues} setValues={setThresholdValues} setReadyToCheckEvents={setReadyToCheckEvents}> </ThresholdForm>}
                </Grid>
            </Grid>

        </Grid >

    );
}
export default Analyser;