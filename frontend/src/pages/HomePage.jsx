import { useState } from 'react'
import Hero from '../components/Hero'
import JobSearch from '../components/JobSearch'
import ResumeJobSearch from '../components/ResumeJobSearch'

const HomePage = () => {
  const [activeTab, setActiveTab] = useState('search')

  return (
    <>
      <Hero />
      
      {/* Navigation Tabs */}
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-wrap justify-center gap-4 mb-8">
          <button
            onClick={() => setActiveTab('search')}
            className={`px-6 py-3 rounded-full font-semibold transition-all duration-300 transform hover:scale-105 ${
              activeTab === 'search'
                ? 'bg-gradient-to-r from-orange-500 to-amber-500 text-white shadow-lg'
                : 'bg-white text-orange-600 hover:bg-orange-50 shadow-md'
            }`}
          >
            🔍 Job Search
          </button>
          <button
            onClick={() => setActiveTab('smart-search')}
            className={`px-6 py-3 rounded-full font-semibold transition-all duration-300 transform hover:scale-105 ${
              activeTab === 'smart-search'
                ? 'bg-gradient-to-r from-orange-500 to-amber-500 text-white shadow-lg'
                : 'bg-white text-orange-600 hover:bg-orange-50 shadow-md'
            }`}
          >
            🎯 Smart Resume Search
          </button>
        </div>

        {/* Tab Content */}
        <div className="transition-all duration-500 ease-in-out">
          {activeTab === 'search' && <JobSearch />}
          {activeTab === 'smart-search' && <ResumeJobSearch />}
        </div>
      </div>
    </>
  )
}

export default HomePage