import React, { useEffect, useState } from 'react'

type ReportItem = {
  id: string
  tenantId?: string | null
  productLineId: string
  weekId: string
  executiveSummary: string
  ciSummary?: string | null
  urlPdf?: string | null
  urlHtml?: string | null
}

export const App: React.FC = () => {
  const [token, setToken] = useState<string>('')
  const [username, setUsername] = useState<string>('fieldbackmaster')
  const [password, setPassword] = useState<string>('Leader.1986')
  const [tenantName, setTenantName] = useState<string>('Nuovo Cliente')
  const [companyCode, setCompanyCode] = useState<string>('ACME001')
  const [tenantId, setTenantId] = useState<string>('')
  const [message, setMessage] = useState<string>('')

  // Create user
  const [newUserId, setNewUserId] = useState<string>('user-1')
  const [newUserEmail, setNewUserEmail] = useState<string>('client@example.com')
  const [newUserName, setNewUserName] = useState<string>('User One')

  // Assign role/credentials
  const [assignUserId, setAssignUserId] = useState<string>('user-1')
  const [assignRole, setAssignRole] = useState<string>('editor')
  const [assignUsername, setAssignUsername] = useState<string>('user1')
  const [assignPassword, setAssignPassword] = useState<string>('Password.1')
  const [productLineName, setProductLineName] = useState<string>('Linea A')

  const login = async () => {
    const r = await fetch('http://localhost:8000/v1/auth/landlord/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
    const j = await r.json()
    setToken(j.accessToken)
  }

  const createTenant = async () => {
    const r = await fetch('http://localhost:8000/v1/admin/tenants', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ name: tenantName, companyCode })
    })
    const j = await r.json()
    setTenantId(j.id)
    setMessage(JSON.stringify(j))
  }

  const createProductLine = async () => {
    if (!tenantId) return alert('Crea prima un tenant')
    const r = await fetch(`http://localhost:8000/v1/admin/tenants/${tenantId}/product-lines`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ name: productLineName })
    })
    const j = await r.json()
    setMessage(JSON.stringify(j))
  }

  const createUser = async () => {
    const r = await fetch('http://localhost:8000/v1/admin/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ id: newUserId, email: newUserEmail, fullName: newUserName })
    })
    const j = await r.json()
    setMessage(JSON.stringify(j))
  }

  const assignRoleCreds = async () => {
    if (!tenantId) return alert('Tenant mancante')
    const r = await fetch(`http://localhost:8000/v1/admin/users/${assignUserId}/roles`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ tenantId, role: assignRole, username: assignUsername, password: assignPassword })
    })
    const j = await r.json()
    setMessage(JSON.stringify(j))
  }

  return (
    <div style={{ padding: 16, fontFamily: 'system-ui, Arial' }}>
      <h2>Landlord console</h2>
      {!token ? (
        <div style={{ display: 'grid', gap: 8, maxWidth: 420 }}>
          <label>Username</label>
          <input value={username} onChange={e => setUsername(e.target.value)} />
          <label>Password</label>
          <input value={password} onChange={e => setPassword(e.target.value)} type="password" />
          <button onClick={login}>Login</button>
        </div>
      ) : (
        <div style={{ display: 'grid', gap: 8, maxWidth: 560 }}>
          <h3>Crea Tenant</h3>
          <label>Nome</label>
          <input value={tenantName} onChange={e => setTenantName(e.target.value)} />
          <label>Company code</label>
          <input value={companyCode} onChange={e => setCompanyCode(e.target.value)} />
          <button onClick={createTenant}>Crea</button>

          <h3>Linea di venditori</h3>
          <label>Nome linea</label>
          <input value={productLineName} onChange={e => setProductLineName(e.target.value)} />
          <button onClick={createProductLine}>Crea linea per Tenant corrente</button>

          <h3>Utente cliente</h3>
          <label>User ID</label>
          <input value={newUserId} onChange={e => setNewUserId(e.target.value)} />
          <label>Email</label>
          <input value={newUserEmail} onChange={e => setNewUserEmail(e.target.value)} />
          <label>Nome completo</label>
          <input value={newUserName} onChange={e => setNewUserName(e.target.value)} />
          <button onClick={createUser}>Crea utente</button>

          <h3>Assegna ruolo e credenziali</h3>
          <label>User ID</label>
          <input value={assignUserId} onChange={e => setAssignUserId(e.target.value)} />
          <label>Ruolo (super_admin/admin/editor/viewer)</label>
          <input value={assignRole} onChange={e => setAssignRole(e.target.value)} />
          <label>Username</label>
          <input value={assignUsername} onChange={e => setAssignUsername(e.target.value)} />
          <label>Password</label>
          <input value={assignPassword} onChange={e => setAssignPassword(e.target.value)} />
          <button onClick={assignRoleCreds}>Assegna</button>
          {message && <pre style={{ background: '#f5f5f5', padding: 12 }}>{message}</pre>}
        </div>
      )}
    </div>
  )
}

