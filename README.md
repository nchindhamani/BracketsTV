# BracketsTV - Curated Interview Prep Web App

A modern, distraction-free web application for software engineering interview preparation using curated YouTube content.

## Features

- **Categorized Content**: DSA, System Design, Behavioral Questions, and Language-Specific Prep
- **Curated Video Feeds**: Only videos from trusted YouTube channels
- **Language-Specific Sections**: Sub-categories for top 10 programming languages
- **Distraction-Free Player**: Embedded player without YouTube comments or recommendations
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark Theme**: Professional, modern dark theme

## Tech Stack

- **Frontend**: React with Tailwind CSS
- **Backend**: Python FastAPI (Netlify Functions)
- **API**: YouTube Data API v3
- **Deployment**: Netlify
- **Package Management**: 
  - Python: `uv`
  - Frontend: `npm`

## Setup Instructions

### 1. Get YouTube API Key

1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Copy the API key

### 2. Configure Environment

1. Copy the example environment file:
   ```bash
   cp api/.env.example api/.env
   ```

2. Edit `api/.env` and add your YouTube API key:
   ```
   YOUTUBE_API_KEY=your_actual_api_key_here
   ```

### 3. Install Dependencies

#### Backend (Python)
```bash
# Install uv if you haven't already
pip install uv

# Install Python dependencies
uv pip install -r requirements.txt
```

#### Frontend (React)
```bash
cd frontend
npm install
```

### 4. Run Locally

#### Backend
```bash
cd api
uvicorn index:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm start
```

The app will be available at `http://localhost:3000`

### 5. Deploy to Netlify

1. Push your code to GitHub
2. Connect your repository to Netlify
3. Add the `YOUTUBE_API_KEY` environment variable in Netlify's dashboard
4. Deploy!

## Project Structure

```
interview_prep_app/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── index.js         # React entry point
│   │   └── index.css        # Tailwind CSS styles
│   ├── public/
│   │   └── index.html       # HTML template
│   ├── package.json         # Frontend dependencies
│   ├── tailwind.config.js   # Tailwind configuration
│   └── postcss.config.js    # PostCSS configuration
├── api/                     # Python backend
│   ├── index.py            # FastAPI application
│   └── .env                # Environment variables (create from .env.example)
├── requirements.txt        # Python dependencies
├── netlify.toml           # Netlify configuration
└── README.md              # This file
```

## API Endpoints

- `GET /api/videos?category=dsa` - Get DSA videos
- `GET /api/videos?category=system` - Get System Design videos
- `GET /api/videos?category=behavioral` - Get Behavioral videos
- `GET /api/videos?category=languages&subcategory=python` - Get Python videos
- `GET /api/health` - Health check

## Curated Channels

The app uses hand-picked YouTube channels for each category:

- **DSA**: NeetCode, freeCodeCamp.org, Abdul Bari, CS Dojo, etc.
- **System Design**: ByteByteGo, Gaurav Sen, Exponent, etc.
- **Behavioral**: Jeff H Sipe, Exponent, Dan Croitor, etc.
- **Languages**: Various trusted channels for each programming language

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

MIT License
