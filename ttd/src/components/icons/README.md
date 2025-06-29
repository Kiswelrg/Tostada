# SVG Icon System

This directory contains SVG icon components for use with the IconSystem component.

## Basic Usage

```vue
<IconSystem
  name="plus"
  color="blue"
  :size="24"
/>
```

## Using Tailwind CSS Classes for Color

```vue
<IconSystem
  name="plus"
  colorClass="text-interactive-normal"
  :size="24"
/>
```

## Component Registration

```javascript
import IconSystem from '@/components/IconSystem.vue';

export default {
  components: {
    IconSystem
  }
}
```

## Available Icons

- `plus` - A plus icon
- `circle` - A circle icon
- `invite` - An invite icon
- Add more as needed

## How Color Handling Works

The icon components handle colors in two ways:

1. **Direct color values**: When you set the `color` prop to a specific color value (e.g., "blue", "#FF0000"), the icon will use that color directly.

2. **Inherited colors**: When you set the `color` prop to "currentColor" (the default) or use the `colorClass` prop with a Tailwind CSS class, the icon will inherit its color from the parent element.

The `colorClass` prop takes precedence over the `color` prop. When `colorClass` is provided, the `color` prop is ignored.

## Adding New Icons

1. Create a new SVG icon component in this directory
2. Follow the pattern of existing icons
3. Import and register the new icon in `IconSystem.vue`:

```javascript
// In IconSystem.vue
import NewIcon from '@/components/icons/NewIcon.vue';

// Add to iconMap
const iconMap = {
  'plus': PlusIcon,
  'circle': CircleIcon,
  'invite': InviteIcon,
  'new-icon': NewIcon
};
```

```bash
# Automatic Registration:
npm run convert-svg path/to/icon.svg IconName icon-name ✅
npm run convert-all ✅
npm run unregister-icon icon-name ComponentName ✅
```

## Using the Conversion Utility

Alternatively, you can use the conversion utility to automatically create and register a new icon:

```bash
node src/utils/convertSvg.js path/to/icon.svg IconName
```

5. Import and register the new icon in `IconSystem.vue`

## Props

The IconSystem component accepts the following props:

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| name | String | required | Name of the icon to display |
| color | String | 'currentColor' | Direct color value for the icon |
| colorClass | String | '' | Tailwind CSS class for coloring (takes precedence over color) |
| size | Number | 24 | Size of the icon in pixels |

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