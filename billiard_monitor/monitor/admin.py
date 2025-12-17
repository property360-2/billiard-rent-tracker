from django.contrib import admin
from .models import Table, Session, Transaction

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'status', 'current_session_display')
    list_filter = ('status',)
    search_fields = ('table_number',)
    
    def current_session_display(self, obj):
        session = obj.current_session
        if session:
            return f"{session.duration}h - ₱{session.amount}"
        return "No active session"
    current_session_display.short_description = 'Current Session'

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'duration', 'start_time', 'end_time', 'amount', 'status')
    list_filter = ('status', 'duration', 'start_time')
    search_fields = ('table__table_number',)
    date_hierarchy = 'start_time'

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'session', 'transaction_time')
    list_filter = ('transaction_time',)
    search_fields = ('table__table_number',)
    date_hierarchy = 'transaction_time'