from django.contrib import admin
from .models import (
    UserProfile, Team, ActivityType, Activity,
    Leaderboard, LeaderboardEntry, WorkoutSuggestion
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Profile', {
            'fields': ('bio', 'profile_image')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'member_count', 'created_at')
    search_fields = ('name', 'created_by__username')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    filter_horizontal = ('members',)
    fieldsets = (
        ('Team Info', {
            'fields': ('name', 'description')
        }),
        ('Management', {
            'fields': ('created_by', 'members')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'

@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'activity_count')
    search_fields = ('name',)
    fieldsets = (
        ('Activity Type Info', {
            'fields': ('name', 'description')
        }),
    )
    
    def activity_count(self, obj):
        return obj.activity_set.count()
    activity_count.short_description = 'Activities'

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'duration_minutes', 'activity_date', 'calories_burned')
    search_fields = ('user__username', 'activity_type__name')
    list_filter = ('activity_type', 'activity_date', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'activity_date'
    fieldsets = (
        ('Activity Info', {
            'fields': ('user', 'activity_type', 'activity_date')
        }),
        ('Activity Details', {
            'fields': ('duration_minutes', 'distance_km', 'calories_burned', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('team', 'timeframe', 'entry_count', 'created_at')
    search_fields = ('team__name',)
    list_filter = ('timeframe', 'created_at')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Leaderboard Info', {
            'fields': ('team', 'timeframe')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def entry_count(self, obj):
        return obj.entries.count()
    entry_count.short_description = 'Entries'

@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ('leaderboard', 'user', 'rank', 'total_calories', 'total_distance', 'total_activities')
    search_fields = ('user__username', 'leaderboard__team__name')
    list_filter = ('leaderboard__timeframe', 'rank', 'updated_at')
    readonly_fields = ('updated_at',)
    fieldsets = (
        ('Leaderboard Entry Info', {
            'fields': ('leaderboard', 'user', 'rank')
        }),
        ('Statistics', {
            'fields': ('total_calories', 'total_distance', 'total_activities')
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(WorkoutSuggestion)
class WorkoutSuggestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'difficulty', 'accepted', 'suggested_at')
    search_fields = ('user__username', 'activity_type__name')
    list_filter = ('difficulty', 'accepted', 'suggested_at')
    readonly_fields = ('suggested_at',)
    fieldsets = (
        ('Suggestion Info', {
            'fields': ('user', 'activity_type', 'difficulty')
        }),
        ('Details', {
            'fields': ('duration_minutes', 'description', 'accepted')
        }),
        ('Metadata', {
            'fields': ('suggested_at',),
            'classes': ('collapse',)
        }),
    )
