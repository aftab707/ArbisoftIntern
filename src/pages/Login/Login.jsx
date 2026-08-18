import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '@/context/AuthContext.jsx'
import { ApiError } from '@/api/client.js'
import { validateLogin } from '@/utils/validateAuth.js'
import '@/pages/Auth.css'

const icons = {
  email: (
    <svg
      viewBox="0 0 24 24"
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <rect x="3" y="5" width="18" height="14" rx="2" />
      <path d="m4 7 8 6 8-6" />
    </svg>
  ),
  password: (
    <svg
      viewBox="0 0 24 24"
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <rect x="4" y="10" width="16" height="10" rx="2" />
      <path d="M8 10V7a4 4 0 0 1 8 0v3" />
    </svg>
  ),
}

const initialForm = { email: '', password: '' }

function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const redirectTo = location.state?.from?.pathname ?? '/tasks'

  const [form, setForm] = useState(initialForm)
  const [errors, setErrors] = useState({})
  const [apiError, setApiError] = useState('')
  const [status, setStatus] = useState('idle')

  function handleChange(event) {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setApiError('')
    const validationErrors = validateLogin(form)
    setErrors(validationErrors)
    if (Object.keys(validationErrors).length > 0) return

    setStatus('submitting')
    try {
      await login(form.email, form.password)
      navigate(redirectTo, { replace: true })
    } catch (error) {
      setApiError(
        error instanceof ApiError
          ? error.message
          : 'Something went wrong. Please try again.'
      )
      setStatus('idle')
    }
  }

  return (
    <section className="auth-page">
      <div className="container">
        <form
          className="card auth-card auth-form"
          noValidate
          onSubmit={handleSubmit}
        >
          <div className="auth-header">
            <span className="chip">Welcome back</span>
            <h1>Log in to TaskFlow</h1>
            <p>Manage your tasks and stay on top of your work.</p>
          </div>

          {apiError && <p className="form-banner-error">{apiError}</p>}

          <div className="form-field">
            <label htmlFor="email">Email</label>
            <div className="input-wrap">
              <span className="field-icon" aria-hidden="true">
                {icons.email}
              </span>
              <input
                id="email"
                name="email"
                type="email"
                value={form.email}
                onChange={handleChange}
                aria-invalid={Boolean(errors.email)}
                aria-describedby={errors.email ? 'email-error' : undefined}
                placeholder="you@example.com"
              />
            </div>
            {errors.email && (
              <p className="form-error" id="email-error">
                {errors.email}
              </p>
            )}
          </div>

          <div className="form-field">
            <label htmlFor="password">Password</label>
            <div className="input-wrap">
              <span className="field-icon" aria-hidden="true">
                {icons.password}
              </span>
              <input
                id="password"
                name="password"
                type="password"
                value={form.password}
                onChange={handleChange}
                aria-invalid={Boolean(errors.password)}
                aria-describedby={
                  errors.password ? 'password-error' : undefined
                }
                placeholder="••••••••"
              />
            </div>
            {errors.password && (
              <p className="form-error" id="password-error">
                {errors.password}
              </p>
            )}
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={status === 'submitting'}
          >
            {status === 'submitting' && (
              <span className="spinner" aria-hidden="true" />
            )}
            {status === 'submitting' ? 'Logging in…' : 'Log in'}
          </button>

          <p className="auth-switch">
            Don’t have an account? <Link to="/signup">Sign up</Link>
          </p>
        </form>
      </div>
    </section>
  )
}

export default Login
