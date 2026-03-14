import { TIER_CONFIG } from '@/lib/utils';
import type { ReputationTier } from '@/types/user';

interface TrustScoreBadgeProps {
    score: number;
    tier: ReputationTier;
    size?: 'sm' | 'md' | 'lg';
}

export default function TrustScoreBadge({ score, tier, size = 'md' }: TrustScoreBadgeProps) {
    const cfg = TIER_CONFIG[tier];
    const sizes = { sm: 56, md: 80, lg: 120 };
    const dim = sizes[size];
    const radius = (dim / 2) - 8;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (score / 100) * circumference;

    return (
        <div className="flex flex-col items-center gap-2">
            <div className="relative" style={{ width: dim, height: dim }}>
                <svg width={dim} height={dim} className="-rotate-90">
                    <circle cx={dim / 2} cy={dim / 2} r={radius} fill="none" stroke="rgba(255,255,255,0.07)" strokeWidth="4" />
                    <circle
                        cx={dim / 2} cy={dim / 2} r={radius}
                        fill="none"
                        stroke={cfg.color}
                        strokeWidth="4"
                        strokeLinecap="round"
                        strokeDasharray={circumference}
                        strokeDashoffset={offset}
                        style={{ transition: 'stroke-dashoffset 0.8s ease', filter: `drop-shadow(0 0 6px ${cfg.color})` }}
                    />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span style={{ color: cfg.color, fontSize: size === 'lg' ? '1.5rem' : size === 'md' ? '1.1rem' : '0.8rem', fontWeight: 700 }}>
                        {score}
                    </span>
                </div>
            </div>
            <div className="flex items-center gap-1">
                <span>{cfg.icon}</span>
                <span className="text-xs font-semibold" style={{ color: cfg.color }}>{cfg.label}</span>
            </div>
        </div>
    );
}
