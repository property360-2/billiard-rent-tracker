from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('transactions/', views.transactions, name='transactions'),
    path('start-session/<int:table_id>/', views.start_session, name='start_session'),
    path('end-session/<int:session_id>/', views.end_session, name='end_session'),
    path('api/active-sessions/', views.get_active_sessions, name='get_active_sessions'),
    path('api/table-status/', views.table_status, name='table_status'),
]