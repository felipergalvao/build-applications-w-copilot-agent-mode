# OctoFit Tracker Backend - Quick Start Guide

## ✓ Project Status: READY FOR USE

The Django backend for the OctoFit Tracker fitness application has been successfully initialized, configured, and populated with sample data.

## Quick Commands

### Start the Development Server
```bash
cd octofit-tracker/backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

**Server will be available at**: `http://localhost:8000`

### API Base URL
```
http://localhost:8000/api/
```

## Key Features Implemented

### ✅ Authentication & Users
- User registration and authentication
- User profiles with bio and avatar
- Token-based authentication

### ✅ Activities
- Log fitness activities (Running, Cycling, Swimming, etc.)
- Track duration, distance, calories
- History of all user activities

### ✅ Teams
- Create and manage fitness teams
- Add/remove team members
- Team-based leaderboards

### ✅ Leaderboards
- Daily, weekly, monthly, and all-time leaderboards
- Ranked by calories, distance, and activity count
- Team-specific rankings

### ✅ Workout Suggestions
- AI-powered personalized workout suggestions
- Difficulty levels (Easy, Moderate, Hard)
- Accept/decline suggestions

## Database

**MongoDB Connection**: `mongodb://localhost:27017`  
**Database Name**: `octofit_db`

### Sample Data Included
- 5 Test Users (alice, bob, carol, david, emma)
- 3 Teams with members
- 8 Activity Types
- 50 Sample Activities
- 12 Leaderboards with rankings

## API Examples

### Get All Activity Types (No Auth Required)
```bash
curl http://localhost:8000/api/activity-types/
```

### Get Team Leaderboard (No Auth Required)
```bash
curl "http://localhost:8000/api/leaderboards/?team_id=4"
```

### Get Teams (No Auth Required)
```bash
curl http://localhost:8000/api/teams/
```

### Admin Access
```
URL: http://localhost:8000/admin/
Username: admin (needs to be created)
```

## File Structure

```
octofit-tracker/backend/
├── venv/                    # Virtual environment (3rd party packages)
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── db.sqlite3             # SQLite database (not used - MongoDB)
├── octofit_tracker/        # Project settings
│   ├── settings.py        # Django configuration
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI application
│   └── asgi.py            # ASGI application
└── tracker/               # Main Django app
    ├── models.py          # Data models
    ├── views.py           # API endpoints
    ├── serializers.py     # Data serialization
    ├── urls.py            # App URL routing
    ├── admin.py           # Admin interface
    ├── migrations/        # Database migrations
    └── management/        # Custom management commands
        └── commands/
            └── populate_db.py
```

## Available Endpoints Summary

### Public (No Authentication)
- `GET /api/activity-types/` - List activity types
- `GET /api/leaderboards/` - List all leaderboards
- `GET /api/leaderboard-entries/` - List leaderboard entries
- `GET /api/teams/` - List all teams

### Protected (Authentication Required)
- `GET /api/profiles/me/` - Current user profile
- `GET/POST /api/activities/` - User's activities
- `GET/POST /api/suggestions/` - Workout suggestions
- `POST /api/teams/{id}/add_member/` - Add team member
- `POST /api/teams/{id}/remove_member/` - Remove team member

## Django Admin

To create a superuser for admin access:
```bash
python manage.py createsuperuser
```

Then visit `http://localhost:8000/admin/`

## Troubleshooting

### Server Won't Start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill existing process
pkill -f "manage.py runserver"
```

### Database Connection Issues
```bash
# Verify MongoDB is running
ps aux | grep mongod

# Check MongoDB connection
mongo mongodb://localhost:27017
```

### Dependencies Issues
```bash
# Reinstall all dependencies
pip install -r requirements.txt

# Or upgrade pip and reinstall
pip install --upgrade pip
pip install -r requirements.txt
```

## Next Steps

1. **Frontend Development**: Build React frontend in `octofit-tracker/frontend/`
2. **User Authentication**: Implement JWT tokens for secure authentication
3. **Testing**: Add unit and integration tests
4. **Deployment**: Deploy to production (Heroku, AWS, etc.)

## Project Completion Checklist

- [x] Django project initialized
- [x] MongoDB configured
- [x] All models created
- [x] REST API endpoints implemented
- [x] Sample data populated
- [x] Authentication configured
- [x] CORS configured for frontend
- [x] Server tested and working
- [ ] Frontend created (Next step)
- [ ] Production deployment

---

**For Questions or Issues**: Refer to the main README.md or project documentation.

Last Updated: January 21, 2026  
Status: ✓ Backend Ready for Frontend Development
