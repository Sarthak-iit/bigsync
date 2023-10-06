import * as React from 'react';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';
import EventTable from './EventTable'
import { useLocation } from 'react-router-dom';
export default function ClassifyGrid() {
    const location = useLocation();
    const { state } = location;
    const data = state;

    // const events = Object.keys(data); // Use Object.keys directly
    return (
        <Box sx={{ flexGrow: 1,mt:2,flexDirection:'row'}}>
            {!data&&<Alert severity="error">No Data found to classify event!!</Alert>}
            {data&&<EventTable props={data}></EventTable>}
        </Box>
    );
}
