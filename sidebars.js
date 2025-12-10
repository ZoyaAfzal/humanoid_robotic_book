module.exports = {
  mySidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: Introduction to Humanoid Robotics',
      items: [
        'module1/introduction-to-humanoid-robotics',
        'module1/kinematics-and-dynamics',
        'module1/sensors-and-perception',
        'module1/summary',
      ],
    },
    {
      type: 'category',
      label: 'Architecture Decision Records',
      items: [
        'adr/adr-004',
      ],
    },
  ],
};
