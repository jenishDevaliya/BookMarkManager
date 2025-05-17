from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bookmark.urls')),  # Include URLs from your 'bookmark' app
]
