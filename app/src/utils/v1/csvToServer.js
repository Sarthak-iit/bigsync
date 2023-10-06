import setCookie from "../cookieManager";

const csvToServer = async(selectedFile,serverAddress,windowSize,sd_th) => {
    if (!selectedFile) {
      alert('Please select a file.');
      return;
    }
    // Create a FormData object to send the file
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('windowSize', windowSize);
    formData.append('sd_th', sd_th);
    console.log(sd_th); 
    try {
        // Send the file to the server
        const response = await fetch(serverAddress, {
          method: 'POST',
          body: formData,
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
export default csvToServer