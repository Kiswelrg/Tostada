# SVG Conversion Utilities

This directory contains utilities for converting SVG files to Vue components and registering them in the IconSystem.

## Available Scripts

### `npm run convert-svg <path> [componentName] [iconName]`

Converts a single SVG file to a Vue component and registers it in the IconSystem.

```bash
# Example: Convert an SVG file
npm run convert-svg ./public/static/tool/ToolList/Invite.svg InviteIcon invite
```

### `npm run convert-invite`

Converts the Invite.svg file to a Vue component and registers it in the IconSystem.

```bash
# Example: Convert the Invite.svg file
npm run convert-invite
```

### `npm run convert-all`

Converts all SVG files in the public/static/tool directory to Vue components and registers them in the IconSystem.

```bash
# Example: Convert all SVG files
npm run convert-all
```

## How It Works

1. The `svgToComponent.js` utility converts an SVG string to a Vue component template.
2. The `convertSvg.js` utility reads an SVG file, converts it to a Vue component, and registers it in the IconSystem.
3. The `convertInviteIcon.js` utility is a specific script for converting the Invite.svg file.
4. The `convertAllIcons.js` utility recursively finds all SVG files in a directory and converts them to Vue components.

## Manual Conversion

If you prefer to manually convert an SVG file:

1. Open the SVG file in a text editor
2. Create a new Vue component in the `src/components/icons` directory
3. Copy the SVG path data into the component
4. Update the IconSystem.vue file to import and register the new icon

## Example

```vue
<!-- src/components/icons/MyIcon.vue -->
<template>
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    viewBox="0 0 24 24"
    width="100%"
    height="100%"
  >
    <path 
      :fill="color" 
      d="..." /> <!-- SVG path data here -->
  </svg>
</template>

<script setup>
defineProps({
  color: {
    type: String,
    default: 'currentColor'
  }
});
</script>
```

Then update the IconSystem.vue file:

```js
// In IconSystem.vue
import MyIcon from '@/components/icons/MyIcon.vue';

// Add to iconMap
const iconMap = {
  // existing icons...
  'my-icon': MyIcon,
};
```

And use it in your components:

```vue
<IconSystem 
  name="my-icon" 
  color="white" 
  :size="16"
/>
``` 