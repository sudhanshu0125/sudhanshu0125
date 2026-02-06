export type Lead = {
  id: number;
  name?: string;
  company_name: string;
  role?: string;
  email?: string;
  phone?: string;
  whatsapp?: string;
  linkedin_url?: string;
  website?: string;
  location?: string;
  notes?: string;
  source: string;
  score: number;
  status: 'Hot' | 'Warm' | 'Cold';
  approved: boolean;
  outreach_state: string;
  created_at: string;
};
