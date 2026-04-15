import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'

export function PrivateRoute() {
  const { isAuthenticated, loading } = useAuth()

  if (loading) {
    return (
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh',
          background: '#f8f9fa',
          color: '#0d1b2a',
          fontSize: '1.1rem',
          fontFamily: 'system-ui, -apple-system, sans-serif',
        }}
      >
        <span style={{ marginRight: '10px' }}>&#10084;</span> Carregando CardioIA...
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return <Outlet />
}
