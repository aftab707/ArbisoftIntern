import { useState } from 'react'
import { validateContact } from '../utils/validateContact.js'
import './Contact.css'

const initialForm = { name: '', email: '', message: '' }

const icons = {
  name: (
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
      <circle cx="12" cy="8" r="4" />
      <path d="M4 20c0-4 3.5-6 8-6s8 2 8 6" />
    </svg>
  ),
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
  message: (
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
      <path d="M4 5h16v11H8l-4 4z" />
    </svg>
  ),
}

function Contact() {
  const [form, setForm] = useState(initialForm)
  const [errors, setErrors] = useState({})
  const [status, setStatus] = useState('idle')

  function handleChange(event) {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  function handleSubmit(event) {
    event.preventDefault()
    const validationErrors = validateContact(form)
    setErrors(validationErrors)

    if (Object.keys(validationErrors).length > 0) {
      setStatus('idle')
      return
    }

    setStatus('submitting')
    window.setTimeout(() => {
      setStatus('success')
      setForm(initialForm)
    }, 400)
  }

  if (status === 'success') {
    return (
      <section className="contact-page">
        <div className="container">
          <div className="success-card">
            <span className="success-icon" aria-hidden="true">
              <svg
                viewBox="0 0 24 24"
                width="28"
                height="28"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.4"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M5 12l5 5 9-9" />
              </svg>
            </span>
            <h2>Thanks! Your message has been sent.</h2>
            <p>I’ll get back to you as soon as possible.</p>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => setStatus('idle')}
            >
              Send another message
            </button>
          </div>
        </div>
      </section>
    )
  }

  return (
    <section className="contact-page">
      <div className="container contact-grid">
        <div className="contact-info">
          <span className="chip">Contact</span>
          <h1>Let’s talk</h1>
          <p>
            Have a question about this project? Send a message and I’ll get back
            to you.
          </p>
        </div>

        <form className="card contact-form" noValidate onSubmit={handleSubmit}>
          <div className="form-field">
            <label htmlFor="name">Name</label>
            <div className="input-wrap">
              <span className="field-icon" aria-hidden="true">
                {icons.name}
              </span>
              <input
                id="name"
                name="name"
                type="text"
                value={form.name}
                onChange={handleChange}
                aria-invalid={Boolean(errors.name)}
                aria-describedby={errors.name ? 'name-error' : undefined}
                placeholder="Your name"
              />
            </div>
            {errors.name && (
              <p className="form-error" id="name-error">
                {errors.name}
              </p>
            )}
          </div>

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
            <label htmlFor="message">Message</label>
            <div className="input-wrap input-wrap-textarea">
              <span className="field-icon" aria-hidden="true">
                {icons.message}
              </span>
              <textarea
                id="message"
                name="message"
                rows="5"
                value={form.message}
                onChange={handleChange}
                aria-invalid={Boolean(errors.message)}
                aria-describedby={errors.message ? 'message-error' : undefined}
                placeholder="How can I help?"
              />
            </div>
            {errors.message && (
              <p className="form-error" id="message-error">
                {errors.message}
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
            {status === 'submitting' ? 'Sending…' : 'Send message'}
          </button>
        </form>
      </div>
    </section>
  )
}

export default Contact
