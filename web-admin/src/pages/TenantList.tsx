import React, { useState, useEffect } from 'react'
import { Layout } from '../components/Layout'
import { apiFetch } from '../modules/api'

interface Tenant {
  id: string
  name: string
  companyCode: string
  createdAt: string
}

export const TenantListPage: React.FC = () => {
  const [tenants, setTenants] = useState<Tenant[]>([])
  const [loading, setLoading] = useState(true)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [name, setName] = useState('')
  const [companyCode, setCompanyCode] = useState('')
  const [creating, setCreating] = useState(false)

  const fetchTenants = async () => {
    try {
      setLoading(true)
      const data = await apiFetch('/admin/tenants')
      setTenants(data)
    } catch (error) {
      console.error('Error fetching tenants:', error)
    } finally {
      setLoading(false)
    }
  }

  const createTenant = async () => {
    if (!name.trim() || !companyCode.trim()) {
      alert('Inserire nome e company code')
      return
    }
    
    try {
      setCreating(true)
      await apiFetch('/admin/tenants', {
        method: 'POST',
        body: JSON.stringify({ name: name.trim(), companyCode: companyCode.trim() })
      })
      
      // Reset form
      setName('')
      setCompanyCode('')
      setShowCreateForm(false)
      
      // Refresh list
      await fetchTenants()
    } catch (error) {
      console.error('Error creating tenant:', error)
      alert('Errore durante la creazione del tenant')
    } finally {
      setCreating(false)
    }
  }

  useEffect(() => {
    fetchTenants()
  }, [])

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('it-IT', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">Lista Tenant</h1>
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
          >
            Crea Nuovo
          </button>
        </div>

        {showCreateForm && (
          <div className="bg-white border rounded-lg p-6 shadow-sm">
            <h2 className="text-lg font-semibold mb-4">Crea Nuovo Tenant</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nome
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Nome del tenant"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Company Code
                </label>
                <input
                  type="text"
                  value={companyCode}
                  onChange={(e) => setCompanyCode(e.target.value)}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Codice azienda (es. ACME001)"
                />
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={createTenant}
                  disabled={creating}
                  className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {creating ? 'Creazione...' : 'Crea'}
                </button>
                <button
                  onClick={() => {
                    setShowCreateForm(false)
                    setName('')
                    setCompanyCode('')
                  }}
                  className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 transition-colors"
                >
                  Annulla
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="bg-white border rounded-lg shadow-sm">
          {loading ? (
            <div className="p-8 text-center">
              <div className="text-gray-500">Caricamento tenant...</div>
            </div>
          ) : tenants.length === 0 ? (
            <div className="p-8 text-center">
              <div className="text-gray-500 mb-4">Nessun tenant trovato</div>
              <button
                onClick={() => setShowCreateForm(true)}
                className="text-blue-600 hover:text-blue-800 underline"
              >
                Crea il primo tenant
              </button>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Nome
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Company Code
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Data Creazione
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Azioni
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {tenants.map((tenant) => (
                    <tr key={tenant.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {tenant.name}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          {tenant.companyCode}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          {formatDate(tenant.createdAt)}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button className="text-blue-600 hover:text-blue-900 mr-3">
                          Modifica
                        </button>
                        <button className="text-red-600 hover:text-red-900">
                          Elimina
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </Layout>
  )
}
