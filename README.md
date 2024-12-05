# AuthChrono

A Flask-based web application with AI-powered chat functionality and OAuth authentication.

## Features

- User Authentication (Traditional + OAuth)
  - Email/Password Registration and Login
  - Google OAuth Integration
  - Facebook OAuth Integration
  - Password Reset Functionality
- AI Chat Interface
- Secure Session Management
- Modern, Responsive UI

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AuthChrono.git
cd AuthChrono
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up OAuth credentials:

### Google OAuth Setup:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Go to Credentials → Create Credentials → OAuth Client ID
5. Configure the OAuth consent screen
6. Add authorized redirect URIs:
   - `http://localhost:5000/auth/callback/google`
7. Copy the Client ID and Client Secret

### Facebook OAuth Setup:
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app or select an existing one
3. Add the Facebook Login product
4. Configure OAuth settings:
   - Add `http://localhost:5000/auth/callback/facebook` as a valid OAuth redirect URI
5. Copy the App ID and App Secret

5. Configure environment variables:
- Create a `.env` file in the project root
- Add the following variables:
```ini
SECRET_KEY=your-secure-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FACEBOOK_CLIENT_ID=your-facebook-app-id
FACEBOOK_CLIENT_SECRET=your-facebook-app-secret
DATABASE_URL=sqlite:///authchrono.db
```

6. Initialize the database:
```bash
flask db upgrade
```

7. Run the application:
```bash
flask run
```

The application will be available at `http://localhost:5000`

## Project Structure

```
AuthChrono/
├── app.py              # Application factory and configuration
├── auth_routes.py      # Authentication routes and handlers
├── forms.py            # Form definitions
├── models.py           # Database models
├── oauth_config.py     # OAuth configuration
├── requirements.txt    # Project dependencies
├── static/            
│   ├── css/           # Stylesheets
│   └── images/        # Static images
└── templates/         
    ├── base.html      # Base template
    ├── login.html     # Login page
    ├── register.html  # Registration page
    └── chat.html      # Chat interface
```

## Security Considerations

- All sensitive credentials are stored in environment variables
- Passwords are hashed using strong algorithms
- CSRF protection is enabled
- Secure session management
- OAuth state verification
- Input validation and sanitization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
