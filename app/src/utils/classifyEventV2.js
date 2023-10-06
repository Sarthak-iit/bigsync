import setCookie from "./cookieManager";

const dataToServerClassify = async([time,data],serverAddress) => {
    if (!time || !data) {
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
            time: time,
            data: data,
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
export default dataToServerClassify