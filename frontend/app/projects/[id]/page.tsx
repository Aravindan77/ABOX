import { getProjectById } from '@/lib/api';
import { formatCurrency } from '@/lib/utils';
import { Shield, Bug, DollarSign, CheckCircle, XCircle } from 'lucide-react';
import { notFound } from 'next/navigation';

export default async function ProjectDetailPage({ params }: { params: { id: string } }) {
    const project = await getProjectById(params.id);
    if (!project) notFound();

    return (
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            {/* Header */}
            <div className="flex items-start gap-4 mb-8">
                <div className="w-14 h-14 rounded-xl bg-neon/10 border border-neon/20 flex items-center justify-center flex-shrink-0">
                    <Shield className="w-7 h-7 text-neon" />
                </div>
                <div>
                    <h1 className="text-2xl font-bold text-text-primary">{project.name}</h1>
                    <p className="text-text-secondary text-sm">{project.company}</p>
                </div>
                <div className="ml-auto">
                    <a href={`/submit?project=${project.id}`}>
                        <button className="btn-neon">
                            <Bug className="w-4 h-4" /> Submit Bug
                        </button>
                    </a>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Main content */}
                <div className="lg:col-span-2 flex flex-col gap-6">
                    <div className="glass border border-border rounded-xl p-6">
                        <h2 className="font-semibold text-text-primary mb-3">About this Program</h2>
                        <p className="text-sm text-text-secondary leading-relaxed">{project.description}</p>
                    </div>

                    <div className="glass border border-border rounded-xl p-6">
                        <h2 className="font-semibold text-neon mb-3 flex items-center gap-2">
                            <CheckCircle className="w-4 h-4" /> In Scope
                        </h2>
                        <ul className="space-y-2">
                            {project.scope.map(s => (
                                <li key={s} className="flex items-center gap-2 text-sm text-text-secondary">
                                    <span className="w-1.5 h-1.5 rounded-full bg-neon flex-shrink-0" />
                                    {s}
                                </li>
                            ))}
                        </ul>
                    </div>

                    <div className="glass border border-border rounded-xl p-6">
                        <h2 className="font-semibold text-danger mb-3 flex items-center gap-2">
                            <XCircle className="w-4 h-4" /> Out of Scope
                        </h2>
                        <ul className="space-y-2">
                            {project.out_of_scope.map(s => (
                                <li key={s} className="flex items-center gap-2 text-sm text-text-secondary">
                                    <span className="w-1.5 h-1.5 rounded-full bg-danger flex-shrink-0" />
                                    {s}
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>

                {/* Sidebar stats */}
                <div className="flex flex-col gap-4">
                    <div className="glass-neon rounded-xl p-5">
                        <div className="flex items-center gap-2 mb-1">
                            <DollarSign className="w-4 h-4 text-neon" />
                            <span className="text-xs text-muted">Bounty Pool</span>
                        </div>
                        <p className="text-3xl font-black text-neon">{formatCurrency(project.bounty_pool)}</p>
                        <p className="text-xs text-muted mt-1">Range: {formatCurrency(project.min_bounty)} – {formatCurrency(project.max_bounty)}</p>
                    </div>

                    <div className="glass border border-border rounded-xl p-5 flex flex-col gap-3">
                        <div className="flex justify-between text-sm">
                            <span className="text-muted">Total Reports</span>
                            <span className="text-text-primary font-medium">{project.bug_count}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                            <span className="text-muted">Accepted</span>
                            <span className="text-neon font-medium">{project.accepted_count}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                            <span className="text-muted">Acceptance Rate</span>
                            <span className="text-text-primary font-medium">
                                {project.bug_count > 0 ? Math.round((project.accepted_count / project.bug_count) * 100) : 0}%
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
