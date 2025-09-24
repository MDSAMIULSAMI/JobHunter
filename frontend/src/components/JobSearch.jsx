import { useState } from 'react'
import LoadingSpinner from './LoadingSpinner'
import JobCard from './JobCard'
import ResumeDownloadModal from './ResumeDownloadModal'

const JobSearch = () => {
  const [searchData, setSearchData] = useState({
    location: 'India',
    search_keyword: '',
    results_wanted: 10
  })
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [searchPerformed, setSearchPerformed] = useState(false)
  
  // New state for resume customization
  const [showDownloadModal, setShowDownloadModal] = useState(false)
  const [customizedResumeData, setCustomizedResumeData] = useState(null)
  const [selectedJob, setSelectedJob] = useState(null)

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!searchData.search_keyword.trim()) {
      setError('Please enter a search keyword')
      return
    }

    setLoading(true)
    setError('')
    setSearchPerformed(true)

    try {
      const response = await fetch('http://localhost:8000/jobs/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchData)
      })

      const data = await response.json()
      
      if (data.success) {
        setJobs(data.jobs || [])
      } else {
        setError(data.message || 'Failed to search jobs')
        setJobs([])
      }
    } catch {
      setError('Failed to connect to the server. Please make sure the backend is running.')
      setJobs([])
    } finally {
      setLoading(false)
    }
  }

  const handleResumeCustomized = (latexData, job) => {
    setCustomizedResumeData(latexData)
    setSelectedJob(job)
    setShowDownloadModal(true)
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Search Form */}
      <div className="bg-white rounded-2xl shadow-xl p-8 mb-8 border border-orange-100">
        <h2 className="text-3xl font-bold text-orange-800 mb-6 text-center">
          🔍 Find Your Perfect Job
        </h2>
        
        <form onSubmit={handleSearch} className="space-y-6">
          <div className="grid md:grid-cols-3 gap-6">
            <div className="space-y-2">
              <label className="block text-sm font-semibold text-orange-700">
                📍 Location
              </label>
              <input
                type="text"
                value={searchData.location}
                onChange={(e) => setSearchData({...searchData, location: e.target.value})}
                className="w-full px-4 py-3 border-2 border-orange-200 rounded-lg focus:border-orange-500 focus:outline-none transition-colors duration-200"
                placeholder="e.g., India, New York, Remote"
              />
            </div>
            
            <div className="space-y-2">
              <label className="block text-sm font-semibold text-orange-700">
                💼 Job Title
              </label>
              <input
                type="text"
                value={searchData.search_keyword}
                onChange={(e) => setSearchData({...searchData, search_keyword: e.target.value})}
                className="w-full px-4 py-3 border-2 border-orange-200 rounded-lg focus:border-orange-500 focus:outline-none transition-colors duration-200"
                placeholder="e.g., Software Engineer, Data Scientist"
                required
              />
            </div>
            
            <div className="space-y-2">
              <label className="block text-sm font-semibold text-orange-700">
                📊 Results Count
              </label>
              <select
                value={searchData.results_wanted}
                onChange={(e) => setSearchData({...searchData, results_wanted: parseInt(e.target.value)})}
                className="w-full px-4 py-3 border-2 border-orange-200 rounded-lg focus:border-orange-500 focus:outline-none transition-colors duration-200"
              >
                <option value={10}>10 jobs</option>
                <option value={25}>25 jobs</option>
                <option value={50}>50 jobs</option>
                <option value={100}>100 jobs</option>
              </select>
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
            {loading ? <LoadingSpinner /> : '🚀 Search Jobs'}
          </button>
        </form>
      </div>

      {/* Results */}
      {searchPerformed && (
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-orange-100">
          <h3 className="text-2xl font-bold text-orange-800 mb-6">
            Search Results {jobs.length > 0 && `(${jobs.length} jobs found)`}
          </h3>
          
          {loading ? (
            <div className="flex justify-center py-12">
              <LoadingSpinner size="large" />
            </div>
          ) : jobs.length > 0 ? (
            <div className="grid gap-6">
              {jobs.map((job, index) => (
                <JobCard 
                  key={job.id || index} 
                  job={job} 
                  resumeData={null} // No resume data in regular job search
                  onResumeCustomized={handleResumeCustomized}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">🔍</div>
              <p className="text-orange-600 text-lg">
                {error ? 'No jobs found. Try different keywords or location.' : 'Start your job search above!'}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Resume Download Modal */}
      <ResumeDownloadModal
        isOpen={showDownloadModal}
        onClose={() => setShowDownloadModal(false)}
        latexData={customizedResumeData}
        jobTitle={selectedJob?.title || 'Job'}
      />
    </div>
  )
}

export default JobSearch