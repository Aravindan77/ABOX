import { SEVERITY_CONFIG, STATUS_CONFIG } from '@/lib/utils';
import type { BugStatus, BugSeverity } from '@/types/bug';

export function BugStatusBadge({ status }: { status: BugStatus }) {
    const cfg = STATUS_CONFIG[status];
    return (
        <span
            className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold"
            style={{ background: cfg.bg, color: cfg.color }}
        >
            {cfg.label}
        </span>
    );
}

export function SeverityBadge({ severity }: { severity: BugSeverity }) {
    const cfg = SEVERITY_CONFIG[severity];
    return (
        <span
            className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold border"
            style={{ background: cfg.bg, color: cfg.color, borderColor: cfg.border }}
        >
            {cfg.label}
        </span>
    );
}
