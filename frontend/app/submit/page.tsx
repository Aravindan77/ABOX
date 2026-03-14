'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input, Textarea } from '@/components/ui/input';
import { analyzeBugReport } from '@/lib/api';
import { TRIAGE_STATUS_CONFIG, SEVERITY_CONFIG } from '@/lib/utils';
import type { AITriageResult, BugSeverity } from '@/types/bug';
import { Brain, Send, Shield, AlertTriangle, CheckCircle } from 'lucide-react';

const SEVERITIES: BugSeverity[] = ['critical', 'high', 'medium', 'low'];

export default function SubmitPage() {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [steps, setSteps] = useState('');
    const [severity, setSeverity] = useState<BugSeverity>('high');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<AITriageResult | null>(null);
    const [error, setError] = useState('');

    const handleAnalyze = async () => {
        if (!title || !description || !steps) { setError('Please fill in all required fields.'); return; }
        setError(''); setLoading(true);
        try {
            const res = await analyzeBugReport({ bug_title: title, bug_description: description, steps_to_reproduce: steps });
            setResult(res);
        } catch (e: unknown) {
            setError('Could not connect to AI backend. Make sure the FastAPI server is running on localhost:8000.');
        } finally {
            setLoading(false);
        }
    };

    const triage = result ? TRIAGE_STATUS_CONFIG[result.status] : null;

    return (
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-text-primary mb-2">Submit a Bug Report</h1>
                <p className="text-text-secondary text-sm">Our AI engine will instantly analyze your report for OWASP classification, severity, and priority status.</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
                {/* Form */}
                <div className="lg:col-span-3 flex flex-col gap-5">
                    <div className="glass border border-border rounded-xl p-6 flex flex-col gap-5">
                        <Input
                            id="bug-title"
                            label="Bug Title *"
                            placeholder="e.g., SQL Injection in /api/login allows auth bypass"
                            value={title}
                            onChange={e => setTitle(e.target.value)}
                            maxLength={500}
                        />

                        {/* Severity selector */}
                        <div className="flex flex-col gap-1.5">
                            <label className="text-sm font-medium text-text-secondary">Reported Severity</label>
                            <div className="flex gap-2 flex-wrap">
                                {SEVERITIES.map(s => {
                                    const cfg = SEVERITY_CONFIG[s];
                                    return (
                                        <button
                                            key={s}
                                            onClick={() => setSeverity(s)}
                                            className="px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all"
                                            style={{
                                                background: severity === s ? cfg.bg : 'transparent',
                                                color: severity === s ? cfg.color : '#888',
                                                borderColor: severity === s ? cfg.border : 'rgba(255,255,255,0.1)',
                                            }}
                                        >
                                            {cfg.label}
                                        </button>
                                    );
                                })}
                            </div>
                        </div>

                        <Textarea
                            id="bug-desc"
                            label="Bug Description *"
                            placeholder="Describe the vulnerability — what it is, what it affects, and the potential impact..."
                            rows={5}
                            value={description}
                            onChange={e => setDescription(e.target.value)}
                        />

                        <Textarea
                            id="bug-steps"
                            label="Steps to Reproduce *"
                            placeholder={"1. Go to...\n2. Enter...\n3. Click...\n4. Observe..."}
                            rows={4}
                            value={steps}
                            onChange={e => setSteps(e.target.value)}
                        />

                        {error && (
                            <div className="flex items-center gap-2 text-xs text-danger bg-danger/10 border border-danger/20 rounded-lg px-3 py-2">
                                <AlertTriangle className="w-4 h-4 flex-shrink-0" /> {error}
                            </div>
                        )}

                        <Button variant="purple" onClick={handleAnalyze} loading={loading} id="analyze-btn">
                            <Brain className="w-4 h-4" /> {loading ? 'Analyzing...' : 'Analyze with AI'}
                        </Button>
                    </div>
                </div>

                {/* AI Triage Panel */}
                <div className="lg:col-span-2 flex flex-col gap-4">
                    <div className="glass border border-white/5 rounded-xl p-5">
                        <h3 className="text-sm font-semibold text-text-primary mb-3 flex items-center gap-2">
                            <Brain className="w-4 h-4 text-purple" /> AI Triage Preview
                        </h3>
                        {!result ? (
                            <p className="text-xs text-muted leading-relaxed">Fill in the form and click &quot;Analyze with AI&quot; to see OWASP classification, confidence score, severity assessment, and priority status.</p>
                        ) : (
                            <div className="flex flex-col gap-4">
                                {/* Status */}
                                {triage && (
                                    <div className="rounded-lg p-3 border" style={{ background: triage.bg, borderColor: triage.border }}>
                                        <div className="text-base font-bold" style={{ color: triage.color }}>{triage.icon} {triage.label}</div>
                                        <div className="text-xs mt-0.5" style={{ color: triage.color, opacity: 0.7 }}>
                                            Confidence: {result.confidence_score}%
                                        </div>
                                    </div>
                                )}

                                {/* OWASP */}
                                <div>
                                    <p className="text-xs text-muted mb-1">OWASP Category</p>
                                    <p className="text-xs font-semibold text-neon">{result.owasp_category.code}</p>
                                    <p className="text-xs text-text-secondary">{result.owasp_category.name}</p>
                                    {result.owasp_category.matched_keywords.length > 0 && (
                                        <div className="flex flex-wrap gap-1 mt-2">
                                            {result.owasp_category.matched_keywords.slice(0, 4).map(kw => (
                                                <span key={kw} className="font-mono text-xs px-1.5 py-0.5 rounded bg-neon/10 text-neon border border-neon/20">{kw}</span>
                                            ))}
                                        </div>
                                    )}
                                </div>

                                {/* Severity */}
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="text-xs text-muted mb-1">AI Severity</p>
                                        <span className="text-xs font-bold uppercase" style={{ color: SEVERITY_CONFIG[result.severity.level].color }}>
                                            {result.severity.level}
                                        </span>
                                    </div>
                                    <div className="text-right">
                                        <p className="text-xs text-muted mb-1">CVSS</p>
                                        <p className="text-xs font-bold text-text-primary">{result.severity.cvss_score}/100</p>
                                    </div>
                                </div>

                                {/* Text quality + spam */}
                                <div className="grid grid-cols-2 gap-2">
                                    {[
                                        { label: 'Text Quality', value: `${result.text_quality.score}/100` },
                                        { label: 'Spam Score', value: `${result.spam_detection.spam_score}/100` },
                                    ].map(({ label, value }) => (
                                        <div key={label} className="glass rounded-lg px-3 py-2">
                                            <p className="text-xs text-muted">{label}</p>
                                            <p className="text-xs font-semibold text-text-primary">{value}</p>
                                        </div>
                                    ))}
                                </div>

                                {/* Submit button */}
                                <Button variant="neon" className="w-full mt-1">
                                    <Send className="w-4 h-4" /> Submit Report
                                </Button>
                            </div>
                        )}
                    </div>

                    {/* Tips */}
                    <div className="glass border border-purple/15 rounded-xl p-4">
                        <h4 className="text-xs font-semibold text-purple mb-2 flex items-center gap-1.5"><Shield className="w-3 h-3" /> Tips for HIGH_PRIORITY</h4>
                        <ul className="text-xs text-muted space-y-1.5 leading-relaxed">
                            <li className="flex items-start gap-1.5"><span className="text-neon mt-0.5">✓</span> Use a clear, technical title</li>
                            <li className="flex items-start gap-1.5"><span className="text-neon mt-0.5">✓</span> Include numbered reproduction steps</li>
                            <li className="flex items-start gap-1.5"><span className="text-neon mt-0.5">✓</span> Describe impact and affected endpoints</li>
                            <li className="flex items-start gap-1.5"><span className="text-neon mt-0.5">✓</span> Use technical security terminology</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
}
