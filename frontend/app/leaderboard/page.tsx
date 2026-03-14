import { getLeaderboard } from '@/lib/api';
import { TIER_CONFIG, formatAddress, formatCurrency } from '@/lib/utils';
import TrustScoreBadge from '@/components/reputation/TrustScoreBadge';
import { Trophy, Bug, DollarSign } from 'lucide-react';

export const metadata = { title: 'Leaderboard | Anti-Gravity Bug Bounty' };

export default async function LeaderboardPage() {
    const leaders = await getLeaderboard();
    const top3 = leaders.slice(0, 3);
    const rest = leaders.slice(3);

    return (
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div className="text-center mb-12">
                <h1 className="text-3xl font-bold text-text-primary mb-2">🏆 Leaderboard</h1>
                <p className="text-text-secondary text-sm">Top security researchers ranked by trust score</p>
            </div>

            {/* Top 3 Podium */}
            <div className="flex items-end justify-center gap-3 mb-10">
                {[top3[1], top3[0], top3[2]].map((entry, i) => {
                    if (!entry) return null;
                    const height = i === 1 ? 'h-36' : 'h-24';
                    const tierCfg = TIER_CONFIG[entry.tier];
                    return (
                        <div key={entry.rank} className={`flex flex-col items-center gap-3 ${i === 1 ? 'order-2' : i === 0 ? 'order-1' : 'order-3'}`}>
                            <TrustScoreBadge score={entry.trust_score} tier={entry.tier} size={i === 1 ? 'md' : 'sm'} />
                            <div className={`${height} w-24 glass-neon rounded-t-xl flex flex-col items-center justify-center gap-1 relative`}
                                style={{ border: `1px solid ${tierCfg.color}30` }}>
                                <span className="text-2xl">{i === 1 ? '🥇' : i === 0 ? '🥈' : '🥉'}</span>
                                <span className="text-xs font-mono text-text-secondary">{formatAddress(entry.address)}</span>
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Full table */}
            <div className="glass border border-border rounded-xl overflow-hidden">
                <div className="grid grid-cols-6 gap-4 px-5 py-3 border-b border-border text-xs font-semibold text-muted uppercase tracking-wide">
                    <span>Rank</span>
                    <span className="col-span-2">Researcher</span>
                    <span>Score</span>
                    <span className="flex items-center gap-1"><Bug className="w-3 h-3" /> Bugs</span>
                    <span className="flex items-center gap-1"><DollarSign className="w-3 h-3" /> Earned</span>
                </div>

                {leaders.map((entry, idx) => {
                    const tierCfg = TIER_CONFIG[entry.tier];
                    return (
                        <div key={entry.rank}
                            className="grid grid-cols-6 gap-4 px-5 py-4 border-b border-border/50 last:border-0 hover:bg-white/2 transition-colors"
                        >
                            <span className="text-sm font-bold" style={{ color: entry.rank <= 3 ? tierCfg.color : '#888' }}>
                                #{entry.rank}
                            </span>
                            <div className="col-span-2 flex items-center gap-2">
                                <div className="w-7 h-7 rounded-full glass flex items-center justify-center text-xs">{tierCfg.icon}</div>
                                <div>
                                    <p className="text-xs font-mono text-text-primary">{formatAddress(entry.address)}</p>
                                    <p className="text-xs" style={{ color: tierCfg.color }}>{tierCfg.label}</p>
                                </div>
                            </div>
                            <span className="text-sm font-bold" style={{ color: tierCfg.color }}>{entry.trust_score}</span>
                            <span className="text-sm text-text-secondary">{entry.accepted_bugs}</span>
                            <span className="text-sm text-neon font-medium">{formatCurrency(entry.total_earnings)}</span>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
