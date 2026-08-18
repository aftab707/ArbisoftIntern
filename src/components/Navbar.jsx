import { useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'
import ThemeToggle from './ThemeToggle.jsx'
import './Navbar.css'

const publicLinks = [
  { to: '/', label: 'Home' },
  { to: '/about', label: 'About' },
  { to: '/contact', label: 'Contact' },
]

function Navbar() {
  const [open, setOpen] = useState(false)
  const { user, isAuthenticated, isAdmin, logout } = useAuth()

  function handleLogout() {
    // Logging out while on a protected route (e.g. /tasks) makes
    // ProtectedRoute redirect to /login on its own — no need to navigate
    // here too, and racing it with a manual navigate() is what caused
    // the destination to end up wrong.
    logout()
    setOpen(false)
  }

  const links = [
    ...publicLinks,
    ...(isAuthenticated ? [{ to: '/tasks', label: 'Tasks' }] : []),
    ...(isAdmin ? [{ to: '/users', label: 'Users' }] : []),
  ]

  return (
    <header className="navbar">
      <div className="navbar-inner container">
        <Link to="/" className="navbar-brand" onClick={() => setOpen(false)}>
          <span className="navbar-mark" aria-hidden="true">
            T
          </span>
          TaskFlow
        </Link>

        <button
          type="button"
          className="navbar-toggle"
          aria-label="Toggle navigation menu"
          aria-expanded={open}
          onClick={() => setOpen((prev) => !prev)}
        >
          <span />
          <span />
          <span />
        </button>

        <div className={`navbar-menu${open ? ' is-open' : ''}`}>
          <ul className="navbar-links">
            {links.map(({ to, label }) => (
              <li key={to}>
                <NavLink
                  to={to}
                  end={to === '/'}
                  className={({ isActive }) =>
                    isActive ? 'navbar-link active' : 'navbar-link'
                  }
                  onClick={() => setOpen(false)}
                >
                  {label}
                </NavLink>
              </li>
            ))}
          </ul>

          <div className="navbar-auth">
            {isAuthenticated ? (
              <>
                <span className="navbar-user">
                  {user.name}
                  <span className="badge badge-role-user navbar-role-badge">
                    {user.role}
                  </span>
                </span>
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={handleLogout}
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="btn btn-secondary"
                  onClick={() => setOpen(false)}
                >
                  Log in
                </Link>
                <Link
                  to="/signup"
                  className="btn btn-primary"
                  onClick={() => setOpen(false)}
                >
                  Sign up
                </Link>
              </>
            )}
          </div>

          <ThemeToggle />
        </div>
      </div>
    </header>
  )
}

export default Navbar
