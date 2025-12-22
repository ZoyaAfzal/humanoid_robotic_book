import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import RAGChatWidget from '@site/src/components/RAGChatWidget';

export default function Layout(props) {
  return (
    <>
      <OriginalLayout {...props} />
      <RAGChatWidget position="bottom-right" />
    </>
  );
}