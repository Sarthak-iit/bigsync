import * as React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import NavBar from './Components/Topnav'
import DetectEvent from './Components/v-1/DetectEvent'
import { createTheme, useTheme, ThemeProvider } from '@mui/material/styles';
import Paper from '@mui/material/Paper';
import History from './Components/History'
import Home from './Components/Home'
import Classify from './Components/ClassifyEvent'
import Analyser from './Components/Analyser&Detecter';


function App() {
  
  const theme = useTheme();
  const [colorMode, setColorMode] = React.useState(theme.palette.mode);
  const newTheme = createTheme({ palette: { mode: colorMode } });
  return (
    <ThemeProvider theme={newTheme}>
      <Paper sx={{ width: '100%', height: '100vh' }} elevation={0}>
        <div>
        <NavBar props={[colorMode,setColorMode]}></NavBar>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<Home></Home>}></Route>
              <Route path="/analyse" element={<Analyser></Analyser>}></Route>
              <Route path="/detect-event" element={<DetectEvent></DetectEvent>}></Route>
              <Route path="/detected-event-history" element={<History></History>}></Route>
              <Route path="/classify-event" element={<Classify></Classify>}></Route>
            </Routes>
          </BrowserRouter>
        </div>
      </Paper>
    </ThemeProvider>
  );
}

export default App;

