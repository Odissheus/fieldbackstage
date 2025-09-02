import { useEffect, useState } from 'react'
import { apiFetch } from './api'

export function useProfile() {
  const [role, setRole] = useState<string>('')
  useEffect(() => { apiFetch('/auth/me').then((j:any)=> setRole(j.role || '')).catch(()=>{}) }, [])
  return { role }
}

