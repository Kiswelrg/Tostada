// Import all icon components
import PlusIcon from './PlusIcon.vue';
import CircleIcon from './CircleIcon.vue';
import MapPin from './MapPin.vue';
import ToggleCrossIcon from './ToggleCrossIcon.vue';
import ToggleCheckIcon from './ToggleCheckIcon.vue';
import InviteIcon from './InviteIcon.vue';
import SearchIcon from './SearchIcon.vue';
import CloseIcon from './CloseIcon.vue';
import ChevronDownIcon from './ChevronDownIcon.vue';
import MemberList from './MemberList.vue';

// Central icon registry - single source of truth
export const iconMap = {
  'plus': PlusIcon,
  'circle': CircleIcon,
  'invite': InviteIcon,
  'search': SearchIcon,
  'close': CloseIcon,
  'chevron-down': ChevronDownIcon,
  'toggle-check': ToggleCheckIcon,
  'toggle-cross': ToggleCrossIcon,
  'map-pin': MapPin,
  'member-list': MemberList,
  // Add more mappings as needed
};

// Helper function to get all available icon names
export const getAvailableIcons = () => Object.keys(iconMap);

// Helper function to check if an icon exists
export const hasIcon = (iconName) => iconName in iconMap;