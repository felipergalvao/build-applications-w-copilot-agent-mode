from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import (
    UserProfile, Team, ActivityType, Activity,
    Leaderboard, LeaderboardEntry, WorkoutSuggestion
)
from datetime import datetime, timedelta
from django.utils import timezone

class UserProfileTestCase(TestCase):
    """Test UserProfile model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_profile_creation(self):
        """Test creating a user profile"""
        profile = UserProfile.objects.create(
            user=self.user,
            bio='Test bio',
            profile_image='https://example.com/avatar.jpg'
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.bio, 'Test bio')
        self.assertIsNotNone(profile.created_at)
    
    def test_user_profile_str(self):
        """Test string representation"""
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(str(profile), f"{self.user.username} Profile")

class ActivityTypeTestCase(TestCase):
    """Test ActivityType model"""
    
    def test_activity_type_creation(self):
        """Test creating an activity type"""
        activity_type = ActivityType.objects.create(
            name='Running',
            description='High-intensity cardio'
        )
        self.assertEqual(activity_type.name, 'Running')
        self.assertEqual(str(activity_type), 'Running')
    
    def test_unique_activity_type_name(self):
        """Test that activity type names are unique"""
        ActivityType.objects.create(name='Running')
        with self.assertRaises(Exception):
            ActivityType.objects.create(name='Running')

class TeamTestCase(TestCase):
    """Test Team model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='teamcreator',
            email='creator@example.com',
            password='testpass123'
        )
    
    def test_team_creation(self):
        """Test creating a team"""
        team = Team.objects.create(
            name='Fitness Warriors',
            description='Fitness team',
            created_by=self.user
        )
        self.assertEqual(team.name, 'Fitness Warriors')
        self.assertEqual(team.created_by, self.user)
    
    def test_team_add_member(self):
        """Test adding members to team"""
        team = Team.objects.create(
            name='Test Team',
            created_by=self.user
        )
        member = User.objects.create_user(
            username='member1',
            email='member@example.com',
            password='testpass123'
        )
        team.members.add(member)
        self.assertIn(member, team.members.all())
        self.assertEqual(team.members.count(), 1)

class ActivityTestCase(TestCase):
    """Test Activity model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='activeuser',
            email='active@example.com',
            password='testpass123'
        )
        self.activity_type = ActivityType.objects.create(name='Running')
    
    def test_activity_creation(self):
        """Test creating an activity"""
        activity = Activity.objects.create(
            user=self.user,
            activity_type=self.activity_type,
            duration_minutes=60,
            distance_km=10.5,
            calories_burned=500,
            activity_date=timezone.now()
        )
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.duration_minutes, 60)
        self.assertEqual(activity.distance_km, 10.5)
    
    def test_activity_str(self):
        """Test activity string representation"""
        activity = Activity.objects.create(
            user=self.user,
            activity_type=self.activity_type,
            duration_minutes=30,
            activity_date=timezone.now()
        )
        self.assertIn(self.user.username, str(activity))
        self.assertIn(self.activity_type.name, str(activity))

class APIActivityTypeTestCase(APITestCase):
    """Test ActivityType API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.activity_type = ActivityType.objects.create(
            name='Cycling',
            description='Bike riding'
        )
    
    def test_list_activity_types(self):
        """Test listing activity types"""
        response = self.client.get('/api/activity-types/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_retrieve_activity_type(self):
        """Test retrieving single activity type"""
        response = self.client.get(f'/api/activity-types/{self.activity_type.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Cycling')

class APITeamTestCase(APITestCase):
    """Test Team API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.team = Team.objects.create(
            name='Test Team',
            created_by=self.user
        )
        self.team.members.add(self.user)
    
    def test_list_teams(self):
        """Test listing teams"""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_team(self):
        """Test retrieving a team"""
        response = self.client.get(f'/api/teams/{self.team.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Team')

class APIActivityTestCase(APITestCase):
    """Test Activity API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='activeuser',
            email='active@example.com',
            password='testpass123'
        )
        self.activity_type = ActivityType.objects.create(name='Swimming')
        self.client.force_authenticate(user=self.user)
    
    def test_list_user_activities(self):
        """Test listing user's activities"""
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_activity(self):
        """Test creating an activity"""
        data = {
            'activity_type_id': self.activity_type.id,
            'duration_minutes': 45,
            'distance_km': 1.5,
            'calories_burned': 300,
            'notes': 'Great session!',
            'activity_date': timezone.now().isoformat()
        }
        response = self.client.post('/api/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)
    
    def test_create_activity_without_auth(self):
        """Test that creating activity requires authentication"""
        self.client.force_authenticate(user=None)
        data = {
            'activity_type_id': self.activity_type.id,
            'duration_minutes': 30,
            'activity_date': timezone.now().isoformat()
        }
        response = self.client.post('/api/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class APILeaderboardTestCase(APITestCase):
    """Test Leaderboard API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='leader',
            email='leader@example.com',
            password='testpass123'
        )
        self.team = Team.objects.create(
            name='Test Team',
            created_by=self.user
        )
        self.leaderboard = Leaderboard.objects.create(
            team=self.team,
            timeframe='daily'
        )
    
    def test_list_leaderboards(self):
        """Test listing leaderboards"""
        response = self.client.get('/api/leaderboards/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_filter_leaderboards_by_team(self):
        """Test filtering leaderboards by team"""
        response = self.client.get(f'/api/leaderboards/?team_id={self.team.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_leaderboard(self):
        """Test retrieving a leaderboard"""
        response = self.client.get(f'/api/leaderboards/{self.leaderboard.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['timeframe'], 'daily')

class APIWorkoutSuggestionTestCase(APITestCase):
    """Test WorkoutSuggestion API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='suggestionuser',
            email='suggestion@example.com',
            password='testpass123'
        )
        self.activity_type = ActivityType.objects.create(name='Yoga')
        self.client.force_authenticate(user=self.user)
    
    def test_create_suggestion(self):
        """Test creating a workout suggestion"""
        data = {
            'activity_type_id': self.activity_type.id,
            'duration_minutes': 60,
            'difficulty': 'moderate',
            'description': 'Relaxing yoga session'
        }
        response = self.client.post('/api/suggestions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorkoutSuggestion.objects.count(), 1)
    
    def test_list_suggestions(self):
        """Test listing user's suggestions"""
        response = self.client.get('/api/suggestions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class APIUserProfileTestCase(APITestCase):
    """Test UserProfile API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='profileuser',
            email='profile@example.com',
            password='testpass123'
        )
        UserProfile.objects.create(
            user=self.user,
            bio='Test profile'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_get_own_profile(self):
        """Test getting own profile"""
        response = self.client.get('/api/profiles/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'profileuser')

