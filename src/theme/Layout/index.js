import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import RAGChatWidget from '../../components/RAGChatWidget';

export default function Layout(props) {
  return (
    <>
      <OriginalLayout {...props} />
      {/* Ensure the chat widget is properly loaded and displayed */}
      <RAGChatWidget position="bottom-right" />
    </>
  );
}