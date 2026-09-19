/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          500: '#1a365d',
          600: '#152c4a',
          900: '#0f1f38'
        },
        electric: {
          500: '#2563eb',
          600: '#1d4ed8'
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
