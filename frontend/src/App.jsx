import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { SignedIn, SignedOut, RedirectToSignIn, useUser } from '@clerk/clerk-react'
import Header from './components/Header'
import Footer from './components/Footer'
import HomePage from './pages/HomePage'
import FeaturesPage from './pages/FeaturesPage'
import AboutPage from './pages/AboutPage'
import LandingPage from './components/LandingPage'
import SignInPage from './pages/SignInPage'
import SignUpPage from './pages/SignUpPage'

function App() {
  const [isLoaded, setIsLoaded] = useState(false)
  const {isLoaded: userLoaded } = useUser()

  useEffect(() => {
    setIsLoaded(true)
  }, [])

  if (!userLoaded) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>
  }

  return (
    <Router>
      <div className={`min-h-screen bg-gradient-to-br from-orange-50 via-amber-50 to-yellow-50 transition-opacity duration-1000 flex flex-col ${isLoaded ? 'opacity-100' : 'opacity-0'}`}>
        <Header />
        
        <main className="flex-grow">
          <Routes>
            {/* Public routes */}
            <Route path="/" element={<LandingPage />} />
            <Route path="/features" element={<FeaturesPage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/sign-in" element={<SignInPage />} />
            <Route path="/sign-up" element={<SignUpPage />} />
            
            {/* Protected routes */}
            <Route 
              path="/home" 
              element={
                <>
                  <SignedIn>
                    <HomePage />
                  </SignedIn>
                  <SignedOut>
                    <RedirectToSignIn />
                  </SignedOut>
                </>
              } 
            />
            
            {/* Redirect unsigned users to sign in */}
            <Route 
              path="/protected/*" 
              element={
                <>
                  <SignedIn>
                    <Routes>
                      <Route path="/home" element={<HomePage />} />
                    </Routes>
                  </SignedIn>
                  <SignedOut>
                    <RedirectToSignIn />
                  </SignedOut>
                </>
              } 
            />
          </Routes>
        </main>

        <Footer />
      </div>
    </Router>
  )
}

export default App
