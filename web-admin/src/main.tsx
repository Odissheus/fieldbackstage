import React from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom'
import { App } from './modules/App'
import './index.css'
import { AuthProvider, useAuth } from './modules/AuthContext'
import { LoginPage } from './pages/Login'
import { DashboardPage } from './pages/Dashboard'
import { TenantsPage } from './pages/Tenants'
import { ProductLinesPage } from './pages/ProductLines'
import { UsersPage } from './pages/Users'
import { JobsPage } from './pages/Jobs'

const RequireAuth: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { token } = useAuth()
  if (!token) return <Navigate to="/login" replace />
  return <>{children}</>
}

const router = createBrowserRouter([
  { path: '/', element: <Navigate to="/dashboard" replace /> },
  { path: '/login', element: <LoginPage /> },
  { path: '/dashboard', element: <RequireAuth><DashboardPage /></RequireAuth> },
  { path: '/tenants', element: <RequireAuth><TenantsPage /></RequireAuth> },
  { path: '/lines', element: <RequireAuth><ProductLinesPage /></RequireAuth> },
  { path: '/users', element: <RequireAuth><UsersPage /></RequireAuth> },
  { path: '/jobs', element: <RequireAuth><JobsPage /></RequireAuth> },
])

createRoot(document.getElementById('root')!).render(
  <AuthProvider>
    <RouterProvider router={router} />
  </AuthProvider>
)

