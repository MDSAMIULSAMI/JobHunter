const LoadingSpinner = ({ size = 'normal' }) => {
  const sizeClasses = {
    small: 'w-4 h-4',
    normal: 'w-6 h-6',
    large: 'w-12 h-12'
  }

  return (
    <div className="flex items-center justify-center">
      <div className={`${sizeClasses[size]} border-2 border-white border-t-transparent rounded-full animate-spin`}></div>
      {size === 'large' && (
        <span className="ml-3 text-orange-600 font-semibold">Loading...</span>
      )}
    </div>
  )
}

export default LoadingSpinner