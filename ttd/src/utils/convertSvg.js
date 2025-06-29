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
    
    // 4. Update iconRegistry.js to register the new icon
    updateIconRegistry(componentName, iconName);
    console.log(`✅ Registered icon '${iconName}' in icon registry`);
    
    return { success: true, componentPath: outputPath };
  } catch (error) {
    console.error('Error converting SVG:', error);
    return { success: false, error };
  }
}

/**
 * Updates iconRegistry.js to register a new icon
 * @param {string} componentName - Name of the component (PascalCase)
 * @param {string} iconName - Name for the icon in iconRegistry (kebab-case)
 */
function updateIconRegistry(componentName, iconName) {
  const iconRegistryPath = path.resolve('./src/components/icons/iconRegistry.js');
  let iconRegistryContent = fs.readFileSync(iconRegistryPath, 'utf8');
  
  // Check if the icon is already registered
  if (iconRegistryContent.includes(`'${iconName}':`)) {
    console.log(`⚠️ Icon '${iconName}' is already registered in icon registry`);
    return;
  }
  
  // Add import statement at the top
  const importStatement = `import ${componentName} from './${componentName}.vue';`;
  const importSection = iconRegistryContent.match(/(\/\/ Import all icon components[\s\S]*?)(?=\n\n|\/\/ Central icon registry)/);
  
  if (importSection) {
    iconRegistryContent = iconRegistryContent.replace(
      importSection[1],
      `${importSection[1]}\n${importStatement}`
    );
  } else {
    // Add import after the last import statement
    const lastImportMatch = iconRegistryContent.match(/import\s+\w+\s+from\s+['"]\.\/.+\.vue['"];/g);
    if (lastImportMatch) {
      const lastImport = lastImportMatch[lastImportMatch.length - 1];
      iconRegistryContent = iconRegistryContent.replace(
        lastImport,
        `${lastImport}\n${importStatement}`
      );
    }
  }
  
  // Add to iconMap - find the position just before the closing brace and comment
  const iconMapRegex = /(export const iconMap = \{[\s\S]*?)(  \/\/ Add more mappings as needed[\s\S]*?\};)/;
  iconRegistryContent = iconRegistryContent.replace(
    iconMapRegex,
    `$1  '${iconName}': ${componentName},\n$2`
  );
  
  // Write updated content back to file
  fs.writeFileSync(iconRegistryPath, iconRegistryContent);
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