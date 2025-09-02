import React from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom'
import { App } from './modules/App'
import './index.css'
import { AuthProvider, useAuth } from './modules/AuthContext'
import { LoginPage } from './pages/Login'
import { DashboardPage } from './pages/Dashboard'
import { ChangePasswordPage } from './pages/ChangePassword'
import { CapturePage } from './pages/Capture'
import { ExplorerPage } from './pages/Explorer'
import { CIPage } from './pages/CI'
import { ReportsPage } from './pages/Reports'
import { AdminDashboardPage } from './pages/AdminDashboard'

const RequireAuth: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { token } = useAuth()
  if (!token) return <Navigate to="/login" replace />
  return <>{children}</>
}

const router = createBrowserRouter([
  { path: '/', element: <Navigate to="/dashboard" replace /> },
  { path: '/login', element: <LoginPage /> },
  { path: '/dashboard', element: <RequireAuth><DashboardPage /></RequireAuth> },
  { path: '/change-password', element: <RequireAuth><ChangePasswordPage /></RequireAuth> },
  { path: '/capture', element: <RequireAuth><CapturePage /></RequireAuth> },
  { path: '/explorer', element: <RequireAuth><ExplorerPage /></RequireAuth> },
  { path: '/ci', element: <RequireAuth><CIPage /></RequireAuth> },
  { path: '/reports', element: <RequireAuth><ReportsPage /></RequireAuth> },
  { path: '/admin', element: <RequireAuth><AdminDashboardPage /></RequireAuth> },
])

createRoot(document.getElementById('root')!).render(
  <AuthProvider>
    <RouterProvider router={router} />
  </AuthProvider>
)

