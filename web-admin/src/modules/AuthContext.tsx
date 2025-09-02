import React, { createContext, useContext, useEffect, useState } from 'react'
import { setToken as persistToken, getToken } from './api'

type AuthContextType = { token: string | null; login: (t: string) => void; logout: () => void }
const AuthContext = createContext<AuthContextType>({ token: null, login: () => {}, logout: () => {} })

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(getToken())
  useEffect(() => { persistToken(token) }, [token])
  return <AuthContext.Provider value={{ token, login: setToken, logout: () => setToken(null) }}>{children}</AuthContext.Provider>
}

export function useAuth() { return useContext(AuthContext) }

