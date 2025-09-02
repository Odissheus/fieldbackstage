import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../modules/AuthContext'
import { useProfile } from '../modules/Profile'

export const Layout: React.FC<{ children: React.ReactNode }>= ({ children }) => {
  const { logout } = useAuth()
  const loc = useLocation()
  const { role } = useProfile()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  
  const links = [
    { to: '/dashboard', label: '📊 Dashboard', icon: '📊' },
    { to: '/capture', label: '📱 Cattura', icon: '📱' },
    { to: '/explorer', label: '🔍 Explorer', icon: '🔍' },
    { to: '/ci', label: '🎯 CI', icon: '🎯' },
    { to: '/reports', label: '📋 Report', icon: '📋' },
    { to: '/admin', label: '⚙️ Admin', icon: '⚙️' },
    { to: '/change-password', label: '🔐 Password', icon: '🔐' },
  ]
  
  const visible = (l: {to:string;label:string}) => {
    if (l.to === '/admin') return role === 'admin' || role === 'editor'
    return true
  }

  const visibleLinks = links.filter(visible)
  
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile Header */}
      <header className="bg-white border-b sticky top-0 z-50 shadow-sm">
        <div className="px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="font-bold text-lg text-gray-900">📊 Field Insights</div>
          </div>
          
          <div className="flex items-center gap-2">
            {/* Mobile Menu Button */}
            <button 
              className="md:hidden p-2 rounded-lg hover:bg-gray-100"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              <div className="w-6 h-6 flex flex-col justify-center space-y-1">
                <div className={`w-6 h-0.5 bg-gray-600 transition-all ${mobileMenuOpen ? 'rotate-45 translate-y-1.5' : ''}`}></div>
                <div className={`w-6 h-0.5 bg-gray-600 transition-all ${mobileMenuOpen ? 'opacity-0' : ''}`}></div>
                <div className={`w-6 h-0.5 bg-gray-600 transition-all ${mobileMenuOpen ? '-rotate-45 -translate-y-1.5' : ''}`}></div>
              </div>
            </button>
            
            <button className="text-sm text-red-600 font-medium px-3 py-1 rounded-lg hover:bg-red-50" onClick={logout}>
              Logout
            </button>
          </div>
        </div>
        
        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t bg-white">
            <nav className="px-4 py-2 space-y-1">
              {visibleLinks.map(l => (
                <Link 
                  key={l.to} 
                  to={l.to} 
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    loc.pathname === l.to 
                      ? 'bg-blue-50 text-blue-700 font-medium' 
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <span className="text-lg">{l.icon}</span>
                  <span>{l.label.split(' ').slice(1).join(' ')}</span>
                </Link>
              ))}
            </nav>
          </div>
        )}
      </header>

      <div className="flex">
        {/* Desktop Sidebar */}
        <nav className="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0 md:pt-16">
          <div className="flex-1 bg-white border-r shadow-sm overflow-y-auto">
            <div className="px-4 py-6 space-y-2">
              {visibleLinks.map(l => (
                <Link 
                  key={l.to} 
                  to={l.to} 
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    loc.pathname === l.to 
                      ? 'bg-blue-50 text-blue-700 font-medium border border-blue-200' 
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <span className="text-lg">{l.icon}</span>
                  <span>{l.label.split(' ').slice(1).join(' ')}</span>
                </Link>
              ))}
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="flex-1 md:pl-64">
          {children}
        </main>
      </div>

      {/* Mobile Bottom Navigation for Key Actions */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t shadow-lg">
        <div className="flex">
          <Link 
            to="/capture" 
            className={`flex-1 flex flex-col items-center py-3 px-2 ${
              loc.pathname === '/capture' ? 'text-blue-600' : 'text-gray-600'
            }`}
          >
            <span className="text-xl mb-1">📱</span>
            <span className="text-xs font-medium">Cattura</span>
          </Link>
          <Link 
            to="/dashboard" 
            className={`flex-1 flex flex-col items-center py-3 px-2 ${
              loc.pathname === '/dashboard' ? 'text-blue-600' : 'text-gray-600'
            }`}
          >
            <span className="text-xl mb-1">📊</span>
            <span className="text-xs font-medium">Dashboard</span>
          </Link>
          <Link 
            to="/reports" 
            className={`flex-1 flex flex-col items-center py-3 px-2 ${
              loc.pathname === '/reports' ? 'text-blue-600' : 'text-gray-600'
            }`}
          >
            <span className="text-xl mb-1">📋</span>
            <span className="text-xs font-medium">Report</span>
          </Link>
          <Link 
            to="/ci" 
            className={`flex-1 flex flex-col items-center py-3 px-2 ${
              loc.pathname === '/ci' ? 'text-blue-600' : 'text-gray-600'
            }`}
          >
            <span className="text-xl mb-1">🎯</span>
            <span className="text-xs font-medium">CI</span>
          </Link>
        </div>
      </div>

      {/* Bottom padding for mobile navigation */}
      <div className="md:hidden h-20"></div>
    </div>
  )
}

