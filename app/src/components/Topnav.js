import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import * as React from 'react';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import HomeIcon from '@mui/icons-material/Home';
import HistoryIcon from '@mui/icons-material/History';
import BalanceIcon from '@mui/icons-material/Balance';
import TroubleshootIcon from '@mui/icons-material/Troubleshoot';
export default function NavBar(props) {
  props = props.props;
  const colorMode = props[0];
  const setColorMode = props[1];
  const [state, setState] = React.useState({
    left: false,
  });
  const icons = [<HomeIcon/>,<TroubleshootIcon/>,<BalanceIcon/>,<HistoryIcon/>]
  // Define the toggleDrawer function
  const toggleDrawer = (open) => (event) => {
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return;
    }

    setState({ left: open });
  };

  const list = (
    <Box
      sx={{ width: 250 }}
      role="presentation"
      onClick={toggleDrawer(false)}
      onKeyDown={toggleDrawer(false)}
    >
      <List>
        {[
          { text: 'Home', href: '/' },
          { text: 'Detect Event', href: '/detect-event'},
          { text: 'Classify Event', href: '/classify-event' },
          { text: 'Detected event history', href: '/detected-event-history' },
          
        ].map((item, index) => (
          <ListItem key={item.text} disablePadding>

            <ListItemButton component="a" href={item.href}>
            <ListItemIcon>
              {icons[index]}
            </ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Drawer
            anchor="left"
            open={state.left}
            onClose={toggleDrawer(false)}
          >
            {list}
          </Drawer>
          <IconButton
            onClick={toggleDrawer(true)}
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            BigSync
          </Typography>
          <Button color="inherit" href="/">Home</Button>
          <Button color="inherit" href="/detected-event-history">History</Button>
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

