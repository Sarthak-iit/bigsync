export const styles = {
  container: {
    maxHeight: '90vh',
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
    height: '90vh',
    overflowY: 'auto',
    flexGrow: 1,
    padding: '10px',
    border: '1px solid #0073ba',
  },
  flexItemB: {
    flex: 1,
    height: '90vh',
    padding: '10px',
    border: '1px solid #0073ba',
  },
  label: {
    fontWeight: 'bold',
    color: '#333',
    // textDecoration: 'underline'
  },
  appear:{
    opacity:0,
    
    transition: 'opacity 0.3s',
  }
};
