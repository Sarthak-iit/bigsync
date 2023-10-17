export const styles = {
  container: {
    maxHeight: '93vh',
    overflowY: 'auto',
  },
  
  containerChild: {
    // opacity: 0,
    transition: 'opacity 0.3s',
    maxHeight: '40vh',
    overflowY: 'auto',
    padding: '10px',
    margin: '2px',

  },
  flexContainer: {
    
    display: 'flex',
    justifyContent: 'space-between',
  },
  flexItem: {
    height: '93vh',
    overflowY: 'auto',
    flexGrow: 1,
    padding: '10px',
    border: '3px solid #0073ba',
  },
  flexItemB: {
    flex: 1,
    height: '93vh',
    padding: '10px',
    border: '3px solid #0073ba',
  },
  label: {
    fontWeight: 'bold',
    color: '#333',
    // textDecoration: 'underline'
  },
  appear:{
    opacity:0,
    
    transition: 'opacity 0.3s',
  },
  fileInputStyle : {
    color: '#fff',
    padding: '10px 20px',
    border: 'none',
    borderRadius: '5px',
    fontSize: '16px',
    margin: '10px',
    textAlign: 'center',
  },
  navbar:{
    minHeight:'50px',
    height:'7vh'
  }
};
