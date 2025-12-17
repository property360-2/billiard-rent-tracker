"""
URL configuration for billiard_monitor project.
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_monitor(request):
    return redirect('index')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('monitor.urls')),  # This line includes your app's URLs
]