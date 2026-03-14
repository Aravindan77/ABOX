import Link from 'next/link';
import { Shield, Github, Twitter, ExternalLink } from 'lucide-react';

export default function Footer() {
    return (
        <footer className="border-t border-white/5 bg-surface/50 mt-20">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                    {/* Brand */}
                    <div className="md:col-span-1">
                        <div className="flex items-center gap-2 mb-4">
                            <div className="w-7 h-7 rounded-lg flex items-center justify-center" style={{ background: 'linear-gradient(135deg, #00ff88, #00cc6a)' }}>
                                <Shield className="w-3.5 h-3.5 text-black" strokeWidth={2.5} />
                            </div>
                            <span className="font-bold text-sm">
                                <span className="text-gradient-neon">Anti</span>
                                <span className="text-text-primary">Gravity</span>
                            </span>
                        </div>
                        <p className="text-xs text-muted leading-relaxed">
                            Decentralized bug bounty platform powered by AI triage and on-chain payments.
                        </p>
                        <div className="flex items-center gap-3 mt-4">
                            <a href="#" className="text-muted hover:text-neon transition-colors"><Github className="w-4 h-4" /></a>
                            <a href="#" className="text-muted hover:text-neon transition-colors"><Twitter className="w-4 h-4" /></a>
                        </div>
                    </div>

                    {/* Platform */}
                    <div>
                        <h4 className="text-xs font-semibold text-text-secondary uppercase tracking-wider mb-3">Platform</h4>
                        <ul className="space-y-2">
                            {['Browse Programs', 'Submit Bug', 'Leaderboard', 'Dashboard'].map(item => (
                                <li key={item}>
                                    <Link href="#" className="text-xs text-muted hover:text-neon transition-colors">{item}</Link>
                                </li>
                            ))}
                        </ul>
                    </div>

                    {/* Resources */}
                    <div>
                        <h4 className="text-xs font-semibold text-text-secondary uppercase tracking-wider mb-3">Resources</h4>
                        <ul className="space-y-2">
                            {['API Docs', 'OWASP Top 10', 'Smart Contracts', 'IPFS Storage'].map(item => (
                                <li key={item}>
                                    <Link href="#" className="text-xs text-muted hover:text-neon transition-colors flex items-center gap-1">{item}<ExternalLink className="w-3 h-3" /></Link>
                                </li>
                            ))}
                        </ul>
                    </div>

                    {/* Network */}
                    <div>
                        <h4 className="text-xs font-semibold text-text-secondary uppercase tracking-wider mb-3">Network</h4>
                        <div className="flex items-center gap-2 glass px-3 py-2 rounded-lg w-fit">
                            <div className="w-2 h-2 rounded-full bg-neon animate-pulse-neon" />
                            <span className="text-xs text-text-secondary">Polygon Mumbai</span>
                        </div>
                        <p className="text-xs text-muted mt-3">Chain ID: 80001</p>
                        <p className="text-xs text-muted mt-1">AI Demo: localhost:8501</p>
                        <p className="text-xs text-muted mt-1">API: localhost:8000</p>
                    </div>
                </div>

                <div className="border-t border-white/5 mt-8 pt-6 flex flex-col sm:flex-row justify-between items-center gap-4">
                    <p className="text-xs text-muted">© 2025 Anti-Gravity Bug Bounty Platform. All rights reserved.</p>
                    <p className="text-xs text-muted">Built with ❤️ by security researchers, for security researchers.</p>
                </div>
            </div>
        </footer>
    );
}
