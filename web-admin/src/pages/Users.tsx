import React, { useState } from 'react'
import { Layout } from '../components/Layout'
import { apiFetch } from '../modules/api'

export const UsersPage: React.FC = () => {
  const [userId, setUserId] = useState('user-1')
  const [email, setEmail] = useState('client@example.com')
  const [fullName, setFullName] = useState('User One')
  const [tenantId, setTenantId] = useState('')
  const [role, setRole] = useState('editor')
  const [username, setUsername] = useState('user1')
  const [password, setPassword] = useState('Password.1')
  const [out, setOut] = useState('')

  const createUser = async () => {
    const j = await apiFetch('/admin/users', { method: 'POST', body: JSON.stringify({ id: userId, email, fullName }) })
    setOut(JSON.stringify(j, null, 2))
  }

  const assignRole = async () => {
    if (!tenantId) return alert('Tenant mancante')
    const j = await apiFetch(`/admin/users/${userId}/roles`, { method: 'POST', body: JSON.stringify({ tenantId, role, username, password }) })
    setOut(JSON.stringify(j, null, 2))
  }

  return (
    <Layout>
      <div className="bg-white border rounded p-4 max-w-xl space-y-3">
        <h2 className="text-lg font-semibold">Utenti & Ruoli</h2>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm">User ID</label>
            <input className="mt-1 w-full border rounded px-3 py-2" value={userId} onChange={e=>setUserId(e.target.value)} />
          </div>
          <div>
            <label className="block text-sm">Email</label>
            <input className="mt-1 w-full border rounded px-3 py-2" value={email} onChange={e=>setEmail(e.target.value)} />
          </div>
          <div className="col-span-2">
            <label className="block text-sm">Nome completo</label>
            <input className="mt-1 w-full border rounded px-3 py-2" value={fullName} onChange={e=>setFullName(e.target.value)} />
          </div>
        </div>
        <button className="bg-black text-white rounded px-4 py-2" onClick={createUser}>Crea utente</button>

        <div className="h-px bg-gray-200" />
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm">Tenant Id</label>
            <input className="mt-1 w-full border rounded px-3 py-2" value={tenantId} onChange={e=>setTenantId(e.target.value)} />
          </div>
          <div>
            <label className="block text-sm">Ruolo</label>
            <input className="mt-1 w-full border rounded px-3 py-2" value={role} onChange={e=>setRole(e.target.value)} />
          </div>
          <div>
            <label className="block text-sm">Username</label>
            <input className="mt-1 w-full border rounded px-3 py-2" value={username} onChange={e=>setUsername(e.target.value)} />
          </div>
          <div>
            <label className="block text-sm">Password</label>
            <input className="mt-1 w-full border rounded px-3 py-2" value={password} onChange={e=>setPassword(e.target.value)} />
          </div>
        </div>
        <button className="border rounded px-4 py-2" onClick={assignRole}>Assegna ruolo e credenziali</button>
        {out && <pre className="bg-gray-50 border rounded p-3 text-sm mt-3">{out}</pre>}
      </div>
    </Layout>
  )
}

