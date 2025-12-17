from django.db import models
from django.utils import timezone

class Table(models.Model):
    TABLE_STATUS = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
    ]
    
    table_number = models.IntegerField(unique=True)
    status = models.CharField(max_length=20, choices=TABLE_STATUS, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Table {self.table_number}"
    
    @property
    def current_session(self):
        return self.sessions.filter(status='active').first()

class Session(models.Model):
    SESSION_STATUS = [
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]
    
    DURATION_CHOICES = [
        (1, '1 hour'),
        (2, '2 hours'),
        (3, '3 hours'),
    ]
    
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='sessions')
    duration = models.IntegerField(choices=DURATION_CHOICES, default=1)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=SESSION_STATUS, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Session #{self.id} - Table {self.table.table_number}"
    
    def save(self, *args, **kwargs):
        # Calculate price based on duration
        if self.duration == 1:
            self.amount = 50
        elif self.duration == 2:
            self.amount = 90
        elif self.duration == 3:
            self.amount = 125
        
        if not self.start_time:
            self.start_time = timezone.now()
            
        super().save(*args, **kwargs)
    
    @property
    def time_remaining(self):
        if self.status == 'active':
            end = self.start_time + timezone.timedelta(hours=self.duration)
            remaining = end - timezone.now()
            return max(remaining.total_seconds(), 0)
        return 0
    
    @property
    def is_near_end(self):
        return self.time_remaining <= 600  # 10 minutes
    
    @property
    def formatted_end_time(self):
        end = self.start_time + timezone.timedelta(hours=self.duration)
        return end.strftime('%H:%M')

class Transaction(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    transaction_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Transaction #{self.id} - {self.table.table_number}"