module.exports = {
  mySidebar: [
    'intro',
    {
      type: 'category',
      label: 'Chapter 1: Spec-Kit Plus & Robotics Foundation',
      items: [
        'chapter1/lesson1/spec-kit-plus-workflow',
        'chapter1/lesson2/physical-ai-embodied-intelligence',
        'chapter1/lesson3/development-environment-setup',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 2: The Robotic Nervous System (ROS 2)',
      items: [
        'chapter2/lesson1/ros2-architecture',
        'chapter2/lesson2/humanoid-robot-modeling',
        'chapter2/lesson3/bridging-ai-agents',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 3: The Digital Twin (Simulation)',
      items: [
        'chapter3/lesson1/gazebo-environment-setup',
        'chapter3/lesson2/simulating-physics-collisions',
        'chapter3/lesson3/sensor-simulation',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 4: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'chapter4/lesson1/isaac-sim-synthetic-data',
        'chapter4/lesson2/hardware-accelerated-navigation',
        'chapter4/lesson3/bipedal-path-planning',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 5: Vision-Language-Action (VLA) & Capstone',
      items: [
        'chapter5/lesson1/voice-to-action',
        'chapter5/lesson2/cognitive-planning',
        'chapter5/lesson3/capstone-project-execution',
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
