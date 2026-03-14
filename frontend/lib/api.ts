import axios from 'axios';
import type { SubmitBugPayload, AITriageResult } from '@/types/bug';
import type { LeaderboardEntry } from '@/types/user';
import type { Project } from '@/types/project';

const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    timeout: 30000,
    headers: { 'Content-Type': 'application/json' },
});

// AI Triage
export async function analyzeBugReport(payload: SubmitBugPayload): Promise<AITriageResult> {
    const { data } = await api.post('/api/v1/analyze-report', {
        bug_title: payload.bug_title,
        bug_description: payload.bug_description,
        steps_to_reproduce: payload.steps_to_reproduce,
    });
    return data;
}

// OWASP Categories
export async function getOWASPCategories() {
    const { data } = await api.get('/api/v1/owasp-categories');
    return data;
}

// Health
export async function checkHealth() {
    const { data } = await api.get('/health');
    return data;
}

// Mock data functions (until full backend routes are built)
export async function getProjects(): Promise<Project[]> {
    return MOCK_PROJECTS;
}

export async function getProjectById(id: string): Promise<Project | undefined> {
    return MOCK_PROJECTS.find(p => p.id === id);
}

export async function getLeaderboard(): Promise<LeaderboardEntry[]> {
    return MOCK_LEADERBOARD;
}

// ── Mock Data ──
export const MOCK_PROJECTS: Project[] = [
    {
        id: '1', name: 'DeFi Swap Protocol', company: 'SwapLabs', status: 'active',
        description: 'Decentralized token swap protocol on Polygon. Scope includes smart contracts, API, and web interface.',
        logo_url: '', bounty_pool: 50000, min_bounty: 100, max_bounty: 10000,
        scope: ['*.swaplabs.io', '/api/v2/*', 'Smart contracts on Polygon'],
        out_of_scope: ['Third-party integrations', 'Social engineering'],
        bug_count: 23, accepted_count: 8, created_at: '2025-01-15T00:00:00Z',
    },
    {
        id: '2', name: 'NFT Marketplace', company: 'PixelVault', status: 'active',
        description: 'NFT minting and trading platform. All user-facing endpoints and smart contracts in scope.',
        logo_url: '', bounty_pool: 25000, min_bounty: 50, max_bounty: 5000,
        scope: ['app.pixelvault.io', 'api.pixelvault.io', 'NFT contracts'],
        out_of_scope: ['IPFS content', 'Third-party wallets'],
        bug_count: 11, accepted_count: 4, created_at: '2025-02-01T00:00:00Z',
    },
    {
        id: '3', name: 'Cross-Chain Bridge', company: 'BridgeNet', status: 'active',
        description: 'Cross-chain asset bridge supporting Ethereum, Polygon, BSC. Critical infrastructure — high rewards.',
        logo_url: '', bounty_pool: 200000, min_bounty: 500, max_bounty: 50000,
        scope: ['bridge.bridgenet.io', 'All smart contracts', 'Relayer nodes'],
        out_of_scope: ['Layer 1 chain bugs', 'Gas optimizations'],
        bug_count: 5, accepted_count: 2, created_at: '2025-03-01T00:00:00Z',
    },
    {
        id: '4', name: 'Lending Protocol', company: 'YieldMax', status: 'paused',
        description: 'Algorithmic lending and borrowing protocol. Currently paused for V2 upgrade.',
        logo_url: '', bounty_pool: 75000, min_bounty: 200, max_bounty: 15000,
        scope: ['app.yieldmax.finance', 'V1 contracts (Ethereum)'],
        out_of_scope: ['V2 contracts (not yet deployed)'],
        bug_count: 18, accepted_count: 7, created_at: '2024-11-01T00:00:00Z',
    },
];

export const MOCK_LEADERBOARD: LeaderboardEntry[] = [
    { rank: 1, address: '0x1234...5678', trust_score: 98, tier: 'legend', accepted_bugs: 47, total_earnings: 125000 },
    { rank: 2, address: '0xabcd...ef01', trust_score: 92, tier: 'elite', accepted_bugs: 31, total_earnings: 87500 },
    { rank: 3, address: '0x9876...4321', trust_score: 88, tier: 'elite', accepted_bugs: 24, total_earnings: 62000 },
    { rank: 4, address: '0xdead...beef', trust_score: 81, tier: 'expert', accepted_bugs: 18, total_earnings: 41000 },
    { rank: 5, address: '0xcafe...babe', trust_score: 76, tier: 'expert', accepted_bugs: 14, total_earnings: 28500 },
    { rank: 6, address: '0x1111...2222', trust_score: 69, tier: 'hunter', accepted_bugs: 10, total_earnings: 17000 },
    { rank: 7, address: '0x3333...4444', trust_score: 63, tier: 'hunter', accepted_bugs: 7, total_earnings: 11200 },
    { rank: 8, address: '0x5555...6666', trust_score: 55, tier: 'hunter', accepted_bugs: 5, total_earnings: 7800 },
    { rank: 9, address: '0x7777...8888', trust_score: 42, tier: 'novice', accepted_bugs: 3, total_earnings: 3500 },
    { rank: 10, address: '0x9999...0000', trust_score: 35, tier: 'novice', accepted_bugs: 2, total_earnings: 1800 },
];

export default api;
