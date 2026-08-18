import { createContext, useContext, useEffect, useState } from 'react'
import { api, TOKEN_STORAGE_KEY } from '@/api/client.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const token = window.localStorage.getItem(TOKEN_STORAGE_KEY)
    if (!token) {
      setIsLoading(false)
      return
    }

    api
      .me()
      .then(setUser)
      .catch(() => {
        window.localStorage.removeItem(TOKEN_STORAGE_KEY)
        setUser(null)
      })
      .finally(() => setIsLoading(false))
  }, [])

  useEffect(() => {
    function handleUnauthorized() {
      window.localStorage.removeItem(TOKEN_STORAGE_KEY)
      setUser(null)
    }

    window.addEventListener('taskflow:unauthorized', handleUnauthorized)
    return () =>
      window.removeEventListener('taskflow:unauthorized', handleUnauthorized)
  }, [])

  async function login(email, password) {
    const { access_token: token } = await api.login({ email, password })
    window.localStorage.setItem(TOKEN_STORAGE_KEY, token)
    const currentUser = await api.me()
    setUser(currentUser)
    return currentUser
  }

  async function register(name, email, password) {
    await api.register({ name, email, password })
    return login(email, password)
  }

  function logout() {
    window.localStorage.removeItem(TOKEN_STORAGE_KEY)
    setUser(null)
  }

  const value = {
    user,
    isLoading,
    isAuthenticated: Boolean(user),
    isAdmin: user?.role === 'admin',
    login,
    register,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within an AuthProvider')
  return context
}
