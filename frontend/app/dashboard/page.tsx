'use client';

import { useAccount } from 'wagmi';
import TrustScoreBadge from '@/components/reputation/TrustScoreBadge';
import { formatAddress, formatCurrency } from '@/lib/utils';
import { Bug, DollarSign, CheckCircle, Clock, Shield, Wallet } from 'lucide-react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

const MOCK_STATS = {
    trust_score: 72, tier: 'expert' as const, total_submissions: 14, accepted_bugs: 9,
    rejected_bugs: 3, total_earnings: 28500, rank: 5,
};

const MOCK_RECENT = [
    { id: '1', title: 'SQL Injection in login endpoint', status: 'accepted', severity: 'high', confidence: 91, date: '2025-02-28' },
    { id: '2', title: 'XSS in user profile bio', status: 'needs_review', severity: 'medium', confidence: 73, date: '2025-02-25' },
    { id: '3', title: 'JWT missing expiry', status: 'accepted', severity: 'high', confidence: 86, date: '2025-02-20' },
    { id: '4', title: 'SSRF via avatar URL', status: 'pending', severity: 'critical', confidence: 68, date: '2025-02-15' },
];

const STATUS_MAP: Record<string, { label: string; color: string }> = {
    accepted: { label: 'Accepted', color: '#00ff88' },
    needs_review: { label: 'Under Review', color: '#ffa500' },
    pending: { label: 'Pending', color: '#888' },
    rejected: { label: 'Rejected', color: '#ff3232' },
};
const SEV_MAP: Record<string, string> = { critical: '#ff3232', high: '#ff8c00', medium: '#ffa500', low: '#00ff88' };

export default function DashboardPage() {
    const { address, isConnected } = useAccount();

    if (!isConnected) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[calc(100vh-160px)] gap-6 px-4">
                <div className="w-16 h-16 rounded-2xl glass-neon flex items-center justify-center animate-float">
                    <Wallet className="w-8 h-8 text-neon" />
                </div>
                <div className="text-center">
                    <h2 className="text-2xl font-bold text-text-primary mb-2">Connect Your Wallet</h2>
                    <p className="text-text-secondary text-sm max-w-sm">Connect your Web3 wallet to view your dashboard, track submissions, and see your reputation score.</p>
                </div>
                <Link href="/submit"><Button variant="neon">Get Started <Bug className="w-4 h-4" /></Button></Link>
            </div>
        );
    }

    const stats = MOCK_STATS;

    return (
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            {/* Welcome */}
            <div className="flex items-start gap-4 mb-8">
                <div>
                    <h1 className="text-2xl font-bold text-text-primary">Welcome back 👋</h1>
                    <p className="text-sm font-mono text-muted mt-1">{formatAddress(address || '', 6)}</p>
                </div>
                <div className="ml-auto">
                    <Link href="/submit"><Button variant="neon" size="sm"><Bug className="w-4 h-4" /> Submit Bug</Button></Link>
                </div>
            </div>

            {/* Stats row */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
                {[
                    { icon: Bug, label: 'Total Submissions', value: stats.total_submissions, color: '#7c3aed' },
                    { icon: CheckCircle, label: 'Accepted', value: stats.accepted_bugs, color: '#00ff88' },
                    { icon: DollarSign, label: 'Total Earned', value: formatCurrency(stats.total_earnings), color: '#00ff88' },
                    { icon: Shield, label: 'Global Rank', value: `#${stats.rank}`, color: '#ffa500' },
                ].map(({ icon: Icon, label, value, color }) => (
                    <div key={label} className="glass border border-border rounded-xl p-4">
                        <div className="flex items-center gap-2 mb-2">
                            <Icon className="w-4 h-4" style={{ color }} />
                            <span className="text-xs text-muted">{label}</span>
                        </div>
                        <p className="text-xl font-bold" style={{ color }}>{value}</p>
                    </div>
                ))}
            </div>

            {/* Main grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Recent submissions */}
                <div className="lg:col-span-2 glass border border-border rounded-xl p-5">
                    <h2 className="text-sm font-semibold text-text-primary mb-4 flex items-center gap-2">
                        <Clock className="w-4 h-4 text-muted" /> Recent Submissions
                    </h2>
                    <div className="flex flex-col gap-2">
                        {MOCK_RECENT.map(bug => {
                            const s = STATUS_MAP[bug.status];
                            return (
                                <div key={bug.id} className="flex items-center gap-3 px-3 py-3 rounded-lg hover:bg-white/3 transition-colors border border-transparent hover:border-border">
                                    <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ background: SEV_MAP[bug.severity] }} />
                                    <div className="flex-1 min-w-0">
                                        <p className="text-xs font-medium text-text-primary truncate">{bug.title}</p>
                                        <p className="text-xs text-muted">{bug.date}</p>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <span className="text-xs font-mono text-muted">{bug.confidence}%</span>
                                        <span className="text-xs font-semibold px-2 py-0.5 rounded-full" style={{ color: s.color, background: `${s.color}18` }}>{s.label}</span>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>

                {/* Reputation card */}
                <div className="flex flex-col gap-4">
                    <div className="glass-neon rounded-xl p-5 flex flex-col items-center gap-4">
                        <TrustScoreBadge score={stats.trust_score} tier={stats.tier} size="lg" />
                        <div className="w-full grid grid-cols-2 gap-2 mt-2">
                            {[
                                { label: 'Accepted', value: stats.accepted_bugs },
                                { label: 'Rejected', value: stats.rejected_bugs },
                                { label: 'Rank', value: `#${stats.rank}` },
                                { label: 'Earnings', value: formatCurrency(stats.total_earnings) },
                            ].map(({ label, value }) => (
                                <div key={label} className="glass rounded-lg px-3 py-2 text-center">
                                    <p className="text-xs text-muted">{label}</p>
                                    <p className="text-sm font-bold text-text-primary">{value}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                    <Link href="/submit" className="w-full">
                        <Button variant="outline" className="w-full"><Bug className="w-4 h-4" /> New Submission</Button>
                    </Link>
                </div>
            </div>
        </div>
    );
}
