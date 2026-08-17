import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { AuthProvider } from '../../context/AuthContext.jsx'
import Signup from './Signup.jsx'

function renderSignup() {
  return render(
    <MemoryRouter>
      <AuthProvider>
        <Signup />
      </AuthProvider>
    </MemoryRouter>
  )
}

test('shows validation errors when submitting an empty form', async () => {
  renderSignup()

  await userEvent.click(screen.getByRole('button', { name: /sign up/i }))

  expect(await screen.findByText('Name is required.')).toBeInTheDocument()
  expect(screen.getByText('Email is required.')).toBeInTheDocument()
  expect(screen.getByText('Password is required.')).toBeInTheDocument()
})

test('shows an error when the password is too short', async () => {
  renderSignup()

  await userEvent.type(screen.getByLabelText('Name'), 'Aftab')
  await userEvent.type(screen.getByLabelText('Email'), 'aftab@example.com')
  await userEvent.type(screen.getByLabelText('Password'), 'short')
  await userEvent.click(screen.getByRole('button', { name: /sign up/i }))

  expect(
    await screen.findByText('Password must be at least 8 characters.')
  ).toBeInTheDocument()
})
