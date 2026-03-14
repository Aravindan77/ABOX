import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { formatCurrency } from '@/lib/utils';
import type { Project } from '@/types/project';
import Link from 'next/link';
import { Shield, Bug, ArrowRight } from 'lucide-react';

const STATUS_COLOR = {
    active: { dot: '#00ff88', label: 'Active' },
    paused: { dot: '#ffa500', label: 'Paused' },
    completed: { dot: '#888', label: 'Completed' },
};

interface ProjectCardProps {
    project: Project;
}

export default function ProjectCard({ project }: ProjectCardProps) {
    const statusCfg = STATUS_COLOR[project.status];
    return (
        <Link href={`/projects/${project.id}`}>
            <Card className="card-cyber p-6 flex flex-col gap-4 h-full cursor-pointer group">
                {/* Top */}
                <div className="flex items-start justify-between">
                    <div>
                        <div className="flex items-center gap-2 mb-1">
                            <div className="w-8 h-8 rounded-lg bg-neon/10 border border-neon/20 flex items-center justify-center">
                                <Shield className="w-4 h-4 text-neon" />
                            </div>
                            <div>
                                <h3 className="text-sm font-semibold text-text-primary group-hover:text-neon transition-colors">{project.name}</h3>
                                <p className="text-xs text-muted">{project.company}</p>
                            </div>
                        </div>
                    </div>
                    <div className="flex items-center gap-1.5">
                        <div className="w-2 h-2 rounded-full animate-pulse-neon" style={{ backgroundColor: statusCfg.dot }} />
                        <span className="text-xs text-muted">{statusCfg.label}</span>
                    </div>
                </div>

                {/* Description */}
                <p className="text-xs text-text-secondary leading-relaxed line-clamp-2">{project.description}</p>

                {/* Bounty pool */}
                <div className="glass-neon rounded-lg px-4 py-3 flex items-center justify-between">
                    <div>
                        <p className="text-xs text-muted">Bounty Pool</p>
                        <p className="text-lg font-bold text-neon">{formatCurrency(project.bounty_pool)}</p>
                    </div>
                    <div className="text-right">
                        <p className="text-xs text-muted">Range</p>
                        <p className="text-xs text-text-secondary">{formatCurrency(project.min_bounty)} – {formatCurrency(project.max_bounty)}</p>
                    </div>
                </div>

                {/* Stats + CTA */}
                <div className="flex items-center justify-between mt-auto pt-2 border-t border-white/5">
                    <div className="flex items-center gap-3">
                        <div className="flex items-center gap-1 text-xs text-muted">
                            <Bug className="w-3 h-3" />
                            {project.bug_count} reports
                        </div>
                        <div className="flex items-center gap-1 text-xs text-neon">
                            ✓ {project.accepted_count} accepted
                        </div>
                    </div>
                    <ArrowRight className="w-4 h-4 text-muted group-hover:text-neon group-hover:translate-x-1 transition-all" />
                </div>
            </Card>
        </Link>
    );
}
