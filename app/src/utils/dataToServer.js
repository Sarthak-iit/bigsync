import setCookie from "./cookieManager";

const dataToServer = async([time,data],serverAddress,windowSize,sd_th) => {
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
          }),
        });
        if (response.ok) {
            const responseData = await response.json(); // Parse the response as JSON
            setCookie([new Date(),"success",responseData["fault"]]);
            return responseData;
        } 
        else{
          setCookie([new Date(),"fail",null]);
          return null;
        }

      } catch (error) {
        console.error('Error:', error);
      }
    };
export default dataToServer