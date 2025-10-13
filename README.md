# SignLearn - Modern React + Flask Sign Language Learning App

A cutting-edge web application for learning sign language through AI-powered real-time gesture recognition. Built with React frontend and Flask API backend.

## 🚀 **NEW ARCHITECTURE** - React + Flask API

### **What's Changed:**
- ✅ **Modern React Frontend** - Component-based, responsive UI
- ✅ **Flask API Backend** - RESTful API endpoints
- ✅ **Browser Camera Integration** - WebRTC MediaDevices API
- ✅ **Real-time Predictions** - Live gesture recognition
- ✅ **Better Performance** - Optimized for web deployment
- ✅ **Mobile Friendly** - Responsive design for all devices

## 🎯 Features

- **Real-time Hand Gesture Recognition** using AI models
- **Learn Alphabets (A-H)** with instant feedback
- **Learn Common Words** (Bye, Hello, No, Perfect, Thank You, Yes)
- **Bilingual Support** (English/Gujarati)
- **Browser-based Camera** access (no desktop dependencies)
- **Modern UI/UX** with beautiful animations
- **Responsive Design** for desktop and mobile
- **Real-time Confidence Scores** and prediction analytics

## 🏗️ Architecture

```
SignLearn/
├── learning-app-for-mute-and-deaf/          # Backend (Flask API)
│   ├── app.py                               # Flask API server
│   ├── model1/                              # Alphabet recognition model
│   ├── Model2/                              # Words recognition model
│   ├── requirements.txt                     # Python dependencies
│   └── signlearn-frontend/                  # Frontend (React App)
│       ├── src/
│       │   ├── App.js                       # Main app component
│       │   ├── components/
│       │   │   ├── HomePage.js              # Landing page
│       │   │   ├── LearningInterface.js     # Main learning UI
│       │   │   └── CameraCapture.js         # Camera component
│       │   └── ...
│       └── package.json                     # Node dependencies
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn
- Webcam/Camera access

### Backend Setup (Flask API)

1. **Navigate to backend directory:**
```bash
cd learning-app-for-mute-and-deaf
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Start Flask API server:**
```bash
python app.py
```
🌐 **Backend running at:** `http://localhost:5000`

### Frontend Setup (React)

1. **Navigate to frontend directory:**
```bash
cd learning-app-for-mute-and-deaf/signlearn-frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start React development server:**
```bash
npm start
```
🌐 **Frontend running at:** `http://localhost:3000`

## 🚀 Quick Start

1. **Start Backend API:**
```bash
cd learning-app-for-mute-and-deaf
python app.py
```

2. **Start Frontend (in new terminal):**
```bash
cd learning-app-for-mute-and-deaf/signlearn-frontend
npm start
```

3. **Open your browser:** `http://localhost:3000`

4. **Allow camera access** when prompted

5. **Start learning!** 🎉

## 📱 Usage

### Learning Flow:
1. **Home Page:** Choose between "Learn Alphabets" or "Learn Words"
2. **Camera Setup:** Allow camera access
3. **Start Recognition:** Click "Start Recognition" button
4. **Practice Signs:** Position your hand in front of camera
5. **Get Feedback:** See real-time predictions and confidence scores
6. **Improve:** Practice until you achieve high confidence!

### Supported Signs:
- **Alphabets:** A, B, C, D, E, F, G, H
- **Words:** Bye, Hello, No, Perfect, Thank You, Yes

## 🌐 Deployment

### Deploy Frontend (Netlify/Vercel)

1. **Build React app:**
```bash
cd signlearn-frontend
npm run build
```

2. **Deploy build folder** to Netlify/Vercel

### Deploy Backend (Heroku/Railway)

1. **Ensure Procfile exists** (already included)
2. **Deploy to Heroku:**
```bash
git add .
git commit -m "Deploy SignLearn"
heroku create your-app-name
git push heroku main
```

### Environment Variables:
```env
# For production
FLASK_ENV=production
API_BASE_URL=https://your-backend-url.herokuapp.com/api
```

## 🔧 API Endpoints

### Base URL: `http://localhost:5000/api`

- **GET** `/health` - Health check
- **POST** `/predict/alphabet` - Predict alphabet sign
- **POST** `/predict/words` - Predict word sign  
- **GET** `/labels/alphabet` - Get alphabet labels
- **GET** `/labels/words` - Get word labels

### Example Request:
```javascript
const response = await fetch('http://localhost:5000/api/predict/alphabet', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ image: base64ImageData })
});
```

## 🎨 Technology Stack

### Frontend:
- **React 18** - Modern UI library
- **CSS3** - Custom responsive styling
- **MediaDevices API** - Camera access
- **Fetch API** - HTTP requests

### Backend:
- **Flask** - Python web framework
- **Flask-CORS** - Cross-origin requests
- **OpenCV** - Image processing
- **TensorFlow/Keras** - ML model inference
- **cvzone** - Computer vision utilities

## 🔍 Troubleshooting

### Camera Issues:
- **Permission Denied:** Allow camera access in browser settings
- **No Camera Found:** Check camera connection
- **Not Supported:** Use Chrome/Firefox/Safari

### API Connection Issues:
- **CORS Errors:** Ensure Flask-CORS is installed
- **Connection Refused:** Check if Flask server is running on port 5000
- **404 Errors:** Verify API endpoint URLs

### Performance Issues:
- **Slow Predictions:** Check network connection
- **High CPU Usage:** Reduce capture frequency in CameraCapture.js

![Uploading Screenshot 2025-10-13 at 11.48.07 PM.png…]()



### Home Page
Beautiful landing page with language selection and learning mode options.

### Learning Interface  
Real-time camera feed with prediction overlay and confidence scores.

### Mobile Responsive
Fully responsive design works on all devices.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

