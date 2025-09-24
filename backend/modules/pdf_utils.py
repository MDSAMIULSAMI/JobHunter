"""
PDF generation utilities for LaTeX resume conversion.
"""

import os
import re
import json
import tempfile
import subprocess
import logging
from typing import Optional, List

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import black

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PDFGenerator:
    """Utility class for generating PDFs from LaTeX code."""

    # Section patterns for extracting content
    SECTION_PATTERNS = [
        ("Professional Summary", r"\\section\*?\{(?:Professional\s+Summary|Summary|Profile)\}(.*?)(?=\\section|\\end\{document\})"),
        ("Skills", r"\\section\*?\{(?:Skills|Technical Skills|Core Competencies)\}(.*?)(?=\\section|\\end\{document\})"),
        ("Professional Experience", r"\\section\*?\{(?:Professional Experience|Experience|Work Experience|Employment History)\}(.*?)(?=\\section|\\end\{document\})"),
        ("Education", r"\\section\*?\{(?:Education|Academic Background|Educational Background)\}(.*?)(?=\\section|\\end\{document\})"),
        ("Projects", r"\\section\*?\{(?:Projects|Personal Projects|Key Projects)\}(.*?)(?=\\section|\\end\{document\})"),
    ]

    @staticmethod
    def latex_to_pdf_with_pdflatex(latex_code: str) -> Optional[bytes]:
        """
        Convert LaTeX code to PDF using pdflatex binary (requires LaTeX installation).

        Args:
            latex_code: LaTeX source code or JSON containing LaTeX.

        Returns:
            PDF bytes if successful, None if failed.
        """
        try:
            # Check if the input is JSON and extract LaTeX content
            actual_latex = latex_code
            if latex_code.strip().startswith('{'):
                try:
                    import json
                    data = json.loads(latex_code)
                    # Extract LaTeX from nested JSON structure
                    if 'result' in data and 'Output' in data['result'] and 'latex_resume' in data['result']['Output']:
                        actual_latex = data['result']['Output']['latex_resume']
                    elif 'latex_resume' in data:
                        actual_latex = data['latex_resume']
                    elif 'latex' in data:
                        actual_latex = data['latex']
                    else:
                        logger.error(f"Could not find LaTeX content in JSON: {list(data.keys())}")
                        return None
                except json.JSONDecodeError:
                    logger.error("Input appears to be JSON but failed to parse")
                    return None
            
            # Clean up escaped LaTeX strings
            cleaned_latex = actual_latex
            # Handle multiple levels of escaping
            cleaned_latex = cleaned_latex.replace('\\\\\\\\', '\\\\')
            while '\\\\\\\\' in cleaned_latex:
                cleaned_latex = cleaned_latex.replace('\\\\\\\\', '\\\\')
            
            with tempfile.TemporaryDirectory() as temp_dir:
                tex_file = os.path.join(temp_dir, "resume.tex")
                pdf_file = os.path.join(temp_dir, "resume.pdf")
                
                # Write cleaned LaTeX to file
                with open(tex_file, "w", encoding="utf-8") as f:
                    f.write(cleaned_latex)

                # Run pdflatex using subprocess
                result = subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                     "-output-directory", temp_dir, tex_file],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=temp_dir
                )

                if result.returncode == 0:
                    if os.path.exists(pdf_file):
                        with open(pdf_file, "rb") as f:
                            logger.info("PDF generated successfully using pdflatex binary.")
                            return f.read()
                    else:
                        logger.error("PDF file not created despite pdflatex success.")
                else:
                    logger.error(f"pdflatex failed with return code {result.returncode}")
                    logger.error(f"Stderr: {result.stderr}")
                    if result.stdout:
                        logger.error(f"Stdout: {result.stdout}")
                    # Log the first few lines of LaTeX for debugging
                    latex_preview = '\n'.join(cleaned_latex.split('\n')[:10])
                    logger.error(f"LaTeX content preview (first 10 lines):\n{latex_preview}")
                    # Log the actual LaTeX content for debugging
                    logger.debug(f"LaTeX content: {cleaned_latex[:200]}...")

        except subprocess.TimeoutExpired:
            logger.error("pdflatex process timed out.")
        except FileNotFoundError:
            logger.error("pdflatex binary not found. Please ensure MacTeX is installed and in PATH.")
        except Exception as e:
            logger.exception(f"Unexpected error in latex_to_pdf_with_pdflatex: {e}")

        return None

    @staticmethod
    def _clean_latex_content(text: str) -> str:
        """
        Clean LaTeX commands and convert to simple HTML-like markup.

        Args:
            text: Raw LaTeX content.

        Returns:
            Cleaned text.
        """
        # First, extract content from textbf and textit commands
        text = re.sub(r"\\textbf\{([^}]+)\}", r"\1", text)  # Remove \textbf but keep content
        text = re.sub(r"\\textit\{([^}]+)\}", r"\1", text)  # Remove \textit but keep content
        
        # Handle other common LaTeX commands
        text = re.sub(r"\\item\s+", "• ", text)
        text = re.sub(r"\\begin\{itemize\}|\s*\\end\{itemize\}", "", text)
        text = re.sub(r"\\\\", "<br/>", text)
        text = re.sub(r"\\hfill", " - ", text)
        
        # Remove any remaining LaTeX commands with braces
        text = re.sub(r"\\[a-zA-Z]+\*?\{[^}]*\}", "", text)
        # Remove any remaining LaTeX commands without braces
        text = re.sub(r"\\[a-zA-Z]+\*?", "", text)
        # Clean up extra whitespace
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @staticmethod
    def latex_to_pdf_fallback(latex_code: str) -> bytes:
        """
        Fallback PDF generation using ReportLab when LaTeX is not available.

        Args:
            latex_code: LaTeX source code.

        Returns:
            PDF bytes.
        """
        try:
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                temp_path = temp_file.name

            doc = SimpleDocTemplate(
                temp_path, pagesize=A4,
                rightMargin=72, leftMargin=72,
                topMargin=72, bottomMargin=18
            )

            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                "CustomTitle",
                parent=styles["Heading1"],
                fontSize=18, spaceAfter=30,
                alignment=1, textColor=black
            )
            heading_style = ParagraphStyle(
                "CustomHeading",
                parent=styles["Heading2"],
                fontSize=14, spaceAfter=12,
                spaceBefore=12, textColor=black
            )
            normal_style = ParagraphStyle(
                "CustomNormal",
                parent=styles["Normal"],
                fontSize=11, spaceAfter=6,
                textColor=black
            )

            content: List[Paragraph] = []

            # Extract name
            name_match = re.search(r"\\textbf\{\\Huge\s+([^}]+)\}", latex_code)
            if not name_match:
                name_match = re.search(r"\\begin\{center\}.*?\\textbf\{([^}]+)\}", latex_code, re.DOTALL)
            if name_match:
                content.append(Paragraph(name_match.group(1).strip(), title_style))
                content.append(Spacer(1, 12))

            # Extract contact info
            contact_info = []
            email_match = re.search(r"\\href\{mailto:([^}]+)\}", latex_code)
            if email_match:
                contact_info.append(f"Email: {email_match.group(1)}")

            phone_match = re.search(r"(?:\\faPhone|Phone:?)\s*([+\d\s()-]+)", latex_code)
            if phone_match:
                contact_info.append(f"Phone: {phone_match.group(1).strip()}")

            location_match = re.search(r"(?:\\faMapMarker|Location:?)\s*([^,\\]+(?:,[^,\\]+)*)", latex_code)
            if location_match:
                contact_info.append(f"Location: {location_match.group(1).strip()}")

            if contact_info:
                content.append(Paragraph(" | ".join(contact_info), normal_style))
                content.append(Spacer(1, 20))

            # Extract sections
            for section_name, pattern in PDFGenerator.SECTION_PATTERNS:
                match = re.search(pattern, latex_code, re.DOTALL | re.IGNORECASE)
                if match:
                    content.append(Paragraph(section_name, heading_style))
                    cleaned_text = PDFGenerator._clean_latex_content(match.group(1))
                    for para in filter(None, cleaned_text.split("<br/>")):
                        content.append(Paragraph(para.strip(), normal_style))
                    content.append(Spacer(1, 12))

            doc.build(content)

            with open(temp_path, "rb") as f:
                pdf_bytes = f.read()

            os.unlink(temp_path)
            return pdf_bytes

        except Exception as e:
            logger.exception(f"Error in latex_to_pdf_fallback: {e}")
            raise

    @staticmethod
    def generate_pdf_from_latex(latex_code: str) -> bytes:
        """
        Generate PDF from LaTeX code using latex package with ReportLab fallback.

        Args:
            latex_code: LaTeX source code.

        Returns:
            PDF bytes.
        """
        # Try LaTeX compilation first
        pdf_bytes = PDFGenerator.latex_to_pdf_with_pdflatex(latex_code)
        if pdf_bytes:
            return pdf_bytes
        
        # Use ReportLab fallback when LaTeX fails
        logger.warning("LaTeX compilation failed, using ReportLab fallback")
        try:
            return PDFGenerator.latex_to_pdf_fallback(latex_code)
        except Exception as e:
            logger.error(f"Both LaTeX and ReportLab fallback failed: {e}")
            raise Exception("PDF generation failed. Both LaTeX and ReportLab methods failed.")