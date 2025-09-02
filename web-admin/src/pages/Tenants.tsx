import React, { useState } from 'react'
import { Layout } from '../components/Layout'
import { apiFetch } from '../modules/api'

export const TenantsPage: React.FC = () => {
  const [name, setName] = useState('Nuovo Cliente')
  const [companyCode, setCompanyCode] = useState('ACME001')
  const [out, setOut] = useState('')

  const createTenant = async () => {
    const j = await apiFetch('/admin/tenants', { method: 'POST', body: JSON.stringify({ name, companyCode }) })
    setOut(JSON.stringify(j, null, 2))
  }

  return (
    <Layout>
      <div className="bg-white border rounded p-4 max-w-xl space-y-3">
        <h2 className="text-lg font-semibold">Crea tenant</h2>
        <div>
          <label className="block text-sm">Nome</label>
          <input className="mt-1 w-full border rounded px-3 py-2" value={name} onChange={e=>setName(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm">Company code</label>
          <input className="mt-1 w-full border rounded px-3 py-2" value={companyCode} onChange={e=>setCompanyCode(e.target.value)} />
        </div>
        <button className="bg-black text-white rounded px-4 py-2" onClick={createTenant}>Crea</button>
        {out && <pre className="bg-gray-50 border rounded p-3 text-sm">{out}</pre>}
      </div>
    </Layout>
  )
}

