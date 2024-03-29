const dataToServer = async([time,data,thresholdValues],serverAddress,windowSize,sd_th) => {
    console.log('serverAddress',serverAddress);
    if (!time || !data) {
      alert('Please select a file.');
      return;
    }
    // Create a FormData object to send the file
    console.log(sd_th); 
    try {
        // Send the file to the server
        const response = await fetch(serverAddress, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            time: time,
            data: data,
            windowSize: windowSize,
            sd_th: sd_th,
            thresholdValues: thresholdValues||null
          }),
        });
        console.log('response',response)
        if (response.ok) {
            const responseData = await response.json(); // Parse the response as JSON
            return responseData;
        } 
        else{
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

      } catch (error) {
        console.error('Error:', error);
        return {'error':{
          message:error
        }};
        
      }
    };
export default dataToServer