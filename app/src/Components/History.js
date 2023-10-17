import Cookies from 'js-cookie';  
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

  
const getCookie = ()=> {
    if(!Cookies.get('bigsyncData')){
        return ""
    }
    return Cookies.get('bigsyncData');
  }
const temp = getCookie().split(',');
let rows = [];
for (let i = 0; i < temp.length; i += 3) {
    rows.push(temp.slice(i, i + 3));
  }

export default function History() {
    return (
        <TableContainer sx={{ minWidth: 650 ,width:'80vw',mr:'10vw',ml:'10vw',mt:'5vh',height:'80vh'}}component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Date</TableCell>
                <TableCell align="right">Status</TableCell>
                <TableCell align="right">Fault Detected</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map((row,i) => (
                <TableRow
                  key={rows[i][0]}
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell component="th" scope="row">
                    {rows[i][0].slice(0,-31)}
                  </TableCell>
                  <TableCell align="right">{rows[i][1]}</TableCell>
                  <TableCell align="right">{rows[i][2]}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      );
    }