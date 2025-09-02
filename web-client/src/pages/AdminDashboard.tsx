import React, { useEffect, useState } from 'react'
import { Layout } from '../components/Layout'
import { apiFetch } from '../modules/api'

type ProductLine = { id:string; name:string }

export const AdminDashboardPage: React.FC = () => {
  const [lines, setLines] = useState<ProductLine[]>([])
  const [lineId, setLineId] = useState('')
  const [kpi, setKpi] = useState<{reports:number;contributors:number}>({reports:0,contributors:0})
  const [trend, setTrend] = useState<Array<{weekId:string;count:number}>>([])
  const [heatmap, setHeatmap] = useState<{bins:Array<{territoryName:string; value:number}>}>({bins:[]})

  useEffect(() => { apiFetch('/product-lines').then(setLines).catch(()=>{}) }, [])
  useEffect(() => {
    const qs = lineId ? `?productLineId=${encodeURIComponent(lineId)}` : ''
    apiFetch(`/analytics/weekly${qs}`).then((d:any)=>{ setKpi(d.kpi); setTrend(d.trend) }).catch(()=>{})
    apiFetch(`/analytics/heatmap${qs}`).then((d:any)=> setHeatmap(d)).catch(()=>{})
  }, [lineId])

  return (
    <Layout>
      <div className="space-y-4">
        <div className="bg-white border rounded p-4 flex gap-3 items-end">
          <div>
            <label className="block text-sm">Linea</label>
            <select className="mt-1 border rounded px-3 py-2" value={lineId} onChange={e=>setLineId(e.target.value)}>
              <option value="">Tutte</option>
              {lines.map(l => <option key={l.id} value={l.id}>{l.name}</option>)}
            </select>
          </div>
        </div>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="bg-white border rounded p-4"><div className="text-sm text-gray-500">Report</div><div className="text-2xl font-semibold">{kpi.reports}</div></div>
          <div className="bg-white border rounded p-4"><div className="text-sm text-gray-500">Contributori</div><div className="text-2xl font-semibold">{kpi.contributors}</div></div>
          <div className="bg-white border rounded p-4"><div className="text-sm text-gray-500">Linee</div><div className="text-2xl font-semibold">{lines.length}</div></div>
        </div>
        {trend.length>0 && (
          <div className="bg-white border rounded p-4">
            <h2 className="text-lg font-semibold mb-2">Trend 8 settimane</h2>
            <div className="flex gap-2 items-end">
              {trend.map(t => (
                <div key={t.weekId} className="w-10 bg-blue-500/20 text-center" style={{ height: 20 + t.count*10 }} title={t.weekId}>{/* bar */}</div>
              ))}
            </div>
          </div>
        )}
        {heatmap.bins.length>0 && (
          <div className="bg-white border rounded p-4">
            <h2 className="text-lg font-semibold mb-2">Heatmap territori</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
              {heatmap.bins.map(b => (
                <div key={b.territoryName} className="border rounded p-2 flex items-center justify-between">
                  <div className="text-sm">{b.territoryName}</div>
                  <div className="text-sm font-semibold">{b.value}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </Layout>
  )
}

