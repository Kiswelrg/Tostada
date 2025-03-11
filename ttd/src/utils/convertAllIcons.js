import { convertMultipleSvgs } from './convertSvg.js';
import fs from 'fs';
import path from 'path';

/**
 * Recursively find all SVG files in a directory
 * @param {string} dir - Directory to search
 * @param {Array} fileList - Array to store found files
 * @returns {Array} - Array of SVG file paths
 */
function findSvgFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      findSvgFiles(filePath, fileList);
    } else if (path.extname(file).toLowerCase() === '.svg') {
      fileList.push(filePath);
    }
  });
  
  return fileList;
}

/**
 * Convert all SVG files in a directory to Vue components
 * @param {string} directory - Directory containing SVG files
 */
async function convertDirectorySvgs(directory) {
  try {
    // Find all SVG files
    const svgFiles = findSvgFiles(directory);
    console.log(`Found ${svgFiles.length} SVG files in ${directory}`);
    
    // Prepare the list of SVGs to convert
    const svgList = svgFiles.map(filePath => {
      const fileName = path.basename(filePath, '.svg');
      // Convert to PascalCase and add Icon suffix
      const componentName = fileName
        .replace(/[^a-zA-Z0-9]/g, ' ')
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join('') + 'Icon';
      
      // Convert to kebab-case
      const iconName = fileName
        .replace(/[^a-zA-Z0-9]/g, '-')
        .toLowerCase()
        .replace(/-+/g, '-')
        .replace(/^-|-$/g, '');
      
      return {
        path: filePath,
        componentName,
        iconName
      };
    });
    
    // Convert all SVGs
    const results = await convertMultipleSvgs(svgList);
    
    // Print summary
    const successful = results.filter(r => r.success).length;
    console.log(`✅ Successfully converted ${successful} of ${svgList.length} SVG files`);
    
    if (successful < svgList.length) {
      console.log(`❌ Failed to convert ${svgList.length - successful} SVG files`);
    }
  } catch (error) {
    console.error('Error converting directory SVGs:', error);
  }
}

// Example usage: Convert all SVGs in the public/static/tool directory
convertDirectorySvgs('./public/static/tool');

// You can also convert specific directories:
// convertDirectorySvgs('./public/static/Message/Emoji/svg'); 