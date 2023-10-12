/* eslint-disable no-useless-concat */
import React, { useState, useEffect } from 'react';
import { Checkbox, Grid, Typography, Button, Divider, Alert, TextField } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import { useLocation } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import dataToServer from '../utils/dataToServer'
import AlertDialog from './ErrorAlert'
import MyBarChart from './Barchart';

const serverAddress = 'https://bigsync.onrender.com/';
function Baseliner() {

    // ------------ Getting csv Data -----------------//
    const location = useLocation();
    const [subLnData, data] = location.state || [null, null, null];

    // -------------- Making state variables ------------//
    const [selectedSub, setSelectedSub] = useState(null);
    const [selectedLine, setSelectedLine] = useState(null);
    const [err_message, setErr_message] = React.useState(null);
    const [statData, setStatData] = React.useState({ "Minimum": 0, "Maximum": 0, "Mean": 0, "99.5% Limit": 0, "99.9% Limit": 0 });
    // making table rows
    const makeRows = (object) => {
        let rows = [];
        const events = Object.keys(object);
        events.map((e, i) => {
            let row = { id: i, statName: e, value: Number(object[e]) }
            rows.push(row);
        })
        return rows;

    }
    let rows = makeRows(statData);
    let r = 0;
    const columns = [
        { field: 'id', headerName: 'ID', width: '50' },
        {
            field: 'statName',
            headerName: 'Statistical measure',
            width: '200',
        },
        {
            field: 'value',
            headerName: 'Value',
            width: '200',
        }
    ];

    // --------------- handeling Button functions ------------------ // 

    // const resetPlotData = () => {
    //     setPlotData([[], []]);
    //     setislandingEventData([[], []])
    // }
    const sendToServer = async (e) => {
        console.log(selectedSub, selectedLine)
        console.log(data[`${selectedSub}` + ':' + `${selectedLine}`]['F']);
        const serverData = await dataToServer([1, data[`${selectedSub}` + ':' + `${selectedLine}`]['F']], serverAddress + 'v2/find-statistics', 1, 1);
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
            setStatData(serverData);
        }
        else {
            setErr_message("Server error!!!");
        }
    }

    // --------------- useeffect -----------------------------------------------------//

    useEffect(() => {
        rows = makeRows(statData);
    }, [statData])

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
            </Grid>
            <Grid >
                <Grid >
                    <Typography variant="h6">Statistics of {`${selectedSub}` + ':' + `${selectedLine}`}, Frequency data</Typography>
                    <Grid container flexDirection="column" xs={3} mt={5}>
                        <DataGrid
                            rows={rows}
                            columns={columns}
                            pageSizeOptions={[2]}
                            rowHeight={40}
                            disableMultipleRowSelection={true}
                        />
                    </Grid>

                </Grid>
                <Grid container margin={2} direction={'column'} justifyContent={'center'} alignItems={'center'}>
                    {selectedSub && selectedLine&&<Button variant="contained" sx={{ margin: 2 }} onClick={sendToServer}>{'Check Stats'}</Button>}
                </Grid>


            </Grid>
            <Grid>
            <MyBarChart xData={Object.keys(statData)} values={Object.values(statData)} />
            </Grid>
        </Grid >

    );
}
export default Baseliner;