import * as React from 'react';
import { cn } from '@/lib/utils';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
    variant?: 'neon' | 'purple' | 'danger' | 'warning' | 'muted' | 'critical' | 'high' | 'medium' | 'low';
}

const Badge = ({ className, variant = 'muted', ...props }: BadgeProps) => {
    const variants = {
        neon: 'bg-neon/10    text-neon    border border-neon/25',
        purple: 'bg-purple/15  text-purple  border border-purple/30',
        danger: 'bg-danger/15  text-danger  border border-danger/30',
        warning: 'bg-warning/15 text-warning  border border-warning/30',
        muted: 'bg-white/5    text-muted    border border-white/10',
        critical: 'bg-danger/15  text-[#ff5555] border border-danger/30',
        high: 'bg-[rgba(255,140,0,0.15)] text-[#ff8c00] border border-[rgba(255,140,0,0.3)]',
        medium: 'bg-warning/15 text-warning  border border-warning/30',
        low: 'bg-neon/10    text-neon    border border-neon/25',
    };
    return (
        <span
            className={cn('inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold', variants[variant], className)}
            {...props}
        />
    );
};

export { Badge };
