import { useState } from 'react'
import LoadingSpinner from './LoadingSpinner'

const ResumeAnalyzer = () => {
  const [file, setFile] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    const files = e.dataTransfer.files
    if (files && files[0]) {
      handleFileSelect(files[0])
    }
  }

  const handleFileSelect = (selectedFile) => {
    if (selectedFile.type !== 'application/pdf') {
      setError('Please select a PDF file')
      return
    }
    
    if (selectedFile.size > 10 * 1024 * 1024) { // 10MB limit
      setError('File size must be less than 10MB')
      return
    }
    
    setFile(selectedFile)
    setError('')
    setAnalysis(null)
  }

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      handleFileSelect(selectedFile)
    }
  }

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please select a PDF file first')
      return
    }

    setLoading(true)
    setError('')

    const formData = new FormData()
    formData.append('resume_file', file)

    try {
      const response = await fetch('http://localhost:8000/resume/upload', {
        method: 'POST',
        body: formData
      })

      const data = await response.json()
      
      if (response.ok) {
        setAnalysis(data)
      } else {
        setError(data.detail || 'Failed to analyze resume')
      }
    } catch {
      setError('Failed to connect to the server. Please make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Upload Section */}
      <div className="bg-white rounded-2xl shadow-xl p-8 mb-8 border border-orange-100">
        <h2 className="text-3xl font-bold text-orange-800 mb-6 text-center">
          📄 Resume Analyzer
        </h2>
        
        <div
          className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 ${
            dragActive 
              ? 'border-orange-500 bg-orange-50' 
              : 'border-orange-300 hover:border-orange-400 hover:bg-orange-50'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <div className="text-6xl mb-4">📎</div>
          <p className="text-xl text-orange-700 mb-4">
            {file ? file.name : 'Drop your resume PDF here or click to browse'}
          </p>
          <p className="text-orange-600 mb-6">
            Supported format: PDF (max 10MB)
          </p>
          
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="hidden"
            id="resume-upload"
          />
          
          <label
            htmlFor="resume-upload"
            className="bg-gradient-to-r from-orange-500 to-amber-500 text-white px-8 py-3 rounded-lg font-semibold cursor-pointer hover:shadow-lg transition-all duration-300 transform hover:scale-105 inline-block"
          >
            Choose File
          </label>
        </div>
        
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mt-4">
            {error}
          </div>
        )}
        
        {file && (
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="w-full mt-6 bg-gradient-to-r from-orange-500 to-amber-500 text-white py-4 rounded-lg font-semibold text-lg hover:shadow-lg transition-all duration-300 transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? <LoadingSpinner /> : '🔍 Analyze Resume'}
          </button>
        )}
      </div>

      {/* Analysis Results */}
      {analysis && (
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-orange-100">
          <h3 className="text-2xl font-bold text-orange-800 mb-6">
            📊 Analysis Results
          </h3>
          
          <div className="grid md:grid-cols-2 gap-6">
            {Object.entries(analysis.result.Output).map(([key, value]) => (
              <div key={key} className="bg-gradient-to-r from-orange-50 to-amber-50 p-4 rounded-lg border border-orange-200">
                <h4 className="font-semibold text-orange-800 mb-2 capitalize">
                  {key.replace(/_/g, ' ')}
                </h4>
                <p className="text-orange-700">
                  {value || 'Not provided or Not found'}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default ResumeAnalyzer