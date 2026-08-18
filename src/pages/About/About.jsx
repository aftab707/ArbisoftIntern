import Reveal from '@/components/Reveal.jsx'
import '@/pages/About/About.css'

const timeline = [
  {
    title: 'Scaffold the project',
    detail: 'React + Vite, with ESLint and Prettier wired in from the start.',
  },
  {
    title: 'Routing & layout',
    detail:
      'React Router with a shared Navbar across Home, About, and Contact.',
  },
  {
    title: 'Contact form',
    detail:
      'Controlled inputs with client-side validation for required fields and email format.',
  },
  {
    title: 'Testing',
    detail:
      'Vitest and React Testing Library cover rendering and form validation.',
  },
]

const stack = [
  'React',
  'Vite',
  'React Router',
  'ESLint',
  'Prettier',
  'Vitest',
  'Testing Library',
]

function About() {
  return (
    <div className="container about-page">
      <Reveal as="section" className="about-intro">
        <span className="chip">About this project</span>
        <h1>A hands-on pass through frontend fundamentals.</h1>
        <p>
          This app was scaffolded and built with React, Vite, and React Router
          as part of the Arbisoft Internship Program 2026 — Week 1 assignment.
          Every step, from routing to testing, was built with an AI coding
          assistant reviewing and refining the output.
        </p>
      </Reveal>

      <section className="timeline">
        {timeline.map((step, index) => (
          <Reveal
            key={step.title}
            as="div"
            className="timeline-item"
            delay={index * 100}
          >
            <span className="timeline-index">{index + 1}</span>
            <div>
              <h3>{step.title}</h3>
              <p>{step.detail}</p>
            </div>
          </Reveal>
        ))}
      </section>

      <Reveal as="section" className="stack">
        <h2>Built with</h2>
        <div className="stack-chips">
          {stack.map((item) => (
            <span key={item} className="chip">
              {item}
            </span>
          ))}
        </div>
      </Reveal>
    </div>
  )
}

export default About
