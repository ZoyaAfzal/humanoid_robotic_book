import React from 'react';
import styles from './Context7.module.css';

// Context 7: Physical AI Textbook Feedback Component
// This component embeds a Google Form for collecting feedback on the textbook content
const Context7 = () => {
  return (
    <div className={styles.context7Container}>
      <div className={styles.context7Header}>
        <h3>Context 7: Textbook Feedback</h3>
        <p>Please provide feedback on this module to help us improve the Physical AI textbook.</p>
      </div>

      <div className={styles.feedbackForm}>
        {/* Embedded Google Form - Replace with actual form URL */}
        <iframe
          src="https://docs.google.com/forms/d/e/1FAIpQLSf5iL6Y9Hkxj4zR7F5J7PmK7PmK7PmK7PmK7PmK7PmK7PmK7P/viewform?embedded=true"
          width="100%"
          height="800"
          frameborder="0"
          marginheight="0"
          marginwidth="0"
          title="Physical AI Textbook Feedback Form"
          className={styles.googleForm}
        >
          Loading feedback form...
        </iframe>
      </div>

      <div className={styles.feedbackGuidance}>
        <h4>Feedback Areas:</h4>
        <ul>
          <li>Content clarity and accuracy</li>
          <li>Difficulty level appropriateness</li>
          <li>Examples and practical applications</li>
          <li>Overall learning experience</li>
          <li>Suggestions for improvements</li>
        </ul>
      </div>
    </div>
  );
};

export default Context7;