export interface User {
  id: string;
  wallet_address: string;
  trust_score: number;
  total_submissions: number;
  accepted_submissions: number;
  rejected_submissions: number;
  total_earned_matic: number;
  last_seen: string;
  created_at: string;
}

export interface TrustTier {
  tier: 'elite' | 'expert' | 'trusted' | 'novice' | 'unverified';
  label: string;
  color: string;
}

export interface ReputationProfile {
  wallet_address: string;
  trust_score: number;
  tier: TrustTier;
  stats: {
    total_submissions: number;
    accepted: number;
    rejected: number;
    acceptance_rate: number;
    total_earned_matic: number;
  };
}

export interface LeaderboardEntry {
  rank: number;
  wallet_address: string;
  trust_score: number;
  tier: string;
  tier_color: string;
  accepted_submissions: number;
  total_earned_matic: number;
}
