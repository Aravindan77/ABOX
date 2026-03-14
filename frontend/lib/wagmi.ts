'use client';

import { getDefaultConfig } from '@rainbow-me/rainbowkit';
import { polygon, polygonMumbai } from 'wagmi/chains';
import { http } from 'wagmi';

export const wagmiConfig = getDefaultConfig({
    appName: 'Anti-Gravity Bug Bounty',
    projectId: process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID || 'demo-project-id',
    chains: [polygonMumbai, polygon],
    transports: {
        [polygonMumbai.id]: http(),
        [polygon.id]: http(),
    },
    ssr: true,
});
