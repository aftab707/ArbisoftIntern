const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export function validateLogin({ email, password }) {
  const errors = {}

  if (!email.trim()) {
    errors.email = 'Email is required.'
  } else if (!EMAIL_REGEX.test(email.trim())) {
    errors.email = 'Enter a valid email address.'
  }

  if (!password) {
    errors.password = 'Password is required.'
  }

  return errors
}

export function validateSignup({ name, email, password }) {
  const errors = {}

  if (!name.trim()) {
    errors.name = 'Name is required.'
  }

  if (!email.trim()) {
    errors.email = 'Email is required.'
  } else if (!EMAIL_REGEX.test(email.trim())) {
    errors.email = 'Enter a valid email address.'
  }

  if (!password) {
    errors.password = 'Password is required.'
  } else if (password.length < 8) {
    errors.password = 'Password must be at least 8 characters.'
  }

  return errors
}
