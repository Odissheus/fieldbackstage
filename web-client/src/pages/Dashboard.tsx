import React, { useEffect, useState } from 'react'
import { apiFetch } from '../modules/api'
import { Layout } from '../components/Layout'

type ReportItem = { id: string; weekId: string; productLineId: string; executiveSummary: string }
type ProductLine = { id: string; name: string }

export const DashboardPage: React.FC = () => {
  const [lines, setLines] = useState<ProductLine[]>([])
  const [reports, setReports] = useState<ReportItem[]>([])
  const [kpi, setKpi] = useState<{reports:number;contributors:number}>({reports:0,contributors:0})
  const [trend, setTrend] = useState<Array<{weekId:string;count:number}>>([])
  const [heatmap, setHeatmap] = useState<{bins:Array<{territoryName:string; value:number}>}>({bins:[]})

  useEffect(() => { apiFetch('/product-lines').then(setLines).catch(()=>{}) }, [])
  useEffect(() => { apiFetch('/reports').then(setReports).catch(()=>{}) }, [])
  useEffect(() => { apiFetch('/analytics/weekly').then((d:any)=>{ setKpi(d.kpi); setTrend(d.trend) }).catch(()=>{}) }, [])
  useEffect(() => { apiFetch('/analytics/heatmap').then((d:any)=> setHeatmap(d)).catch(()=>{}) }, [])

  return (
    <Layout>
      <div className="space-y-6">
        <div className="grid md:grid-cols-3 gap-4">
          <div className="bg-white border rounded p-4"><div className="text-sm text-gray-500">Linee</div><div className="text-2xl font-semibold">{lines.length}</div></div>
          <div className="bg-white border rounded p-4"><div className="text-sm text-gray-500">Report</div><div className="text-2xl font-semibold">{kpi.reports}</div></div>
          <div className="bg-white border rounded p-4"><div className="text-sm text-gray-500">Contributori</div><div className="text-2xl font-semibold">{kpi.contributors}</div></div>
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
        <div className="bg-white border rounded p-4">
          <h2 className="text-lg font-semibold mb-2">Ultimi report</h2>
          <ul className="divide-y">
            {reports.map(r => (
              <li key={r.id} className="py-2">{r.weekId} — {r.productLineId} — {r.executiveSummary.slice(0, 80)}</li>
            ))}
          </ul>
        </div>
      </div>
    </Layout>
  )
}

