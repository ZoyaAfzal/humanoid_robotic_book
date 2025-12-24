import React, { useState, useEffect } from 'react';

// Root component that wraps the entire app
const Root = ({ children }) => {
  const [showChat, setShowChat] = useState(false);
  const [chatLoaded, setChatLoaded] = useState(false);

  // Dynamically import the ChatInterface component to avoid SSR issues
  useEffect(() => {
    const loadChatComponent = async () => {
      try {
        const { default: ChatInterface } = await import('../components/ChatInterface');
        setChatLoaded(ChatInterface);
      } catch (error) {
        console.error('Failed to load chat component:', error);
      }
    };

    loadChatComponent();
  }, []);

  const toggleChat = () => {
    setShowChat(!showChat);
  };

  return (
    <>
      {/* Render the children (the main content) */}
      {children}

      {/* Floating chat button */}
      <button
        onClick={toggleChat}
        className="chat-toggle-button"
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          backgroundColor: '#3498db',
          color: 'white',
          border: 'none',
          borderRadius: '50%',
          width: '60px',
          height: '60px',
          fontSize: '24px',
          cursor: 'pointer',
          zIndex: 1000,
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
        aria-label="Open AI Assistant"
      >
        💬
      </button>

      {/* Chat modal */}
      {showChat && chatLoaded && (
        <div
          style={{
            position: 'fixed',
            bottom: '90px',
            right: '20px',
            width: '400px',
            height: '500px',
            backgroundColor: 'white',
            border: '1px solid #ddd',
            borderRadius: '8px',
            zIndex: 1000,
            boxShadow: '0 8px 32px rgba(0,0,0,0.15)',
            display: 'flex',
            flexDirection: 'column'
          }}
        >
          <div
            style={{
              padding: '12px',
              backgroundColor: '#f8f9fa',
              borderBottom: '1px solid #eee',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              borderTopLeftRadius: '8px',
              borderTopRightRadius: '8px'
            }}
          >
            <h3 style={{ margin: 0, color: '#2c3e50' }}>AI Assistant</h3>
            <button
              onClick={toggleChat}
              style={{
                background: 'none',
                border: 'none',
                fontSize: '24px',
                cursor: 'pointer',
                color: '#7f8c8d',
                width: '30px',
                height: '30px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>
          <div style={{ flex: 1, overflow: 'hidden' }}>
            <chatLoaded />
          </div>
        </div>
      )}

      {/* Overlay when chat is open */}
      {showChat && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0,0,0,0.1)',
            zIndex: 999,
          }}
          onClick={toggleChat}
        />
      )}
    </>
  );
};

export default Root;