export const styles = {
  container: {
    width:'99%',
    maxHeight: '90vh',
    overflowY: 'auto',
    transition: 'scroll-height 1s ease', // Adjust the duration and timing function as needed
  },
  
  containerChild: {
    maxHeight: '40vh',
    overflowY: 'auto',
    padding: '10px',
    margin: '2px',
    transition: 'max-height 1s ease', // Adjust the duration and timing function as needed
    // Other styles for the child container
  },
  flexContainer: {
    
    display: 'flex',
    justifyContent: 'space-between',
    transition: 'max-height 1s ease'
  },
  flexItem: {
    maxHeight: '90vh',
    overflowY: 'auto',
    flexGrow: 1,
    padding: '10px',
    border: '1px solid #0073ba',
    transition: 'height 1s ease'
  },
  flexItemB: {
    flex: 1,
    padding: '10px',
    border: '1px solid #0073ba',
    transition: 'height 1s ease'
  },
  label: {
    fontWeight: 'bold',
    color: '#333',
    // textDecoration: 'underline'
  }
};
