import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/humanoid_robotic_book/docs',
    component: ComponentCreator('/humanoid_robotic_book/docs', 'dca'),
    routes: [
      {
        path: '/humanoid_robotic_book/docs/adr/adr-004',
        component: ComponentCreator('/humanoid_robotic_book/docs/adr/adr-004', '2e0'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter1',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter1', 'bdf'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter1/lesson1/spec-kit-plus-workflow',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter1/lesson1/spec-kit-plus-workflow', '0d7'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter1/lesson2/physical-ai-embodied-intelligence',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter1/lesson2/physical-ai-embodied-intelligence', '051'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter1/lesson3/development-environment-setup',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter1/lesson3/development-environment-setup', '97b'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter2',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter2', 'd79'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter2/lesson1/ros2-architecture',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter2/lesson1/ros2-architecture', '513'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter2/lesson2/humanoid-robot-modeling',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter2/lesson2/humanoid-robot-modeling', '752'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter2/lesson3/bridging-ai-agents',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter2/lesson3/bridging-ai-agents', '302'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter3',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter3', '22c'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter3/lesson1/gazebo-environment-setup',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter3/lesson1/gazebo-environment-setup', '226'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter3/lesson2/simulating-physics-collisions',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter3/lesson2/simulating-physics-collisions', 'aad'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter3/lesson3/sensor-simulation',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter3/lesson3/sensor-simulation', '1a6'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter4',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter4', '679'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter4/lesson1/isaac-sim-synthetic-data',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter4/lesson1/isaac-sim-synthetic-data', 'ad6'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter4/lesson2/hardware-accelerated-navigation',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter4/lesson2/hardware-accelerated-navigation', '635'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter4/lesson3/bipedal-path-planning',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter4/lesson3/bipedal-path-planning', '383'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter5',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter5', '587'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter5/lesson1/voice-to-action',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter5/lesson1/voice-to-action', '839'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter5/lesson2/cognitive-planning',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter5/lesson2/cognitive-planning', 'c13'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/chapter5/lesson3/capstone-project-execution',
        component: ComponentCreator('/humanoid_robotic_book/docs/chapter5/lesson3/capstone-project-execution', '3a8'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/COMPLETION_SUMMARY',
        component: ComponentCreator('/humanoid_robotic_book/docs/COMPLETION_SUMMARY', '3d9'),
        exact: true
      },
      {
        path: '/humanoid_robotic_book/docs/COURSE_COMPLETION_CERTIFICATE',
        component: ComponentCreator('/humanoid_robotic_book/docs/COURSE_COMPLETION_CERTIFICATE', '983'),
        exact: true
      },
      {
        path: '/humanoid_robotic_book/docs/intro',
        component: ComponentCreator('/humanoid_robotic_book/docs/intro', '178'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/humanoid_robotic_book/docs/module1/introduction-to-humanoid-robotics',
        component: ComponentCreator('/humanoid_robotic_book/docs/module1/introduction-to-humanoid-robotics', '156'),
        exact: true
      },
      {
        path: '/humanoid_robotic_book/docs/module1/kinematics-and-dynamics',
        component: ComponentCreator('/humanoid_robotic_book/docs/module1/kinematics-and-dynamics', 'cbf'),
        exact: true
      },
      {
        path: '/humanoid_robotic_book/docs/module1/sensors-and-perception',
        component: ComponentCreator('/humanoid_robotic_book/docs/module1/sensors-and-perception', '5a0'),
        exact: true
      },
      {
        path: '/humanoid_robotic_book/docs/module1/summary',
        component: ComponentCreator('/humanoid_robotic_book/docs/module1/summary', '307'),
        exact: true
      }
    ]
  },
  {
    path: '/humanoid_robotic_book/',
    component: ComponentCreator('/humanoid_robotic_book/', 'ea7'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
