from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import (
    UserProfile, Team, ActivityType, Activity,
    Leaderboard, LeaderboardEntry, WorkoutSuggestion
)
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate the database with initial data for the OctoFit Tracker'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))
        
        # Create activity types
        activity_types_data = [
            ('Running', 'High-intensity cardiovascular exercise'),
            ('Cycling', 'Biking activity for fitness'),
            ('Swimming', 'Water-based exercise'),
            ('Walking', 'Low-impact cardio exercise'),
            ('Gym Workout', 'Strength and resistance training'),
            ('Yoga', 'Flexibility and mindfulness practice'),
            ('Basketball', 'Team sport activity'),
            ('Soccer', 'Football team sport'),
        ]
        
        activity_types = {}
        for name, description in activity_types_data:
            activity_type, created = ActivityType.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            activity_types[name] = activity_type
            if created:
                self.stdout.write(f'Created ActivityType: {name}')
        
        # Create users
        users_data = [
            ('alice', 'alice@octofit.com', 'Alice', 'Johnson'),
            ('bob', 'bob@octofit.com', 'Bob', 'Smith'),
            ('carol', 'carol@octofit.com', 'Carol', 'Williams'),
            ('david', 'david@octofit.com', 'David', 'Brown'),
            ('emma', 'emma@octofit.com', 'Emma', 'Davis'),
        ]
        
        users = {}
        for username, email, first_name, last_name in users_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )
            users[username] = user
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created User: {username}')
            
            # Create user profile
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'bio': f'{first_name} is a fitness enthusiast.',
                    'profile_image': f'https://i.pravatar.cc/150?img={hash(username) % 70}',
                }
            )
        
        # Create teams
        teams_data = [
            ('Team Fitness Warriors', 'A team of dedicated fitness enthusiasts', users['alice']),
            ('Sunday Runners', 'Weekly running group for beginners', users['bob']),
            ('Gym Crew', 'Strength training enthusiasts', users['carol']),
        ]
        
        teams = {}
        for name, description, created_by in teams_data:
            team, created = Team.objects.get_or_create(
                name=name,
                defaults={
                    'description': description,
                    'created_by': created_by,
                }
            )
            teams[name] = team
            if created:
                self.stdout.write(f'Created Team: {name}')
            
            # Add members to team
            for user in users.values():
                team.members.add(user)
        
        # Create activities for the last 30 days
        base_date = datetime.now()
        for i in range(50):
            user = random.choice(list(users.values()))
            activity_type = random.choice(list(activity_types.values()))
            activity_date = base_date - timedelta(days=random.randint(0, 30))
            
            Activity.objects.get_or_create(
                user=user,
                activity_type=activity_type,
                activity_date=activity_date,
                defaults={
                    'duration_minutes': random.randint(30, 120),
                    'distance_km': round(random.uniform(2, 15), 2) if activity_type.name in ['Running', 'Cycling', 'Walking'] else None,
                    'calories_burned': random.randint(200, 800),
                    'notes': f'Great {activity_type.name} session today!',
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Created 50 activity records'))
        
        # Create leaderboards
        for team in teams.values():
            for timeframe, _ in Leaderboard.TIMEFRAME_CHOICES:
                leaderboard, created = Leaderboard.objects.get_or_create(
                    team=team,
                    timeframe=timeframe,
                )
                if created:
                    self.stdout.write(f'Created Leaderboard: {team.name} - {timeframe}')
                
                # Create leaderboard entries
                users_list = list(team.members.all())
                for rank, user in enumerate(users_list, 1):
                    total_activities = Activity.objects.filter(user=user).count()
                    total_calories = sum([a.calories_burned or 0 for a in Activity.objects.filter(user=user)])
                    total_distance = sum([a.distance_km or 0 for a in Activity.objects.filter(user=user)])
                    
                    LeaderboardEntry.objects.get_or_create(
                        leaderboard=leaderboard,
                        user=user,
                        defaults={
                            'total_calories': total_calories,
                            'total_distance': total_distance,
                            'total_activities': total_activities,
                            'rank': rank,
                        }
                    )
        
        self.stdout.write(self.style.SUCCESS('✓ Database population completed successfully!'))
