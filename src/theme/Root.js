import React from 'react';

// Root component that wraps the entire app
const Root = ({ children }) => {
  return (
    <>
      {/* Render the children (the main content) */}
      {children}
    </>
  );
};

export default Root;