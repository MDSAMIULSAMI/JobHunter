import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

const LandingPage = () => {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    setIsVisible(true)
  }, [])

  const features = [
    {
      icon: "🔍",
      title: "Multi-Platform Job Search",
      description: "Search across LinkedIn, Indeed, Glassdoor, and BDJobs simultaneously",
      color: "from-orange-400 to-amber-400"
    },
    {
      icon: "🎯",
      title: "AI-Powered Resume Analysis",
      description: "Extract keywords and skills from your resume for better job matching",
      color: "from-amber-400 to-yellow-400"
    },
    {
      icon: "📄",
      title: "Custom Resume Builder",
      description: "Generate tailored resumes using professional LaTeX templates",
      color: "from-orange-500 to-red-400"
    }
  ]

  const stats = [
    { number: "10K+", label: "Jobs Scraped Daily" },
    { number: "500+", label: "Resumes Analyzed" },
    { number: "50+", label: "Companies Supported" },
    { number: "95%", label: "Success Rate" }
  ]

  const techStack = {
    frontend: [
      { name: "React 19", icon: "⚛️" },
      { name: "Tailwind CSS", icon: "🎨" },
      { name: "Vite", icon: "⚡" },
      { name: "React Router", icon: "🧭" }
    ],
    backend: [
      { name: "FastAPI", icon: "🐍" },
      { name: "Scrapper", icon: "🔍" },
      { name: "Pandas", icon: "📊" },
      { name: "LaTeX/PDF", icon: "📄" }
    ]
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-amber-50 to-yellow-50">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        {/* Background Elements */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-32 h-32 bg-orange-200/30 rounded-full animate-bounce" style={{animationDelay: '0s'}}></div>
          <div className="absolute top-40 right-20 w-24 h-24 bg-amber-200/30 rounded-full animate-bounce" style={{animationDelay: '1s'}}></div>
          <div className="absolute bottom-40 left-1/4 w-20 h-20 bg-yellow-200/30 rounded-full animate-bounce" style={{animationDelay: '2s'}}></div>
          <div className="absolute bottom-20 right-1/3 w-16 h-16 bg-orange-300/30 rounded-full animate-bounce" style={{animationDelay: '3s'}}></div>
        </div>

        <div className={`container mx-auto px-4 text-center relative z-10 transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
          <div className="max-w-5xl mx-auto">
            <h1 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-orange-600 via-amber-600 to-yellow-600 bg-clip-text text-transparent mb-6 leading-tight">
              Find Your Dream Job with
              <span className="block mt-2">AI-Powered Search</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-orange-700/80 mb-12 leading-relaxed max-w-4xl mx-auto">
              Harness the power of artificial intelligence to search jobs across multiple platforms, 
              analyze your resume, and build tailored applications that get noticed by employers.
            </p>

            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center mb-16">
              <Link 
                to="/home" 
                className="bg-gradient-to-r from-orange-500 to-amber-500 text-white px-10 py-5 rounded-full text-xl font-semibold hover:shadow-2xl transition-all duration-300 transform hover:scale-105 animate-pulse-glow"
              >
                🚀 Start Job Hunting
              </Link>
              <Link 
                to="/features" 
                className="border-2 border-orange-300 text-orange-600 px-10 py-5 rounded-full text-xl font-semibold hover:bg-orange-50 transition-all duration-300 transform hover:scale-105"
              >
                📋 Explore Features
              </Link>
            </div>

            {/* Stats Section */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent mb-2">
                    {stat.number}
                  </div>
                  <div className="text-orange-700/70 font-medium">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features Preview Section */}
      <section className="py-20 bg-white/50 backdrop-blur-sm">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent mb-6">
              Why Choose JobHunter?
            </h2>
            <p className="text-xl text-orange-700/80 max-w-3xl mx-auto">
              Experience the future of job searching with our cutting-edge AI technology
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 mb-16">
            {features.map((feature, index) => (
              <div 
                key={index}
                className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-orange-100 hover:shadow-xl transition-all duration-300 transform hover:scale-[1.02] animate-fade-in-up"
                style={{ animationDelay: `${index * 0.2}s` }}
              >
                <div className={`w-16 h-16 bg-gradient-to-r ${feature.color} rounded-full flex items-center justify-center text-white text-3xl mx-auto mb-6`}>
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold text-orange-800 mb-4 text-center">{feature.title}</h3>
                <p className="text-orange-700/80 text-center leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>

          <div className="text-center">
            <Link 
              to="/features" 
              className="inline-flex items-center bg-gradient-to-r from-orange-100 to-amber-100 border border-orange-200 text-orange-600 px-8 py-4 rounded-full text-lg font-semibold hover:shadow-lg transition-all duration-300 transform hover:scale-105"
            >
              View All Features 🔍
            </Link>
          </div>
        </div>
      </section>

      {/* Technology Stack Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent mb-6">
              Built with Modern Technology
            </h2>
            <p className="text-xl text-orange-700/80 max-w-3xl mx-auto">
              Powered by the latest technologies for optimal performance and reliability
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-12 max-w-6xl mx-auto">
            {/* Frontend */}
            <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-orange-100">
              <h3 className="text-2xl font-bold text-orange-800 mb-8 flex items-center justify-center">
                <span className="mr-3">🎨</span> Frontend Technologies
              </h3>
              <div className="grid grid-cols-2 gap-6">
                {techStack.frontend.map((tech, index) => (
                  <div key={index} className="bg-orange-50 rounded-xl p-4 text-center hover:shadow-md transition-all duration-200">
                    <div className="text-3xl mb-3">{tech.icon}</div>
                    <div className="font-semibold text-orange-700">{tech.name}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Backend */}
            <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-orange-100">
              <h3 className="text-2xl font-bold text-orange-800 mb-8 flex items-center justify-center">
                <span className="mr-3">⚙️</span> Backend Technologies
              </h3>
              <div className="grid grid-cols-2 gap-6">
                {techStack.backend.map((tech, index) => (
                  <div key={index} className="bg-orange-50 rounded-xl p-4 text-center hover:shadow-md transition-all duration-200">
                    <div className="text-3xl mb-3">{tech.icon}</div>
                    <div className="font-semibold text-orange-700">{tech.name}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-white/50 backdrop-blur-sm">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent mb-6">
              How It Works
            </h2>
            <p className="text-xl text-orange-700/80 max-w-3xl mx-auto">
              Get started in just three simple steps
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-r from-orange-400 to-amber-400 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-6">
                1
              </div>
              <h3 className="text-xl font-bold text-orange-800 mb-4">Upload Your Resume</h3>
              <p className="text-orange-700/80">
                Upload your resume and let our AI analyze your skills, experience, and career interests
              </p>
            </div>

            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-r from-amber-400 to-yellow-400 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-6">
                2
              </div>
              <h3 className="text-xl font-bold text-orange-800 mb-4">AI-Powered Matching</h3>
              <p className="text-orange-700/80">
                Our AI extracts relevant keywords and searches across multiple job platforms for perfect matches
              </p>
            </div>

            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-r from-yellow-400 to-orange-400 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-6">
                3
              </div>
              <h3 className="text-xl font-bold text-orange-800 mb-4">Apply with Confidence</h3>
              <p className="text-orange-700/80">
                Generate tailored resumes and cover letters for each application to maximize your success
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="bg-gradient-to-r from-orange-500 to-amber-500 rounded-3xl p-12 text-white text-center max-w-4xl mx-auto">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Ready to Transform Your Job Search?
            </h2>
            <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
              Join thousands of job seekers who have found their dream careers with JobHunter's AI-powered platform. 
              Start your journey today and discover opportunities you never knew existed.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
              <Link 
                to="/" 
                className="bg-white text-orange-600 px-10 py-5 rounded-full text-xl font-semibold hover:shadow-2xl transition-all duration-300 transform hover:scale-105"
              >
                🚀 Get Started Now
              </Link>
              <Link 
                to="/about" 
                className="border-2 border-white text-white px-10 py-5 rounded-full text-xl font-semibold hover:bg-white/10 transition-all duration-300 transform hover:scale-105"
              >
                📖 Learn More
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 bg-white/50 backdrop-blur-sm">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent mb-6">
              Success Stories
            </h2>
            <p className="text-xl text-orange-700/80 max-w-3xl mx-auto">
              See how JobHunter has helped professionals land their dream jobs
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-orange-100">
              <div className="text-orange-400 text-4xl mb-4">⭐⭐⭐⭐⭐</div>
              <p className="text-orange-700/80 mb-6 italic">
                "JobHunter's AI analysis helped me identify skills I didn't even know I had. 
                I landed my dream job at a Fortune 500 company within 2 weeks!"
              </p>
              <div className="font-semibold text-orange-800">Sarah Chen</div>
              <div className="text-orange-600 text-sm">Software Engineer at Google</div>
            </div>

            <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-orange-100">
              <div className="text-orange-400 text-4xl mb-4">⭐⭐⭐⭐⭐</div>
              <p className="text-orange-700/80 mb-6 italic">
                "The multi-platform search saved me hours of manual searching. 
                I found opportunities I would have never discovered otherwise."
              </p>
              <div className="font-semibold text-orange-800">Michael Rodriguez</div>
              <div className="text-orange-600 text-sm">Data Scientist at Microsoft</div>
            </div>

            <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-orange-100">
              <div className="text-orange-400 text-4xl mb-4">⭐⭐⭐⭐⭐</div>
              <p className="text-orange-700/80 mb-6 italic">
                "The custom resume builder created professional documents that 
                perfectly matched each job application. Highly recommended!"
              </p>
              <div className="font-semibold text-orange-800">Emily Johnson</div>
              <div className="text-orange-600 text-sm">Product Manager at Amazon</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default LandingPage