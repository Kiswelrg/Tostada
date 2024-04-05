/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./**/*.{vue,js}"
  ],
  theme: {
    fontSize: {
      // 'base': ['13px', '16px'],
      '1s': ['10px', '14px'],
      '2s': ['8px', '12px'],
      '3s': ['14px', '24px'],
      '625': ['.625rem', '1rem'],
    },
    colors: {
      'text-muted': 'hsl( 214 calc( 1 * 8.1%) 61.2% / 1)',
      'msgbutton':{
        'primary': 'hsl( 223 calc( 1 * 6.7%) 20.6% / 1)',
        'hover': '#393c41',
      },
      'interactive-normal': 'hsl( 215 calc( 1 * 8.8%) 73.3% / 1)',
      'fclist': {
        'bg': '#1e1f22',
      },
      'serverpanel': {
        'bg': '#2b2d31',
      },
      'tooldetail': {
        'bg': '#313338',
      },
      'userbar': {
        'bg': '#232428',
        'hoverbg': '#3d3e45',
      },
      'white': '#ffffff',
      'black': '#000000',
      'delimeter': {
        'toolhead': '#3f4147',
        'serverpanel': '#2b2d31',
      },
      'hui': {
        700: '#404249',
        800: '#81848e',
      },
      extend: {
        colors: {
          my_color: '#4dcb7a',
        },
      },
    },
    minHeight: {
      '10': '40px',
    },
    extend: {
      flex: {
        'zero': '0 1 0%',
        'zauto': '0 0 auto',
      }
    },
  },
  plugins: [
  ],
}

