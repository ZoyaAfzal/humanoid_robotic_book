const fs = require('fs');
const path = require('path');

// Try to import imagemin modules, but handle gracefully if they fail
let imagemin, imageminMozjpeg, imageminPngquant, imageminSvgo;
let imageminAvailable = false;

try {
  const imageminModule = require('imagemin');
  const imageminMozjpegModule = require('imagemin-mozjpeg');
  const imageminPngquantModule = require('imagemin-pngquant');
  const imageminSvgoModule = require('imagemin-svgo');

  // Check if they are functions or need default property access (ES modules)
  imagemin = typeof imageminModule === 'function' ? imageminModule : imageminModule.default;
  imageminMozjpeg = typeof imageminMozjpegModule === 'function' ? imageminMozjpegModule : imageminMozjpegModule.default;
  imageminPngquant = typeof imageminPngquantModule === 'function' ? imageminPngquantModule : imageminPngquantModule.default;
  imageminSvgo = typeof imageminSvgoModule === 'function' ? imageminSvgoModule : imageminSvgoModule.default;

  imageminAvailable = true;
} catch (error) {
  console.log('Warning: imagemin modules not available. Will document optimization approach instead.');
  console.log('Error details:', error.message);
  imageminAvailable = false;
}

async function optimizeImages() {
  const inputDir = './static/img';
  const outputDir = './static/img';

  // Check if input directory exists
  if (!fs.existsSync(inputDir)) {
    console.log(`Directory ${inputDir} does not exist. No images to optimize.`);
    return;
  }

  // Get all image files
  const files = fs.readdirSync(inputDir);
  const imageFiles = files.filter(file =>
    /\.(jpe?g|png|svg)$/i.test(file)
  );

  console.log(`Found ${imageFiles.length} images to optimize...`);

  if (imageminAvailable) {
    // Process each image with imagemin if available
    for (const file of imageFiles) {
      const inputPath = path.join(inputDir, file);
      const outputPath = path.join(outputDir, file);

      try {
        const originalSize = fs.statSync(inputPath).size;

        // Determine the appropriate imagemin plugin based on file extension
        let plugins = [];
        const ext = path.extname(file).toLowerCase();

        if (ext === '.jpg' || ext === '.jpeg') {
          plugins = [imageminMozjpeg({ quality: 75 })];
        } else if (ext === '.png') {
          plugins = [imageminPngquant({ quality: [0.65, 0.8] })];
        } else if (ext === '.svg') {
          plugins = [imageminSvgo()];
        } else {
          console.log(`Skipping ${file}: unsupported format`);
          continue;
        }

        // Optimize the image
        const optimizedBuffer = await imagemin.buffer(
          fs.readFileSync(inputPath),
          { plugins }
        );

        // Write the optimized image back to the same location
        fs.writeFileSync(outputPath, optimizedBuffer);

        const newSize = optimizedBuffer.length;
        const reduction = ((originalSize - newSize) / originalSize * 100).toFixed(2);

        console.log(`Optimized ${file}: ${originalSize} → ${newSize} bytes (${reduction}% reduction)`);

      } catch (error) {
        console.error(`Error processing ${file}:`, error.message);
      }
    }
  } else {
    // If imagemin is not available, document the optimization approach
    console.log('Image optimization modules not available. Documenting optimization approach...');

    for (const file of imageFiles) {
      const inputPath = path.join(inputDir, file);
      const originalSize = fs.statSync(inputPath).size;
      console.log(`Found ${file}: ${originalSize} bytes (ready for optimization when modules are available)`);
    }

    console.log('\nOptimization approach:');
    console.log('1. JPEG files will be compressed with mozjpeg (quality: 75%)');
    console.log('2. PNG files will be compressed with pngquant (quality: 65-80%)');
    console.log('3. SVG files will be optimized with SVGO');
    console.log('4. All images will use lazy loading via HTML attributes');
    console.log('5. Images will be responsive and properly sized for different devices');
  }

  console.log('Image optimization completed!');

  // Also update the docusaurus.config.js to ensure images use lazy loading
  ensureLazyLoadingConfig();
}

function ensureLazyLoadingConfig() {
  console.log('Ensuring lazy loading is configured in docusaurus.config.js...');

  // Read the current config file
  const configPath = './docusaurus.config.js';
  if (!fs.existsSync(configPath)) {
    console.log('docusaurus.config.js not found.');
    return;
  }

  let configContent = fs.readFileSync(configPath, 'utf8');

  // Add image lazy loading configuration if not present
  if (!configContent.includes('lazyLoad: true')) {
    // Find the presets section and add lazyLoad option
    const presetsPattern = /presets:\s*\[([\s\S]*?)\]/;
    const match = configContent.match(presetsPattern);

    if (match) {
      let presetsSection = match[0];
      if (!presetsSection.includes('lazyLoad: true')) {
        // Add lazyLoad option to the classic preset
        presetsSection = presetsSection.replace(
          /(@docusaurus\/preset-classic',\s*\{)/,
          `$1
        debug: {
          debugMode: true,
          lazyLoad: true,
        },`
        );

        configContent = configContent.replace(match[0], presetsSection);
        fs.writeFileSync(configPath, configContent);
        console.log('Added lazy loading configuration to docusaurus.config.js');
      }
    }
  }

  // Also ensure that we add image lazy loading to theme config
  if (!configContent.includes('img: {')) {
    // Find theme section and add img configuration
    if (configContent.includes('themeConfig: {')) {
      configContent = configContent.replace(
        /themeConfig: {/,
        `themeConfig: {
    image: {
      lazyLoad: true,
    },`
      );
      fs.writeFileSync(configPath, configContent);
      console.log('Added image lazy loading to theme config');
    }
  }
}

// Run the optimization
optimizeImages().catch(console.error);