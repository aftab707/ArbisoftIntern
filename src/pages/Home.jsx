import { Link } from 'react-router-dom'
import Reveal from '../components/Reveal.jsx'
import './Home.css'

const features = [
  {
    title: 'Client-side routing',
    description:
      'React Router powers three pages behind a single shared layout and navbar.',
    icon: (
      <svg
        viewBox="0 0 24 24"
        width="22"
        height="22"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M4 19V7l6-3 6 3 4-2v12l-4 2-6-3-6 3z" />
        <path d="M10 4v13M16 7v13" />
      </svg>
    ),
  },
  {
    title: 'Validated forms',
    description:
      'The contact form checks required fields and email format before it submits.',
    icon: (
      <svg
        viewBox="0 0 24 24"
        width="22"
        height="22"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z" />
        <path d="M9 12l2 2 4-4" />
      </svg>
    ),
  },
  {
    title: 'Tested with confidence',
    description:
      'Vitest and React Testing Library cover rendering and validation behaviour.',
    icon: (
      <svg
        viewBox="0 0 24 24"
        width="22"
        height="22"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M9 3h6M10 3v6l-5.5 9.5A1 1 0 0 0 5.4 20h13.2a1 1 0 0 0 .9-1.5L14 9V3" />
        <path d="M8 15h8" />
      </svg>
    ),
  },
]

function Home() {
  return (
    <>
      <section className="hero">
        <div className="hero-glow" aria-hidden="true" />
        <div className="container hero-inner">
          <span className="chip">Week 1 · Frontend Fundamentals</span>
          <h1>
            Building the <span className="gradient-text">fundamentals</span> of
            modern web apps.
          </h1>
          <p className="hero-lead">
            A small React + Vite app covering routing, layout, forms, and
            testing — scaffolded and refined with Claude Code.
          </p>
          <div className="hero-actions">
            <Link to="/contact" className="btn btn-primary">
              Get in touch
            </Link>
            <Link to="/about" className="btn btn-secondary">
              Learn more
            </Link>
          </div>
        </div>
      </section>

      <section className="container features">
        {features.map((feature, index) => (
          <Reveal
            key={feature.title}
            as="article"
            className="card feature-card"
            delay={index * 100}
          >
            <div className="feature-icon">{feature.icon}</div>
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </Reveal>
        ))}
      </section>
    </>
  )
}

export default Home
