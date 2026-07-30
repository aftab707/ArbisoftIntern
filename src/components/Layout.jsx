import { Outlet, useLocation } from 'react-router-dom'
import Navbar from './Navbar.jsx'
import Footer from './Footer.jsx'
import './Layout.css'

function Layout() {
  const location = useLocation()

  return (
    <div className="layout">
      <Navbar />
      <main className="layout-content">
        <div key={location.pathname} className="page-transition">
          <Outlet />
        </div>
      </main>
      <Footer />
    </div>
  )
}

export default Layout
