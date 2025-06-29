import fs from 'fs';
import path from 'path';

/**
 * Unregisters an icon from iconRegistry and removes the component file
 * @param {string} iconName - Name of the icon in iconRegistry (kebab-case)
 * @param {string} componentName - Name of the component (PascalCase)
 * @returns {Object} Result of the operation
 */
export function unregisterIcon(iconName, componentName) {
  try {
    const iconRegistryPath = path.resolve('./src/components/icons/iconRegistry.js');
    const componentPath = path.resolve('./src/components/icons', `${componentName}.vue`);
    
    // Check if the component file exists
    if (!fs.existsSync(componentPath)) {
      console.error(`❌ Component file not found: ${componentPath}`);
      return { success: false, error: 'Component file not found' };
    }
    
    // Read iconRegistry.js content
    let iconRegistryContent = fs.readFileSync(iconRegistryPath, 'utf8');
    
    // Check if the icon is registered in iconMap
    const iconMapRegex = new RegExp(`'${iconName}':\\s*${componentName},?`);
    if (!iconMapRegex.test(iconRegistryContent)) {
      console.error(`❌ Icon '${iconName}' is not registered in icon registry`);
      return { success: false, error: 'Icon not registered in icon registry' };
    }
    
    // Remove from iconMap
    iconRegistryContent = iconRegistryContent.replace(
      new RegExp(`\\s*'${iconName}':\\s*${componentName},?`), 
      ''
    );
    
    // Clean up trailing commas in iconMap if needed
    iconRegistryContent = iconRegistryContent.replace(
      /,(\s*\/\/ Add more mappings as needed)/g, 
      '$1'
    );
    
    // Remove import statement
    const importRegex = new RegExp(`\\s*import\\s+${componentName}\\s+from\\s+['"]\\./${componentName}\\.vue['"];?`);
    iconRegistryContent = iconRegistryContent.replace(importRegex, '');
    
    // Write updated content back to file
    fs.writeFileSync(iconRegistryPath, iconRegistryContent);
    console.log(`✅ Unregistered icon '${iconName}' from icon registry`);
    
    // Delete the component file
    fs.unlinkSync(componentPath);
    console.log(`✅ Deleted component file: ${componentPath}`);
    
    return { success: true };
  } catch (error) {
    console.error('Error unregistering icon:', error);
    return { success: false, error };
  }
}

/**
 * Example usage from command line:
 * node unregisterIcon.js icon-name ComponentName
 */
if (process.argv.length > 2) {
  const iconName = process.argv[2];
  const componentName = process.argv[3];
  
  if (!componentName) {
    console.error('❌ Both iconName and componentName are required');
    process.exit(1);
  }
  
  const result = unregisterIcon(iconName, componentName);
  if (result.success) {
    console.log('✅ Icon unregistered successfully!');
  } else {
    console.error('❌ Failed to unregister icon:', result.error);
    process.exit(1);
  }
} 