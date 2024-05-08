const dataToServerClassify = async ([time, data, thresholdValues], serverAddress) => {
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
        thresholdValues:thresholdValues
      }),
    });
    if (response.ok) {
      const responseData = await response.json(); // Parse the response as JSON
      return responseData;
    }
    else {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

  } catch (error) {
    console.error('Error:', error);
    return {'error':error};
    
  }
};
export default dataToServerClassify