import React, { useState } from 'react'
import { apiFetch, setMeta } from '../modules/api'
import { useAuth } from '../modules/AuthContext'
import { useNavigate } from 'react-router-dom'

export const LoginPage: React.FC = () => {
  const [companyCode, setCompanyCode] = useState('ACME001')
  const [username, setUsername] = useState('user1')
  const [password, setPassword] = useState('Password.1')
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const r = await apiFetch('/auth/landing/login', { method: 'POST', body: JSON.stringify({ companyCode, username, password }) })
      login(r.accessToken)
      setMeta({ companyCode, username })
      navigate('/dashboard')
    } catch (err: any) { setError('Credenziali non valide') }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col">
      {/* Header */}
      <div className="text-center pt-12 pb-8 px-4">
        <div className="text-6xl mb-4">📊</div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Field Insights</h1>
        <p className="text-gray-600">App per venditori sul territorio</p>
      </div>

      {/* Login Form */}
      <div className="flex-1 flex items-center justify-center px-4">
        <form onSubmit={submit} className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-sm space-y-6">
          <div className="text-center">
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">Accedi</h2>
            <p className="text-gray-600 text-sm">Inserisci le tue credenziali</p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-3">
              <div className="flex items-center gap-2">
                <span className="text-red-500">⚠️</span>
                <span className="text-sm text-red-700">{error}</span>
              </div>
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                🏢 Codice Azienda
              </label>
              <input 
                className="w-full border-2 border-gray-200 rounded-lg px-4 py-3 text-lg focus:border-blue-500 focus:ring-0 transition-colors" 
                value={companyCode} 
                onChange={e=>setCompanyCode(e.target.value)}
                placeholder="es. ACME001"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                👤 Nome Utente
              </label>
              <input 
                className="w-full border-2 border-gray-200 rounded-lg px-4 py-3 text-lg focus:border-blue-500 focus:ring-0 transition-colors" 
                value={username} 
                onChange={e=>setUsername(e.target.value)}
                placeholder="Il tuo username"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                🔐 Password
              </label>
              <input 
                type="password" 
                className="w-full border-2 border-gray-200 rounded-lg px-4 py-3 text-lg focus:border-blue-500 focus:ring-0 transition-colors" 
                value={password} 
                onChange={e=>setPassword(e.target.value)}
                placeholder="••••••••"
              />
            </div>
          </div>

          <button 
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-lg py-4 font-bold text-lg transition-colors shadow-lg"
          >
            🚀 Accedi
          </button>

          <div className="text-center text-sm text-gray-500">
            <p>Problemi di accesso?</p>
            <button 
              type="button" 
              className="text-blue-600 hover:text-blue-700 font-medium"
              onClick={() => alert('Contatta il tuo amministratore per il reset password')}
            >
              Recupera password
            </button>
          </div>
        </form>
      </div>

      {/* Footer */}
      <div className="text-center text-xs text-gray-500 py-6 px-4">
        <p>React Field Insights v1.0</p>
        <p>🔒 Connessione sicura</p>
      </div>
    </div>
  )
}

