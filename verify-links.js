// Link verification script for Docusaurus site
// Checks for broken internal and external links

const fs = require('fs');
const path = require('path');
const axios = require('axios');
const { globSync } = require('glob');

// Function to get all markdown files in the docs directory
function getMarkdownFiles(dir) {
  let results = [];
  const items = fs.readdirSync(dir);

  for (const item of items) {
    const itemPath = path.join(dir, item);
    const stat = fs.statSync(itemPath);

    if (stat.isDirectory()) {
      results = results.concat(getMarkdownFiles(itemPath));
    } else if (item.endsWith('.md') || item.endsWith('.mdx')) {
      results.push(itemPath);
    }
  }

  return results;
}

// Function to extract links from markdown content
function extractLinks(content) {
  // Regular expression to match markdown links [text](url)
  const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
  const links = [];
  let match;

  while ((match = linkRegex.exec(content)) !== null) {
    const url = match[2];

    // Skip anchor links (starting with #) and mailto links
    if (!url.startsWith('#') && !url.startsWith('mailto:')) {
      links.push({
        text: match[1],
        url: url,
        isInternal: url.startsWith('/') || url.startsWith('./') || url.startsWith('../')
      });
    }
  }

  return links;
}

// Function to check if internal file exists
function checkInternalLink(url, basePath) {
  let filePath;

  if (url.startsWith('/')) {
    // Absolute path from docs root
    filePath = path.join(basePath, url.substring(1));
  } else {
    // Relative path
    filePath = path.join(basePath, url);
  }

  // Add .md extension if not present for docs
  if (!path.extname(filePath)) {
    filePath += '.md';
  }

  return fs.existsSync(filePath) || fs.existsSync(filePath.replace('.md', '.mdx'));
}

// Function to check external link
async function checkExternalLink(url) {
  try {
    const response = await axios.head(url, { timeout: 10000 });
    return {
      valid: response.status >= 200 && response.status < 400,
      status: response.status
    };
  } catch (error) {
    // If HEAD fails, try GET
    try {
      const response = await axios.get(url, { timeout: 10000 });
      return {
        valid: response.status >= 200 && response.status < 400,
        status: response.status
      };
    } catch (getError) {
      return {
        valid: false,
        status: getError.response ? getError.response.status : 'ERROR',
        error: getError.message
      };
    }
  }
}

// Function to check for placeholder/invalid URLs in source files
function checkSourceFilesForLinks() {
  console.log('Checking source files for links...');

  const sourceFiles = [
    ...globSync('./src/**/*.{js,jsx,ts,tsx}'),
    ...globSync('./static/**/*.{html,js}'),
    ...globSync('./*.{js,jsx,ts,tsx}')
  ];

  const results = [];

  for (const file of sourceFiles) {
    try {
      const content = fs.readFileSync(file, 'utf8');
      // Look for URLs in source code
      const urlRegex = /https?:\/\/[^\s"'<>]+/g;
      let match;

      while ((match = urlRegex.exec(content)) !== null) {
        const url = match[0];
        // Check for placeholder URLs like the one we found
        if (url.includes('1FAIpQLSf5iL6Y9Hkxj4zR7F5J7PmK7PmK7PmK7PmK7PmK7PmK7PmK7P') ||
            url.includes('placeholder') || url.includes('example.com') || url.includes('your-')) {
          results.push({
            file: file,
            url: url,
            type: 'placeholder',
            issue: 'Placeholder/invalid URL detected'
          });
        } else {
          results.push({
            file: file,
            url: url,
            type: 'external',
            issue: null
          });
        }
      }
    } catch (error) {
      console.log(`  Error reading file ${file}: ${error.message}`);
    }
  }

  return results;
}

// Main function to verify links
async function verifyLinks() {
  console.log('Starting link verification...\n');

  const docsPath = './docs';
  const markdownFiles = getMarkdownFiles(docsPath);
  let totalLinks = 0;
  let brokenLinks = [];
  let validLinks = [];

  for (const file of markdownFiles) {
    console.log(`Checking links in: ${file}`);

    const content = fs.readFileSync(file, 'utf8');
    const links = extractLinks(content);

    for (const link of links) {
      totalLinks++;

      if (link.isInternal) {
        const exists = checkInternalLink(link.url, docsPath);
        if (exists) {
          console.log(`  ✓ Internal: ${link.url}`);
          validLinks.push({ file, ...link, exists });
        } else {
          console.log(`  ✗ Broken internal link: ${link.url} in ${file}`);
          brokenLinks.push({ file, ...link, exists: false });
        }
      } else {
        // Check if it's a relative link that should be internal
        if (link.url.startsWith('./') || link.url.startsWith('../')) {
          // This should be treated as internal relative to the current file
          const relativePath = path.resolve(path.dirname(file), link.url);
          const docsAbsolutePath = path.resolve(docsPath);
          const relativeToDocs = path.relative(docsAbsolutePath, relativePath);

          const exists = fs.existsSync(relativePath) ||
                         fs.existsSync(relativePath.replace('.md', '.mdx')) ||
                         fs.existsSync(relativePath + '.md') ||
                         fs.existsSync(relativePath + '.mdx');

          if (exists) {
            console.log(`  ✓ Internal (relative): ${link.url}`);
            validLinks.push({ file, ...link, exists });
          } else {
            console.log(`  ✗ Broken internal link (relative): ${link.url} in ${file}`);
            brokenLinks.push({ file, ...link, exists: false });
          }
        } else {
          // External link
          try {
            const result = await checkExternalLink(link.url);
            if (result.valid) {
              console.log(`  ✓ External: ${link.url} (${result.status})`);
              validLinks.push({ file, ...link, status: result.status });
            } else {
              console.log(`  ✗ Broken external link: ${link.url} in ${file} (Status: ${result.status})`);
              brokenLinks.push({ file, ...link, status: result.status, error: result.error });
            }
          } catch (error) {
            console.log(`  ✗ Error checking external link: ${link.url} in ${file} (${error.message})`);
            brokenLinks.push({ file, ...link, error: error.message });
          }
        }
      }
    }
  }

  // Check source files for any URLs
  console.log('\nChecking source files for potential links...');
  const sourceLinkResults = checkSourceFilesForLinks();

  for (const result of sourceLinkResults) {
    if (result.issue) {
      console.log(`  ✗ ${result.issue}: ${result.url} in ${result.file}`);
      brokenLinks.push(result);
    } else {
      console.log(`  ✓ Source file URL: ${result.url}`);
      validLinks.push(result);
    }
  }

  // Summary
  console.log('\n' + '='.repeat(50));
  console.log('LINK VERIFICATION SUMMARY');
  console.log('='.repeat(50));
  console.log(`Total links checked: ${totalLinks + sourceLinkResults.length}`);
  console.log(`Valid links: ${validLinks.length}`);
  console.log(`Broken links: ${brokenLinks.length}`);

  if (brokenLinks.length > 0) {
    console.log('\nBROKEN LINKS:');
    brokenLinks.forEach((link, index) => {
      console.log(`${index + 1}. File: ${link.file}`);
      if (link.url) {
        console.log(`   URL: ${link.url}`);
      }
      if (link.text) {
        console.log(`   Text: [${link.text}](${link.url})`);
      }
      console.log(`   Type: ${link.type || (link.isInternal ? 'Internal' : 'External')}`);
      if (link.status) console.log(`   Status: ${link.status}`);
      if (link.error) console.log(`   Error: ${link.error}`);
      if (link.issue) console.log(`   Issue: ${link.issue}`);
      console.log('');
    });
  } else {
    console.log('\n✓ No broken links found!');
  }

  return {
    total: totalLinks + sourceLinkResults.length,
    valid: validLinks.length,
    broken: brokenLinks.length,
    brokenLinks
  };
}

// Run the link verification
verifyLinks().catch(console.error);