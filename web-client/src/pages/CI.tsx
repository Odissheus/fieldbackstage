import React, { useEffect, useState } from 'react'
import { Layout } from '../components/Layout'
import { apiFetch } from '../modules/api'

type Insight = { id:string; photoUrl?:string; text?:string }

export const CIPage: React.FC = () => {
  const [items, setItems] = useState<Insight[]>([])
  const [query, setQuery] = useState('claim X')
  const [answer, setAnswer] = useState('')

  const load = async () => {
    const j = await apiFetch('/insights?type=CI')
    setItems(j)
  }
  useEffect(() => { load().catch(()=>{}) }, [])

  const ask = async () => {
    const j = await apiFetch('/qa', { method:'POST', body: JSON.stringify({ query, includeCI: true }) })
    setAnswer(j.answer)
  }

  return (
    <Layout>
      <div className="grid md:grid-cols-[2fr_1fr] gap-4">
        <div className="bg-white border rounded p-4">
          <h2 className="text-lg font-semibold mb-2">CI Gallery</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
            {items.map(it => (
              <div key={it.id} className="border rounded p-2">
                {it.photoUrl ? (<div className="aspect-video bg-gray-100 flex items-center justify-center text-xs">img</div>) : null}
                <div className="text-sm mt-1">{(it.text||'').slice(0,120)}</div>
              </div>
            ))}
          </div>
        </div>
        <div className="bg-white border rounded p-4">
          <h2 className="text-lg font-semibold mb-2">Chatbot CI</h2>
          <input className="border rounded px-3 py-2 w-full" value={query} onChange={e=>setQuery(e.target.value)} />
          <button className="mt-2 bg-black text-white rounded px-4 py-2" onClick={ask}>Chiedi</button>
          {answer && <div className="mt-3 text-sm bg-gray-50 border rounded p-2">{answer}</div>}
        </div>
      </div>
    </Layout>
  )
}

