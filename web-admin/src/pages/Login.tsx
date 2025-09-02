import React, { useState } from 'react'
import { apiFetch } from '../modules/api'
import { useAuth } from '../modules/AuthContext'
import { useNavigate } from 'react-router-dom'

export const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('fieldbackmaster')
  const [password, setPassword] = useState('Leader.1986')
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const r = await apiFetch('/auth/landlord/login', { method: 'POST', body: JSON.stringify({ username, password }) })
      login(r.accessToken)
      navigate('/dashboard')
    } catch (err: any) { setError('Credenziali non valide') }
  }

  return (
    <div className="min-h-screen grid place-items-center bg-gray-50">
      <form onSubmit={submit} className="bg-white p-6 rounded border w-[360px] space-y-4">
        <h1 className="text-xl font-semibold">Landlord Login</h1>
        {error && <div className="text-sm text-red-600">{error}</div>}
        <div>
          <label className="block text-sm">Username</label>
          <input className="mt-1 w-full border rounded px-3 py-2" value={username} onChange={e=>setUsername(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm">Password</label>
          <input type="password" className="mt-1 w-full border rounded px-3 py-2" value={password} onChange={e=>setPassword(e.target.value)} />
        </div>
        <button className="w-full bg-black text-white rounded py-2">Entra</button>
      </form>
    </div>
  )
}

