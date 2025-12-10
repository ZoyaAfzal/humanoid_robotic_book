import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', 'b36'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '4f6'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', '6e3'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', '558'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '4bd'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '75a'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '64a'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', 'f17'),
    routes: [
      {
        path: '/docs/adr/adr-004',
        component: ComponentCreator('/docs/adr/adr-004', '4fb'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/docs/chapter1/lesson1/spec-kit-plus-workflow',
        component: ComponentCreator('/docs/chapter1/lesson1/spec-kit-plus-workflow', 'a8b'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/docs/chapter1/lesson2/physical-ai-embodied-intelligence',
        component: ComponentCreator('/docs/chapter1/lesson2/physical-ai-embodied-intelligence', 'e1e'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/docs/chapter1/lesson3/development-environment-setup',
        component: ComponentCreator('/docs/chapter1/lesson3/development-environment-setup', '7a0'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/docs/chapter2/lesson1/ros2-architecture',
        component: ComponentCreator('/docs/chapter2/lesson1/ros2-architecture', 'cc7'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/docs/chapter2/lesson2/humanoid-robot-modeling',
        component: ComponentCreator('/docs/chapter2/lesson2/humanoid-robot-modeling', '878'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/docs/chapter2/lesson3/bridging-ai-agents',
        component: ComponentCreator('/docs/chapter2/lesson3/bridging-ai-agents', 'a74'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/docs/chapter3/lesson1/gazebo-environment-setup',
        component: ComponentCreator('/docs/chapter3/lesson1/gazebo-environment-setup', '37c'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/docs/chapter3/lesson2/simulating-physics-collisions',
        component: ComponentCreator('/docs/chapter3/lesson2/simulating-physics-collisions', 'e51'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/docs/chapter3/lesson3/sensor-simulation',
        component: ComponentCreator('/docs/chapter3/lesson3/sensor-simulation', 'd6d'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/docs/chapter4/lesson1/isaac-sim-synthetic-data',
        component: ComponentCreator('/docs/chapter4/lesson1/isaac-sim-synthetic-data', '188'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/docs/chapter4/lesson2/hardware-accelerated-navigation',
        component: ComponentCreator('/docs/chapter4/lesson2/hardware-accelerated-navigation', '9d0'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/docs/chapter4/lesson3/bipedal-path-planning',
        component: ComponentCreator('/docs/chapter4/lesson3/bipedal-path-planning', 'd42'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/docs/chapter5/lesson1/voice-to-action',
        component: ComponentCreator('/docs/chapter5/lesson1/voice-to-action', '25c'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/docs/chapter5/lesson2/cognitive-planning',
        component: ComponentCreator('/docs/chapter5/lesson2/cognitive-planning', 'ecc'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/docs/chapter5/lesson3/capstone-project-execution',
        component: ComponentCreator('/docs/chapter5/lesson3/capstone-project-execution', '353'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/docs/COMPLETION_SUMMARY',
        component: ComponentCreator('/docs/COMPLETION_SUMMARY', 'f27'),
        exact: true
      },
      {
        path: '/docs/COURSE_COMPLETION_CERTIFICATE',
        component: ComponentCreator('/docs/COURSE_COMPLETION_CERTIFICATE', '69f'),
        exact: true
      },
      {
        path: '/docs/intro',
        component: ComponentCreator('/docs/intro', '0c0'),
        exact: true,
        sidebar: "mySidebar"
      },
      {
        path: '/docs/module1/introduction-to-humanoid-robotics',
        component: ComponentCreator('/docs/module1/introduction-to-humanoid-robotics', '076'),
        exact: true
      },
      {
        path: '/docs/module1/kinematics-and-dynamics',
        component: ComponentCreator('/docs/module1/kinematics-and-dynamics', 'f11'),
        exact: true
      },
      {
        path: '/docs/module1/sensors-and-perception',
        component: ComponentCreator('/docs/module1/sensors-and-perception', '709'),
        exact: true
      },
      {
        path: '/docs/module1/summary',
        component: ComponentCreator('/docs/module1/summary', '386'),
        exact: true
      },
      {
        path: '/docs/test-route',
        component: ComponentCreator('/docs/test-route', '87d'),
        exact: true
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '754'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
