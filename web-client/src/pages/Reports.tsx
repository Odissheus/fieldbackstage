import React, { useEffect, useState } from 'react'
import { Layout } from '../components/Layout'
import { apiFetch } from '../modules/api'

type Report = { id:string; weekId:string; productLineId:string; urlPdf?:string; urlHtml?:string; executiveSummary:string }

export const ReportsPage: React.FC = () => {
  const [items, setItems] = useState<Report[]>([])
  useEffect(() => { apiFetch('/reports').then(setItems).catch(()=>{}) }, [])
  return (
    <Layout>
      <div className="bg-white border rounded p-4">
        <h2 className="text-lg font-semibold mb-2">Report</h2>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left border-b">
              <th className="py-2">Settimana</th>
              <th>Linea</th>
              <th>Azioni</th>
            </tr>
          </thead>
          <tbody>
            {items.map(r => (
              <tr key={r.id} className="border-b">
                <td className="py-2">{r.weekId}</td>
                <td>{r.productLineId}</td>
                <td className="space-x-2">
                  {r.urlHtml && <a className="text-blue-600" href={r.urlHtml} target="_blank">HTML</a>}
                  {r.urlPdf && <a className="text-blue-600" href={r.urlPdf} target="_blank">PDF</a>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Layout>
  )
}

