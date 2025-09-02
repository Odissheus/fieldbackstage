import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../modules/AuthContext'

export const Layout: React.FC<{ children: React.ReactNode }>= ({ children }) => {
  const { logout } = useAuth()
  const loc = useLocation()
  const links = [
    { to: '/dashboard', label: 'Dashboard' },
    { to: '/tenants', label: 'Tenant' },
    { to: '/lines', label: 'Linee' },
    { to: '/users', label: 'Utenti/Ruoli' },
    { to: '/jobs', label: 'Jobs' },
  ]
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
          <div className="font-semibold">Fieldback Landlord</div>
          <button className="text-sm text-red-600" onClick={logout}>Logout</button>
        </div>
      </header>
      <div className="max-w-6xl mx-auto px-4 py-6 grid md:grid-cols-[220px_1fr] gap-6">
        <nav className="md:sticky md:top-20 bg-white border rounded p-2 h-max">
          {links.map(l => (
            <Link key={l.to} to={l.to} className={`block px-3 py-2 rounded hover:bg-gray-100 ${loc.pathname===l.to?'bg-gray-100 font-medium':''}`}>{l.label}</Link>
          ))}
        </nav>
        <main>{children}</main>
      </div>
    </div>
  )
}

