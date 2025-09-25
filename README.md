
## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/MDSAMIULSAMI/JobHunter.git
   cd FastAPI
   ```

2. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   Create a `.env` file in the backend directory:
   ```env
   RESUME_ANALYZER_API_URL=your_resume_analyzer_api_url
   ```

5. **Run the backend server**
   ```bash
   python main.py
   ```
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   Create a `.env.local` file:
   ```env
   VITE_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
   ```

4. **Run the development server**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

## 📚 API Documentation

### Job Search Endpoints

#### Search Jobs
```http
POST /jobs/search
```
Search for jobs across multiple platforms.

**Request Body:**
```json
{
  "search_keyword": "Software Engineer",
  "location": "New York, NY",
  "results_wanted": 50,
  "sites": ["linkedin", "indeed", "glassdoor"]
}
```

#### Get Available Sites
```http
GET /jobs/available-sites
```
Returns list of supported job sites.

### Resume Endpoints

#### Upload Resume for Analysis
```http
POST /resume/upload
```
Upload and analyze a PDF resume.

#### Custom Resume Builder
```http
POST /resume/custom-builder
```
Generate a custom resume based on requirements.

#### Job-Specific Resume Customization
```http
POST /resume/job-customization
```
Customize resume for a specific job posting.

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Python**: Core programming language
- **Pandas**: Data manipulation and analysis
- **BeautifulSoup**: Web scraping
- **ReportLab**: PDF generation
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Frontend
- **React 19**: Modern UI library
- **Vite**: Fast build tool
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Clerk**: Authentication and user management

### Job Scraping
- **LinkedIn**: Professional networking platform
- **Indeed**: Global job search engine
- **Glassdoor**: Company reviews and job listings
- **BDJobs**: Bangladesh-focused job portal

## 🌍 Supported Regions

- **Global**: LinkedIn, Indeed, Glassdoor
- **Bangladesh**: BDJobs (specialized for local market)
- **Location-aware**: Automatically selects appropriate job sites based on search location

## 🔧 Configuration

### Backend Configuration
- **CORS**: Configured for cross-origin requests
- **Logging**: Structured logging with different levels
- **Error Handling**: Comprehensive exception handling
- **Rate Limiting**: Built-in delays for respectful scraping

### Frontend Configuration
- **Authentication**: Clerk integration for secure user management
- **Routing**: Protected routes for authenticated users
- **Responsive Design**: Mobile-first approach with Tailwind CSS

## 📈 Performance Features

- **Concurrent Scraping**: Multi-threaded job scraping for faster results
- **Caching**: Optimized data processing and caching
- **Error Recovery**: Robust error handling and retry mechanisms
- **Pagination**: Efficient handling of large result sets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please open an issue in the GitHub repository or contact the development team.

## 🔮 Future Enhancements

- [ ] Additional job board integrations
- [ ] Advanced AI resume optimization
- [ ] Job application tracking
- [ ] Salary insights and analytics
- [ ] Mobile application
- [ ] Email notifications for new jobs
- [ ] Interview preparation tools

---

**Built with ❤️ for job seekers everywhere**