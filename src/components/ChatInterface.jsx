import React, { useState, useRef, useEffect } from 'react';
import useChatState from '../hooks/useChatState';
import styles from './ChatInterface.module.css';

const ChatInterface = () => {
  const { messages, isLoading, error, sendQuery, addMessage } = useChatState();
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Function to get selected text
  const getSelectedText = () => {
    const selection = window.getSelection();
    return selection.toString().trim();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    await sendQuery(inputValue);
    setInputValue('');
  };

  const handleContextQuery = () => {
    const selectedText = getSelectedText();
    if (!selectedText) {
      addMessage({
        type: 'error',
        content: 'Please select some text first',
        timestamp: new Date().toISOString()
      });
      return;
    }

    // Pre-fill the input with selected text context
    setInputValue(`Based on this text: "${selectedText}", explain in more detail:`);
  };

  return (
    <div className={styles['chat-interface']}>
      <div className={styles['chat-header-extra']}>
        <button onClick={handleContextQuery} className={styles['context-button']} title="Ask about selected text">
          💬 Ask About Selection
        </button>
      </div>
      <div className={styles['chat-messages']}>
        {messages.length === 0 ? (
          <div className={styles['welcome-message']}>
            <div className={styles['welcome-icon']}>
              <svg width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 1H5C3.89 1 3 1.89 3 3V7H1V9H3V15C3 17.21 4.79 19 7 19H17C19.21 19 21 17.21 21 15V9H21ZM19 9H17V15C17 16.1 16.1 17 15 17H9C7.9 17 7 16.1 7 15V9H5V7H13V9H19V9Z" fill="white"/>
              </svg>
            </div>
            <h3 className={styles['welcome-title']}>🤖 Humanoid Robotics Assistant</h3>
            <p className={styles['welcome-subtitle']}>Ask me anything about humanoid robotics and the textbook content! 🤖</p>
            <div className={styles['welcome-description']}>
              <p>✨ Select text on the page and click "Ask About Selection" for context-specific answers.</p>
              <p>💡 I can help explain complex concepts, answer questions, and provide insights about humanoid robotics!</p>
            </div>
          </div>
        ) : (
          messages.map((message, index) => (
            <div key={index} className={`${styles['message']} ${styles[message.type]}`}>
              <div className="message-content" style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: '12px'
              }}>
                {message.type === 'agent' && (
                  <div className={styles['agent-avatar']}>
                    <span className={styles['agent-avatar-icon']}>🤖</span>
                  </div>
                )}
                {message.type === 'user' && (
                  <div className={styles['user-avatar']}>
                    <span className={styles['user-avatar-icon']}>👤</span>
                  </div>
                )}
                <div style={{ flex: 1 }}>
                  <p style={{
                    margin: 0,
                    lineHeight: '1.5',
                    fontSize: '14px'
                  }}>{message.content}</p>
                  {message.type === 'agent' && message.sources && message.sources.length > 0 && (
                    <div className="sources" style={{
                      marginTop: '10px',
                      paddingTop: '8px',
                      borderTop: '1px solid #e9ecef',
                      fontSize: '12px'
                    }}>
                      <div style={{
                        color: '#6c757d',
                        marginBottom: '6px',
                        fontWeight: '500'
                      }}>Sources:</div>
                      <ul style={{
                        margin: 0,
                        padding: '0 0 0 16px',
                        color: '#495057'
                      }}>
                        {message.sources.slice(0, 3).map((source, idx) => (
                          <li key={idx} style={{
                            marginBottom: '4px',
                            wordBreak: 'break-word'
                          }}>
                            <a href={source} target="_blank" rel="noopener noreferrer" style={{
                              color: '#4a6cf7',
                              textDecoration: 'none',
                              fontSize: '12px',
                              fontWeight: '500'
                            }}>
                              {new URL(source).pathname.replace('/docs/', '').replace(/-/g, ' ') || 'Reference'}
                            </a>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className={`${styles['message']} ${styles['loading']}`}>
            <div className="message-content" style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px'
            }}>
              <div style={{
                minWidth: '32px',
                minHeight: '32px',
                backgroundColor: '#28a745',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                flexShrink: 0
              }}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 1H5C3.89 1 3 1.89 3 3V7H1V9H3V15C3 17.21 4.79 19 7 19H17C19.21 19 21 17.21 21 15V9H21ZM19 9H17V15C17 16.1 16.1 17 15 17H9C7.9 17 7 16.1 7 15V9H5V7H13V9H19V9Z" fill="white"/>
                </svg>
              </div>
              <div className={styles['typing-indicator']}>
                <span className={styles['typing-text']}>🤖 AI is thinking</span>
                <div className={styles['typing-dots']}>
                  <div className={styles['typing-dot']}></div>
                  <div className={styles['typing-dot']}></div>
                  <div className={styles['typing-dot']}></div>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {error && (
        <div className={styles['error-message']}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 1H5C3.89 1 3 1.89 3 3V7H1V9H3V15C3 17.21 4.79 19 7 19H17C19.21 19 21 17.21 21 15V9H21ZM19 9H17V15C17 16.1 16.1 17 15 17H9C7.9 17 7 16.1 7 15V9H5V7H13V9H19V9Z" fill="#721c24"/>
            </svg>
            {error}
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className={styles['chat-input-form']}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask about humanoid robotics..."
          disabled={isLoading}
          className={styles['chat-input']}
          onKeyPress={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e);
            }
          }}
        />
        <button
          type="submit"
          disabled={isLoading || !inputValue.trim()}
          className={styles['send-button']}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M2.01 21L23 12L2.01 3L2 10L17 12L2 14L2.01 21Z" fill="white"/>
          </svg>
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;