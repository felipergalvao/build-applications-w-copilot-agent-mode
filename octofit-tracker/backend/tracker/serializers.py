from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, Team, ActivityType, Activity,
    Leaderboard, LeaderboardEntry, WorkoutSuggestion
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'profile_image', 'created_at']

class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = ['id', 'name', 'description']

class ActivitySerializer(serializers.ModelSerializer):
    activity_type = ActivityTypeSerializer(read_only=True)
    activity_type_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Activity
        fields = [
            'id', 'user', 'activity_type', 'activity_type_id',
            'duration_minutes', 'distance_km', 'calories_burned',
            'notes', 'activity_date', 'created_at', 'updated_at'
        ]

class TeamSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_by', 'members', 'created_at']

class LeaderboardEntrySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = LeaderboardEntry
        fields = [
            'id', 'user', 'total_calories', 'total_distance',
            'total_activities', 'rank', 'updated_at'
        ]

class LeaderboardSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    entries = LeaderboardEntrySerializer(many=True, read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'team', 'timeframe', 'entries', 'created_at']

class WorkoutSuggestionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    activity_type = ActivityTypeSerializer(read_only=True)
    activity_type_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = WorkoutSuggestion
        fields = [
            'id', 'user', 'activity_type', 'activity_type_id',
            'duration_minutes', 'difficulty', 'description',
            'suggested_at', 'accepted'
        ]
