import { useState } from 'react'
import LoadingSpinner from './LoadingSpinner'
import JobCard from './JobCard'

const ResumeJobSearch = () => {
  const [file, setFile] = useState(null)
  const [keywords, setKeywords] = useState([])
  const [selectedKeyword, setSelectedKeyword] = useState('')
  const [customKeyword, setCustomKeyword] = useState('')
  const [resumeData, setResumeData] = useState(null)
  const [jobs, setJobs] = useState([])
  const [step, setStep] = useState(1)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [isSearching, setIsSearching] = useState(false)
  const [error, setError] = useState('')
  const [searchMessage, setSearchMessage] = useState('')
  const [location, setLocation] = useState('India')
  const [resultsWanted, setResultsWanted] = useState(10)
  const [dragActive, setDragActive] = useState(false)
  
  // New state for resume customization
  const [, setSelectedJob] = useState(null)
  const [, setIsCustomizing] = useState(false)
  
  // Add new state for PDF preview
  const [, setPdfUrl] = useState(null)
  const [, setShowPdfPreview] = useState(false)
  const [, setCustomizedResumeData] = useState(null)

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
  }

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      handleFileSelect(selectedFile)
    }
  }

  const analyzeResume = async () => {
    if (!file) {
      setError('Please select a PDF file first')
      return
    }

    setIsAnalyzing(true)
    setError('')
  
    const formData = new FormData()
    formData.append('resume_file', file)
  
    try {
      const response = await fetch('http://localhost:8000/resume/upload-with-keywords', {
        method: 'POST',
        body: formData,
      })
  
      const data = await response.json()
  
      if (data.success) {
        // Parse search_keywords from JSON string
        let extractedKeywords = []
        try {
          if (data.resume_data.search_keywords && data.resume_data.search_keywords !== "Not provided or Not found") {
            extractedKeywords = JSON.parse(data.resume_data.search_keywords)
          }
        } catch (parseError) {
          console.error('Error parsing search_keywords:', parseError)
          // Fallback to empty array if parsing fails
          extractedKeywords = []
        }
        
        setKeywords(extractedKeywords)
        setResumeData(data.resume_data)
        setStep(2)
      } else {
        setError('Failed to analyze resume')
      }
    } catch (err) {
      setError('Error analyzing resume. Please try again.')
      console.error('Resume analysis error:', err)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const searchJobs = async () => {
    if (!selectedKeyword) {
      setError('Please select a keyword first')
      return
    }

    setIsSearching(true)
    setError('')
    setSearchMessage('')

    try {
      const response = await fetch('http://localhost:8000/resume/search-by-keyword', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          selected_keyword: selectedKeyword,
          location: location,
          results_wanted: resultsWanted
        })
      })

      const data = await response.json()

      if (data.success) {
        setJobs(data.jobs || [])
        setSearchMessage(`Found ${data.jobs?.length || 0} jobs for "${selectedKeyword}" in ${location}`)
        setStep(3)
      } else {
        setError(data.message || 'Failed to search jobs')
      }
    } catch (err) {
      setError('Error searching jobs. Please try again.')
      console.error('Job search error:', err)
    } finally {
      setIsSearching(false)
    }
  }

  const searchJobsWithCustomKeyword = async () => {
    if (!customKeyword.trim()) {
      setError('Please enter a keyword first')
      return
    }

    setIsSearching(true)
    setError('')
    setSearchMessage('')

    try {
      const response = await fetch('http://localhost:8000/resume/search-by-keyword', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          selected_keyword: customKeyword.trim(),
          location: location,
          results_wanted: resultsWanted
        })
      })

      const data = await response.json()

      if (data.success) {
        setJobs(data.jobs || [])
        setSelectedKeyword(customKeyword.trim())
        setSearchMessage(`Found ${data.jobs?.length || 0} jobs for "${customKeyword.trim()}" in ${location}`)
        setStep(3)
      } else {
        setError(data.message || 'Failed to search jobs')
      }
    } catch (err) {
      setError('Error searching jobs. Please try again.')
      console.error('Job search error:', err)
    } finally {
      setIsSearching(false)
    }
  }

  const resetSearch = () => {
    setStep(1)
    setFile(null)
    setKeywords([])
    setResumeData(null)
    setSelectedKeyword('')
    setJobs([])
    setSearchMessage('')
    setError('')
  }

  const handleCustomizeResume = async (job, resumeData) => {
    setIsCustomizing(true)
    try {
      // Add debugging to see the actual job object structure
      console.log('Full job object:', job)
      console.log('Job keys:', Object.keys(job))
      console.log('Starting resume customization for job:', job.title)
      
      // Prepare job details as JSON string
      const jobDetails = JSON.stringify({
        id: job.id || `job_${Date.now()}`,
        title: job.title || 'Job Position',
        description: job.description || `${job.title} at ${job.company_name}`,
        company_name: job.company_name || job.company || 'Company',
        location: job.location || 'Not specified',
        job_type: job.job_type || 'Not specified',
        site: job.site || 'Unknown',
        job_url: job.job_url || '',
        salary_min: job.salary_min || null,
        salary_max: job.salary_max || null,
        salary_currency: job.salary_currency || null,
        salary_interval: job.salary_interval || null,
        date_posted: job.date_posted || null,
        is_remote: job.is_remote || false
      })
      
      // Prepare resume details as JSON string
      const resumeDetails = typeof resumeData === 'string' ? resumeData : JSON.stringify(resumeData)
      
      // First get the LaTeX code
      const response = await fetch('http://localhost:8000/resume/custom-builder', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          job_details: jobDetails,
          resume_details: resumeDetails
        })
      })

      if (response.ok) {
        const data = await response.json()
        console.log('Resume customization API response received')
        
        if (data.success && data.latex_code) {
          // Parse the latex_code which is a JSON string
          let latexData
          try {
            latexData = JSON.parse(data.latex_code)
          } catch (parseError) {
            console.error('Error parsing latex_code:', parseError)
            throw new Error('Invalid LaTeX data format')
          }
          
          if (latexData.result && latexData.result.Output && latexData.result.Output.latex_resume) {
            const latexCode = latexData.result.Output.latex_resume
            console.log('LaTeX code extracted, length:', latexCode.length)
            
            // Store the LaTeX code for download
            setCustomizedResumeData(latexCode)
            
            // Now get the PDF from backend
            const pdfResponse = await fetch('http://localhost:8000/resume/custom-builder/pdf', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                job_details: jobDetails,
                resume_details: resumeDetails
              })
            })
            
            if (pdfResponse.ok) {
              const pdfBlob = await pdfResponse.blob()
              const pdfBlobUrl = URL.createObjectURL(pdfBlob)
              setPdfUrl(pdfBlobUrl)
              setSelectedJob(job)
              setShowPdfPreview(true)
              
              console.log('Resume customization completed successfully')
            } else {
              throw new Error('Failed to generate PDF')
            }
          } else {
            console.error('Invalid LaTeX data structure:', latexData)
            throw new Error('Invalid LaTeX data structure')
          }
        } else {
          console.error('Invalid response structure:', data)
          throw new Error('Invalid response from server')
        }
        
      } else {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }))
        console.error('API Error:', response.status, errorData)
        throw new Error(`Failed to generate customized resume: ${errorData.detail || 'Server error'}`)
      }
    } catch (error) {
      console.error('Error in handleCustomizeResume:', error)
      alert(`Error generating customized resume: ${error.message}. Please try again.`)
    } finally {
      setIsCustomizing(false)
    }
  }

  const handleResumeCustomized = (job) => {
    setSelectedJob(job)
    handleCustomizeResume(job, resumeData)
  }

  return (
    <div className="max-w-6xl mx-auto p-6 bg-white rounded-xl shadow-lg">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-4 text-center">
          🎯 Smart Resume Job Search
        </h2>
        <p className="text-gray-600 text-center">
          Upload your resume, select relevant keywords, and find matching jobs
          automatically
        </p>
      </div>

      {/* Progress Steps */}
      <div className="flex justify-center mb-8">
        <div className="flex items-center space-x-4">
          <div
            className={`flex items-center justify-center w-8 h-8 rounded-full ${
              step >= 1
                ? "bg-orange-500 text-white"
                : "bg-gray-300 text-gray-600"
            }`}
          >
            1
          </div>
          <div
            className={`w-16 h-1 ${
              step >= 2 ? "bg-orange-500" : "bg-gray-300"
            }`}
          ></div>
          <div
            className={`flex items-center justify-center w-8 h-8 rounded-full ${
              step >= 2
                ? "bg-orange-500 text-white"
                : "bg-gray-300 text-gray-600"
            }`}
          >
            2
          </div>
          <div
            className={`w-16 h-1 ${
              step >= 3 ? "bg-orange-500" : "bg-gray-300"
            }`}
          ></div>
          <div
            className={`flex items-center justify-center w-8 h-8 rounded-full ${
              step >= 3
                ? "bg-orange-500 text-white"
                : "bg-gray-300 text-gray-600"
            }`}
          >
            3
          </div>
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-600">{error}</p>
        </div>
      )}

      {/* Step 1: Upload Resume */}
      {step === 1 && (
        <div className="space-y-6">
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

          <div className="text-center">
            <button
              onClick={analyzeResume}
              disabled={!file || isAnalyzing}
              className="w-full mt-6 bg-gradient-to-r from-orange-500 to-amber-500 text-white py-4 rounded-lg font-semibold text-lg hover:shadow-lg transition-all duration-300 transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isAnalyzing ? (
                <div className="flex items-center justify-center space-x-2">
                  <LoadingSpinner size="small" />
                  <span>Analyzing Resume...</span>
                </div>
              ) : (
                "🔍 Analyze Resume & Extract Keywords"
              )}
            </button>
          </div>
        </div>
      )}

      {/* Step 2: Select Keywords */}
      {step === 2 && (
        <div className="space-y-6">
          <div className="text-center">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              Select a keyword to search for jobs
            </h3>
            <p className="text-gray-600 mb-6">
              We found {keywords.length} relevant keywords from your resume
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {keywords.map((keyword, index) => (
              <button
                key={index}
                onClick={() => setSelectedKeyword(keyword)}
                className={`p-3 rounded-lg border-2 transition-all duration-300 ${
                  selectedKeyword === keyword
                    ? "border-orange-500 bg-orange-50 text-orange-700"
                    : "border-gray-200 hover:border-orange-300 hover:bg-orange-50"
                }`}
              >
                {keyword}
              </button>
            ))}
          </div>

          {/* Manual Keyword Entry */}
          <div className="border-t pt-6">
            <h4 className="text-lg font-medium text-gray-800 mb-4 text-center">
              Or enter your own keyword
            </h4>
            <div className="max-w-md mx-auto">
              <input
                type="text"
                value={customKeyword}
                onChange={(e) => setCustomKeyword(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                placeholder="Enter custom keyword (e.g., React Developer)"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Location
              </label>
              <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                placeholder="e.g., India, New York, Remote"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Number of Results
              </label>
              <select
                value={resultsWanted}
                onChange={(e) => setResultsWanted(parseInt(e.target.value))}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              >
                <option value={5}>5 jobs</option>
                <option value={10}>10 jobs</option>
                <option value={20}>20 jobs</option>
                <option value={50}>50 jobs</option>
              </select>
            </div>
          </div>

          <div className="flex justify-center space-x-4">
            <button
              onClick={resetSearch}
              className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Start Over
            </button>

            {/* Show custom keyword search if user has entered something, otherwise show selected keyword */}
            {customKeyword.trim() ? (
              <button
                onClick={searchJobsWithCustomKeyword}
                disabled={isSearching}
                className="px-8 py-3 bg-gradient-to-r from-orange-500 to-amber-500 text-white font-semibold rounded-lg shadow-md hover:shadow-lg transform hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                {isSearching ? (
                  <div className="flex items-center space-x-2">
                    <LoadingSpinner size="small" />
                    <span>Searching Jobs...</span>
                  </div>
                ) : (
                  `Search Jobs for "${customKeyword.trim()}"`
                )}
              </button>
            ) : selectedKeyword ? (
              <button
                onClick={searchJobs}
                disabled={isSearching}
                className="px-8 py-3 bg-gradient-to-r from-orange-500 to-amber-500 text-white font-semibold rounded-lg shadow-md hover:shadow-lg transform hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                {isSearching ? (
                  <div className="flex items-center space-x-2">
                    <LoadingSpinner size="small" />
                    <span>Searching Jobs...</span>
                  </div>
                ) : (
                  `Search Jobs for "${selectedKeyword}"`
                )}
              </button>
            ) : null}
          </div>
        </div>
      )}

      {/* Step 3: Job Results */}
      {step === 3 && (
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-orange-100">
          <div className="text-center">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              Job Search Results
            </h3>
            <p className="text-gray-600 mb-4">{searchMessage}</p>
            <div className="flex justify-center space-x-4 mb-6">
              <span className="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm">
                Keyword: {selectedKeyword}
              </span>
              <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                Location: {location}
              </span>
            </div>
          </div>

          {jobs.length > 0 ? (
            <div className="grid gap-6">
              {jobs.map((job, index) => (
                <JobCard 
                  key={index} 
                  job={job} 
                  resumeData={resumeData}
                  onResumeCustomized={handleResumeCustomized}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">
                No jobs found for the selected criteria.
              </p>
              <p className="text-gray-400 mt-2">
                Try selecting a different keyword or location.
              </p>
            </div>
          )}

          <div className="flex justify-center space-x-4 mt-6">
            <button
              onClick={() => setStep(2)}
              className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Try Different Keyword
            </button>
            <button
              onClick={resetSearch}
              className="px-6 py-2 bg-gradient-to-r from-orange-500 to-amber-500 text-white rounded-lg hover:shadow-lg transition-all duration-300"
            >
              Upload New Resume
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default ResumeJobSearch