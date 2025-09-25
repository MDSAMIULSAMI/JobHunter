const About = () => {
  return (
    <section id="about" className="py-20 bg-gradient-to-br from-orange-50 via-amber-50 to-yellow-50">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent mb-6">
            About JobHunter
          </h2>
          <p className="text-xl text-orange-700/80 max-w-3xl mx-auto leading-relaxed">
            Revolutionizing job search with AI-powered tools that connect talent with opportunity across multiple platforms.
          </p>
        </div>

        {/* Mission Section */}
        <div className="grid lg:grid-cols-2 gap-12 mb-16">
          <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-orange-100 hover:shadow-xl transition-all duration-300">
            <div className="flex items-center mb-6">
              <div className="w-12 h-12 bg-gradient-to-r from-orange-400 to-amber-400 rounded-full flex items-center justify-center text-white text-2xl mr-4">
                🎯
              </div>
              <h3 className="text-2xl font-bold text-orange-800">Our Mission</h3>
            </div>
            <p className="text-orange-700/80 leading-relaxed">
              JobHunter empowers job seekers by aggregating opportunities from multiple job boards, 
              analyzing resumes with AI, and generating tailored applications. We believe in making 
              job searching more efficient, intelligent, and successful for everyone.
            </p>
          </div>

          <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-orange-100 hover:shadow-xl transition-all duration-300">
            <div className="flex items-center mb-6">
              <div className="w-12 h-12 bg-gradient-to-r from-orange-400 to-amber-400 rounded-full flex items-center justify-center text-white text-2xl mr-4">
                🚀
              </div>
              <h3 className="text-2xl font-bold text-orange-800">Our Vision</h3>
            </div>
            <p className="text-orange-700/80 leading-relaxed">
              To become the leading AI-powered job search platform that eliminates barriers between 
              talented individuals and their dream careers, making job hunting a seamless and 
              personalized experience.
            </p>
          </div>
        </div>

        {/* Technology Stack */}
        <div className="mb-16">
          <h3 className="text-3xl font-bold text-center bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent mb-12">
            Built with Modern Technology
          </h3>
          
          <div className="grid md:grid-cols-2 gap-8">
            {/* Frontend */}
            <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-orange-100">
              <h4 className="text-xl font-bold text-orange-800 mb-6 flex items-center">
                <span className="mr-3">🎨</span> Frontend
              </h4>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-orange-50 rounded-lg p-3 text-center">
                  <div className="text-2xl mb-2">⚛️</div>
                  <div className="font-semibold text-orange-700">React 19</div>
                </div>
                <div className="bg-orange-50 rounded-lg p-3 text-center">
                  <div className="text-2xl mb-2">🎨</div>
                  <div className="font-semibold text-orange-700">Tailwind CSS</div>
                </div>
                <div className="bg-orange-50 rounded-lg p-3 text-center">
                  <div className="text-2xl mb-2">⚡</div>
                  <div className="font-semibold text-orange-700">Vite</div>
                </div>
                <div className="bg-orange-50 rounded-lg p-3 text-center">
                  <div className="text-2xl mb-2">🧭</div>
                  <div className="font-semibold text-orange-700">React Router</div>
                </div>
              </div>
            </div>

            {/* Backend */}
            <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-orange-100">
              <h4 className="text-xl font-bold text-orange-800 mb-6 flex items-center">
                <span className="mr-3">⚙️</span> Backend
              </h4>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-orange-50 rounded-lg p-3 text-center">
                  <div className="text-2xl mb-2">🐍</div>
                  <div className="font-semibold text-orange-700">FastAPI</div>
                </div>
                <div className="bg-orange-50 rounded-lg p-3 text-center">
                  <div className="text-2xl mb-2">🔍</div>
                  <div className="font-semibold text-orange-700">Scrapper</div>
                </div>
                <div className="bg-orange-50 rounded-lg p-3 text-center">
                  <div className="text-2xl mb-2">📊</div>
                  <div className="font-semibold text-orange-700">Pandas</div>
                </div>
                <div className="bg-orange-50 rounded-lg p-3 text-center">
                  <div className="text-2xl mb-2">📄</div>
                  <div className="font-semibold text-orange-700">LaTeX/PDF</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Key Features */}
        <div className="mb-16">
          <h3 className="text-3xl font-bold text-center bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent mb-12">
            What Makes Us Different
          </h3>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-orange-400 to-amber-400 rounded-full flex items-center justify-center text-white text-3xl mx-auto mb-4">
                🌐
              </div>
              <h4 className="text-xl font-bold text-orange-800 mb-3">Multi-Platform Scraping</h4>
              <p className="text-orange-700/80">
                Aggregate jobs from LinkedIn, Indeed, Glassdoor, BDJobs, and more in one search.
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-orange-400 to-amber-400 rounded-full flex items-center justify-center text-white text-3xl mx-auto mb-4">
                🤖
              </div>
              <h4 className="text-xl font-bold text-orange-800 mb-3">AI-Powered Analysis</h4>
              <p className="text-orange-700/80">
                Smart resume analysis and keyword extraction for better job matching.
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-orange-400 to-amber-400 rounded-full flex items-center justify-center text-white text-3xl mx-auto mb-4">
                📝
              </div>
              <h4 className="text-xl font-bold text-orange-800 mb-3">Custom Resume Builder</h4>
              <p className="text-orange-700/80">
                Generate tailored LaTeX resumes for specific job applications with professional formatting.
              </p>
            </div>
          </div>
        </div>

        {/* Statistics */}
        <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-orange-100 mb-16">
          <h3 className="text-3xl font-bold text-center bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent mb-12">
            Platform Capabilities
          </h3>
          
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-orange-600 mb-2">5+</div>
              <div className="text-orange-700/80">Job Platforms</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-orange-600 mb-2">∞</div>
              <div className="text-orange-700/80">Job Listings</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-orange-600 mb-2">AI</div>
              <div className="text-orange-700/80">Powered Analysis</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-orange-600 mb-2">PDF</div>
              <div className="text-orange-700/80">Resume Generation</div>
            </div>
          </div>
        </div>

        {/* Call to Action */}
        <div className="text-center">
          <div className="bg-gradient-to-r from-orange-500 to-amber-500 rounded-2xl p-8 text-white">
            <h3 className="text-3xl font-bold mb-4">Ready to Transform Your Job Search?</h3>
            <p className="text-xl mb-6 opacity-90">
              Join thousands of job seekers who have found their dream careers with JobHunter's AI-powered platform.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-white text-orange-600 px-8 py-4 rounded-full text-lg font-semibold hover:shadow-xl transition-all duration-300 transform hover:scale-105">
                Get Started Now 🚀
              </button>
              <button className="border-2 border-white text-white px-8 py-4 rounded-full text-lg font-semibold hover:bg-white/10 transition-all duration-300 transform hover:scale-105">
                View Features 📋
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default About