import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuth } from '@/context/AuthContext.jsx'

export function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuth()
  const location = useLocation()

  if (isLoading) return null
  if (!isAuthenticated)
    return <Navigate to="/login" state={{ from: location }} replace />

  return <Outlet />
}

export function AdminRoute() {
  const { isAdmin, isLoading } = useAuth()

  if (isLoading) return null
  if (!isAdmin) return <Navigate to="/tasks" replace />

  return <Outlet />
}
