module.exports = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'Learn Humanoid Robotics Step by Step',
  url: 'http://localhost:3000', // Base URL for local development
  baseUrl: '/', // Root base URL for local development
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  trailingSlash: false,
  organizationName: 'ZoyaAfzal', // GitHub organization name
  projectName: 'humanoid_robotic_book', // GitHub repository name
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        debug: {
          debugMode: true,
          lazyLoad: true,
        },
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
        },
        blog: {
          showReadingTime: true,
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
  themeConfig: {
    colorMode: {
      defaultMode: 'light',  // Set default to light mode
      disableSwitch: false,  // Allow theme switching
      respectPrefersColorScheme: false,  // Don't respect system preference
    },
    // Navigation bar configuration
    navbar: {
      title: 'Humanoid Robotics',
      logo: {
        alt: 'Humanoid Robotics Logo',
        src: 'img/logo.svg', // You can add a logo image in static/img/
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'mySidebar',
          position: 'left',
          label: 'Learn',
        },
        {
          to: '/docs/intro',
          label: 'Getting Started',
          position: 'left'
        },
        {
          type: 'dropdown',
          label: 'Chapters',
          position: 'left',
          items: [
            {
              label: 'Chapter 1: Spec-Kit Plus & Robotics Foundation',
              to: '/docs/chapter1/lesson1/spec-kit-plus-workflow',
            },
            {
              label: 'Chapter 2: The Robotic Nervous System (ROS 2)',
              to: '/docs/chapter2/lesson1/ros2-architecture',
            },
            {
              label: 'Chapter 3: The Digital Twin (Simulation)',
              to: '/docs/chapter3/lesson1/gazebo-environment-setup',
            },
            {
              label: 'Chapter 4: The AI-Robot Brain (NVIDIA Isaac™)',
              to: '/docs/chapter4/lesson1/isaac-sim-synthetic-data',
            },
            {
              label: 'Chapter 5: Vision-Language-Action (VLA) & Capstone',
              to: '/docs/chapter5/lesson1/voice-to-action',
            },
          ],
        },
        {
          type: 'dropdown',
          label: 'Resources',
          position: 'right',
          items: [
            {
              label: 'Interactive Lessons',
              to: '/docs/intro',
            },
            {
              label: 'ROS 2 Documentation',
              href: 'https://docs.ros.org/en/humble/',
            },
            {
              label: 'Simulation Guide',
              to: '/docs/chapter3/lesson1/gazebo-environment-setup',
            },
          ],
        },
        {
          type: 'search', // Add search bar
          position: 'right',
        },
      ],
    },
    // algolia: {
    //   // The application ID provided by Algolia
    //   appId: 'YOUR_APP_ID', // Replace with actual Algolia App ID
    //   // Public API key: it is safe to commit it
    //   apiKey: 'YOUR_SEARCH_API_KEY', // Replace with actual Algolia API Key
    //   indexName: 'humanoid-robotics-book',
    //   // Optional: see doc section below
    //   contextualSearch: true,
    //   // Optional: Specify domains where the navigation should occur through window.location instead on history.push. Useful when our Algolia config crawls multiple documentation sites and we want to navigate with window.location.href to them.
    //   externalUrlRegex: 'external\\.com|domain\\.com',
    //   // Optional: Replace parts of the item URLs from Algolia. Useful when using the same search index for multiple deployments using a different baseUrl. You can use regexp or string in the `from` param. For example: localhost:3000 vs myCompany.com/docs
    //   replaceSearchResultPathname: {
    //     from: '/docs/', // or as RegExp: /\/docs\//
    //     to: '/',
    //   },
    //   // Optional: Algolia search parameters
    //   searchParameters: {},
    //   // Optional: path for search page that enabled by default
    //   searchPagePath: 'search',
    // },
  },
};