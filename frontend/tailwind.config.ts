import type { Config } from 'tailwindcss';

const config: Config = {
    content: [
        './pages/**/*.{js,ts,jsx,tsx,mdx}',
        './components/**/*.{js,ts,jsx,tsx,mdx}',
        './app/**/*.{js,ts,jsx,tsx,mdx}',
    ],
    theme: {
        extend: {
            colors: {
                background: '#0a0a0f',
                surface: '#0d1117',
                'surface-2': '#161b22',
                border: 'rgba(255,255,255,0.08)',
                neon: '#00ff88',
                'neon-dim': '#00cc6a',
                purple: '#7c3aed',
                'purple-dim': '#5b21b6',
                danger: '#ff3232',
                warning: '#ffa500',
                muted: '#888888',
                'text-primary': '#e0e0e0',
                'text-secondary': '#aaaaaa',
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
                mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
            },
            backgroundImage: {
                'cyber-gradient': 'linear-gradient(135deg, #0a0a0f 0%, #0d1117 50%, #0a0f0a 100%)',
                'neon-gradient': 'linear-gradient(135deg, #00ff88, #00cc6a)',
                'purple-gradient': 'linear-gradient(135deg, #7c3aed, #5b21b6)',
                'card-gradient': 'linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01))',
            },
            boxShadow: {
                neon: '0 0 20px rgba(0, 255, 136, 0.3)',
                'neon-lg': '0 0 40px rgba(0, 255, 136, 0.2)',
                purple: '0 0 20px rgba(124, 58, 237, 0.3)',
                glass: '0 8px 32px rgba(0, 0, 0, 0.4)',
            },
            animation: {
                'pulse-neon': 'pulse-neon 2s ease-in-out infinite',
                'float': 'float 3s ease-in-out infinite',
                'glow': 'glow 2s ease-in-out infinite alternate',
                'shimmer': 'shimmer 2s linear infinite',
                'fade-in': 'fade-in 0.5s ease-out',
                'slide-up': 'slide-up 0.4s ease-out',
            },
            keyframes: {
                'pulse-neon': {
                    '0%, 100%': { opacity: '1' },
                    '50%': { opacity: '0.5' },
                },
                'float': {
                    '0%, 100%': { transform: 'translateY(0px)' },
                    '50%': { transform: 'translateY(-10px)' },
                },
                'glow': {
                    '0%': { boxShadow: '0 0 10px rgba(0, 255, 136, 0.2)' },
                    '100%': { boxShadow: '0 0 30px rgba(0, 255, 136, 0.5)' },
                },
                'shimmer': {
                    '0%': { backgroundPosition: '-1000px 0' },
                    '100%': { backgroundPosition: '1000px 0' },
                },
                'fade-in': {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                'slide-up': {
                    '0%': { opacity: '0', transform: 'translateY(20px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
            },
        },
    },
    plugins: [],
};

export default config;
