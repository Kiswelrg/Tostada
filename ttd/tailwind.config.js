/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./**/*.{vue,js}"
  ],
  theme: {
    fontSize: {
      '1s': ['10px', '14px'],
      '2s': ['8px', '12px'],
    },
    colors: {
      'white': '#ffffff',
      'hui': {
        700: '#404249',
        800: '#81848e',
      }
    },
    minHeight: {
      '10': '40px',
    },
    extend: {},
  },
  plugins: [],
}

