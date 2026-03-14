import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Shield, Zap, Globe, Lock, ArrowRight, Bug, Trophy, DollarSign } from 'lucide-react';

const features = [
    { icon: Zap, title: 'AI Auto-Triage', color: '#7c3aed', desc: 'DistilBERT-powered analysis classifies bugs against OWASP Top 10 in milliseconds, scoring confidence and filtering spam automatically.' },
    { icon: DollarSign, title: 'On-Chain Payments', color: '#00ff88', desc: 'Smart contract escrow on Polygon releases bounty payments automatically when AI confidence exceeds 85% — no manual approval needed.' },
    { icon: Trophy, title: 'Reputation System', color: '#ffa500', desc: 'Build your trust score across every submission. Higher reputation unlocks private programs, higher bounties, and elite tier status.' },
    { icon: Globe, title: 'IPFS Evidence', color: '#00ccff', desc: 'PoC files, screenshots, and code snippets stored permanently on IPFS — tamper-proof, censorship-resistant, always accessible.' },
    { icon: Lock, title: 'Wallet Identity', color: '#ff8c00', desc: 'No accounts, no emails. Your Ethereum wallet IS your identity. Connect MetaMask or any Web3 wallet to start hunting instantly.' },
    { icon: Shield, title: 'OWASP Coverage', color: '#ff3232', desc: 'Full OWASP Top 10 (2021) classification with keyword confidence scoring across injection, broken auth, XSS, SSRF, and more.' },
];

const stats = [
    { value: '$350K+', label: 'Total Bounties Paid' },
    { value: '1,240+', label: 'Bugs Accepted' },
    { value: '89%', label: 'AI Accuracy', },
    { value: '4', label: 'Active Programs' },
];

const steps = [
    { n: '01', title: 'Connect Wallet', desc: 'Link your MetaMask or WalletConnect wallet. No registration required.' },
    { n: '02', title: 'Find a Program', desc: 'Browse active bug bounty programs and pick your target.' },
    { n: '03', title: 'Submit a Bug', desc: 'Describe the vulnerability. Our AI instantly triages and classifies it.' },
    { n: '04', title: 'Get Paid', desc: 'High-confidence bugs trigger automatic on-chain MATIC payment.' },
];

export default function HomePage() {
    return (
        <div className="relative min-h-screen">
            {/* Background grid */}
            <div className="fixed inset-0 pointer-events-none" style={{
                backgroundImage: 'radial-gradient(circle at 20% 20%, rgba(0,255,136,0.04) 0%, transparent 50%), radial-gradient(circle at 80% 80%, rgba(124,58,237,0.06) 0%, transparent 50%)',
            }} />

            {/* Hero */}
            <section className="relative flex flex-col items-center justify-center text-center px-4 pt-28 pb-20">
                <div className="inline-flex items-center gap-2 glass border border-neon/20 px-4 py-2 rounded-full text-xs font-medium text-neon mb-8 animate-fade-in">
                    <div className="w-2 h-2 rounded-full bg-neon animate-pulse-neon" />
                    Live on Polygon Mumbai Testnet
                </div>

                <h1 className="text-5xl sm:text-6xl md:text-7xl font-black tracking-tight leading-tight mb-6 animate-fade-in" style={{ animationDelay: '0.1s' }}>
                    <span className="text-gradient-neon">AI-Powered</span>
                    <br />
                    <span className="text-text-primary">Bug Bounty</span>
                    <br />
                    <span className="text-gradient-purple">Decentralized</span>
                </h1>

                <p className="max-w-2xl text-base sm:text-lg text-text-secondary leading-relaxed mb-10 animate-fade-in" style={{ animationDelay: '0.2s' }}>
                    Submit vulnerabilities and get paid instantly on-chain. Our AI engine auto-triages reports against OWASP Top 10, assigns severity, and releases smart contract bounties — no middlemen.
                </p>

                <div className="flex flex-col sm:flex-row gap-4 animate-fade-in" style={{ animationDelay: '0.3s' }}>
                    <Link href="/projects">
                        <Button variant="neon" size="lg" className="w-full sm:w-auto">
                            Browse Programs <ArrowRight className="w-4 h-4" />
                        </Button>
                    </Link>
                    <Link href="/submit">
                        <Button variant="outline" size="lg" className="w-full sm:w-auto">
                            <Bug className="w-4 h-4" /> Submit a Bug
                        </Button>
                    </Link>
                </div>

                {/* Stats ticker */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-16 w-full max-w-3xl animate-fade-in" style={{ animationDelay: '0.4s' }}>
                    {stats.map(({ value, label }) => (
                        <div key={label} className="glass-neon rounded-xl px-4 py-4 text-center">
                            <p className="text-2xl font-black text-neon">{value}</p>
                            <p className="text-xs text-muted mt-1">{label}</p>
                        </div>
                    ))}
                </div>
            </section>

            {/* Features */}
            <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
                <div className="text-center mb-12">
                    <h2 className="text-3xl font-bold text-text-primary mb-3">Why Anti-Gravity?</h2>
                    <p className="text-text-secondary max-w-xl mx-auto text-sm">The next generation of bug bounty infrastructure — automated, transparent, and on-chain.</p>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                    {features.map(({ icon: Icon, title, color, desc }) => (
                        <Card key={title} className="card-cyber p-6 flex flex-col gap-4">
                            <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: `${color}18`, border: `1px solid ${color}30` }}>
                                <Icon className="w-5 h-5" style={{ color }} />
                            </div>
                            <div>
                                <h3 className="font-semibold text-text-primary mb-2">{title}</h3>
                                <p className="text-xs text-text-secondary leading-relaxed">{desc}</p>
                            </div>
                        </Card>
                    ))}
                </div>
            </section>

            {/* How it works */}
            <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
                <div className="text-center mb-12">
                    <h2 className="text-3xl font-bold text-text-primary mb-3">How It Works</h2>
                    <p className="text-text-secondary text-sm">From discovery to payment in minutes</p>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                    {steps.map(({ n, title, desc }) => (
                        <div key={n} className="flex flex-col items-center text-center gap-3">
                            <div className="w-12 h-12 rounded-xl glass-neon flex items-center justify-center font-mono text-neon font-bold text-lg">{n}</div>
                            <h4 className="font-semibold text-sm text-text-primary">{title}</h4>
                            <p className="text-xs text-text-secondary leading-relaxed">{desc}</p>
                        </div>
                    ))}
                </div>
            </section>

            {/* CTA */}
            <section className="max-w-3xl mx-auto px-4 text-center py-20">
                <div className="glass-neon rounded-2xl px-8 py-12">
                    <h2 className="text-3xl font-bold text-text-primary mb-3">Ready to Hunt?</h2>
                    <p className="text-text-secondary text-sm mb-8">Connect your wallet and start earning bounties in the next decentralized security marketplace.</p>
                    <Link href="/projects">
                        <Button variant="neon" size="lg">Start Bug Hunting <ArrowRight className="w-4 h-4" /></Button>
                    </Link>
                </div>
            </section>
        </div>
    );
}
