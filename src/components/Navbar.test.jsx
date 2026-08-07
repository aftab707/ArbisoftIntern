import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { AuthProvider } from '../context/AuthContext.jsx'
import Navbar from './Navbar.jsx'

test('renders a link for each of the Home, About, and Contact routes', () => {
  render(
    <MemoryRouter>
      <AuthProvider>
        <Navbar />
      </AuthProvider>
    </MemoryRouter>
  )

  expect(screen.getByRole('link', { name: 'Home' })).toHaveAttribute(
    'href',
    '/'
  )
  expect(screen.getByRole('link', { name: 'About' })).toHaveAttribute(
    'href',
    '/about'
  )
  expect(screen.getByRole('link', { name: 'Contact' })).toHaveAttribute(
    'href',
    '/contact'
  )
})
