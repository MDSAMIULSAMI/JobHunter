const JobCard = ({ job }) => {
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

  return (
    <div className="bg-gradient-to-r from-orange-50 to-amber-50 border border-orange-200 rounded-xl p-6 hover:shadow-lg transition-all duration-300 transform hover:scale-[1.02]">
      <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
        <div className="flex-1">
          <div className="flex items-start justify-between mb-3">
            <h4 className="text-xl font-bold text-orange-800 hover:text-orange-600 transition-colors">
              <a href={job.job_url} target="_blank" rel="noopener noreferrer">
                {job.title}
              </a>
            </h4>
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
                {job.is_remote && <span className="ml-2 bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">Remote</span>}
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
        </div>
      </div>
    </div>
  )
}

export default JobCard