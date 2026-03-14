'use client';

import { Bug, Calendar, ExternalLink } from 'lucide-react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { formatAddress, formatDate, SEVERITY_CONFIG, STATUS_CONFIG, TRIAGE_STATUS_CONFIG } from '@/lib/utils';
import type { BugReport } from '@/types/bug';

interface BugCardProps {
    bug: BugReport;
}

export default function BugCard({ bug }: BugCardProps) {
    const sev = SEVERITY_CONFIG[bug.severity];
    const status = STATUS_CONFIG[bug.status];
    const triage = bug.confidence_score !== undefined
        ? bug.confidence_score > 80 ? TRIAGE_STATUS_CONFIG.HIGH_PRIORITY
            : bug.confidence_score > 40 ? TRIAGE_STATUS_CONFIG.NEEDS_REVIEW
                : TRIAGE_STATUS_CONFIG.REJECTED_SPAM
        : null;

    return (
        <Card className="card-cyber p-5 flex flex-col gap-4">
            {/* Header row */}
            <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-2 flex-shrink-0">
                    <Bug className="w-4 h-4 text-muted" />
                </div>
                <div className="flex items-center gap-2 flex-wrap justify-end">
                    <span
                        className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold border"
                        style={{ background: sev.bg, color: sev.color, borderColor: sev.border }}
                    >
                        {sev.label}
                    </span>
                    <span
                        className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold border"
                        style={{ background: status.bg, color: status.color, borderColor: 'transparent' }}
                    >
                        {status.label}
                    </span>
                </div>
            </div>

            {/* Title */}
            <h3 className="text-sm font-semibold text-text-primary leading-tight line-clamp-2">{bug.title}</h3>

            {/* OWASP + confidence */}
            {bug.owasp_category && (
                <div className="flex items-center gap-2">
                    <Badge variant="purple" className="text-xs">{bug.owasp_category.code}</Badge>
                    {triage && (
                        <span className="text-xs px-2 py-0.5 rounded-full border"
                            style={{ background: triage.bg, color: triage.color, borderColor: triage.border }}>
                            {triage.icon} {bug.confidence_score}% confidence
                        </span>
                    )}
                </div>
            )}

            {/* Footer */}
            <div className="flex items-center justify-between text-xs text-muted mt-auto pt-2 border-t border-white/5">
                <span className="font-mono">{formatAddress(bug.submitter_address)}</span>
                <div className="flex items-center gap-1">
                    <Calendar className="w-3 h-3" />
                    {formatDate(bug.created_at)}
                </div>
            </div>
        </Card>
    );
}
