/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./**/*.{vue,js}"
  ],
  theme: {
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

