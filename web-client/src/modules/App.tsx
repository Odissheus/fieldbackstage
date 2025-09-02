import React, { useState } from 'react'

type Presign = { url: string; fields: Record<string, string> }

export const App: React.FC = () => {
  const [companyCode, setCompanyCode] = useState<string>('ACME001')
  const [username, setUsername] = useState<string>('user1')
  const [password, setPassword] = useState<string>('Password.1')
  const [token, setToken] = useState<string>('')

  const [filename, setFilename] = useState<string>('photo.jpg')
  const [mime, setMime] = useState<string>('image/jpeg')
  const [presign, setPresign] = useState<Presign | null>(null)
  const [resetEmail, setResetEmail] = useState<string>('client@example.com')
  const [productLines, setProductLines] = useState<Array<{id:string;name:string}>>([])
  const [insightText, setInsightText] = useState<string>('Osservazione dal campo...')
  const [qaQuery, setQaQuery] = useState<string>('trend dosaggio')
  const [reports, setReports] = useState<Array<{id:string;weekId:string;productLineId:string;executiveSummary:string}>>([])

  const login = async () => {
    const r = await fetch('http://localhost:8000/v1/auth/landing/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ companyCode, username, password })
    })
    const j = await r.json()
    setToken(j.accessToken)
  }

  const requestPresign = async () => {
    const r = await fetch('http://localhost:8000/v1/upload/presign', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ filename, mime }),
    })
    const j = (await r.json()) as Presign
    setPresign(j)
  }

  const loadProductLines = async () => {
    const r = await fetch('http://localhost:8000/v1/product-lines', {
      headers: { Authorization: `Bearer ${token}` }
    })
    const j = await r.json()
    setProductLines(j)
  }

  const createInsight = async (productLineId?: string) => {
    if (!productLineId) return alert('Seleziona una linea')
    await fetch('http://localhost:8000/v1/insights', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ productLineId, territoryId: null, type: 'INSIGHT', text: insightText })
    })
    alert('Insight creato')
  }

  const runQA = async () => {
    const r = await fetch('http://localhost:8000/v1/qa', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ query: qaQuery })
    })
    const j = await r.json()
    alert(j.answer)
  }

  const loadReports = async () => {
    const r = await fetch('http://localhost:8000/v1/reports', {
      headers: { Authorization: `Bearer ${token}` }
    })
    const j = await r.json()
    setReports(j)
  }

  const resetPassword = async () => {
    const r = await fetch('http://localhost:8000/v1/auth/landing/reset-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ companyCode, username, email: resetEmail })
    })
    await r.json()
    alert('Se configurato, email inviata con password temporanea')
  }

  return (
    <div style={{ padding: 16, fontFamily: 'system-ui, Arial' }}>
      <h2>Client portal</h2>
      {!token ? (
        <div style={{ display: 'grid', gap: 8, maxWidth: 420 }}>
          <label>Codice azienda</label>
          <input value={companyCode} onChange={e => setCompanyCode(e.target.value)} />
          <label>Utente</label>
          <input value={username} onChange={e => setUsername(e.target.value)} />
          <label>Password</label>
          <input value={password} onChange={e => setPassword(e.target.value)} type="password" />
          <button onClick={login}>Entra</button>
          <div style={{ marginTop: 8 }}>
            <label>Email per reset</label>
            <input value={resetEmail} onChange={e => setResetEmail(e.target.value)} />
            <button onClick={resetPassword}>Password dimenticata</button>
          </div>
        </div>
      ) : (
        <div style={{ marginTop: 16, display: 'grid', gap: 8, maxWidth: 640 }}>
          <label>Filename</label>
          <input value={filename} onChange={e => setFilename(e.target.value)} />
          <label>Mime</label>
          <input value={mime} onChange={e => setMime(e.target.value)} />
          <button onClick={requestPresign}>Richiedi URL presignato</button>
          {presign && (
            <pre style={{ marginTop: 16, background: '#f5f5f5', padding: 12 }}>
              {JSON.stringify(presign, null, 2)}
            </pre>
          )}

          <h3>Linee</h3>
          <button onClick={loadProductLines}>Carica linee</button>
          <ul>
            {productLines.map(pl => (
              <li key={pl.id}>{pl.name} <button onClick={() => createInsight(pl.id)}>Aggiungi insight</button></li>
            ))}
          </ul>

          <h3>QA</h3>
          <input value={qaQuery} onChange={e => setQaQuery(e.target.value)} />
          <button onClick={runQA}>Chiedi</button>

          <h3>Report</h3>
          <button onClick={loadReports}>Carica report</button>
          <ul>
            {reports.map(r => (
              <li key={r.id}>{r.weekId} — {r.productLineId} — {r.executiveSummary.slice(0,60)}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

