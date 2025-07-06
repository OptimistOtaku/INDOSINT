# INDOSINT - AI-Powered OSINT System for India

A comprehensive Open Source Intelligence (OSINT) system designed specifically for India, featuring advanced AI-powered search capabilities, multi-language support, and sophisticated analytics.

## 🚀 Features

### Core OSINT Capabilities
- **Social Media Intelligence**: Search across Twitter, LinkedIn, Facebook, Instagram, YouTube, TikTok, ShareChat, and Koo
- **Digital Footprint Analysis**: Email breach detection, domain registration lookup, and online presence mapping
- **Face Recognition**: Advanced facial recognition and matching across platforms
- **Multi-Language Support**: Native support for 10+ Indian languages including Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, and Urdu
- **Comprehensive Search**: All-in-one search across multiple intelligence sources

### Advanced Analytics & Visualization
- **Real-time Analytics**: Search trends, performance metrics, and user activity insights
- **Data Visualization**: Interactive charts and graphs for intelligence analysis
- **Risk Assessment**: Automated risk scoring and privacy exposure analysis
- **Trend Analysis**: Historical data analysis and pattern recognition

### Security & Privacy
- **Role-based Access Control**: Admin, Analyst, and User roles with appropriate permissions
- **JWT Authentication**: Secure token-based authentication system
- **Data Encryption**: End-to-end encryption for sensitive information
- **Audit Logging**: Comprehensive activity tracking and logging

### User Experience
- **Modern Dashboard**: Clean, intuitive interface with real-time updates
- **Mobile Responsive**: Optimized for desktop, tablet, and mobile devices
- **Real-time Notifications**: Instant updates on search progress and results
- **Export Capabilities**: Multiple format support for data export

## 🏗️ Architecture

### Backend (Flask + Python)
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: SQLite (production-ready for PostgreSQL)
- **Authentication**: JWT with refresh tokens
- **Background Tasks**: Celery for async processing
- **AI/ML Services**: Mock implementations ready for real AI integration

### Frontend (React + JavaScript)
- **Framework**: React 18 with React Router
- **Styling**: Tailwind CSS for modern, responsive design
- **State Management**: React Context API
- **HTTP Client**: Native fetch API with authentication

### Key Components
```
INDOSINT/
├── app/                    # Flask application
│   ├── api/               # API blueprints
│   ├── models/            # Database models
│   ├── services/          # OSINT services
│   └── tasks/             # Background tasks
├── frontend/              # React application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── contexts/      # React contexts
│   │   └── pages/         # Page components
├── run.py                 # Application entry point
└── requirements.txt       # Python dependencies
```

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.8+** (3.13 compatible)
- **Node.js 16+** and npm
- **Git**

### Quick Start (Windows)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd INDOSINT
   ```

2. **Run the startup script**
   ```bash
   start.bat
   ```
   
   This script will:
   - Install Python dependencies
   - Install Node.js dependencies
   - Initialize the database
   - Start both backend and frontend servers

### Manual Setup

#### Backend Setup
1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize database**
   ```bash
   python run.py init-db
   ```

3. **Start the backend server**
   ```bash
   python run.py run
   ```

#### Frontend Setup
1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

## 🌐 Access the Application

- **Backend API**: http://localhost:5000
- **Frontend**: http://localhost:3000
- **Health Check**: http://localhost:5000/health

## 👤 Demo Accounts

The system comes with pre-configured demo accounts:

| Role | Email | Password | Permissions |
|------|-------|----------|-------------|
| Admin | admin@indosint.com | admin123 | Full system access |
| Analyst | analyst@indosint.com | analyst123 | Search and analytics |
| User | user@indosint.com | user123 | Basic search access |

## 🔍 Usage Guide

### 1. Authentication
- Navigate to http://localhost:3000
- Login with any demo account
- The system will automatically redirect to the dashboard

### 2. OSINT Search
- Go to the "OSINT Search" page
- Choose search type:
  - **Comprehensive**: Search across all sources
  - **Social Media**: Focus on social platforms
  - **Digital Footprint**: Analyze online presence
  - **Face Recognition**: Search using facial recognition
- Enter search query and select language
- Click "Search" to start the investigation

### 3. Analytics Dashboard
- Visit the "Analytics" page for insights
- View search trends, performance metrics
- Analyze data distribution by source and type
- Monitor daily activity patterns

### 4. Profile Management
- Access profile settings from the sidebar
- Update personal information
- Change password
- View account statistics

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### OSINT Operations
- `POST /api/osint/search` - Perform OSINT search
- `GET /api/osint/history` - Get search history
- `POST /api/osint/analyze` - Analyze search results

### Analytics
- `GET /api/analytics/dashboard` - Get dashboard analytics
- `GET /api/analytics/trends` - Get trend analysis
- `GET /api/analytics/insights` - Get AI insights

### Search
- `POST /api/search/advanced` - Advanced search with filters
- `GET /api/search/analytics` - Search analytics

## 🎯 Key Features in Detail

### Multi-Language Support
The system supports 10+ Indian languages:
- **Hindi** (हिंदी)
- **Tamil** (தமிழ்)
- **Telugu** (తెలుగు)
- **Bengali** (বাংলা)
- **Marathi** (मराठी)
- **Gujarati** (ગુજરાતી)
- **Kannada** (ಕನ್ನಡ)
- **Malayalam** (മലയാളം)
- **Punjabi** (ਪੰਜਾਬੀ)
- **Urdu** (اردو)

### Social Media Intelligence
- **Platform Coverage**: Twitter, LinkedIn, Facebook, Instagram, YouTube, TikTok, ShareChat, Koo
- **Data Extraction**: Profile information, posts, engagement metrics, location data
- **Sentiment Analysis**: AI-powered sentiment analysis of social media content
- **Influence Scoring**: Automated calculation of social media influence

### Digital Footprint Analysis
- **Data Breach Detection**: Check email addresses against known data breaches
- **Domain Intelligence**: WHOIS lookup, DNS analysis, domain registration history
- **Online Presence Mapping**: Comprehensive mapping of digital presence
- **Risk Assessment**: Automated risk scoring based on exposure level

### Face Recognition
- **Multi-Platform Matching**: Search for faces across social media and news sources
- **Confidence Scoring**: AI-powered confidence scoring for matches
- **Facial Attribute Analysis**: Age, gender, emotion, and ethnicity detection
- **Quality Assessment**: Image quality and pose analysis

## 🔒 Security Features

### Authentication & Authorization
- **JWT Tokens**: Secure token-based authentication
- **Role-based Access**: Granular permissions based on user roles
- **Session Management**: Secure session handling with automatic logout
- **Password Security**: Strong password requirements and secure storage

### Data Protection
- **Encryption**: End-to-end encryption for sensitive data
- **Audit Logging**: Comprehensive activity logging
- **Data Retention**: Configurable data retention policies
- **Privacy Controls**: User-controlled privacy settings

## 🚀 Deployment

### Development
The current setup is optimized for development with:
- SQLite database for simplicity
- Mock AI services for testing
- Hot reloading for both frontend and backend

### Production
For production deployment, consider:
- **Database**: PostgreSQL or MySQL
- **AI Services**: Real AI/ML model integration
- **Caching**: Redis for performance optimization
- **Load Balancing**: Nginx or Apache
- **SSL/TLS**: HTTPS encryption
- **Monitoring**: Application monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the documentation
- Review the code comments
- Create an issue on GitHub

## 🔮 Future Enhancements

- **Real AI Integration**: Integration with actual AI/ML models
- **Advanced Visualization**: 3D data visualization
- **Mobile App**: Native mobile applications
- **API Marketplace**: Third-party API integrations
- **Advanced Analytics**: Machine learning-powered insights
- **Collaboration Features**: Team-based investigations
- **Real-time Monitoring**: Live threat intelligence feeds

---

**INDOSINT** - Empowering intelligence gathering with AI-powered insights for India's digital landscape. 