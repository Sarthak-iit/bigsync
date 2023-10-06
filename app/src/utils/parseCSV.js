import Papa from 'papaparse';

const parseCSV = async (csvFile) => {
  return new Promise((resolve, reject) => {
    Papa.parse(csvFile, {
      header: true,
      skipEmptyLines: true,
      dynamicTyping: true,
      complete: function (results) {
        if (results.data.length > 0) {
          const dataWithSkippedRows = results.data.slice(3); // Skip 3 rows
          resolve(dataWithSkippedRows); // Resolve the promise with the parsed data
        } else {
          reject("No data found in the CSV file.");
        }
      },
      error: function (error) {
        reject(error.message); // Reject the promise with an error message
      },
    });
  });
};

export default parseCSV;
