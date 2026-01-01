import React, { useState, useEffect } from 'react';
import ChatInterface from './ChatInterface';

const RAGChatWidget = ({ position = 'bottom-right' }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMounted, setIsMounted] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    // Only set mounted on client side to avoid SSR issues
    setIsMounted(true);
    console.log('RAGChatWidget mounted');

    // Check initial theme
    const checkTheme = () => {
      if (document.documentElement.getAttribute('data-theme') === 'dark') {
        setIsDarkMode(true);
      } else {
        setIsDarkMode(false);
      }
    };

    checkTheme();

    // Create a MutationObserver to watch for theme changes
    const observer = new MutationObserver(checkTheme);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['data-theme']
    });

    // Cleanup
    return () => {
      observer.disconnect();
    };
  }, []);

  // Click handlers with more debugging
  const handleOpenClick = (e) => {
    e.stopPropagation();
    e.preventDefault();
    console.log('Open button clicked - event object:', e);
    console.log('Current isOpen state:', isOpen);
    setIsOpen(true);
    console.log('State updated to:', true);
  };

  const handleCloseClick = (e) => {
    e.stopPropagation();
    e.preventDefault();
    console.log('Close button clicked - event object:', e);
    console.log('Current isOpen state:', isOpen);
    setIsOpen(false);
    console.log('State updated to:', false);
  };

  if (!isMounted) {
    // Return a placeholder during SSR
    return (
      <div style={{ display: 'none' }} />
    );
  }

  const positionStyles = {
    'bottom-right': {
      bottom: '20px',
      right: '20px',
    },
    'bottom-left': {
      bottom: '20px',
      left: '20px',
    },
    'top-right': {
      top: '20px',
      right: '20px',
    },
    'top-left': {
      top: '20px',
      left: '20px',
    },
  };

  const widgetPosition = positionStyles[position] || positionStyles['bottom-right'];

  return (
    <div
      style={{
        position: 'fixed',
        ...widgetPosition,
        zIndex: 9999, // Higher z-index to ensure it's on top
        fontFamily: 'system-ui, -apple-system, sans-serif',
        pointerEvents: 'auto', // Ensure it receives pointer events
      }}
    >
      {!isOpen ? (
        <button
          onClick={handleOpenClick}
          style={{
            width: '60px',
            height: '60px',
            borderRadius: '50%',
            backgroundColor: isDarkMode ? '#28a745' : '#28a745',
            color: 'white',
            border: '2px solid white', // Add border to make sure it's clickable
            fontSize: '24px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: isDarkMode
              ? '0 4px 20px rgba(40, 167, 69, 0.6)'
              : '0 4px 20px rgba(40, 167, 69, 0.4)',
            transition: 'transform 0.2s, box-shadow 0.2s, background-color 0.2s',
            outline: 'none',
            position: 'relative', // Ensure proper positioning
            pointerEvents: 'auto', // Ensure it receives pointer events
          }}
          onMouseEnter={(e) => {
            e.target.style.transform = 'scale(1.1)';
            e.target.style.boxShadow = isDarkMode
              ? '0 6px 25px rgba(40, 167, 69, 0.8)'
              : '0 6px 25px rgba(40, 167, 69, 0.5)';
            e.target.style.backgroundColor = isDarkMode ? '#218838' : '#218838';
          }}
          onMouseLeave={(e) => {
            e.target.style.transform = 'scale(1)';
            e.target.style.boxShadow = isDarkMode
              ? '0 4px 20px rgba(40, 167, 69, 0.6)'
              : '0 4px 20px rgba(40, 167, 69, 0.4)';
            e.target.style.backgroundColor = isDarkMode ? '#28a745' : '#28a745';
          }}
          aria-label="Open AI Assistant"
          type="button"
          id="chat-widget-open-btn" // Add ID for easier debugging
        >
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M20 2H4C2.9 2 2 2.9 2 4V22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2ZM20 16H6L4.5 17.5V4H20V16ZM8 7H16V9H8V7ZM8 11H16V13H8V11Z" fill="white"/>
          </svg>
        </button>
      ) : (
        <div
          className="chat-widget-container"
          style={{
            width: '400px',
            height: '500px',
            maxWidth: '95vw',
            maxHeight: '80vh',
            backgroundColor: isDarkMode ? '#121212' : 'white',
            border: isDarkMode ? '1px solid #444' : '1px solid #e9ecef', // Subtle border to match theme
            borderRadius: '16px',
            overflow: 'hidden',
            boxShadow: isDarkMode
              ? '0 12px 40px rgba(0,0,0,0.5)'
              : '0 12px 40px rgba(0,0,0,0.15)',
            display: 'flex',
            flexDirection: 'column',
            pointerEvents: 'auto', // Ensure it receives pointer events
          }}
        >
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '16px',
              backgroundColor: isDarkMode ? '#28a745' : '#28a745',
              color: 'white',
            }}
          >
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px'
            }}>
              <div style={{
                width: '32px',
                height: '32px',
                backgroundColor: 'rgba(255,255,255,0.2)',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 1H5C3.89 1 3 1.89 3 3V7H1V9H3V15C3 17.21 4.79 19 7 19H17C19.21 19 21 17.21 21 15V9H21ZM19 9H17V15C17 16.1 16.1 17 15 17H9C7.9 17 7 16.1 7 15V9H5V7H13V9H19V9Z" fill="white"/>
                </svg>
              </div>
              <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>Humanoid Robotics AI</h3>
            </div>
            <button
              onClick={handleCloseClick}
              style={{
                background: isDarkMode
                  ? 'rgba(255,255,255,0.2)'
                  : 'rgba(255,255,255,0.2)',
                border: 'none',
                fontSize: '20px',
                cursor: 'pointer',
                color: 'white',
                width: '36px',
                height: '36px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                borderRadius: '50%',
                transition: 'background-color 0.2s',
                outline: 'none',
              }}
              onMouseEnter={(e) => {
                e.target.style.backgroundColor = isDarkMode
                  ? 'rgba(255,255,255,0.3)'
                  : 'rgba(255,255,255,0.3)';
              }}
              onMouseLeave={(e) => {
                e.target.style.backgroundColor = isDarkMode
                  ? 'rgba(255,255,255,0.2)'
                  : 'rgba(255,255,255,0.2)';
              }}
              aria-label="Close chat"
              type="button"
              id="chat-widget-close-btn" // Add ID for easier debugging
            >
              ×
            </button>
          </div>
          <div style={{ flex: 1, overflow: 'hidden' }}>
            <ChatInterface />
          </div>
        </div>
      )}
    </div>
  );
};

export default RAGChatWidget;