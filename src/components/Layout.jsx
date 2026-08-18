import { Outlet, useLocation } from 'react-router-dom'
import Navbar from '@/components/Navbar.jsx'
import Footer from '@/components/Footer.jsx'
import '@/components/Layout.css'

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
