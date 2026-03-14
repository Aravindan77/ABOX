'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { LayoutDashboard, Bug, FolderOpen, Trophy, Settings, ChevronLeft, ChevronRight } from 'lucide-react';
import { useState } from 'react';

const items = [
    { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/projects', label: 'Programs', icon: FolderOpen },
    { href: '/submit', label: 'Submit Bug', icon: Bug },
    { href: '/leaderboard', label: 'Leaderboard', icon: Trophy },
    { href: '/dashboard?tab=settings', label: 'Settings', icon: Settings },
];

export default function Sidebar() {
    const pathname = usePathname();
    const [collapsed, setCollapsed] = useState(false);

    return (
        <aside
            className={cn(
                'fixed top-16 left-0 h-[calc(100vh-64px)] z-40 transition-all duration-300 flex flex-col',
                collapsed ? 'w-16' : 'w-56',
            )}
            style={{ background: 'rgba(13,17,23,0.95)', borderRight: '1px solid rgba(255,255,255,0.06)', backdropFilter: 'blur(12px)' }}
        >
            <nav className="flex flex-col gap-1 p-3 flex-1">
                {items.map(({ href, label, icon: Icon }) => {
                    const active = pathname === href || pathname.startsWith(href + '/');
                    return (
                        <Link
                            key={href}
                            href={href}
                            className={cn(
                                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200',
                                active ? 'text-neon bg-neon/10 border border-neon/20' : 'text-text-secondary hover:text-text-primary hover:bg-white/5',
                            )}
                        >
                            <Icon className="w-4 h-4 flex-shrink-0" />
                            {!collapsed && <span>{label}</span>}
                        </Link>
                    );
                })}
            </nav>

            <button
                onClick={() => setCollapsed(!collapsed)}
                className="flex items-center justify-center p-4 text-muted hover:text-text-primary border-t border-white/5 transition-colors"
            >
                {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
            </button>
        </aside>
    );
}
