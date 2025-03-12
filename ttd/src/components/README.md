# SVG Icon System

This directory contains components for working with SVG icons in the application.

## Components

### SvgIcon

A reusable component for displaying SVG icons with customizable colors and sizes.

#### Usage

2 usages examples at [README.md](./icons/README.md).


#### Props

- `icon` (String, required): Path to the SVG component relative to the assets directory
- `color` (String, default: 'currentColor'): Color of the SVG icon
- `size` (Number, default: 24): Size of the icon in pixels

## Creating SVG Components

### Method 1: Manual Creation

1. Create a new `.vue` file in the `src/assets` directory
2. Use the following template:

```vue
<template>
  <svg 
    ref="svg"
    xmlns="http://www.w3.org/2000/svg" 
    viewBox="0 0 24 24"
    width="100%"
    height="100%"
  >
    <path 
      :fill="fill" 
      d="..." /> <!-- SVG path data here -->
  </svg>
</template>

<script setup>
import { ref, watch } from 'vue';

const svg = ref(null);
const fill = ref('currentColor');

// Watch for changes to the SVG element
watch(svg, (newValue) => {
  if (newValue) {
    // Get the computed color from the parent element
    const computedStyle = window.getComputedStyle(newValue);
    fill.value = computedStyle.color;
  }
}, { immediate: true });
</script>
```

### Method 2: Using the Utility Function

You can use the `svgToVueComponent` utility function to convert SVG files to Vue components:

```js
import { svgToVueComponent } from '@/utils/svgToComponent';
import fs from 'fs';

// Read an SVG file
const svgContent = fs.readFileSync('path/to/icon.svg', 'utf8');

// Convert to Vue component
const vueComponent = svgToVueComponent(svgContent);

// Write to a .vue file
fs.writeFileSync('path/to/IconComponent.vue', vueComponent);
```

## Alternative Method: CSS Filters

For static color changes, you can also use CSS filters:

```css
.svg-icon {
  filter: invert(100%) sepia(3%) saturate(7453%) hue-rotate(138deg) brightness(111%) contrast(104%);
}
```

This method is useful for simple color changes but less flexible than the component approach for dynamic colors.

## Example

See `IconExample.vue` for a complete example of how to use the SVG icon system with different colors and sizes. 