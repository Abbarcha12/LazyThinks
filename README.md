# AutomateX - AI Automation Suite

A modern web application featuring AI-powered tools for proposal generation and UGC video script creation.

## 🚀 Features

### Proposal Generator
- **AI-Powered Proposal Generation**: Transform job descriptions into winning proposals
- **Smart Job Analysis**: Automatically extracts role, company, skills, and experience requirements
- **Edit Mode**: Fine-tune generated proposals before copying
- **Job Insights Dashboard**: Visual breakdown of extracted job details
- **Web Scraping**: Supports both URLs and raw text input (with anti-blocking headers)

### UGC Video Generator ✨ NEW
- **Shot-by-Shot Script Generation**: AI creates complete UGC video scripts following industry best practices
- **5-Part UGC Structure**: Hook → Problem → Solution → Proof → CTA framework
- **Ready-to-Use Prompts**: Get image and video generation prompts for HeyGen/Runway
- **Voice Scripts**: Complete scripts optimized for ElevenLabs voice generation
- **Production Guide**: Step-by-step instructions for creating videos with CapCut
- **Multiple Platforms**: Optimized for Instagram Reels, TikTok, and YouTube Shorts
- **Customizable**: Choose tone, length, and target audience

### Data Analytics Tool 🎯 LATEST
- **Database Management**: Store and manage analytics records with SQLite
- **Smart Record System**: Track name, category, value, and custom metadata (JSON)
- **AI-Powered Analysis**: Analyze your data using Llama 3 or Grok models
- **Multiple LLM Models**: Choose from Llama 3.3 70B, Mixtral 8x7B, or Llama 3.1 70B
- **Natural Language Queries**: Ask questions about your data in plain English
- **CRUD Operations**: Create, read, and delete records with a modern UI
- **Markdown Results**: Analysis results formatted for easy reading
- **Real-time Updates**: Instant feedback on all database operations

### UI/UX
- **Premium Design**: Modern gradient design with glassmorphism effects
- **Sidebar Navigation**: Modular, ready for multiple tools
- **Responsive**: Mobile-friendly with collapsible sidebar

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **LLM**: Groq (llama-3.3-70b-versatile, mixtral-8x7b-32768)
- **AI Orchestration**: LangChain
- **Database**: SQLite with SQLAlchemy ORM
- **Web Scraping**: BeautifulSoup4, WebBaseLoader
- **Vector Store**: ChromaDB

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
│   ├── main.py                  # FastAPI app with all API endpoints
│   ├── utils.py                 # AI logic (scraping, extraction, generation)
│   ├── db.py                    # ChromaDB setup
│   ├── analytics_models.py      # SQLAlchemy models for analytics
│   ├── analytics_utils.py       # LLM analysis utilities
│   ├── analytics.db             # SQLite database (auto-generated)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Sidebar.jsx
│   │   ├── tools/
│   │   │   ├── ProposalGenerator.jsx
│   │   │   ├── UGCVideoGenerator.jsx
│   │   │   └── DataAnalytics.jsx
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
- UGC Script Generation: `temp=0.9` (maximum creativity)

### UGC Video Production Workflow
Generated scripts follow industry-standard 5-part structure:
1. **Hook** (3 seconds) - Grab attention
2. **Problem** (5-8 seconds) - Establish pain point  
3. **Solution** (8-12 seconds) - Introduce product
4. **Proof/Demo** (8-12 seconds) - Build credibility
5. **CTA** (3-5 seconds) - Drive action

Each shot includes:
- Scene description
- Natural UGC-style script
- Image prompt (for first-frame generation)
- Video prompt (for HeyGen/Runway)
- Production notes

## 🚀 Future Enhancements

- [x] ~~Additional AI tools (email templates, cover letters, etc.)~~ - **UGC Video Generator added!**
- [ ] UGC Video History & Templates
- [ ] Full automation (Option B): Auto-generate videos via HeyGen/Runway APIs
- [ ] User authentication and saved proposals/scripts
- [ ] ChromaDB integration for portfolio matching
- [ ] A/B testing different proposal frameworks
- [ ] Browser extension for one-click generation

## 📝 License

MIT

## 👨‍💻 Author

Built with ❤️ using AI-assisted development
