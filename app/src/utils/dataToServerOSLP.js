const dataToServerOSLP = async([time,data,points],serverAddress) => {
    if (!data) {
      alert('Please select a file.');
      return;
    }
    try {
        // Send the file to the server
        const response = await fetch(serverAddress, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            data: data,
            time:time,
            points:[points[0].x, points[1].x]
          }),
        });
        console.log([points[0].x, points[1].x])
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
export default dataToServerOSLP