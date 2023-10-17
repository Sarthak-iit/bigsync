import * as React from 'react';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import { DataGrid } from '@mui/x-data-grid';
import PlotlyPlot from './PlotV2'
const makeRows = (rows, object) => {
  const events = Object.keys(object);
  events.map((e, i) => {
    let row = { id: i, eventName: e, isDetected: String(object[e])}
    rows.push(row);
  })
  return rows;

}
let r = 0;
const columns = [
  { field: 'id', headerName: 'ID', width: '50' },
  {
    field: 'eventName',
    headerName: 'Event Name',
    width: '200',
  },
  {
    field: 'isDetected',
    headerName: 'Detected',
    width: '100',
  }
];



export default function EventDataGrid(props) {
  const [selectedRowId, setSelectedRowId] = React.useState(null);
  const [eventData, setEventData] = React.useState([[], []]);

  const result = props.props["result"];
  const data = props.props["data"];
  // console.log(data.length)
  let rows = [];
  rows = makeRows(rows, result);

  const handleSelectionChange = (selection) => {
    // console.log(selectedRowId)
    if (selection.length > 0) {

      setSelectedRowId((selection[selection.length - 1]));
    }
    else {
      setSelectedRowId(null);
    }
  };
  const handleAction = () => {
    r = selectedRowId;
    console.log(eventData)
    setEventData(data[selectedRowId])
  };

  return (
    <Grid

      container
      flexDirection="row"  // Center vertically
      alignItems="center"
      justifyContent={'space-around'}     // Center horizontally
    >
      <Grid container flexDirection="column" xs={3} >
        <DataGrid
          rows={rows}
          columns={columns}
          pageSizeOptions={[2]}
          rowHeight={40}
          selectionModel={selectedRowId}
          onRowSelectionModelChange={handleSelectionChange}
          disableMultipleRowSelection={true} // Restrict multiple selection
        />
        {(selectedRowId || selectedRowId === 0) && <Button
          onClick={handleAction}
          variant="contained"
          style={{ margin: 10 }}
        >
          See data
        </Button>}
      </Grid>



      <PlotlyPlot props={[eventData[1], eventData[0],'' ,rows[selectedRowId],'Detected event' ]} />

    </Grid>

  );
}