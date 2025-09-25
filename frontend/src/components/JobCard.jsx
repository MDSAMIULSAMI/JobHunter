import { useState } from 'react'

const JobCard = ({ job, resumeData, onResumeCustomized }) => {
  const [isCustomizing, setIsCustomizing] = useState(false)
  
  const formatDate = (dateString) => {
    if (!dateString) return 'Date not specified'
    try {
      return new Date(dateString).toLocaleDateString()
    } catch {
      return dateString
    }
  }

  const formatSalary = (min, max, currency, interval) => {
    if (!min && !max) return null
    const curr = currency || 'USD'
    const int = interval || 'year'
    
    if (min && max) {
      return `${curr} ${min.toLocaleString()} - ${max.toLocaleString()} per ${int}`
    } else if (min) {
      return `${curr} ${min.toLocaleString()}+ per ${int}`
    } else if (max) {
      return `Up to ${curr} ${max.toLocaleString()} per ${int}`
    }
  }

  const handleCustomizeResume = async () => {
    if (!resumeData) {
      alert('Please upload and analyze your resume first to use this feature.')
      return
    }

    setIsCustomizing(true)
    
    try {
      // Generate PDF directly
      const response = await fetch('http://localhost:8000/resume/customize-for-job/pdf', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          job_id: job.id || `job_${Date.now()}`,
          job_title: job.title,
          job_description: job.description || 'No description available',
          company_name: job.company_name || 'Company not specified',
          resume_data: JSON.stringify(resumeData)
        })
      })

      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `resume_${job.title.replace(/[^a-zA-Z0-9]/g, '_')}.pdf`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        if (onResumeCustomized) {
          onResumeCustomized(job) // Remove the first parameter
        }
      } else {
        const errorData = await response.json()
        alert(`Failed to customize resume: ${errorData.detail || 'Unknown error'}`)
      }
    } catch (error) {
      console.error('Error customizing resume:', error)
      alert('Failed to customize resume. Please try again.')
    } finally {
      setIsCustomizing(false)
    }
  }

  return (
    <div className="bg-gradient-to-r from-orange-50 to-amber-50 border border-orange-200 rounded-xl p-6 hover:shadow-lg transition-all duration-300 transform hover:scale-[1.02]">
      <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
        <div className="flex-1">
          <div className="flex items-start justify-between mb-3">
            <div className="flex items-center gap-2">
              <h4 className="text-xl font-bold text-orange-800 hover:text-orange-600 transition-colors">
                <a href={job.job_url} target="_blank" rel="noopener noreferrer">
                  {job.title}
                </a>
              </h4>
              {job.is_remote !== undefined && (
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  job.is_remote 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-blue-100 text-blue-800'
                }`}>
                  {job.is_remote ? 'Remote' : 'On-site'}
                </span>
              )}
            </div>
            <span className="bg-orange-200 text-orange-800 px-3 py-1 rounded-full text-sm font-medium ml-4">
              {job.site}
            </span>
          </div>
          
          <div className="space-y-2 mb-4">
            {job.company_name && (
              <p className="text-orange-700 font-semibold flex items-center">
                🏢 {job.company_name}
              </p>
            )}
            
            {job.location && (
              <p className="text-orange-600 flex items-center">
                📍 {job.location}
              </p>
            )}
            
            {job.job_type && (
              <p className="text-orange-600 flex items-center">
                💼 {job.job_type}
              </p>
            )}
            
            <p className="text-orange-600 flex items-center">
              📅 {formatDate(job.date_posted)}
            </p>
            
            {formatSalary(job.min_amount, job.max_amount, job.currency, job.interval) && (
              <p className="text-green-700 font-semibold flex items-center">
                💰 {formatSalary(job.min_amount, job.max_amount, job.currency, job.interval)}
              </p>
            )}
          </div>
          
          {job.description && (
            <p className="text-orange-700 text-sm line-clamp-3 mb-4">
              {job.description.substring(0, 200)}...
            </p>
          )}
        </div>
        
        <div className="flex flex-col gap-2 md:ml-4">
          <a
            href={job.job_url}
            target="_blank"
            rel="noopener noreferrer"
            className="bg-gradient-to-r from-orange-500 to-amber-500 text-white px-6 py-2 rounded-full text-center font-semibold hover:shadow-md transition-all duration-200 transform hover:scale-105"
          >
            Apply Now
          </a>
          
          {job.company_url && (
            <a
              href={job.company_url}
              target="_blank"
              rel="noopener noreferrer"
              className="border-2 border-orange-300 text-orange-600 px-6 py-2 rounded-full text-center font-semibold hover:bg-orange-50 transition-all duration-200"
            >
              Company
            </a>
          )}
          
          {/* New Customize Resume Button */}
          <button
            onClick={handleCustomizeResume}
            disabled={isCustomizing || !resumeData}
            className={`px-6 py-2 rounded-full text-center font-semibold transition-all duration-200 ${
              resumeData 
                ? 'bg-gradient-to-r from-purple-500 to-indigo-500 text-white hover:shadow-md transform hover:scale-105' 
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
            title={!resumeData ? 'Upload and analyze your resume first' : 'Customize your resume for this job'}
          >
            {isCustomizing ? (
              <div className="flex items-center justify-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Generating...</span>
              </div>
            ) : (
              'Get Customized Resume'
            )}
          </button>
        </div>
      </div>
    </div>
  )
}

export default JobCard