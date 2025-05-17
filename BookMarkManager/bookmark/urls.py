from django.urls import path
from . import views
from .views import delete_bookmark, edit_bookmark  # Import the view

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete_bookmark/<int:bookmark_id>/', delete_bookmark, name="delete_bookmark"),
    path('edit_bookmark/<int:bookmark_id>/', edit_bookmark, name="edit_bookmark"),
]
