import type { Metadata } from 'next';
import { Providers } from './providers';
import Header from '@/components/layout/Header';
import Footer from '@/components/layout/Footer';
import './globals.css';

export const metadata: Metadata = {
    title: 'Anti-Gravity Bug Bounty | AI-Powered Decentralized Platform',
    description: 'Submit and track security vulnerabilities on the AI-driven decentralized bug bounty platform. On-chain payments, reputation system, and OWASP classification.',
    keywords: ['bug bounty', 'web3', 'security', 'blockchain', 'AI triage', 'polygon'],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en" suppressHydrationWarning>
            <head>
                <link rel="preconnect" href="https://fonts.googleapis.com" />
                <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
            </head>
            <body className="bg-background text-text-primary antialiased">
                <Providers>
                    <Header />
                    <main className="min-h-screen pt-16">
                        {children}
                    </main>
                    <Footer />
                </Providers>
            </body>
        </html>
    );
}
