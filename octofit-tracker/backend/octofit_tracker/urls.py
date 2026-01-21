"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import os
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from tracker.views import (
    UserProfileViewSet, ActivityTypeViewSet, ActivityViewSet,
    TeamViewSet, LeaderboardViewSet, LeaderboardEntryViewSet,
    WorkoutSuggestionViewSet
)

# Create router for API endpoints
router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'activity-types', ActivityTypeViewSet, basename='activity-type')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'leaderboards', LeaderboardViewSet, basename='leaderboard')
router.register(r'leaderboard-entries', LeaderboardEntryViewSet, basename='leaderboard-entry')
router.register(r'suggestions', WorkoutSuggestionViewSet, basename='suggestion')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
