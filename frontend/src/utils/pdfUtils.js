// Utility function to convert LaTeX to PDF and download
export const generateAndDownloadPDF = async (latexCode, jobTitle = 'job') => {
  try {
    // For LaTeX to PDF conversion, we'll use a service like LaTeX.js or send to backend
    // For now, let's create a simple implementation that downloads the LaTeX file
    // and provides instructions for PDF conversion
    
    const blob = new Blob([latexCode], { type: 'text/plain' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `customized_resume_${jobTitle.replace(/[^a-zA-Z0-9]/g, '_')}.tex`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    // Show instructions for PDF conversion
    alert(`LaTeX file downloaded! To convert to PDF:
1. Install LaTeX (MiKTeX, TeX Live, or MacTeX)
2. Run: pdflatex your_resume.tex
3. Or use online converters like Overleaf`)
    
    return true
  } catch (error) {
    console.error('Error generating PDF:', error)
    alert('Error generating PDF. Please try again.')
    return false
  }
}

// Alternative: If you want to use a LaTeX to PDF service
export const convertLatexToPDF = async (latexCode) => {
  try {
    // This would call a LaTeX to PDF conversion service
    // For example, using LaTeX.js or a backend service
    const response = await fetch('/api/latex-to-pdf', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ latex: latexCode })
    })
    
    if (response.ok) {
      const blob = await response.blob()
      return blob
    }
    throw new Error('Conversion failed')
  } catch (error) {
    console.error('LaTeX to PDF conversion error:', error)
    throw error
  }
}