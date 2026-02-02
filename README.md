# AI Automation - Cold Email Agent

A modern web application that generates high-converting Upwork proposals using AI.

## 🚀 Features

- **AI-Powered Proposal Generation**: Transform job descriptions into winning proposals
- **Smart Job Analysis**: Automatically extracts role, company, skills, and experience requirements
- **Premium UI/UX**: Modern gradient design with glassmorphism effects
- **Edit Mode**: Fine-tune generated proposals before copying
- **Job Insights Dashboard**: Visual breakdown of extracted job details
- **Web Scraping**: Supports both URLs and raw text input (with anti-blocking headers)

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **LLM**: Groq (llama-3.3-70b-versatile)
- **AI Orchestration**: LangChain
- **Web Scraping**: BeautifulSoup4, WebBaseLoader
- **Vector Store**: ChromaDB (for future enhancements)

### Frontend
- **Framework**: React + Vite
- **Styling**: Tailwind CSS v4
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Markdown Rendering**: react-markdown

## 📦 Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- Groq API Key

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Run the server:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`

## 🎨 UI/UX Highlights

- **Color Palette**: Indigo/Purple/Pink gradient theme
- **Sidebar Navigation**: Modular, ready for multiple tools
- **Responsive Design**: Mobile-friendly with collapsible sidebar
- **Micro-interactions**: Smooth hover states, scale animations
- **Glassmorphism**: Backdrop blur effects for modern aesthetics

## 📁 Project Structure

```
coldEmailAgent/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── utils.py             # AI logic (scraping, extraction, generation)
│   ├── db.py                # ChromaDB setup
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Sidebar.jsx
│   │   ├── tools/
│   │   │   └── ProposalGenerator.jsx
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
└── README.md
```

## 🔑 Key Features Explained

### Proposal Generation Engine
Uses a "Mental Hunter" framework:
1. **Diagnosis**: Validates client pain points
2. **Authority**: Explains approach and ROI
3. **Proof**: Demonstrates past results
4. **Power CTA**: Commands next steps confidently

### Smart Extraction
LLM-powered structured data extraction from job descriptions:
- Role
- Company Name
- Summary
- Required Experience
- Key Skills

### Temperature Optimization
- Extraction: `temp=0` (accuracy)
- Proposal Writing: `temp=0.8` (creativity)

## 🚀 Future Enhancements

- [ ] Additional AI tools (email templates, cover letters, etc.)
- [ ] User authentication and saved proposals
- [ ] ChromaDB integration for portfolio matching
- [ ] A/B testing different proposal frameworks
- [ ] Browser extension for one-click generation

## 📝 License

MIT

## 👨‍💻 Author

Built with ❤️ using AI-assisted development
