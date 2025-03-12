/**
 * Utility function to convert an SVG string to a Vue component template
 * This can be used to process SVG files and convert them to Vue components
 * 
 * @param {string} svgString - The SVG content as a string
 * @returns {string} - Vue component template string
 */
export function svgToVueComponent(svgString) {
  // Extract the SVG content
  const svgContent = svgString.match(/<svg[^>]*>([\s\S]*?)<\/svg>/i);
  
  if (!svgContent) {
    throw new Error('Invalid SVG content');
  }
  
  // Extract viewBox and other attributes from the original SVG
  const viewBoxMatch = svgString.match(/viewBox=["']([^"']*)["']/i);
  const viewBox = viewBoxMatch ? viewBoxMatch[1] : '0 0 24 24';
  
  // Create the Vue component template
  let template = `<template>
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    viewBox="${viewBox}"
    width="100%"
    height="100%"
  >
`;

  // Process the inner content of the SVG
  let innerContent = svgContent[1];
  
  // If colorizable, replace fill attributes with dynamic binding
  if (true) {
    // Replace fill attributes with dynamic binding
    innerContent = innerContent.replace(/fill=["'][^"']*["']/gi, ':fill="fill"');
    
    // If no fill attribute exists, add it to path elements
    if (!innerContent.includes(':fill="fill"')) {
      innerContent = innerContent.replace(/<path/gi, '<path :fill="fill"');
    }
  }
  
  template += `    ${innerContent}\n  </svg>\n</template>`;
  
  // Add script section if colorizable
  
    template += `\n
<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  color: {
    type: String,
    default: 'currentColor'
  }
});

const inheritedColor = ref('currentColor');

// The fill color is either the explicitly provided color prop
// or the inherited color from the parent element
const fill = computed(() => {
  return props.color !== 'currentColor' ? props.color : inheritedColor.value;
});

</script>`;
  
  
  return template;
}

/**
 * Example usage:
 * 
 * // Read an SVG file
 * const svgContent = fs.readFileSync('path/to/icon.svg', 'utf8');
 * 
 * // Convert to Vue component
 * const vueComponent = svgToVueComponent(svgContent);
 * 
 * // Write to a .vue file
 * fs.writeFileSync('path/to/IconComponent.vue', vueComponent);
 */ 