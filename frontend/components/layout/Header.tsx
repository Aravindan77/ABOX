'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ConnectButton } from '@rainbow-me/rainbowkit';
import { cn } from '@/lib/utils';
import { Shield, Bug, Trophy, LayoutDashboard, FolderOpen, Menu, X } from 'lucide-react';
import { useState } from 'react';

const navLinks = [
    { href: '/projects', label: 'Programs', icon: FolderOpen },
    { href: '/submit', label: 'Submit Bug', icon: Bug },
    { href: '/leaderboard', label: 'Leaderboard', icon: Trophy },
    { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
];

export default function Header() {
    const pathname = usePathname();
    const [mobileOpen, setMobileOpen] = useState(false);

    return (
        <header className="fixed top-0 left-0 right-0 z-50" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)', backdropFilter: 'blur(20px)', backgroundColor: 'rgba(10,10,15,0.85)' }}>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    {/* Logo */}
                    <Link href="/" className="flex items-center gap-2.5 group">
                        <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ background: 'linear-gradient(135deg, #00ff88, #00cc6a)' }}>
                            <Shield className="w-4 h-4 text-black" strokeWidth={2.5} />
                        </div>
                        <span className="font-bold text-base tracking-tight">
                            <span className="text-gradient-neon">Anti</span>
                            <span className="text-text-primary">Gravity</span>
                        </span>
                    </Link>

                    {/* Desktop nav */}
                    <nav className="hidden md:flex items-center gap-1">
                        {navLinks.map(({ href, label }) => (
                            <Link
                                key={href}
                                href={href}
                                className={cn(
                                    'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200',
                                    pathname === href
                                        ? 'text-neon bg-neon/10 border border-neon/20'
                                        : 'text-text-secondary hover:text-text-primary hover:bg-white/5'
                                )}
                            >
                                {label}
                            </Link>
                        ))}
                    </nav>

                    {/* Right side */}
                    <div className="flex items-center gap-3">
                        <ConnectButton
                            accountStatus="avatar"
                            chainStatus="icon"
                            showBalance={false}
                        />
                        {/* Mobile menu toggle */}
                        <button
                            className="md:hidden p-2 text-text-secondary hover:text-text-primary"
                            onClick={() => setMobileOpen(!mobileOpen)}
                        >
                            {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile nav */}
            {mobileOpen && (
                <div className="md:hidden border-t border-white/5 bg-surface/95 backdrop-blur-lg">
                    <nav className="flex flex-col gap-1 p-4">
                        {navLinks.map(({ href, label, icon: Icon }) => (
                            <Link
                                key={href}
                                href={href}
                                onClick={() => setMobileOpen(false)}
                                className={cn(
                                    'flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all',
                                    pathname === href
                                        ? 'text-neon bg-neon/10 border border-neon/20'
                                        : 'text-text-secondary hover:text-text-primary hover:bg-white/5'
                                )}
                            >
                                <Icon className="w-4 h-4" />
                                {label}
                            </Link>
                        ))}
                    </nav>
                </div>
            )}
        </header>
    );
}
