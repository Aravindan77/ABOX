/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    async rewrites() {
        return [
            {
                source: '/api/backend/:path*',
                destination: 'http://localhost:8000/api/v1/:path*',
            },
        ];
    },
    images: {
        domains: ['ipfs.io', 'gateway.pinata.cloud'],
    },
};

module.exports = nextConfig;
