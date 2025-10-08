import React, { useState, useEffect } from 'react';
import { FaCode, FaCogs, FaUserTie, FaCodeBranch, FaPlay, FaArrowLeft, FaExternalLinkAlt, FaPython, FaJs, FaJava, FaRust, FaDatabase, FaTools, FaRobot } from 'react-icons/fa';
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

// API base URL
const API_BASE_URL = 'http://127.0.0.1:8001';

// Custom TextIcon component for languages without specific icons
const TextIcon = ({ name }) => (
  <div className="flex items-center justify-center h-10 w-10 border border-gray-600 rounded-md bg-gray-800">
    <span className="text-xs font-bold font-mono" style={{ color: '#00FFFF' }}>{name}</span>
  </div>
);

// Helper function to format time since upload
const formatTimeAgo = (publishedAt) => {
  if (!publishedAt) return '';
  
  const now = new Date();
  const published = new Date(publishedAt);
  const diffInMs = now - published;
  const diffInHours = Math.floor(diffInMs / (1000 * 60 * 60));
  const diffInDays = Math.floor(diffInHours / 24);
  const diffInWeeks = Math.floor(diffInDays / 7);
  const diffInMonths = Math.floor(diffInDays / 30);
  const diffInYears = Math.floor(diffInDays / 365);

  if (diffInHours < 24) {
    return `${diffInHours} hour${diffInHours !== 1 ? 's' : ''} ago`;
  } else if (diffInDays < 7) {
    return `${diffInDays} day${diffInDays !== 1 ? 's' : ''} ago`;
  } else if (diffInWeeks < 4) {
    return `${diffInWeeks} week${diffInWeeks !== 1 ? 's' : ''} ago`;
  } else if (diffInMonths < 12) {
    return `${diffInMonths} month${diffInMonths !== 1 ? 's' : ''} ago`;
  } else {
    return `${diffInYears} year${diffInYears !== 1 ? 's' : ''} ago`;
  }
};

// Helper function to format view count
const formatViewCount = (viewCount) => {
  if (!viewCount || viewCount === 0) return '';
  
  if (viewCount >= 1000000) {
    return `${(viewCount / 1000000).toFixed(1)}M views`;
  } else if (viewCount >= 1000) {
    return `${(viewCount / 1000).toFixed(1)}k views`;
  } else {
    return `${viewCount} views`;
  }
};

// Navigation categories (static - these are the main categories)
const categories = [
  {
    name: 'Data Structures & Algorithms',
    path: 'dsa',
    icon: <FaCode className="w-4 h-4" />,
    description: 'Master fundamental algorithms and data structures'
  },
  {
    name: 'System Design',
    path: 'system_design',
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
    name: 'Developer Productivity & Tools',
    path: 'dev_productivity',
    icon: <FaTools className="w-4 h-4" />,
    description: 'Boost your development workflow and tooling'
  },
  {
    name: 'AI & Machine Learning',
    path: 'ai_ml',
    icon: <FaRobot className="w-4 h-4" />,
    description: 'Explore artificial intelligence and ML concepts'
  },
  {
    name: 'Language-Specific Prep',
    path: 'languages',
    icon: <FaCodeBranch className="w-4 h-4" />,
    description: 'Deep dive into programming languages'
  }
];

// Language configuration for the Language Hub (static)
const languages = [
  { name: 'Python', path: 'language_python', icon: <FaPython className="w-8 h-8" /> },
  { name: 'JavaScript', path: 'language_javascript', icon: <FaJs className="w-8 h-8" /> },
  { name: 'Java', path: 'language_java', icon: <FaJava className="w-8 h-8" /> },
  { name: 'C++', path: 'language_cpp', icon: <TextIcon name="C++" /> },
  { name: 'C#', path: 'language_csharp', icon: <TextIcon name="C#" /> },
  { name: 'Go', path: 'language_go', icon: <DiGo className="w-8 h-8" /> },
  { name: 'Rust', path: 'language_rust', icon: <FaRust className="w-8 h-8" /> },
  { name: 'SQL', path: 'language_sql', icon: <FaDatabase className="w-8 h-8" /> },
  { name: 'Kotlin', path: 'language_kotlin', icon: <TextIcon name="Kotlin" /> },
  { name: 'Swift', path: 'language_swift', icon: <DiSwift className="w-8 h-8" /> }
];

function App() {
  // State management
  const [activeMainCategory, setActiveMainCategory] = useState('dsa');
  const [subcategories, setSubcategories] = useState([]);
  const [activeSubcategory, setActiveSubcategory] = useState(null);
  const [videos, setVideos] = useState([]);
  const [isLoadingSubcategories, setIsLoadingSubcategories] = useState(false);
  const [isLoadingVideos, setIsLoadingVideos] = useState(false);
  const [error, setError] = useState(null);
  const [selectedVideo, setSelectedVideo] = useState(null);

  // Fetch subcategories whenever activeMainCategory changes
  useEffect(() => {
    const fetchSubcategories = async () => {
      // Only fetch subcategories for non-language categories
      if (activeMainCategory === 'languages') {
        setSubcategories([]);
        return;
      }

      setIsLoadingSubcategories(true);
      setError(null);
      
      try {
        const response = await fetch(`${API_BASE_URL}/?type=subcategories&category=${activeMainCategory}`);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (Array.isArray(data) && data.length > 0) {
          setSubcategories(data);
          // Automatically set the first subcategory as active
          setActiveSubcategory(data[0]);
        } else {
          setSubcategories([]);
          setActiveSubcategory(null);
        }
      } catch (err) {
        console.error('Error fetching subcategories:', err);
        setError(`Failed to load subcategories: ${err.message}`);
        setSubcategories([]);
        setActiveSubcategory(null);
      } finally {
        setIsLoadingSubcategories(false);
      }
    };

    fetchSubcategories();
  }, [activeMainCategory]);

  // Fetch videos whenever activeSubcategory changes
  useEffect(() => {
    const fetchVideos = async () => {
      // Don't fetch if no subcategory is selected or if we're on the language hub
      if (!activeSubcategory || activeMainCategory === 'languages') {
        setVideos([]);
        return;
      }

      setIsLoadingVideos(true);
      setError(null);
      
      try {
        const response = await fetch(
          `${API_BASE_URL}/?type=videos&category=${activeMainCategory}&subcategory=${encodeURIComponent(activeSubcategory)}`
        );
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (Array.isArray(data) && data.length > 0) {
          setVideos(data);
        } else {
          setVideos([]);
        }
      } catch (err) {
        console.error('Error fetching videos:', err);
        setError(`Failed to load videos: ${err.message}`);
        setVideos([]);
      } finally {
        setIsLoadingVideos(false);
      }
    };

    fetchVideos();
  }, [activeMainCategory, activeSubcategory]);

  // Handle navigation clicks
  const handleNavClick = (categoryPath) => {
    if (categoryPath === 'languages') {
      setActiveMainCategory('languages');
      setSubcategories([]);
      setActiveSubcategory(null);
      setVideos([]);
      return;
    }
    
    setActiveMainCategory(categoryPath);
  };

  // Handle language selection from the Language Hub
  const handleLanguageClick = (languagePath) => {
    setActiveMainCategory(languagePath);
  };

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
            onClick={() => handleLanguageClick(language.path)}
            className="rounded-lg p-6 cursor-pointer transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-0"
            style={{ 
              backgroundColor: colors['intermediate-gray'],
              border: 'none',
              outline: 'none'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.boxShadow = '0 0 20px rgba(0,255,255,0.3)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.boxShadow = 'none';
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
          href={`https://www.youtube.com/watch?v=${selectedVideo.video_id}`}
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
              src={`https://www.youtube.com/embed/${selectedVideo.video_id}?autoplay=1&rel=0&modestbranding=1`}
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
              <span>{selectedVideo.channel_title}</span>
              <span>•</span>
              <span>{new Date(selectedVideo.published_at).toLocaleDateString()}</span>
            </div>
            
            {selectedVideo.description && (
              <details className="mt-6">
                <summary className="cursor-pointer text-lg font-semibold mb-2" style={{ color: colors['light-gray'] }}>
                  Description
                </summary>
                <div 
                  className="prose prose-invert max-w-none whitespace-pre-wrap"
                  style={{ color: colors['light-gray'], opacity: 0.8 }}
                >
                  {selectedVideo.description}
                </div>
              </details>
            )}
          </div>
        </div>
      </div>
    </div>
  );

  // Video Grid Component
  const VideoGrid = () => {
    // Get current category display info
    const currentCategoryInfo = categories.find(cat => cat.path === activeMainCategory);
    const isLanguageHub = activeMainCategory === 'languages';
    const isLoading = isLoadingSubcategories || isLoadingVideos;

    return (
      <div className="min-h-screen" style={{ backgroundColor: colors['near-black'] }}>
        <div className="flex">
          {/* Sidebar */}
          <aside className="w-72 h-screen overflow-y-auto fixed" style={{ backgroundColor: colors['dark-charcoal'] }}>
            <div className="p-6">
              <div className="mb-8">
                <h1 className="text-2xl font-bold mb-2" style={{ color: colors['glowing-cyan'] }}>
                  TechieTV
                </h1>
                <p className="text-sm" style={{ color: colors['light-gray'], opacity: 0.6 }}>
                  Curated Interview Prep
                </p>
              </div>
              
              <nav className="space-y-2">
                {categories.map((category) => (
                  <div key={category.path}>
                    <button
                      onClick={() => handleNavClick(category.path)}
                      className={`w-full flex items-center p-3 rounded-lg transition-colors duration-300 border-l-2
                        ${activeMainCategory === category.path
                          ? 'border-cyan-400 shadow-[0_0_10px_#00FFFF]'
                          : 'border-transparent hover:transition-colors duration-300'
                        }`}
                      style={{
                        backgroundColor: activeMainCategory === category.path ? colors['near-black'] : 'transparent',
                        color: activeMainCategory === category.path ? colors['glowing-cyan'] : colors['light-gray']
                      }}
                      onMouseEnter={(e) => {
                        if (activeMainCategory !== category.path) {
                          e.currentTarget.style.backgroundColor = colors['intermediate-gray'];
                          e.currentTarget.style.color = colors['glowing-cyan'];
                        }
                      }}
                      onMouseLeave={(e) => {
                        if (activeMainCategory !== category.path) {
                          e.currentTarget.style.backgroundColor = 'transparent';
                          e.currentTarget.style.color = colors['light-gray'];
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
          <main className="flex-1 ml-72 p-6">
            {isLanguageHub ? (
              <LanguageHub />
            ) : (
              <div>
                <div className="mb-8">
                  <h2 className="text-3xl font-bold mb-2" style={{ color: colors['light-gray'] }}>
                    {currentCategoryInfo?.name || 'Videos'}
                  </h2>
                  <p className="text-lg" style={{ color: colors['light-gray'], opacity: 0.6 }}>
                    {currentCategoryInfo?.description || 'Curated videos for your interview prep'}
                  </p>
                </div>

                {/* Dynamic Subcategory Navigation */}
                {subcategories.length > 0 && (
                  <div className="mb-6 flex flex-wrap gap-2">
                    {subcategories.map((subcategory) => (
                      <button
                        key={subcategory}
                        onClick={() => setActiveSubcategory(subcategory)}
                        className={`px-3 py-1 rounded-md text-sm transition-all focus:outline-none focus:ring-0`}
                        style={{
                          backgroundColor: activeSubcategory === subcategory ? colors['intermediate-gray'] : colors['dark-charcoal'],
                          color: activeSubcategory === subcategory ? colors['glowing-cyan'] : colors['light-gray'],
                          border: `1px solid ${activeSubcategory === subcategory ? colors['glowing-cyan'] : '#2a2f36'}`
                        }}
                      >
                        {subcategory}
                      </button>
                    ))}
                  </div>
                )}

                {/* Loading State */}
                {isLoading && (
                  <div className="text-center py-16">
                    <div className="w-24 h-24 mx-auto mb-6 rounded-full flex items-center justify-center animate-spin" style={{ backgroundColor: colors['dark-charcoal'] }}>
                      <FaCode className="w-12 h-12" style={{ color: colors['glowing-cyan'] }} />
                    </div>
                    <h3 className="text-2xl font-semibold mb-4" style={{ color: colors['light-gray'] }}>
                      {isLoadingSubcategories ? 'Loading Categories...' : 'Loading Videos...'}
                    </h3>
                    <p className="text-lg" style={{ color: colors['light-gray'], opacity: 0.6 }}>
                      Fetching the latest content for you
                    </p>
                  </div>
                )}

                {/* Error State */}
                {error && !isLoading && (
                  <div className="text-center py-16">
                    <div className="w-24 h-24 mx-auto mb-6 rounded-full flex items-center justify-center" style={{ backgroundColor: colors['dark-charcoal'] }}>
                      <FaCode className="w-12 h-12" style={{ color: colors['light-gray'], opacity: 0.5 }} />
                    </div>
                    <h3 className="text-2xl font-semibold mb-4" style={{ color: colors['light-gray'] }}>Error Loading Content</h3>
                    <p className="text-lg mb-6" style={{ color: colors['light-gray'], opacity: 0.6 }}>
                      {error}
                    </p>
                  </div>
                )}

                {/* No Videos State */}
                {!isLoading && !error && videos.length === 0 && subcategories.length > 0 && (
                  <div className="text-center py-16">
                    <div className="w-24 h-24 mx-auto mb-6 rounded-full flex items-center justify-center" style={{ backgroundColor: colors['dark-charcoal'] }}>
                      <FaCode className="w-12 h-12" style={{ color: colors['light-gray'], opacity: 0.5 }} />
                    </div>
                    <h3 className="text-2xl font-semibold mb-4" style={{ color: colors['light-gray'] }}>No Videos Available</h3>
                    <p className="text-lg mb-6" style={{ color: colors['light-gray'], opacity: 0.6 }}>
                      No videos found for this category. Videos will appear here once they are fetched by the ingestion script.
                    </p>
                    <div className="text-sm" style={{ color: colors['light-gray'], opacity: 0.5 }}>
                      <p>Try selecting a different category or subcategory.</p>
                    </div>
                  </div>
                )}

                {/* Video Grid */}
                {!isLoading && !error && videos.length > 0 && (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    {videos.map((video) => (
                      <div
                        key={video.video_id}
                        onClick={() => setSelectedVideo(video)}
                        className="rounded-lg overflow-hidden cursor-pointer transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-0"
                        style={{ backgroundColor: colors['intermediate-gray'] }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.boxShadow = '0 0 20px rgba(0,255,255,0.3)';
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.boxShadow = 'none';
                        }}
                      >
                        <div className="aspect-video bg-black relative">
                          <img
                            src={video.thumbnail_url}
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
                          <div className="flex items-center text-sm" style={{ color: colors['light-gray'], opacity: 0.7 }}>
                            <span>{video.channel_title}</span>
                            {video.view_count && (
                              <>
                                <span className="mx-1">•</span>
                                <span>{formatViewCount(video.view_count)}</span>
                              </>
                            )}
                            {video.published_at && (
                              <>
                                <span className="mx-1">•</span>
                                <span>{formatTimeAgo(video.published_at)}</span>
                              </>
                            )}
                          </div>
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
  };

  return selectedVideo ? <VideoPlayer /> : <VideoGrid />;
}

export default App;
