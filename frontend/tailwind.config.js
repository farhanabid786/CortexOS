/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        darkBg: '#090a0f',
        lightBg: '#f8fafc',
        glassBg: 'rgba(13, 16, 27, 0.45)',
        glassBorder: 'rgba(255, 255, 255, 0.08)',
        neonCyan: '#00f2fe',
        neonPurple: '#4facfe',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin-slow': 'spin 12s linear infinite',
      }
    },
  },
  plugins: [],
}
