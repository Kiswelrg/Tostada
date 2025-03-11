# SVG Icon System

This directory contains SVG icon components for use with the IconSystem component.

## Usage

```vue
<template>
  <IconSystem 
    name="plus" 
    color="white" 
    :size="16"
  />
</template>

<script setup>
import IconSystem from '@/components/IconSystem.vue';
</script>
```

## Available Icons

- `plus` - A plus icon
- `circle` - A circle icon
- Add more as needed

## Adding New Icons

1. Create a new Vue component in this directory
2. Use the following template:

```vue
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

3. Import and register the new icon in `IconSystem.vue`:

```js
// In IconSystem.vue
import NewIcon from '@/components/icons/NewIcon.vue';

// Add to iconMap
const iconMap = {
  // existing icons...
  'new-icon': NewIcon,
};
```

## Converting SVG Files to Components

1. Open the SVG file in a text editor
2. Copy the SVG path data
3. Create a new Vue component using the template above
4. Replace the path data with the copied data
5. Import and register the new icon in `IconSystem.vue`

## Customizing Icons

The IconSystem component accepts the following props:

- `name` (String, required): Name of the icon to display
- `color` (String, default: 'currentColor'): Color of the icon
- `size` (Number, default: 24): Size of the icon in pixels 