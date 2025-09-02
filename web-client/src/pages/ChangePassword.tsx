import React, { useState } from 'react'
import { Layout } from '../components/Layout'
import { apiFetch, getMeta } from '../modules/api'

export const ChangePasswordPage: React.FC = () => {
  const meta = getMeta() || {}
  const [companyCode, setCompanyCode] = useState(meta.companyCode || '')
  const [username, setUsername] = useState(meta.username || '')
  const [oldPassword, setOldPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [msg, setMsg] = useState('')

  const submit = async () => {
    await apiFetch('/auth/landing/change-password', { method: 'POST', body: JSON.stringify({ companyCode, username, oldPassword, newPassword }) })
    setMsg('Password aggiornata')
  }

  return (
    <Layout>
      <div className="bg-white border rounded p-4 max-w-xl space-y-3">
        <h2 className="text-lg font-semibold">Cambio password</h2>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm">Codice azienda</label>
            <input className="mt-1 w-full border rounded px-3 py-2" value={companyCode} onChange={e=>setCompanyCode(e.target.value)} />
          </div>
          <div>
            <label className="block text-sm">Username</label>
            <input className="mt-1 w-full border rounded px-3 py-2" value={username} onChange={e=>setUsername(e.target.value)} />
          </div>
          <div>
            <label className="block text-sm">Password attuale</label>
            <input type="password" className="mt-1 w-full border rounded px-3 py-2" value={oldPassword} onChange={e=>setOldPassword(e.target.value)} />
          </div>
          <div>
            <label className="block text-sm">Nuova password</label>
            <input type="password" className="mt-1 w-full border rounded px-3 py-2" value={newPassword} onChange={e=>setNewPassword(e.target.value)} />
          </div>
        </div>
        <button className="bg-black text-white rounded px-4 py-2" onClick={submit}>Aggiorna</button>
        {msg && <div className="text-green-700">{msg}</div>}
      </div>
    </Layout>
  )
}

