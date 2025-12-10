import React from 'react';
import clsx from 'clsx';
import styles from './InteractiveLesson.module.css';

// Default component to wrap lesson content
const InteractiveLesson = ({ title, chapter, lesson, children }) => {
  return (
    <div className={styles.interactiveLessonContainer}>
      <div className={styles.lessonHeader}>
        <h1>{title}</h1>
        <div className={styles.lessonMeta}>
          Chapter {chapter}, Lesson {lesson}
        </div>
      </div>
      <div className={styles.lessonContent}>
        {children}
      </div>
    </div>
  );
};

export default InteractiveLesson;