export interface Project {
  id: string;
  owner_address: string;
  name: string;
  description: string;
  scope: string;
  bounty_pool_matic: number;
  max_severity: string;
  website_url?: string;
  logo_url?: string;
  active: boolean;
  total_bugs: number;
  resolved_bugs: number;
  created_at: string;
  updated_at?: string;
}

export interface CreateProjectPayload {
  name: string;
  description: string;
  scope: string;
  bounty_pool_matic?: number;
  max_severity?: string;
  website_url?: string;
  logo_url?: string;
}
