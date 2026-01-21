from django.db import models
from django.contrib.auth.models import User
from djongo import models as djongo_models

# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"

# Team Model
class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    members = models.ManyToManyField(User, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

# Activity Type Model
class ActivityType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

# Activity Model
class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.ForeignKey(ActivityType, on_delete=models.PROTECT)
    duration_minutes = models.IntegerField()  # Duration in minutes
    distance_km = models.FloatField(blank=True, null=True)  # Distance in kilometers
    calories_burned = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    activity_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type.name} on {self.activity_date}"

# Leaderboard Model
class Leaderboard(models.Model):
    TIMEFRAME_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('all_time', 'All Time'),
    ]
    
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='leaderboards')
    timeframe = models.CharField(max_length=20, choices=TIMEFRAME_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['team', 'timeframe']
    
    def __str__(self):
        return f"{self.team.name} - {self.timeframe} Leaderboard"

# Leaderboard Entry Model
class LeaderboardEntry(models.Model):
    leaderboard = models.ForeignKey(Leaderboard, on_delete=models.CASCADE, related_name='entries')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_calories = models.IntegerField(default=0)
    total_distance = models.FloatField(default=0)
    total_activities = models.IntegerField(default=0)
    rank = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['leaderboard', 'user']
        ordering = ['rank']
    
    def __str__(self):
        return f"{self.user.username} - Rank {self.rank} in {self.leaderboard}"

# Suggestion Model
class WorkoutSuggestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('hard', 'Hard'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suggestions')
    activity_type = models.ForeignKey(ActivityType, on_delete=models.PROTECT)
    duration_minutes = models.IntegerField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    description = models.TextField()
    suggested_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Suggestion for {self.user.username}: {self.activity_type.name}"
