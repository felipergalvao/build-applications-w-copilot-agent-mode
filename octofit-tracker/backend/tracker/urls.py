from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet, ActivityTypeViewSet, ActivityViewSet,
    TeamViewSet, LeaderboardViewSet, LeaderboardEntryViewSet,
    WorkoutSuggestionViewSet
)

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'activity-types', ActivityTypeViewSet, basename='activity-type')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'leaderboards', LeaderboardViewSet, basename='leaderboard')
router.register(r'leaderboard-entries', LeaderboardEntryViewSet, basename='leaderboard-entry')
router.register(r'suggestions', WorkoutSuggestionViewSet, basename='suggestion')

urlpatterns = [
    path('', include(router.urls)),
]
