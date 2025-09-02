import React, { useState } from 'react'
import { Layout } from '../components/Layout'
import { apiFetch } from '../modules/api'

export const JobsPage: React.FC = () => {
  const [tenantId, setTenantId] = useState('')
  const [productLineId, setProductLineId] = useState('')
  const [weekId, setWeekId] = useState('')
  const [before, setBefore] = useState('')
  const [out, setOut] = useState('')

  const triggerReport = async () => {
    const j = await apiFetch('/admin/jobs/generate-weekly-reports', { method: 'POST', body: JSON.stringify({ tenantId, productLineId, weekId: weekId || undefined }) })
    setOut(JSON.stringify(j, null, 2))
  }
  const triggerPurge = async () => {
    const j = await apiFetch('/admin/jobs/purge-ephemeral', { method: 'POST', body: JSON.stringify({ before }) })
    setOut(JSON.stringify(j, null, 2))
  }

  return (
    <Layout>
      <div className="bg-white border rounded p-4 max-w-xl space-y-3">
        <h2 className="text-lg font-semibold">Jobs</h2>
        <div>
          <label className="block text-sm">Tenant Id</label>
          <input className="mt-1 w-full border rounded px-3 py-2" value={tenantId} onChange={e=>setTenantId(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm">Product Line Id</label>
          <input className="mt-1 w-full border rounded px-3 py-2" value={productLineId} onChange={e=>setProductLineId(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm">Week Id (opzionale)</label>
          <input className="mt-1 w-full border rounded px-3 py-2" value={weekId} onChange={e=>setWeekId(e.target.value)} />
        </div>
        <button className="bg-black text-white rounded px-4 py-2" onClick={triggerReport}>Genera report</button>

        <div className="h-px bg-gray-200" />
        <div>
          <label className="block text-sm">Purge prima di (YYYY-MM-DD)</label>
          <input className="mt-1 w-full border rounded px-3 py-2" value={before} onChange={e=>setBefore(e.target.value)} />
        </div>
        <button className="border rounded px-4 py-2" onClick={triggerPurge}>Purge</button>
        {out && <pre className="bg-gray-50 border rounded p-3 text-sm mt-3">{out}</pre>}
      </div>
    </Layout>
  )
}

