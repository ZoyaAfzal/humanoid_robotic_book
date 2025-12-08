module.exports = {
  title: 'Humanoid Robotics Book',
  tagline: 'Learn Humanoid Robotics Step by Step',
  url: 'https://zoyaafzal.github.io', // Base URL for GitHub Pages deployment
  baseUrl: '/humanoid_robotic_book/', // Repository name for GitHub Pages
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  trailingSlash: false,
  organizationName: 'zoyaafzal', // GitHub organization name
  projectName: 'humanoid_robotics_book', // GitHub repository name
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
    algolia: {
      // The application ID provided by Algolia
      appId: 'YOUR_APP_ID', // Replace with actual Algolia App ID
      // Public API key: it is safe to commit it
      apiKey: 'YOUR_SEARCH_API_KEY', // Replace with actual Algolia API Key
      indexName: 'humanoid-robotics-book',
      // Optional: see doc section below
      contextualSearch: true,
      // Optional: Specify domains where the navigation should occur through window.location instead on history.push. Useful when our Algolia config crawls multiple documentation sites and we want to navigate with window.location.href to them.
      externalUrlRegex: 'external\\.com|domain\\.com',
      // Optional: Replace parts of the item URLs from Algolia. Useful when using the same search index for multiple deployments using a different baseUrl. You can use regexp or string in the `from` param. For example: localhost:3000 vs myCompany.com/docs
      replaceSearchResultPathname: {
        from: '/docs/', // or as RegExp: /\/docs\//
        to: '/',
      },
      // Optional: Algolia search parameters
      searchParameters: {},
      // Optional: path for search page that enabled by default
      searchPagePath: 'search',
    },
  },
};
