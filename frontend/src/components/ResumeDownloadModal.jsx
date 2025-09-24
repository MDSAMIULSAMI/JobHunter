import { useState, useEffect } from "react";

const ResumeDownloadModal = ({ isOpen, onClose, latexData, jobTitle }) => {
  const [pdfUrl, setPdfUrl] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  // Auto-convert LaTeX to PDF when modal opens
  useEffect(() => {
    if (isOpen && latexData) {
      convertLatexToPdf();
    }
  }, [isOpen, latexData]);

  const convertLatexToPdf = async () => {
    setIsLoading(true);
    setError("");

    try {
      // Using a LaTeX to PDF conversion service
      const response = await fetch("https://latex.codecogs.com/pdf.download", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `latex=${encodeURIComponent(
          latexData.result.Output.latex_resume
        )}`,
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        setPdfUrl(url);
      } else {
        throw new Error("Failed to convert LaTeX to PDF");
      }
    } catch (err) {
      console.error("Error converting LaTeX to PDF:", err);
      setError(
        "Failed to convert resume to PDF. You can copy the LaTeX code and use an online LaTeX editor."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const downloadPdf = () => {
    if (pdfUrl) {
      const link = document.createElement("a");
      link.href = pdfUrl;
      link.download = `customized_resume_${jobTitle.replace(
        /[^a-zA-Z0-9]/g,
        "_"
      )}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  const copyLatexCode = () => {
    navigator.clipboard.writeText(latexData.result.Output.latex_resume);
    alert("LaTeX code copied to clipboard!");
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-6xl w-full max-h-[95vh] overflow-hidden">
        <div className="bg-gradient-to-r from-orange-500 to-amber-500 text-white p-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">📄 Resume Preview</h2>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 text-2xl font-bold"
            >
              ×
            </button>
          </div>
          <p className="mt-2 opacity-90">Resume customized for: {jobTitle}</p>
        </div>

        <div className="p-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
              {error}
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex flex-wrap gap-3 mb-6">
            {pdfUrl && (
              <button
                onClick={downloadPdf}
                className="bg-gradient-to-r from-orange-500 to-amber-500 text-white px-6 py-3 rounded-lg font-semibold hover:shadow-md transition-all duration-200"
              >
                📥 Download Resume
              </button>
            )}

            <button
              onClick={copyLatexCode}
              className="bg-gradient-to-r from-orange-400 to-amber-400 text-white px-6 py-3 rounded-lg font-semibold hover:shadow-md transition-all duration-200"
            >
              📋 Copy LaTeX Code
            </button>
          </div>

          {/* PDF Preview */}
          {isLoading ? (
            <div className="flex items-center justify-center h-96 bg-gray-100 rounded-lg">
              <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto mb-4"></div>
                <p className="text-gray-600">Generating PDF preview...</p>
              </div>
            </div>
          ) : pdfUrl ? (
            <div
              className="border rounded-lg overflow-hidden bg-gray-100"
              style={{ height: "70vh" }}
            >
              <iframe
                src={pdfUrl}
                width="100%"
                height="100%"
                title="Resume Preview"
                className="border-0"
              />
            </div>
          ) : (
            <div className="bg-orange-50 rounded-lg p-6">
              <h3 className="font-semibold text-orange-800 mb-4">
                LaTeX Code:
              </h3>
              <div className="bg-white border border-orange-200 rounded p-4 max-h-96 overflow-y-auto">
                <pre className="text-sm text-orange-700 whitespace-pre-wrap">
                  {latexData.result.Output.latex_resume}
                </pre>
              </div>
              <div className="mt-4 bg-orange-50 border border-orange-200 text-orange-700 px-4 py-3 rounded-lg">
                <p className="text-sm">
                  💡 <strong>Tip:</strong> Copy the LaTeX code and paste it into
                  online editors like
                  <a
                    href="https://www.overleaf.com"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="underline ml-1"
                  >
                    Overleaf
                  </a>{" "}
                  to compile and download your resume.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResumeDownloadModal;
