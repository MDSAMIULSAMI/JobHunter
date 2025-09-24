import { Link } from 'react-router-dom'
import { SignedIn, SignedOut, UserButton } from '@clerk/clerk-react'

function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-orange-600">
            JobHunter
          </Link>
          
          <nav className="hidden md:flex items-center space-x-6">
            <Link to="/home" className="text-gray-600 hover:text-orange-600 transition-colors">
              Home
            </Link>
            <Link to="/features" className="text-gray-600 hover:text-orange-600 transition-colors">
              Features
            </Link>
            <Link to="/about" className="text-gray-600 hover:text-orange-600 transition-colors">
              About
            </Link>
            
            <SignedOut>
              <Link to="/sign-in" className="text-gray-600 hover:text-orange-600 transition-colors">
                Sign In
              </Link>
              <Link to="/sign-up" className="bg-orange-600 text-white px-4 py-2 rounded-md hover:bg-orange-700 transition-colors">
                Sign Up
              </Link>
            </SignedOut>
            
            <SignedIn>
              <UserButton afterSignOutUrl="/" />
            </SignedIn>
          </nav>
        </div>
      </div>
    </header>
  )
}

export default Header