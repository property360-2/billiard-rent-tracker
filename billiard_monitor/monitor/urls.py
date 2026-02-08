from django.urls import path
from . import views

urlpatterns = [
    # Monitor App URLs
    path('', views.index, name='index'),
    path('transactions/', views.transactions, name='transactions'),
    path('start-session/<int:table_id>/', views.start_session, name='start_session'),
    path('end-session/<int:session_id>/', views.end_session, name='end_session'),
    path('extend-session/<int:session_id>/', views.extend_session, name='extend_session'),
    path('cancel-session/<int:session_id>/', views.cancel_session, name='cancel_session'),
    path('api/active-sessions/', views.get_active_sessions, name='get_active_sessions'),
    path('api/table-status/', views.table_status, name='table_status'),
    
    # Management URLs
    path('manage/', views.manage_tables, name='manage_tables'),
    path('manage/add/', views.add_table, name='add_table'),
    path('manage/edit/<int:table_id>/', views.edit_table, name='edit_table'),
    path('manage/delete/<int:table_id>/', views.delete_table, name='delete_table'),
]