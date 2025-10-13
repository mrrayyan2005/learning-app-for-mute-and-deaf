import React, { useState } from 'react';
import './HomePage.css';

const HomePage = ({ onStartLearning }) => {
  const [language, setLanguage] = useState('english');

  const translations = {
    english: {
      logo: 'SignLearn',
      heading: 'Welcome to SignLearn',
      subtitle: 'Master sign language with AI-powered real-time recognition',
      description: 'Learn sign language alphabets and common words through interactive, real-time gesture recognition. Our AI models provide instant feedback to help you perfect your signing skills.',
      alphabetBtn: 'Learn Alphabets (A-H)',
      wordsBtn: 'Learn Common Words',
      aboutTitle: 'About SignLearn',
      aboutText: 'SignLearn is designed to help deaf and mute individuals learn sign language through cutting-edge machine learning technology. Practice at your own pace with immediate feedback.',
      features: [
        'Real-time hand gesture recognition',
        'AI-powered instant feedback',
        'Learn alphabets A through H',
        'Master common words and greetings',
        'Responsive design for all devices'
      ]
    },
    gujarati: {
      logo: 'સાઇનલર્ન',
      heading: 'સાઇનલર્નમાં આવકારો',
      subtitle: 'AI સાથે રીઅલ-ટાઇમ ઓળખ સાથે સાઇન લૅંગ્વેજ શીખો',
      description: 'ઇન્ટરેક્ટિવ, રીઅલ-ટાઇમ હાવભાવ ઓળખ દ્વારા સાઇન લૅંગ્વેજ અક્ષરો અને સામાન્ય શબ્દો શીખો। અમારા AI મોડેલ્સ તમારા સાઇનિંગ કૌશલ્યોને સંપૂર્ણ બનાવવામાં મદદ કરવા માટે તાત્કાલિક પ્રતિસાદ આપે છે.',
      alphabetBtn: 'અક્ષરો શીખો (A-H)',
      wordsBtn: 'સામાન્ય શબ્દો શીખો',
      aboutTitle: 'સાઇનલર્ન વિશે',
      aboutText: 'સાઇનલર્ન બહેરા અને મૂંગા વ્યક્તિઓને અત્યાધુનિક મશીન લર્નિંગ ટેક્નોલોજી દ્વારા સાઇન લૅંગ્વેજ શીખવામાં મદદ કરવા માટે ડિઝાઇન કરવામાં આવી છે.',
      features: [
        'રીઅલ-ટાઇમ હાથના હાવભાવની ઓળખ',
        'AI સંચાલિત તાત્કાલિક પ્રતિસાદ',
        'A થી H સુધીના અક્ષરો શીખો',
        'સામાન્ય શબ્દો અને અભિવાદન શીખો',
        'બધા ઉપકરણો માટે રિસ્પોન્સિવ ડિઝાઇન'
      ]
    }
  };

  const t = translations[language];

  return (
    <div className="homepage">
      {/* Navigation */}
      <nav className="navbar">
        <div className="nav-container">
          <div className="logo">{t.logo}</div>
          <div className="language-toggle">
            <button 
              className={`lang-btn ${language === 'english' ? 'active' : ''}`}
              onClick={() => setLanguage('english')}
            >
              English
            </button>
            <button 
              className={`lang-btn ${language === 'gujarati' ? 'active' : ''}`}
              onClick={() => setLanguage('gujarati')}
            >
              ગુજરાતી
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">{t.heading}</h1>
          <p className="hero-subtitle">{t.subtitle}</p>
          <p className="hero-description">{t.description}</p>
          
          <div className="cta-buttons">
            <button 
              className="cta-btn primary"
              onClick={() => onStartLearning('alphabet')}
            >
              <span className="btn-icon">🔤</span>
              {t.alphabetBtn}
            </button>
            <button 
              className="cta-btn secondary"
              onClick={() => onStartLearning('words')}
            >
              <span className="btn-icon">👋</span>
              {t.wordsBtn}
            </button>
          </div>
        </div>
        
        <div className="hero-visual">
          <div className="floating-cards">
            <div className="sign-card">A</div>
            <div className="sign-card">👋</div>
            <div className="sign-card">B</div>
            <div className="sign-card">✌️</div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="features-section">
        <div className="container">
          <h2 className="section-title">{t.aboutTitle}</h2>
          <p className="section-subtitle">{t.aboutText}</p>
          
          <div className="features-grid">
            {t.features.map((feature, index) => (
              <div key={index} className="feature-card">
                <div className="feature-icon">
                  {index === 0 && '📹'}
                  {index === 1 && '🤖'}
                  {index === 2 && '🔤'}
                  {index === 3 && '💬'}
                  {index === 4 && '📱'}
                </div>
                <p className="feature-text">{feature}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-section">
              <h3>{t.logo}</h3>
              <p>Empowering communication through technology</p>
            </div>
            <div className="footer-section">
              <h4>Contact</h4>
              <p>Email: info@signlearn.com</p>
              <p>Knowledge Park-2, Greater Noida</p>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2024 SignLearn. All Rights Reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
