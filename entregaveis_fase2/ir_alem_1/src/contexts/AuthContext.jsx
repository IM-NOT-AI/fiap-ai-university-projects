import { createContext, useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  loginService,
  logoutService,
  getStoredToken,
  getStoredUser,
  isTokenValid,
} from '../services/authService'

export const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    const storedToken = getStoredToken()
    const storedUser = getStoredUser()

    if (storedToken && isTokenValid(storedToken) && storedUser) {
      setToken(storedToken)
      setUser(storedUser)
    } else {
      logoutService()
    }

    setLoading(false)
  }, [])

  const login = useCallback(async (username, password) => {
    const result = await loginService(username, password)
    setToken(result.token)
    setUser(result.user)
    return result
  }, [])

  const logout = useCallback(() => {
    logoutService()
    setToken(null)
    setUser(null)
    navigate('/login', { replace: true })
  }, [navigate])

  const isAuthenticated = Boolean(token && user && isTokenValid(token))

  const value = {
    user,
    token,
    loading,
    isAuthenticated,
    login,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
