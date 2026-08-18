const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
export const TOKEN_STORAGE_KEY = 'taskflow-token'

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

function getToken() {
  return window.localStorage.getItem(TOKEN_STORAGE_KEY)
}

async function request(
  path,
  { method = 'GET', body, auth = true, params } = {}
) {
  const url = new URL(path, API_BASE_URL)
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        url.searchParams.set(key, value)
      }
    })
  }

  const headers = { 'Content-Type': 'application/json' }
  if (auth) {
    const token = getToken()
    if (token) headers.Authorization = `Bearer ${token}`
  }

  const response = await fetch(url, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  })

  if (response.status === 401 && auth) {
    window.dispatchEvent(new CustomEvent('taskflow:unauthorized'))
  }

  if (response.status === 204) return null

  const data = await response.json().catch(() => null)

  if (!response.ok) {
    const message = data?.detail
      ? Array.isArray(data.detail)
        ? data.detail.map((item) => item.msg).join(', ')
        : data.detail
      : `Request failed with status ${response.status}`
    throw new ApiError(message, response.status)
  }

  return data
}

export const api = {
  register: (payload) =>
    request('/api/v1/auth/register', {
      method: 'POST',
      body: payload,
      auth: false,
    }),
  login: (payload) =>
    request('/api/v1/auth/login', {
      method: 'POST',
      body: payload,
      auth: false,
    }),
  me: () => request('/api/v1/auth/me'),

  listTasks: (params) => request('/api/v1/tasks/', { params }),
  createTask: (payload) =>
    request('/api/v1/tasks/', { method: 'POST', body: payload }),
  getTask: (id) => request(`/api/v1/tasks/${id}`),
  updateTask: (id, payload) =>
    request(`/api/v1/tasks/${id}`, { method: 'PUT', body: payload }),
  deleteTask: (id) => request(`/api/v1/tasks/${id}`, { method: 'DELETE' }),

  listUsers: () => request('/api/v1/users/'),
  updateUserRole: (id, role) =>
    request(`/api/v1/users/${id}/role`, { method: 'PATCH', body: { role } }),
}
