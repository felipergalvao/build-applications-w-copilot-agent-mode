from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from .models import (
    UserProfile, Team, ActivityType, Activity,
    Leaderboard, LeaderboardEntry, WorkoutSuggestion
)
from .serializers import (
    UserSerializer, UserProfileSerializer, ActivityTypeSerializer,
    ActivitySerializer, TeamSerializer, LeaderboardSerializer,
    LeaderboardEntrySerializer, WorkoutSuggestionSerializer
)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

class ActivityTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer
    permission_classes = [AllowAny]

class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user).order_by('-activity_date')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_activities(self, request):
        activities = self.get_queryset()
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        team = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            team.members.add(user)
            return Response({'status': 'member added'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        team = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            team.members.remove(user)
            return Response({'status': 'member removed'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        team_id = self.request.query_params.get('team_id')
        if team_id:
            return Leaderboard.objects.filter(team_id=team_id)
        return Leaderboard.objects.all()

class LeaderboardEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LeaderboardEntry.objects.all().order_by('rank')
    serializer_class = LeaderboardEntrySerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        leaderboard_id = self.request.query_params.get('leaderboard_id')
        if leaderboard_id:
            return LeaderboardEntry.objects.filter(leaderboard_id=leaderboard_id).order_by('rank')
        return LeaderboardEntry.objects.all().order_by('rank')

class WorkoutSuggestionViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSuggestionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return WorkoutSuggestion.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        suggestion = self.get_object()
        suggestion.accepted = True
        suggestion.save()
        return Response({'status': 'suggestion accepted'})

