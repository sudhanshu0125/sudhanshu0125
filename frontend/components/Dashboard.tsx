'use client';

import { useMemo, useState } from 'react';
import { Lead } from '@/lib/types';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000/api';

export default function Dashboard() {
  const [token, setToken] = useState('');
  const [email, setEmail] = useState('admin@influencersplace.com');
  const [password, setPassword] = useState('admin12345');
  const [leads, setLeads] = useState<Lead[]>([]);
  const [query, setQuery] = useState('');

  const scoreSummary = useMemo(() => {
    const hot = leads.filter((l) => l.status === 'Hot').length;
    const warm = leads.filter((l) => l.status === 'Warm').length;
    const cold = leads.filter((l) => l.status === 'Cold').length;
    return { hot, warm, cold };
  }, [leads]);

  const authHeaders = token ? { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } : { 'Content-Type': 'application/json' };

  async function loginOrRegister(mode: 'login' | 'register') {
    const res = await fetch(`${API_BASE}/auth/${mode}`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (data.access_token) setToken(data.access_token);
  }

  async function fetchLeads() {
    const res = await fetch(`${API_BASE}/leads/?q=${encodeURIComponent(query)}`, { headers: authHeaders });
    const data = await res.json();
    setLeads(Array.isArray(data) ? data : []);
  }

  async function runAgent() {
    await fetch(`${API_BASE}/agent/run`, {
      method: 'POST', headers: authHeaders,
      body: JSON.stringify({ query: 'influencer marketing agencies india talent managers brand partnerships', max_results: 15 }),
    });
    await fetchLeads();
  }

  async function updateLead(id: number, patch: Partial<Lead>) {
    await fetch(`${API_BASE}/leads/${id}`, {
      method: 'PATCH', headers: authHeaders, body: JSON.stringify(patch),
    });
    await fetchLeads();
  }

  async function triggerOutreach(lead: Lead) {
    await fetch(`${API_BASE}/outreach/trigger`, {
      method: 'POST', headers: authHeaders,
      body: JSON.stringify({ lead_id: lead.id, channel: 'email', message: `Hi ${lead.company_name}, let's collaborate.` }),
    });
    await fetchLeads();
  }

  return (
    <main className="mx-auto max-w-7xl p-6">
      <h1 className="text-2xl font-bold">InfluencersPlace AI Lead Agent</h1>
      <div className="mt-4 grid gap-3 rounded-lg bg-slate-900 p-4 md:grid-cols-4">
        <input className="rounded bg-slate-800 px-3 py-2" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="rounded bg-slate-800 px-3 py-2" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button className="rounded bg-blue-600 px-3 py-2" onClick={() => loginOrRegister('register')}>Register</button>
        <button className="rounded bg-emerald-600 px-3 py-2" onClick={() => loginOrRegister('login')}>Login</button>
      </div>

      <div className="mt-4 flex flex-wrap gap-3">
        <button className="rounded bg-violet-600 px-3 py-2" onClick={runAgent}>Run AI Discovery</button>
        <input className="rounded bg-slate-800 px-3 py-2" placeholder="Search leads" value={query} onChange={(e) => setQuery(e.target.value)} />
        <button className="rounded bg-slate-700 px-3 py-2" onClick={fetchLeads}>Refresh</button>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-3 text-center">
        <div className="rounded bg-red-950 p-3">Hot: {scoreSummary.hot}</div>
        <div className="rounded bg-amber-950 p-3">Warm: {scoreSummary.warm}</div>
        <div className="rounded bg-cyan-950 p-3">Cold: {scoreSummary.cold}</div>
      </div>

      <div className="mt-6 overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead><tr className="border-b border-slate-700 text-left"><th>Company</th><th>Contact</th><th>Score</th><th>Status</th><th>Links</th><th>Actions</th></tr></thead>
          <tbody>
            {leads.map((lead) => (
              <tr key={lead.id} className="border-b border-slate-800 align-top">
                <td className="py-2">{lead.company_name}<div className="text-slate-400">{lead.notes}</div></td>
                <td>{lead.email || '-'}<div>{lead.phone || '-'}</div></td>
                <td>{lead.score}</td>
                <td>{lead.status}</td>
                <td className="space-y-1">
                  {lead.website && <a className="text-blue-400" href={lead.website} target="_blank">Website</a>}
                  <br />
                  {lead.linkedin_url && <a className="text-blue-400" href={lead.linkedin_url} target="_blank">LinkedIn</a>}
                </td>
                <td className="space-x-1">
                  <button className="rounded bg-emerald-700 px-2 py-1" onClick={() => updateLead(lead.id, { approved: !lead.approved })}>{lead.approved ? 'Unapprove' : 'Approve'}</button>
                  <button className="rounded bg-orange-700 px-2 py-1" onClick={() => updateLead(lead.id, { status: 'Hot' })}>Mark Hot</button>
                  <button className="rounded bg-indigo-700 px-2 py-1" onClick={() => triggerOutreach(lead)}>Outreach</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
