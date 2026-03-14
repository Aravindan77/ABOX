export type BugSeverity = 'critical' | 'high' | 'medium' | 'low' | 'informational';
export type BugStatus = 'pending' | 'approved' | 'rejected' | 'spam' | 'human_review' | 'paid';

export interface BugReport {
  id: string;
  project_id: string;
  researcher_address: string;
  title: string;
  description: string;
  severity: BugSeverity;
  steps_to_reproduce: string;
  expected_behavior?: string;
  actual_behavior?: string;
  ipfs_cid?: string;
  status: BugStatus;
  owasp_category?: string;
  cvss_score?: number;
  ai_confidence?: number;
  bounty_amount?: number;
  tx_hash?: string;
  review_notes?: string;
  created_at: string;
  updated_at?: string;
}

export interface TriageResult {
  owasp_category: string;
  owasp_confidence: number;
  cvss_score: number;
  severity: BugSeverity;
  spam_probability: number;
  is_spam: boolean;
  ai_confidence: number;
  auto_approved: boolean;
  requires_human_review: boolean;
  recommendation: string;
  tx_hash?: string;
}

export interface BugSubmissionPayload {
  project_id: string;
  title: string;
  description: string;
  severity: BugSeverity;
  steps_to_reproduce: string;
  expected_behavior?: string;
  actual_behavior?: string;
  evidence_file?: File;
}
