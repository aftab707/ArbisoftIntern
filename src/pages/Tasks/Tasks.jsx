import { useEffect, useState } from 'react'
import { useAuth } from '../../context/AuthContext.jsx'
import { useToast } from '../../context/ToastContext.jsx'
import { api, ApiError } from '../../api/client.js'
import './Tasks.css'

const STATUS_OPTIONS = ['pending', 'in_progress', 'done']
const PRIORITY_OPTIONS = ['low', 'medium', 'high']
const initialForm = {
  title: '',
  description: '',
  status: 'pending',
  priority: 'medium',
}

function TaskForm({ initialValues, submitLabel, onSubmit, onCancel }) {
  const [form, setForm] = useState(initialValues)
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  function handleChange(event) {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    if (!form.title.trim()) {
      setError('Title is required.')
      return
    }
    setError('')
    setIsSubmitting(true)
    try {
      await onSubmit(form)
    } catch (submitError) {
      setError(
        submitError instanceof ApiError
          ? submitError.message
          : 'Something went wrong.'
      )
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      {error && <p className="form-error">{error}</p>}
      <div className="task-form-row">
        <input
          name="title"
          value={form.title}
          onChange={handleChange}
          placeholder="Task title"
          aria-label="Task title"
        />
        <select name="priority" value={form.priority} onChange={handleChange}>
          {PRIORITY_OPTIONS.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
        <select name="status" value={form.status} onChange={handleChange}>
          {STATUS_OPTIONS.map((option) => (
            <option key={option} value={option}>
              {option.replace('_', ' ')}
            </option>
          ))}
        </select>
      </div>
      <textarea
        name="description"
        value={form.description ?? ''}
        onChange={handleChange}
        placeholder="Description (optional)"
        rows="2"
      />
      <div className="task-form-actions">
        <button
          type="submit"
          className="btn btn-primary"
          disabled={isSubmitting}
        >
          {isSubmitting && <span className="spinner" aria-hidden="true" />}
          {submitLabel}
        </button>
        {onCancel && (
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onCancel}
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  )
}

function Tasks() {
  const { user } = useAuth()
  const toast = useToast()
  const [tasks, setTasks] = useState([])
  const [statusFilter, setStatusFilter] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [loadError, setLoadError] = useState('')
  const [editingId, setEditingId] = useState(null)

  useEffect(() => {
    let cancelled = false
    setIsLoading(true)
    setLoadError('')

    api
      .listTasks({ user_id: user.id, status: statusFilter || undefined })
      .then((data) => {
        if (!cancelled) setTasks(data)
      })
      .catch((error) => {
        if (!cancelled) {
          setLoadError(
            error instanceof ApiError ? error.message : 'Could not load tasks.'
          )
        }
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [user.id, statusFilter])

  async function handleCreate(values) {
    const created = await api.createTask(values)
    setTasks((prev) => [...prev, created])
    toast.success('Task created.')
  }

  async function handleUpdate(taskId, values) {
    const updated = await api.updateTask(taskId, values)
    setTasks((prev) =>
      prev.map((task) => (task.id === taskId ? updated : task))
    )
    setEditingId(null)
    toast.success('Task updated.')
  }

  async function handleDelete(taskId) {
    try {
      await api.deleteTask(taskId)
      setTasks((prev) => prev.filter((task) => task.id !== taskId))
      toast.success('Task deleted.')
    } catch (error) {
      toast.error(
        error instanceof ApiError ? error.message : 'Could not delete the task.'
      )
    }
  }

  return (
    <section className="container tasks-page">
      <div className="tasks-header">
        <div>
          <span className="chip">Your tasks</span>
          <h1>Tasks</h1>
        </div>
        <select
          className="tasks-filter"
          value={statusFilter}
          onChange={(event) => setStatusFilter(event.target.value)}
          aria-label="Filter by status"
        >
          <option value="">All statuses</option>
          {STATUS_OPTIONS.map((option) => (
            <option key={option} value={option}>
              {option.replace('_', ' ')}
            </option>
          ))}
        </select>
      </div>

      <div className="card task-create-card">
        <h2>New task</h2>
        <TaskForm
          initialValues={initialForm}
          submitLabel="Add task"
          onSubmit={handleCreate}
        />
      </div>

      {isLoading && <p>Loading tasks…</p>}
      {loadError && <p className="form-banner-error">{loadError}</p>}

      {!isLoading && !loadError && tasks.length === 0 && (
        <p className="tasks-empty">No tasks yet — add your first one above.</p>
      )}

      <ul className="task-list">
        {tasks.map((task) => (
          <li key={task.id} className="card task-item">
            {editingId === task.id ? (
              <TaskForm
                initialValues={task}
                submitLabel="Save"
                onSubmit={(values) => handleUpdate(task.id, values)}
                onCancel={() => setEditingId(null)}
              />
            ) : (
              <>
                <div className="task-item-main">
                  <h3>{task.title}</h3>
                  {task.description && <p>{task.description}</p>}
                  <div className="task-badges">
                    <span className={`badge badge-status-${task.status}`}>
                      {task.status.replace('_', ' ')}
                    </span>
                    <span className={`badge badge-priority-${task.priority}`}>
                      {task.priority}
                    </span>
                  </div>
                </div>
                <div className="task-item-actions">
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => setEditingId(task.id)}
                  >
                    Edit
                  </button>
                  <button
                    type="button"
                    className="btn btn-secondary btn-danger"
                    onClick={() => handleDelete(task.id)}
                  >
                    Delete
                  </button>
                </div>
              </>
            )}
          </li>
        ))}
      </ul>
    </section>
  )
}

export default Tasks
