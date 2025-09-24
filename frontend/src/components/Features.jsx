const Features = () => {
  const features = [
    {
      icon: "🔍",
      title: "Multi-Platform Job Search",
      description: "Search across multiple job platforms including LinkedIn, Indeed, Glassdoor, and BDJobs simultaneously to find the best opportunities.",
      highlights: ["LinkedIn Integration", "Indeed Scraping", "Glassdoor Access", "BDJobs Support"]
    },
    {
      icon: "🎯",
      title: "AI-Powered Resume Analysis",
      description: "Upload your resume and let our AI extract relevant keywords and skills to match you with the most suitable job opportunities.",
      highlights: ["Keyword Extraction", "Skills Analysis", "Smart Matching", "PDF Processing"]
    },
    {
      icon: "📄",
      title: "Custom Resume Builder",
      description: "Generate tailored resumes for specific job applications using LaTeX templates with professional formatting.",
      highlights: ["LaTeX Templates", "PDF Generation", "Custom Formatting", "Professional Design"]
    },
    {
      icon: "🤖",
      title: "Intelligent Job Matching",
      description: "Our AI analyzes your profile and preferences to recommend jobs that align with your career goals and experience.",
      highlights: ["Smart Recommendations", "Profile Analysis", "Career Matching", "Preference Learning"]
    },
    {
      icon: "📊",
      title: "Resume Optimization",
      description: "Get detailed insights on how to improve your resume with AI-powered suggestions and keyword optimization.",
      highlights: ["Content Analysis", "Keyword Optimization", "Format Suggestions", "ATS Compatibility"]
    },
    {
      icon: "🚀",
      title: "One-Click Applications",
      description: "Streamline your job application process with automated form filling and resume customization for each position.",
      highlights: ["Auto Form Fill", "Custom Cover Letters", "Application Tracking", "Quick Apply"]
    }
  ]

  return (
    <section id="features" className="py-20 bg-gradient-to-br from-orange-50 via-amber-50 to-yellow-50">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent mb-6">
            Powerful Features
          </h2>
          <p className="text-xl text-orange-700/80 max-w-3xl mx-auto leading-relaxed">
            Discover how JobHunter's AI-powered tools can transform your job search experience 
            and help you land your dream career faster than ever before.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {features.map((feature, index) => (
            <div 
              key={index}
              className="bg-gradient-to-r from-orange-50 to-amber-50 border border-orange-200 rounded-xl p-8 hover:shadow-xl transition-all duration-300 transform hover:scale-[1.02] animate-fade-in-up"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-bold text-orange-800 mb-4">{feature.title}</h3>
              <p className="text-orange-700/80 mb-6 leading-relaxed">{feature.description}</p>
              
              <div className="space-y-2">
                {feature.highlights.map((highlight, idx) => (
                  <div key={idx} className="flex items-center text-orange-600">
                    <span className="w-2 h-2 bg-orange-400 rounded-full mr-3"></span>
                    <span className="text-sm font-medium">{highlight}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Call to Action */}
        <div className="text-center">
          <div className="bg-gradient-to-r from-orange-100 to-amber-100 border border-orange-200 rounded-2xl p-8 max-w-4xl mx-auto">
            <h3 className="text-2xl md:text-3xl font-bold text-orange-800 mb-4">
              Ready to Supercharge Your Job Search?
            </h3>
            <p className="text-orange-700/80 mb-6 text-lg">
              Join thousands of job seekers who have already discovered their dream careers with JobHunter.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <button className="bg-gradient-to-r from-orange-500 to-amber-500 text-white px-8 py-4 rounded-full text-lg font-semibold hover:shadow-xl transition-all duration-300 transform hover:scale-105 animate-pulse-glow">
                Start Your Journey 🚀
              </button>
              <button className="border-2 border-orange-300 text-orange-600 px-8 py-4 rounded-full text-lg font-semibold hover:bg-orange-50 transition-all duration-300 transform hover:scale-105">
                Learn More 📚
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Features