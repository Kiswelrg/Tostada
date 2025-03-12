import fs from 'fs';
import path from 'path';
import { svgToVueComponent } from './svgToComponent.js';

/**
 * Converts an SVG file to a Vue component and registers it in IconSystem
 * @param {string} svgPath - Path to the SVG file
 * @param {string} componentName - Name for the component (PascalCase)
 * @param {string} iconName - Name for the icon in IconSystem (kebab-case)
 */
export async function convertAndRegisterSvg(svgPath, componentName, iconName) {
  try {
    // 1. Read the SVG file
    const svgContent = fs.readFileSync(svgPath, 'utf8');
    
    // 2. Convert to Vue component
    const vueComponent = svgToVueComponent(svgContent);
    
    // 3. Write to a .vue file in the icons directory
    const outputPath = path.resolve('./src/components/icons', `${componentName}.vue`);
    fs.writeFileSync(outputPath, vueComponent);
    console.log(`✅ Created Vue component: ${outputPath}`);
    
    // 4. Update IconSystem.vue to register the new icon
    updateIconSystem(componentName, iconName);
    console.log(`✅ Registered icon '${iconName}' in IconSystem`);
    
    return { success: true, componentPath: outputPath };
  } catch (error) {
    console.error('Error converting SVG:', error);
    return { success: false, error };
  }
}

/**
 * Updates IconSystem.vue to register a new icon
 * @param {string} componentName - Name of the component (PascalCase)
 * @param {string} iconName - Name for the icon in IconSystem (kebab-case)
 */
function updateIconSystem(componentName, iconName) {
  const iconSystemPath = path.resolve('./src/components/IconSystem.vue');
  let iconSystemContent = fs.readFileSync(iconSystemPath, 'utf8');
  
  // Check if the icon is already registered
  if (iconSystemContent.includes(`'${iconName}':`)) {
    console.log(`⚠️ Icon '${iconName}' is already registered in IconSystem`);
    return;
  }
  
  // Add import statement
  const importStatement = `import ${componentName} from '@/components/icons/${componentName}.vue';`;
  const importRegex = /\/\/ Import all icon components directly[\s\S]*?\/\/ Add more icons as needed/;
  iconSystemContent = iconSystemContent.replace(
    importRegex, 
    match => `${match}\nimport ${componentName} from '@/components/icons/${componentName}.vue';`
  );
  
  // Add to iconMap - ensure proper comma placement
  const iconMapRegex = /const iconMap = \{[\s\S]*?([\s\S]*?)\/\/ Add more mappings as needed/;
  iconSystemContent = iconSystemContent.replace(
    iconMapRegex,
    (match, capturedContent) => {
      // Find the last entry without a trailing comma
      const lastEntry = capturedContent.trim().split('\n').pop().trim();
      
      // If the last entry doesn't end with a comma, add one
      // if (!lastEntry.endsWith(',')) {
      return match.replace(
        lastEntry + '\n  // Add more mappings as needed',
        lastEntry + `${lastEntry.endsWith(',') ? '' : ','}\n  \'${iconName}\': ${componentName},\n  // Add more mappings as needed`
      );
      // } else {
      //   // If it already has a comma, just add the new entry
      //   return `${match}\n  '${iconName}': ${componentName},`;
      // }
    }
  );
  
  // Write updated content back to file
  fs.writeFileSync(iconSystemPath, iconSystemContent);
}

/**
 * Example usage from command line:
 * node convertSvg.js /path/to/icon.svg IconName icon-name
 */
if (process.argv.length > 2) {
  const svgPath = process.argv[2];
  const componentName = process.argv[3] || path.basename(svgPath, '.svg').replace(/[^a-zA-Z0-9]/g, '') + 'Icon';
  const iconName = process.argv[4] || componentName.replace(/([A-Z])/g, '-$1').toLowerCase().replace(/^-/, '').replace(/-icon$/, '');
  
  convertAndRegisterSvg(svgPath, componentName, iconName)
    .then(result => {
      if (result.success) {
        console.log('✅ Conversion completed successfully!');
      } else {
        console.error('❌ Conversion failed:', result.error);
      }
    });
}

/**
 * Function to convert multiple SVGs at once
 * @param {Array<{path: string, componentName: string, iconName: string}>} svgList 
 */
export async function convertMultipleSvgs(svgList) {
  const results = [];
  
  for (const svg of svgList) {
    const result = await convertAndRegisterSvg(
      svg.path, 
      svg.componentName || path.basename(svg.path, '.svg').replace(/[^a-zA-Z0-9]/g, '') + 'Icon',
      svg.iconName || svg.componentName.replace(/([A-Z])/g, '-$1').toLowerCase().replace(/^-/, '').replace(/-icon$/, '')
    );
    results.push(result);
  }
  
  return results;
} 