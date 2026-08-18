import { createContext, useCallback, useContext, useRef, useState } from 'react'
import '@/context/ToastContext.css'

const ToastContext = createContext(null)
let nextId = 0

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])
  const timers = useRef(new Map())

  const dismiss = useCallback((id) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id))
    clearTimeout(timers.current.get(id))
    timers.current.delete(id)
  }, [])

  const push = useCallback(
    (message, type = 'info', duration = 4000) => {
      const id = nextId++
      setToasts((prev) => [...prev, { id, message, type }])
      timers.current.set(
        id,
        setTimeout(() => dismiss(id), duration)
      )
    },
    [dismiss]
  )

  const value = {
    success: (message) => push(message, 'success'),
    error: (message) => push(message, 'error'),
    info: (message) => push(message, 'info'),
  }

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div className="toast-viewport" role="status" aria-live="polite">
        {toasts.map((toast) => (
          <div key={toast.id} className={`toast toast-${toast.type}`}>
            <span>{toast.message}</span>
            <button
              type="button"
              className="toast-dismiss"
              aria-label="Dismiss notification"
              onClick={() => dismiss(toast.id)}
            >
              ×
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}

export function useToast() {
  const context = useContext(ToastContext)
  if (!context) throw new Error('useToast must be used within a ToastProvider')
  return context
}
