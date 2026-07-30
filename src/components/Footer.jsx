import reactLogo from '../assets/react.svg'
import viteLogo from '../assets/vite.svg'
import './Footer.css'

function Footer() {
  return (
    <footer className="footer">
      <div className="container footer-inner">
        <p>Week 1 · Arbisoft Internship Program 2026</p>
        <p className="footer-stack">
          Built with
          <img src={reactLogo} alt="React" />
          <img src={viteLogo} alt="Vite" />
          React Router
        </p>
      </div>
    </footer>
  )
}

export default Footer
