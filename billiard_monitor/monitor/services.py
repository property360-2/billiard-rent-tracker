from django.db.models import Count, Avg
from django.db.models.functions import ExtractHour, ExtractWeekDay
from django.utils import timezone
from .models import Session, Transaction
import json

class AnalyticsService:
    @staticmethod
    def get_peak_hours():
        """
        Returns a list of 24 integers representing the relative busy-ness (0-100)
        of each hour of the day based on historical session start times.
        """
        # Get all completed sessions
        sessions = Session.objects.filter(status='completed')
        
        if not sessions.exists():
            return [0] * 24
            
        # Group by hour
        hour_counts = sessions.annotate(
            hour=ExtractHour('start_time')
        ).values('hour').annotate(
            count=Count('id')
        ).order_by('hour')
        
        # Initialize array
        hourly_data = [0] * 24
        
        # Populate
        max_count = 0
        for entry in hour_counts:
            hour = entry['hour']
            count = entry['count']
            hourly_data[hour] = count
            if count > max_count:
                max_count = count
                
        # Normalize to 0-100 if we have data
        if max_count > 0:
            hourly_data = [int((count / max_count) * 100) for count in hourly_data]
            
        return hourly_data

    @staticmethod
    def get_weekly_trends():
        """
        Returns a list of 7 integers (Sunday=0 to Saturday=6) representing
        sessions count per day of week.
        """
        sessions = Session.objects.filter(status='completed')
        
        if not sessions.exists():
            return [0] * 7
            
        # Django's ExtractWeekDay returns 1 (Sunday) to 7 (Saturday)
        day_counts = sessions.annotate(
            day=ExtractWeekDay('start_time')
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')
        
        daily_data = [0] * 7
        
        for entry in day_counts:
            # Adjust 1-based index (1=Sunday) to 0-based (0=Sunday)
            day_idx = entry['day'] - 1 
            if 0 <= day_idx <= 6:
                daily_data[day_idx] = entry['count']
                
        return daily_data
