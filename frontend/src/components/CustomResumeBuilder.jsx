import { useState } from 'react'
import LoadingSpinner from './LoadingSpinner'

const CustomResumeBuilder = () => {
  const [formData, setFormData] = useState({
    job_details: '',
    resume_details: ''
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!formData.job_details.trim() || !formData.resume_details.trim()) {
      setError('Please fill in both job details and resume information')
      return
    }

    setLoading(true)
    setError('')

    try {
      const response = await fetch('http://localhost:8000/resume/custom-builder', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })

      const data = await response.json()
      
      if (data.success) {
        setResult(data)
      } else {
        setError(data.message || 'Failed to generate resume')
      }
    } catch {
      setError('Failed to connect to the server. Please make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = () => {
    navigator.clipboard.writeText(result.latex_code)
    // You could add a toast notification here
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Form Section */}
      <div className="bg-white rounded-2xl shadow-xl p-8 mb-8 border border-orange-100">
        <h2 className="text-3xl font-bold text-orange-800 mb-6 text-center">
          🛠️ Custom Resume Builder
        </h2>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="block text-sm font-semibold text-orange-700">
                💼 Job Details/Description
              </label>
              <textarea
                value={formData.job_details}
                onChange={(e) => setFormData({...formData, job_details: e.target.value})}
                className="w-full h-48 px-4 py-3 border-2 border-orange-200 rounded-lg focus:border-orange-500 focus:outline-none transition-colors duration-200 resize-none"
                placeholder="Paste the job description, requirements, and any specific details about the position you're applying for..."
                required
              />
            </div>
            
            <div className="space-y-2">
              <label className="block text-sm font-semibold text-orange-700">
                📄 Your Resume Information
              </label>
              <textarea
                value={formData.resume_details}
                onChange={(e) => setFormData({...formData, resume_details: e.target.value})}
                className="w-full h-48 px-4 py-3 border-2 border-orange-200 rounded-lg focus:border-orange-500 focus:outline-none transition-colors duration-200 resize-none"
                placeholder="Enter your personal information, skills, experience, education, projects, and any other relevant details..."
                required
              />
            </div>
          </div>
          
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}
          
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-orange-500 to-amber-500 text-white py-4 rounded-lg font-semibold text-lg hover:shadow-lg transition-all duration-300 transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? <LoadingSpinner /> : '🚀 Generate Tailored Resume'}
          </button>
        </form>
      </div>

      {/* Results Section */}
      {result && (
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-orange-100">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-2xl font-bold text-orange-800">
              📝 Generated LaTeX Resume Code
            </h3>
            <button
              onClick={copyToClipboard}
              className="bg-gradient-to-r from-orange-500 to-amber-500 text-white px-6 py-2 rounded-lg font-semibold hover:shadow-md transition-all duration-200 transform hover:scale-105"
            >
              📋 Copy Code
            </button>
          </div>
          
          <div className="bg-gray-900 rounded-lg p-6 overflow-x-auto">
            <pre className="text-green-400 text-sm whitespace-pre-wrap font-mono">
              {result.latex_code}
            </pre>
          </div>
          
          <div className="mt-6 p-4 bg-gradient-to-r from-orange-50 to-amber-50 rounded-lg border border-orange-200">
            <h4 className="font-semibold text-orange-800 mb-2">📋 How to use this code:</h4>
            <ol className="text-orange-700 space-y-1 list-decimal list-inside">
              <li>Copy the LaTeX code above</li>
              <li>Paste it into a LaTeX editor (like Overleaf, TeXShop, or VS Code with LaTeX extension)</li>
              <li>Compile the document to generate your PDF resume</li>
              <li>Review and make any final adjustments as needed</li>
            </ol>
          </div>
        </div>
      )}
    </div>
  )
}

export default CustomResumeBuilder