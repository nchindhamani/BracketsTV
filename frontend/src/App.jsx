import React, { useState, useEffect } from 'react';
import { FaCode, FaCogs, FaUserTie, FaCodeBranch, FaPlay, FaArrowLeft, FaExternalLinkAlt, FaPython, FaJs, FaJava, FaRust, FaDatabase } from 'react-icons/fa';
import { DiGo, DiSwift } from 'react-icons/di';
import './App.css';

// Custom color palette
const colors = {
  'dark-charcoal': '#21262D',
  'near-black': '#0D1117',
  'intermediate-gray': '#161B22',
  'glowing-cyan': '#00FFFF',
  'light-gray': '#E0E0E0'
};

// Custom TextIcon component for languages without specific icons
const TextIcon = ({ name }) => (
  <div className="flex items-center justify-center h-10 w-10 border border-gray-600 rounded-md bg-gray-800">
    <span className="text-xs font-bold font-mono" style={{ color: '#00FFFF' }}>{name}</span>
  </div>
);

// Navigation categories
const categories = [
  {
    name: 'Data Structures & Algorithms',
    path: 'dsa',
    icon: <FaCode className="w-4 h-4" />,
    description: 'Master fundamental algorithms and data structures'
  },
  {
    name: 'System Design',
    path: 'system',
    icon: <FaCogs className="w-4 h-4" />,
    description: 'Learn to design scalable systems'
  },
  {
    name: 'Behavioral Questions',
    path: 'behavioral',
    icon: <FaUserTie className="w-4 h-4" />,
    description: 'Prepare for behavioral interviews'
  },
  {
    name: 'Language-Specific Prep',
    path: 'languages',
    icon: <FaCodeBranch className="w-4 h-4" />,
    description: 'Deep dive into programming languages'
  }
];

// Language configuration for the Language Hub
const languages = [
  { name: 'Python', path: 'python', icon: <FaPython className="w-8 h-8" /> },
  { name: 'JavaScript', path: 'javascript', icon: <FaJs className="w-8 h-8" /> },
  { name: 'Java', path: 'java', icon: <FaJava className="w-8 h-8" /> },
  { name: 'C++', path: 'cpp', icon: <TextIcon name="C++" /> },
  { name: 'C#', path: 'csharp', icon: <TextIcon name="C#" /> },
  { name: 'Go', path: 'go', icon: <DiGo className="w-8 h-8" /> },
  { name: 'Rust', path: 'rust', icon: <FaRust className="w-8 h-8" /> },
  { name: 'SQL', path: 'sql', icon: <FaDatabase className="w-8 h-8" /> },
  { name: 'Kotlin', path: 'kotlin', icon: <TextIcon name="Kotlin" /> },
  { name: 'Swift', path: 'swift', icon: <DiSwift className="w-8 h-8" /> }
];

function App() {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [currentCategory, setCurrentCategory] = useState('dsa');
  const [selectedLanguage, setSelectedLanguage] = useState(null);

  // Fetch videos from API
  const fetchVideos = async (category, subcategory = null) => {
    setLoading(true);
    setError(null);
    
    try {
      const url = subcategory 
        ? `http://localhost:8001/api/videos?category=${category}&subcategory=${subcategory}`
        : `http://localhost:8001/api/videos?category=${category}`;
      
      const response = await fetch(url);
      const data = await response.json();
      
      if (data.videos && data.videos.length > 0) {
        setVideos(data.videos);
      } else {
        setVideos([]);
        setError('No videos found for this category');
      }
    } catch (err) {
      setError('Failed to fetch videos');
      console.error('Error fetching videos:', err);
    } finally {
      setLoading(false);
    }
  };

  // Load initial videos
  useEffect(() => {
    fetchVideos('dsa');
  }, []);

  // LanguageHub Component
  const LanguageHub = () => (
    <div className="text-center py-16">
      <h2 className="text-4xl font-bold mb-4" style={{ color: colors['light-gray'] }}>
        Select a Language
      </h2>
      <p className="text-lg mb-12" style={{ color: colors['light-gray'], opacity: 0.6 }}>
        Choose a language from the list below to get started.
      </p>
      
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6 max-w-6xl mx-auto">
        {languages.map((language) => (
          <button
            key={language.name}
            onClick={() => handleLanguageClick(language.name)}
            className="rounded-lg p-6 cursor-pointer transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-0"
            style={{ 
              backgroundColor: colors['intermediate-gray'],
              border: 'none',
              outline: 'none'
            }}
            onMouseEnter={(e) => {
              e.target.style.boxShadow = '0 0 20px rgba(0,255,255,0.3)';
            }}
            onMouseLeave={(e) => {
              e.target.style.boxShadow = 'none';
            }}
          >
            <div className="flex flex-col items-center space-y-3">
              <div style={{ color: colors['glowing-cyan'] }}>
                {language.icon}
              </div>
              <h3 className="font-semibold" style={{ color: colors['light-gray'] }}>
                {language.name}
              </h3>
            </div>
          </button>
        ))}
      </div>
    </div>
  );

  // Handle navigation clicks
  const handleNavClick = (categoryName) => {
    if (categoryName === 'Language-Specific Prep') {
      setCurrentCategory('Language-Specific Prep');
      return;
    }
    
    setCurrentCategory(categoryName);
    setSelectedLanguage(null);
    
    if (['Data Structures & Algorithms', 'System Design', 'Behavioral Questions'].includes(categoryName)) {
      const categoryMap = {
        'Data Structures & Algorithms': 'dsa',
        'System Design': 'system',
        'Behavioral Questions': 'behavioral'
      };
      fetchVideos(categoryMap[categoryName]);
    }
  };

  // Handle language selection
  const handleLanguageClick = (languageName) => {
    setSelectedLanguage(languageName);
    const languageMap = {
      'Python': 'python',
      'JavaScript': 'javascript',
      'Java': 'java',
      'C++': 'cpp',
      'C#': 'csharp',
      'Go': 'go',
      'Rust': 'rust',
      'SQL': 'sql',
      'Kotlin': 'kotlin',
      'Swift': 'swift'
    };
    fetchVideos('languages', languageMap[languageName]);
  };

  // Video Player Component
  const VideoPlayer = () => (
    <div className="min-h-screen" style={{ backgroundColor: colors['near-black'] }}>
      <div className="flex items-center justify-between p-6 border-b" style={{ borderColor: colors['intermediate-gray'] }}>
        <button
          onClick={() => setSelectedVideo(null)}
          className="flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors duration-300 hover:scale-105 focus:outline-none focus:ring-0"
          style={{ 
            backgroundColor: colors['intermediate-gray'],
            color: colors['light-gray']
          }}
        >
          <FaArrowLeft className="w-4 h-4" />
          <span>Back to Videos</span>
        </button>
        
        <a
          href={`https://www.youtube.com/watch?v=${selectedVideo.id}`}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors duration-300 hover:scale-105 focus:outline-none focus:ring-0"
          style={{ 
            backgroundColor: colors['glowing-cyan'],
            color: colors['near-black']
          }}
        >
          <FaExternalLinkAlt className="w-4 h-4" />
          <span>Watch on YouTube</span>
        </a>
      </div>
      
      <div className="p-6">
        <div className="max-w-6xl mx-auto">
          <div className="aspect-video bg-black rounded-lg overflow-hidden mb-6">
            <iframe
              src={`https://www.youtube.com/embed/${selectedVideo.id}?autoplay=1&rel=0&modestbranding=1`}
              title={selectedVideo.title}
              className="w-full h-full"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
          
          <div className="space-y-4">
            <h1 className="text-3xl font-bold" style={{ color: colors['light-gray'] }}>
              {selectedVideo.title}
            </h1>
            
            <div className="flex items-center space-x-4 text-sm" style={{ color: colors['light-gray'], opacity: 0.7 }}>
              <span>{selectedVideo.channelTitle}</span>
              <span>•</span>
              <span>{new Date(selectedVideo.publishedAt).toLocaleDateString()}</span>
            </div>
            
            {selectedVideo.description && (
              <details className="mt-6">
                <summary className="cursor-pointer text-lg font-semibold mb-2" style={{ color: colors['light-gray'] }}>
                  Description
                </summary>
                <div 
                  className="prose prose-invert max-w-none"
                  style={{ color: colors['light-gray'], opacity: 0.8 }}
                  dangerouslySetInnerHTML={{ __html: selectedVideo.description }}
                />
              </details>
            )}
          </div>
        </div>
      </div>
    </div>
  );

  // Video Grid Component
  const VideoGrid = () => (
    <div className="min-h-screen" style={{ backgroundColor: colors['near-black'] }}>
      <div className="flex">
        {/* Sidebar */}
        <aside className="w-72 h-screen overflow-y-auto" style={{ backgroundColor: colors['dark-charcoal'] }}>
          <div className="p-6">
            <div className="mb-8">
              <h1 className="text-2xl font-bold mb-2" style={{ color: colors['glowing-cyan'] }}>
                BracketsTV
              </h1>
              <p className="text-sm" style={{ color: colors['light-gray'], opacity: 0.6 }}>
                Curated Interview Prep
              </p>
            </div>
            
            <nav className="space-y-2">
              {categories.map((category) => (
                <div key={category.path}>
                  <button
                    onClick={() => handleNavClick(category.name)}
                    className={`w-full flex items-center p-3 rounded-lg transition-colors duration-300 border-l-2
                      ${currentCategory === category.name
                        ? 'border-cyan-400 shadow-[0_0_10px_#00FFFF]'
                        : 'border-transparent hover:transition-colors duration-300'
                      }`}
                    style={{
                      backgroundColor: currentCategory === category.name ? colors['near-black'] : 'transparent',
                      color: currentCategory === category.name ? colors['glowing-cyan'] : colors['light-gray']
                    }}
                    onMouseEnter={(e) => {
                      if (currentCategory !== category.name) {
                        e.target.style.backgroundColor = colors['intermediate-gray'];
                        e.target.style.color = colors['glowing-cyan'];
                      }
                    }}
                    onMouseLeave={(e) => {
                      if (currentCategory !== category.name) {
                        e.target.style.backgroundColor = 'transparent';
                        e.target.style.color = colors['light-gray'];
                      }
                    }}
                  >
                    {category.icon}
                    <div className="ml-3 text-left">
                      <div className="font-medium">{category.name}</div>
                      <div className="text-xs opacity-60">{category.description}</div>
                    </div>
                  </button>
                </div>
              ))}
            </nav>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6">
          {currentCategory === 'Language-Specific Prep' ? (
            <LanguageHub />
          ) : (
            <div>
              <div className="mb-8">
                <h2 className="text-3xl font-bold mb-2" style={{ color: colors['light-gray'] }}>
                  {categories.find(cat => cat.name === currentCategory)?.name || 'Videos'}
                </h2>
                <p className="text-lg" style={{ color: colors['light-gray'], opacity: 0.6 }}>
                  {categories.find(cat => cat.name === currentCategory)?.description || 'Curated videos for your interview prep'}
                </p>
              </div>

              {loading && (
                <div className="text-center py-16">
                  <div className="w-24 h-24 mx-auto mb-6 rounded-full flex items-center justify-center animate-spin" style={{ backgroundColor: colors['dark-charcoal'] }}>
                    <FaCode className="w-12 h-12" style={{ color: colors['glowing-cyan'] }} />
                  </div>
                  <h3 className="text-2xl font-semibold mb-4" style={{ color: colors['light-gray'] }}>Loading Videos...</h3>
                  <p className="text-lg" style={{ color: colors['light-gray'], opacity: 0.6 }}>
                    Fetching the latest content for you
                  </p>
                </div>
              )}

              {error && (
                <div className="text-center py-16">
                  <div className="w-24 h-24 mx-auto mb-6 rounded-full flex items-center justify-center" style={{ backgroundColor: colors['dark-charcoal'] }}>
                    <FaCode className="w-12 h-12" style={{ color: colors['light-gray'], opacity: 0.5 }} />
                  </div>
                  <h3 className="text-2xl font-semibold mb-4" style={{ color: colors['light-gray'] }}>Error Loading Videos</h3>
                  <p className="text-lg mb-6" style={{ color: colors['light-gray'], opacity: 0.6 }}>
                    {error}
                  </p>
                  <button
                    onClick={() => fetchVideos(currentCategory === 'Data Structures & Algorithms' ? 'dsa' : currentCategory === 'System Design' ? 'system' : 'behavioral')}
                    className="px-6 py-3 rounded-lg font-semibold transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-0"
                    style={{ 
                      backgroundColor: colors['glowing-cyan'],
                      color: colors['near-black']
                    }}
                  >
                    Try Again
                  </button>
                </div>
              )}

              {!loading && !error && videos.length === 0 && (
                <div className="text-center py-16">
                  <div className="w-24 h-24 mx-auto mb-6 rounded-full flex items-center justify-center" style={{ backgroundColor: colors['dark-charcoal'] }}>
                    <FaCode className="w-12 h-12" style={{ color: colors['light-gray'], opacity: 0.5 }} />
                  </div>
                  <h3 className="text-2xl font-semibold mb-4" style={{ color: colors['light-gray'] }}>No Videos Available</h3>
                  <p className="text-lg mb-6" style={{ color: colors['light-gray'], opacity: 0.6 }}>
                    No videos found for this category. Try selecting a different category.
                  </p>
                  <div className="text-sm" style={{ color: colors['light-gray'], opacity: 0.5 }}>
                    <p>Videos will appear here once the YouTube API quota resets.</p>
                    <p>In the meantime, try exploring other categories.</p>
                  </div>
                </div>
              )}

              {!loading && !error && videos.length > 0 && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                  {videos.map((video) => (
                    <div
                      key={video.id}
                      onClick={() => setSelectedVideo(video)}
                      className="rounded-lg overflow-hidden cursor-pointer transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-0"
                      style={{ backgroundColor: colors['intermediate-gray'] }}
                      onMouseEnter={(e) => {
                        e.target.style.boxShadow = '0 0 20px rgba(0,255,255,0.3)';
                      }}
                      onMouseLeave={(e) => {
                        e.target.style.boxShadow = 'none';
                      }}
                    >
                      <div className="aspect-video bg-black relative">
                        <img
                          src={video.thumbnail}
                          alt={video.title}
                          className="w-full h-full object-cover"
                        />
                        <div className="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity duration-300">
                          <div className="w-16 h-16 rounded-full flex items-center justify-center" style={{ backgroundColor: 'rgba(0,0,0,0.8)' }}>
                            <FaPlay className="w-6 h-6 ml-1" style={{ color: colors['glowing-cyan'] }} />
                          </div>
                        </div>
                      </div>
                      <div className="p-4">
                        <h3 className="font-semibold mb-2 line-clamp-2" style={{ color: colors['light-gray'] }}>
                          {video.title}
                        </h3>
                        <p className="text-sm" style={{ color: colors['light-gray'], opacity: 0.7 }}>
                          {video.channelTitle}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  );

  return selectedVideo ? <VideoPlayer /> : <VideoGrid />;
}

export default App;