/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#7C3AED',
        secondary: '#A78BFA',
        cta: '#F97316',
        bgLight: '#FAF5FF',
        textDark: '#4C1D95',
        // Neo-Brutalism x Glassmorphism colors
        'space-purple': '#0F0518',
        'electric-purple': '#A855F7',
        'fluorescent-cyan': '#22D3EE',
      },
      fontFamily: {
        heading: ['Inter', 'Fira Code', 'monospace'],
        body: ['Inter', 'Fira Sans', 'sans-serif'],
      },
      animation: {
        'aurora': 'aurora 20s ease-in-out infinite',
        'aurora-slow': 'aurora-slow 30s ease-in-out infinite',
        'count-up': 'count-up 2s ease-out',
      },
      keyframes: {
        aurora: {
          '0%, 100%': { transform: 'translate(0, 0) scale(1)' },
          '33%': { transform: 'translate(30px, -30px) scale(1.1)' },
          '66%': { transform: 'translate(-20px, 20px) scale(0.9)' },
        },
        'aurora-slow': {
          '0%, 100%': { transform: 'translate(0, 0) rotate(0deg)' },
          '50%': { transform: 'translate(50px, 50px) rotate(5deg)' },
        },
        'count-up': {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}
