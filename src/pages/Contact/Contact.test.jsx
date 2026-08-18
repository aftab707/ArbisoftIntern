import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Contact from '@/pages/Contact/Contact.jsx'

async function fillAndSubmit({ name, email, message }) {
  if (name) {
    await userEvent.type(screen.getByLabelText('Name'), name)
  }
  if (email) {
    await userEvent.type(screen.getByLabelText('Email'), email)
  }
  if (message) {
    await userEvent.type(screen.getByLabelText('Message'), message)
  }
  await userEvent.click(screen.getByRole('button', { name: /send/i }))
}

test('shows validation errors for empty fields and an invalid email', async () => {
  render(<Contact />)

  await fillAndSubmit({ name: '', email: 'not-an-email', message: '' })

  expect(await screen.findByText('Name is required.')).toBeInTheDocument()
  expect(
    await screen.findByText('Enter a valid email address.')
  ).toBeInTheDocument()
  expect(await screen.findByText('Message is required.')).toBeInTheDocument()
})

test('submits successfully and shows a success message with valid input', async () => {
  render(<Contact />)

  await fillAndSubmit({
    name: 'Aftab',
    email: 'aftab@example.com',
    message: 'Hello there!',
  })

  expect(
    await screen.findByText('Thanks! Your message has been sent.')
  ).toBeInTheDocument()
  expect(screen.queryByText('Name is required.')).not.toBeInTheDocument()
})
