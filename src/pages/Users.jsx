import { useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext.jsx'
import { api, ApiError } from '../api/client.js'
import './Users.css'

function Users() {
  const { user: currentUser } = useAuth()
  const [users, setUsers] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [updatingId, setUpdatingId] = useState(null)

  useEffect(() => {
    api
      .listUsers()
      .then(setUsers)
      .catch((err) =>
        setError(
          err instanceof ApiError ? err.message : 'Could not load users.'
        )
      )
      .finally(() => setIsLoading(false))
  }, [])

  async function handleRoleChange(userId, role) {
    setUpdatingId(userId)
    setError('')
    try {
      const updated = await api.updateUserRole(userId, role)
      setUsers((prev) => prev.map((u) => (u.id === userId ? updated : u)))
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not update role.')
    } finally {
      setUpdatingId(null)
    }
  }

  return (
    <section className="container users-page">
      <span className="chip">Admin</span>
      <h1>Users</h1>
      <p>Manage who has admin access to TaskFlow.</p>

      {isLoading && <p>Loading users…</p>}
      {error && <p className="form-banner-error">{error}</p>}

      {!isLoading && (
        <div className="card users-table-wrap">
          <table className="users-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>{user.name}</td>
                  <td>{user.email}</td>
                  <td>
                    <span className={`badge badge-role-${user.role}`}>
                      {user.role}
                    </span>
                  </td>
                  <td>
                    <button
                      type="button"
                      className="btn btn-secondary"
                      disabled={
                        user.id === currentUser.id || updatingId === user.id
                      }
                      onClick={() =>
                        handleRoleChange(
                          user.id,
                          user.role === 'admin' ? 'user' : 'admin'
                        )
                      }
                    >
                      {updatingId === user.id
                        ? 'Updating…'
                        : user.role === 'admin'
                          ? 'Revoke admin'
                          : 'Make admin'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}

export default Users
