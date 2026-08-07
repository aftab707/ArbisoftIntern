import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { AuthProvider } from '../context/AuthContext.jsx'
import Login from './Login.jsx'

function renderLogin() {
  return render(
    <MemoryRouter>
      <AuthProvider>
        <Login />
      </AuthProvider>
    </MemoryRouter>
  )
}

test('shows validation errors when submitting an empty form', async () => {
  renderLogin()

  await userEvent.click(screen.getByRole('button', { name: /log in/i }))

  expect(await screen.findByText('Email is required.')).toBeInTheDocument()
  expect(screen.getByText('Password is required.')).toBeInTheDocument()
})

test('shows an error for an invalid email format', async () => {
  renderLogin()

  await userEvent.type(screen.getByLabelText('Email'), 'not-an-email')
  await userEvent.type(screen.getByLabelText('Password'), 'secret123')
  await userEvent.click(screen.getByRole('button', { name: /log in/i }))

  expect(
    await screen.findByText('Enter a valid email address.')
  ).toBeInTheDocument()
})
