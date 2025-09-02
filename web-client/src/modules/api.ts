export const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/v1'

export function getToken(): string | null {
  return localStorage.getItem('accessToken')
}

export function setToken(token: string | null) {
  if (token) localStorage.setItem('accessToken', token)
  else localStorage.removeItem('accessToken')
}

export function setMeta(meta: Record<string, string>) {
  localStorage.setItem('meta', JSON.stringify({ ...(getMeta()||{}), ...meta }))
}

export function getMeta(): Record<string, string> | null {
  const s = localStorage.getItem('meta'); if (!s) return null
  try { return JSON.parse(s) } catch { return null }
}

export async function apiFetch(path: string, init: RequestInit = {}) {
  const headers: Record<string, string> = { 'Content-Type': 'application/json', ...(init.headers as any) }
  const token = getToken()
  if (token) headers.Authorization = `Bearer ${token}`
  const res = await fetch(`${API_BASE}${path}`, { ...init, headers })
  if (!res.ok) throw new Error(await res.text())
  const ct = res.headers.get('content-type') || ''
  return ct.includes('application/json') ? res.json() : res.text()
}

