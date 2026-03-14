import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

export function formatAddress(address: string, chars = 4): string {
    if (!address) return '';
    return `${address.slice(0, chars + 2)}...${address.slice(-chars)}`;
}

export function formatDate(dateStr: string): string {
    return new Date(dateStr).toLocaleDateString('en-US', {
        year: 'numeric', month: 'short', day: 'numeric',
    });
}

export function formatCurrency(amount: number): string {
    if (amount >= 1000) return `$${(amount / 1000).toFixed(1)}k`;
    return `$${amount.toLocaleString()}`;
}

export function formatMATIC(amount: number): string {
    return `${amount.toFixed(2)} MATIC`;
}

export const SEVERITY_CONFIG = {
    critical: { label: 'Critical', color: '#ff3232', bg: 'rgba(255,50,50,0.15)', border: 'rgba(255,50,50,0.3)' },
    high: { label: 'High', color: '#ff8c00', bg: 'rgba(255,140,0,0.15)', border: 'rgba(255,140,0,0.3)' },
    medium: { label: 'Medium', color: '#ffa500', bg: 'rgba(255,165,0,0.15)', border: 'rgba(255,165,0,0.3)' },
    low: { label: 'Low', color: '#00ff88', bg: 'rgba(0,255,136,0.1)', border: 'rgba(0,255,136,0.25)' },
} as const;

export const STATUS_CONFIG = {
    pending: { label: 'Pending', color: '#888', bg: 'rgba(136,136,136,0.1)' },
    ai_reviewing: { label: 'AI Review', color: '#7c3aed', bg: 'rgba(124,58,237,0.15)' },
    needs_review: { label: 'Under Review', color: '#ffa500', bg: 'rgba(255,165,0,0.1)' },
    accepted: { label: 'Accepted', color: '#00ff88', bg: 'rgba(0,255,136,0.1)' },
    rejected: { label: 'Rejected', color: '#ff3232', bg: 'rgba(255,50,50,0.1)' },
    paid: { label: 'Paid ✓', color: '#00ff88', bg: 'rgba(0,255,136,0.15)' },
} as const;

export const TIER_CONFIG = {
    novice: { label: 'Novice', color: '#888', min: 0, icon: '🔰' },
    hunter: { label: 'Hunter', color: '#00ccff', min: 30, icon: '🎯' },
    expert: { label: 'Expert', color: '#7c3aed', min: 60, icon: '⚡' },
    elite: { label: 'Elite', color: '#ffa500', min: 80, icon: '🔥' },
    legend: { label: 'Legend', color: '#00ff88', min: 95, icon: '👑' },
} as const;

export const TRIAGE_STATUS_CONFIG = {
    HIGH_PRIORITY: { label: 'High Priority', icon: '🚨', color: '#00ff88', bg: 'rgba(0,255,136,0.1)', border: 'rgba(0,255,136,0.3)' },
    NEEDS_REVIEW: { label: 'Needs Review', icon: '🔍', color: '#ffa500', bg: 'rgba(255,165,0,0.08)', border: 'rgba(255,165,0,0.3)' },
    REJECTED_SPAM: { label: 'Rejected', icon: '🚫', color: '#ff3232', bg: 'rgba(255,50,50,0.08)', border: 'rgba(255,50,50,0.3)' },
} as const;
