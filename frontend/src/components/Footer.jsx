const Footer = () => {
  return (
    <footer className="bg-gradient-to-r from-orange-800 to-amber-800 text-white py-12 mt-16">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center">
                <span className="text-orange-600 font-bold text-xl">J</span>
              </div>
              <div>
                <h3 className="text-xl font-bold">JobSpy</h3>
                <p className="text-orange-200 text-sm">Smart Job Search</p>
              </div>
            </div>
            <p className="text-orange-200">
              Empowering job seekers with AI-powered tools to find their dream careers.
            </p>
          </div>
          
          <div>
            <h4 className="font-semibold mb-4">Features</h4>
            <ul className="space-y-2 text-orange-200">
              <li>Job Search</li>
              <li>Resume Analysis</li>
              <li>Resume Builder</li>
              <li>Multi-platform Search</li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-semibold mb-4">Support</h4>
            <ul className="space-y-2 text-orange-200">
              <li>Documentation</li>
              <li>API Reference</li>
              <li>Help Center</li>
              <li>Contact Us</li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-semibold mb-4">Connect</h4>
            <ul className="space-y-2 text-orange-200">
              <li>GitHub</li>
              <li>LinkedIn</li>
              <li>Twitter</li>
              <li>Blog</li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-orange-700 mt-8 pt-8 text-center text-orange-200">
          <p>&copy; 2024 JobSpy. All rights reserved. Built with ❤️ for job seekers.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer