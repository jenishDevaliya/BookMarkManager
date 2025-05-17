from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Bookmark, CATEGORY_CHOICES  # Corrected import


# Home Page
def home(request):
    return render(request, 'home.html')


# About Page
def about(request):
    return render(request, 'about.html')


# User Signup
def user_signup(request):
    if request.method == "POST":
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken!")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')

    return render(request, 'signup.html')


# User Login
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials. Please try again.")

    return render(request, 'login.html')


# User Logout
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    query = request.GET.get('search', '')

    if request.method == "POST":
        title = request.POST['title']
        url = request.POST['url']
        category = request.POST['category']
        if category == "":
            category = Bookmark._meta.get_field('category').get_default()

        Bookmark.objects.create(user=request.user, title=title, url=url, category=category)
        messages.success(request, "Bookmark added successfully")
        return redirect('dashboard')

    # Apply search filter if search query is provided
    if query:
        bookmarks = Bookmark.objects.filter(user=request.user, title__icontains=query)
    else:
        bookmarks = Bookmark.objects.filter(user=request.user)

    return render(request, 'dashboard.html', {'bookmarks': bookmarks})


# Delete Bookmark
@login_required(login_url='login')
def delete_bookmark(request, bookmark_id):
    bookmark = get_object_or_404(Bookmark, id=bookmark_id, user=request.user)
    bookmark.delete()
    messages.success(request, "Bookmark deleted successfully.")
    return redirect('dashboard')


# Edit Bookmark
@login_required(login_url='login')
def edit_bookmark(request, bookmark_id):
    bookmark = get_object_or_404(Bookmark, id=bookmark_id, user=request.user)
    categories = CATEGORY_CHOICES

    if request.method == "POST":
        bookmark.title = request.POST['title']
        bookmark.url = request.POST['url']
        bookmark.category = request.POST['category']
        bookmark.save()
        messages.success(request, "Bookmark updated successfully.")
        return redirect('dashboard')

    return render(request, 'edit_bookmark.html', {'bookmark': bookmark, 'categories': categories})
