import ProjectCard from '@/components/projects/ProjectCard';
import { getProjects } from '@/lib/api';
import { Search, SlidersHorizontal } from 'lucide-react';

export const metadata = { title: 'Bug Bounty Programs | Anti-Gravity' };

export default async function ProjectsPage() {
    const projects = await getProjects();
    const active = projects.filter(p => p.status === 'active');
    const paused = projects.filter(p => p.status === 'paused');

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            {/* Header */}
            <div className="mb-10">
                <h1 className="text-3xl font-bold text-text-primary mb-2">Bug Bounty Programs</h1>
                <p className="text-text-secondary text-sm">Browse active programs and start submitting vulnerabilities</p>
            </div>

            {/* Search + filter bar */}
            <div className="flex gap-3 mb-8">
                <div className="relative flex-1 max-w-md">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted" />
                    <input
                        className="input-cyber pl-10 w-full"
                        placeholder="Search programs..."
                        id="program-search"
                    />
                </div>
                <button className="btn-outline-neon px-4 flex items-center gap-2 text-sm">
                    <SlidersHorizontal className="w-4 h-4" /> Filter
                </button>
            </div>

            {/* Active programs */}
            {active.length > 0 && (
                <section className="mb-12">
                    <div className="flex items-center gap-2 mb-5">
                        <div className="w-2 h-2 rounded-full bg-neon animate-pulse-neon" />
                        <h2 className="text-lg font-semibold text-text-primary">Active Programs</h2>
                        <span className="text-xs text-muted ml-1">({active.length})</span>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                        {active.map(proj => (
                            <ProjectCard key={proj.id} project={proj} />
                        ))}
                    </div>
                </section>
            )}

            {/* Paused programs */}
            {paused.length > 0 && (
                <section>
                    <div className="flex items-center gap-2 mb-5">
                        <div className="w-2 h-2 rounded-full bg-warning" />
                        <h2 className="text-lg font-semibold text-text-secondary">Paused Programs</h2>
                        <span className="text-xs text-muted ml-1">({paused.length})</span>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                        {paused.map(proj => (
                            <ProjectCard key={proj.id} project={proj} />
                        ))}
                    </div>
                </section>
            )}
        </div>
    );
}
