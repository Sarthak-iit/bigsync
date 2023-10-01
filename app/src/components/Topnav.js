import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';

export default function NavBar(props) {
  props = props.props;
  const colorMode = props[0];
  const setColorMode = props[1];
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography  variant="h6" component="div" sx={{ flexGrow: 1 }}>
            BigSync
          </Typography>
          <Button color="inherit" href="/">Home</Button>
          <Button color="inherit" href="/history">History</Button>
          <Button
              sx={{ ml: 1 }}
              onClick={() =>
                setColorMode((prev) => (prev === 'light' ? 'dark' : 'light'))
              }
              color="inherit"
              endIcon={
                colorMode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />
              }
            >
              {colorMode} mode
            </Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}
