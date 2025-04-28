import React, { createContext, useState, useContext } from 'react';

// Create a context for the shared file state
const FileContext = createContext();

// FileProvider component to wrap the app and provide shared file state
export const FileProvider = ({ children }) => {
  const [sharedFile, setSharedFile] = useState(null);

  return (
    <FileContext.Provider value={{ sharedFile, setSharedFile }}>
      {children}
    </FileContext.Provider>
  );
};

// Custom hook to use the FileContext
export const useFileContext = () => useContext(FileContext);
