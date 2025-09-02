import React from 'react'
import { Layout } from '../components/Layout'

export const DashboardPage: React.FC = () => {
  return (
    <Layout>
      <div className="grid md:grid-cols-3 gap-4">
        <div className="bg-white border rounded p-4">
          <div className="text-sm text-gray-500">Tenant</div>
          <div className="text-2xl font-semibold">Gestione</div>
        </div>
        <div className="bg-white border rounded p-4">
          <div className="text-sm text-gray-500">Linee</div>
          <div className="text-2xl font-semibold">Setup</div>
        </div>
        <div className="bg-white border rounded p-4">
          <div className="text-sm text-gray-500">Utenti</div>
          <div className="text-2xl font-semibold">Provisioning</div>
        </div>
      </div>
    </Layout>
  )
}

