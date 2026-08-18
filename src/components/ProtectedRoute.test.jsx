import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { AuthProvider } from '@/context/AuthContext.jsx'
import { ProtectedRoute } from '@/components/ProtectedRoute.jsx'

function renderAtTasks() {
  return render(
    <MemoryRouter initialEntries={['/tasks']}>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<div>Login page</div>} />
          <Route element={<ProtectedRoute />}>
            <Route path="/tasks" element={<div>Tasks page</div>} />
          </Route>
        </Routes>
      </AuthProvider>
    </MemoryRouter>
  )
}

test('redirects an unauthenticated user from a protected route to /login', async () => {
  renderAtTasks()

  expect(await screen.findByText('Login page')).toBeInTheDocument()
  expect(screen.queryByText('Tasks page')).not.toBeInTheDocument()
})
