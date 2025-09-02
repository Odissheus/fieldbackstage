import React, { useEffect, useMemo, useState } from 'react'
import { Layout } from '../components/Layout'
import { apiFetch } from '../modules/api'
import { useLocation } from 'react-router-dom'

type Insight = { id:string; productLineId:string; type:string; text?:string; createdAt?:string }

export const ExplorerPage: React.FC = () => {
  const loc = useLocation()
  const params = useMemo(() => new URLSearchParams(loc.search), [loc.search])
  const [items, setItems] = useState<Insight[]>([])
  const [productLineId, setProductLineId] = useState(params.get('productLineId') || '')
  const [q, setQ] = useState(params.get('q') || '')
  const [lines, setLines] = useState<Array<{id:string;name:string}>>([])

  const load = async () => {
    const params = new URLSearchParams()
    if (productLineId) params.set('productLineId', productLineId)
    if (q) params.set('q', q)
    const qs = params.toString() ? `?${params.toString()}` : ''
    const j = await apiFetch(`/insights${qs}`)
    setItems(j)
  }
  useEffect(() => { load().catch(()=>{}) }, [])
  useEffect(() => { apiFetch('/product-lines').then(setLines).catch(()=>{}) }, [])

  return (
    <Layout>
      <div className="space-y-3">
        <div className="bg-white border rounded p-4">
          <div className="flex gap-2 items-end flex-wrap">
            <div>
              <label className="block text-sm">Linea</label>
              <select className="mt-1 border rounded px-3 py-2" value={productLineId} onChange={e=>setProductLineId(e.target.value)}>
                <option value="">Tutte</option>
                {lines.map(l => <option key={l.id} value={l.id}>{l.name}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm">Testo</label>
              <input className="mt-1 border rounded px-3 py-2" value={q} onChange={e=>setQ(e.target.value)} />
            </div>
            <button className="border rounded px-4 py-2" onClick={load}>Cerca</button>
          </div>
        </div>
        <div className="bg-white border rounded p-4">
          <h2 className="text-lg font-semibold mb-2">Insight recenti</h2>
          <ul className="divide-y">
            {items.map(it => (
              <li key={it.id} className="py-2">
                <div className="text-sm text-gray-500">{it.createdAt} — {it.productLineId} — {it.type}</div>
                <div>{(it.text||'').slice(0,140)}</div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </Layout>
  )
}

