from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, Count
from django.views.decorators.http import require_POST
from .models import Table, Session, Transaction
import json

def index(request):
    tables = Table.objects.all().order_by('table_number')
    active_sessions = Session.objects.filter(status='active').select_related('table')
    
    context = {
        'tables': tables,
        'active_sessions': active_sessions,
        'now': timezone.now(),
    }
    return render(request, 'monitor/index.html', context)

def start_session(request, table_id):
    if request.method == 'POST':
        table = get_object_or_404(Table, id=table_id)
        duration = int(request.POST.get('duration', 1))
        
        # Check if table is available
        if table.status != 'available':
            return JsonResponse({'error': 'Table is not available'}, status=400)
        
        # Create new session
        session = Session.objects.create(
            table=table,
            duration=duration,
            start_time=timezone.now()
        )
        
        # Update table status
        table.status = 'occupied'
        table.save()
        
        # Create transaction
        Transaction.objects.create(table=table, session=session)
        
        return JsonResponse({
            'success': True,
            'session_id': session.id,
            'end_time': session.formatted_end_time
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@require_POST
def end_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    
    # Update session
    session.status = 'completed'
    session.end_time = timezone.now()
    session.save()
    
    # Update table status
    table = session.table
    table.status = 'available'
    table.save()
    
    return JsonResponse({'success': True})

def transactions(request):
    today = timezone.now().date()
    transactions_today = Transaction.objects.filter(
        transaction_time__date=today
    ).select_related('session', 'table')
    
    # Calculate daily summary
    daily_summary = Session.objects.filter(
        start_time__date=today,
        status='completed'
    ).aggregate(
        total_earnings=Sum('amount'),
        total_sessions=Count('id')
    )
    
    context = {
        'transactions': transactions_today,
        'daily_summary': daily_summary,
        'today': today,
    }
    return render(request, 'monitor/transactions.html', context)

def get_active_sessions(request):
    active_sessions = Session.objects.filter(status='active').select_related('table')
    
    sessions_data = []
    for session in active_sessions:
        sessions_data.append({
            'id': session.id,
            'table_number': session.table.table_number,
            'duration': session.duration,
            'start_time': session.start_time.strftime('%H:%M'),
            'end_time': session.formatted_end_time,
            'amount': float(session.amount),
            'time_remaining': int(session.time_remaining),
            'is_near_end': session.is_near_end,
        })
    
    return JsonResponse({'sessions': sessions_data})

def table_status(request):
    tables = Table.objects.all().order_by('table_number')
    
    tables_data = []
    for table in tables:
        current_session = table.current_session
        tables_data.append({
            'id': table.id,
            'table_number': table.table_number,
            'status': table.status,
            'has_active_session': current_session is not None,
            'session_duration': current_session.duration if current_session else None,
            'session_end_time': current_session.formatted_end_time if current_session else None,
            'is_near_end': current_session.is_near_end if current_session else False,
        })
    
    return JsonResponse({'tables': tables_data})