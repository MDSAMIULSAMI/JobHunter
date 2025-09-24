import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'

const Header = () => {
  const [isScrolled, setIsScrolled] = useState(false)
  const location = useLocation()

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled ? "bg-white/90 backdrop-blur-md shadow-lg" : "bg-transparent"
      }`}
    >
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-orange-500 to-amber-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">J</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent">
                JobHunter
              </h1>
              <p className="text-sm text-orange-600/70">Smart Job Search</p>
            </div>
          </Link>

          <nav className="hidden md:flex items-center space-x-6">
            <Link
              to="/home"
              className={`text-orange-700 hover:text-orange-500 transition-colors duration-200 ${
                location.pathname === "/home"
                  ? "font-semibold border-b-2 border-orange-500"
                  : ""
              }`}
            >
              Home
            </Link>
            <Link
              to="/features"
              className={`text-orange-700 hover:text-orange-500 transition-colors duration-200 ${
                location.pathname === "/features"
                  ? "font-semibold border-b-2 border-orange-500"
                  : ""
              }`}
            >
              Features
            </Link>
            <Link
              to="/about"
              className={`text-orange-700 hover:text-orange-500 transition-colors duration-200 ${
                location.pathname === "/about"
                  ? "font-semibold text-orange-500"
                  : ""
              }`}
            >
              About
            </Link>
            <Link
              to="/"
              className="bg-gradient-to-r from-orange-500 to-amber-500 text-white px-6 py-2 rounded-full hover:shadow-lg transition-all duration-200 transform hover:scale-105"
            >
              Get Started
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
}

export default Header