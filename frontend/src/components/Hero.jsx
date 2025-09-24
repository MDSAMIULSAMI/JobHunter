import { useState, useEffect } from 'react'

const Hero = () => {
  const [currentText, setCurrentText] = useState('')
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isDeleting, setIsDeleting] = useState(false)
  
  const texts = [
    'Find Your Dream Job',
    'Analyze Your Resume',
    'Build Perfect Resumes',
    'Land Better Opportunities'
  ]

  useEffect(() => {
    const timeout = setTimeout(() => {
      const current = texts[currentIndex]
      
      if (isDeleting) {
        setCurrentText(current.substring(0, currentText.length - 1))
      } else {
        setCurrentText(current.substring(0, currentText.length + 1))
      }

      if (!isDeleting && currentText === current) {
        setTimeout(() => setIsDeleting(true), 2000)
      } else if (isDeleting && currentText === '') {
        setIsDeleting(false)
        setCurrentIndex((currentIndex + 1) % texts.length)
      }
    }, isDeleting ? 50 : 100)

    return () => clearTimeout(timeout)
  }, [currentText, currentIndex, isDeleting, texts])

  return (
    <section className="pt-24 pb-16 px-4">
      <div className="container mx-auto text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-7xl font-bold mb-6">
            <span className="bg-gradient-to-r from-orange-600 via-amber-600 to-yellow-600 bg-clip-text text-transparent">
              {currentText}
            </span>
            <span className="animate-pulse text-orange-500">|</span>
          </h1>
          
          <p className="text-xl md:text-2xl text-orange-700/80 mb-8 leading-relaxed">
            Harness the power of AI to search jobs across multiple platforms, 
            analyze your resume, and build tailored applications that get noticed.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <button className="bg-gradient-to-r from-orange-500 to-amber-500 text-white px-8 py-4 rounded-full text-lg font-semibold hover:shadow-xl transition-all duration-300 transform hover:scale-105">
              Start Job Search 🚀
            </button>
            <button className="border-2 border-orange-300 text-orange-600 px-8 py-4 rounded-full text-lg font-semibold hover:bg-orange-50 transition-all duration-300 transform hover:scale-105">
              Watch Demo 📹
            </button>
          </div>
        </div>
        
        {/* Floating Elements */}
        <div className="absolute top-32 left-10 w-20 h-20 bg-orange-200/30 rounded-full animate-bounce" style={{animationDelay: '0s'}}></div>
        <div className="absolute top-48 right-16 w-16 h-16 bg-amber-200/30 rounded-full animate-bounce" style={{animationDelay: '1s'}}></div>
        <div className="absolute top-64 left-1/4 w-12 h-12 bg-yellow-200/30 rounded-full animate-bounce" style={{animationDelay: '2s'}}></div>
      </div>
    </section>
  )
}

export default Hero