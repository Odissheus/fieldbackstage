import React, { useState } from 'react'
import { Layout } from '../components/Layout'
import { apiFetch } from '../modules/api'

export const ProductLinesPage: React.FC = () => {
  const [tenantId, setTenantId] = useState('')
  const [name, setName] = useState('Linea A')
  const [out, setOut] = useState('')

  const createLine = async () => {
    if (!tenantId) return alert('Tenant mancante')
    const j = await apiFetch(`/admin/tenants/${tenantId}/product-lines`, { method: 'POST', body: JSON.stringify({ name }) })
    setOut(JSON.stringify(j, null, 2))
  }

  const listLines = async () => {
    if (!tenantId) return alert('Tenant mancante')
    const j = await apiFetch(`/admin/tenants/${tenantId}/product-lines`)
    setOut(JSON.stringify(j, null, 2))
  }

  return (
    <Layout>
      <div className="bg-white border rounded p-4 max-w-xl space-y-3">
        <h2 className="text-lg font-semibold">Linee</h2>
        <div>
          <label className="block text-sm">Tenant Id</label>
          <input className="mt-1 w-full border rounded px-3 py-2" value={tenantId} onChange={e=>setTenantId(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm">Nome linea</label>
          <input className="mt-1 w-full border rounded px-3 py-2" value={name} onChange={e=>setName(e.target.value)} />
        </div>
        <div className="flex gap-2">
          <button className="bg-black text-white rounded px-4 py-2" onClick={createLine}>Crea</button>
          <button className="border rounded px-4 py-2" onClick={listLines}>Elenca</button>
        </div>
        {out && <pre className="bg-gray-50 border rounded p-3 text-sm">{out}</pre>}
      </div>
    </Layout>
  )
}

