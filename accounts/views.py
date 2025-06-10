from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Q
from .models import UserProfile
from .forms import UserUpdateForm, ProfileUpdateForm, CustomUserCreationForm
from courses.models import Course, Purchase, LessonProgress, CourseReview

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_page = request.GET.get('next', 'dashboard')
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('course_list')

@login_required
def dashboard(request):
    user = request.user
    
    # Get user's purchased courses
    purchased_courses = Course.objects.filter(purchases__user=user).distinct()
    enrolled_courses_count = purchased_courses.count()
    
    # Get progress statistics
    total_lessons = 0
    completed_lessons = 0
    lessons_started = 0
    courses_completed = 0
    
    for course in purchased_courses:
        course_lessons = course.get_all_lessons()
        total_lessons += len(course_lessons)
        
        # Count completed lessons for this course
        course_completed_lessons = LessonProgress.objects.filter(
            user=user,
            lesson__in=course_lessons,
            is_completed=True
        ).count()
        completed_lessons += course_completed_lessons
        
        # Count started lessons for this course
        course_started_lessons = LessonProgress.objects.filter(
            user=user,
            lesson__in=course_lessons
        ).count()
        lessons_started += course_started_lessons
        
        # Check if course is completed
        if course_lessons and course_completed_lessons == len(course_lessons):
            courses_completed += 1
    
    # Calculate overall progress percentage
    progress_percentage = 0
    if total_lessons > 0:
        progress_percentage = round((completed_lessons / total_lessons) * 100, 1)
    
    # Recent activity
    recent_progress = LessonProgress.objects.filter(
        user=user
    ).select_related('lesson', 'lesson__section', 'lesson__section__course').order_by('-last_accessed')[:5]
    
    # Reviews written by user
    user_reviews = CourseReview.objects.filter(user=user).select_related('course').order_by('-created_at')[:3]
    reviews_count = user_reviews.count()
    
    context = {
        'purchased_courses': purchased_courses,
        'enrolled_courses_count': enrolled_courses_count,
        'courses_completed': courses_completed,
        'total_lessons': total_lessons,
        'completed_lessons': completed_lessons,
        'lessons_started': lessons_started,
        'progress_percentage': progress_percentage,
        'recent_progress': recent_progress,
        'user_reviews': user_reviews,
        'reviews_count': reviews_count,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile(request):
    # Ensure user has a profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    # Ensure user has a profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required
def my_learning(request):
    user = request.user
    
    # Get purchased courses with progress
    purchased_courses = []
    for purchase in Purchase.objects.filter(user=user).select_related('course'):
        course = purchase.course
        all_lessons = course.get_all_lessons()
        completed_lessons = LessonProgress.objects.filter(
            user=user,
            lesson__in=all_lessons,
            is_completed=True
        ).count()
        
        progress_percentage = 0
        if all_lessons:
            progress_percentage = round((completed_lessons / len(all_lessons)) * 100, 1)
        
        # Get last accessed lesson
        last_progress = LessonProgress.objects.filter(
            user=user,
            lesson__in=all_lessons
        ).order_by('-last_accessed').first()
        
        purchased_courses.append({
            'course': course,
            'purchase': purchase,
            'progress_percentage': progress_percentage,
            'completed_lessons': completed_lessons,
            'total_lessons': len(all_lessons),
            'last_progress': last_progress
        })
    
    context = {
        'purchased_courses': purchased_courses,
    }
    return render(request, 'accounts/my_learning.html', context)

@login_required
def certificates(request):
    # Get completed courses
    user = request.user
    completed_courses = []
    
    for purchase in Purchase.objects.filter(user=user).select_related('course'):
        course = purchase.course
        all_lessons = course.get_all_lessons()
        completed_lessons = LessonProgress.objects.filter(
            user=user,
            lesson__in=all_lessons,
            is_completed=True
        ).count()
        
        if all_lessons and completed_lessons == len(all_lessons):
            completed_courses.append({
                'course': course,
                'purchase': purchase,
                'completion_date': LessonProgress.objects.filter(
                    user=user,
                    lesson__in=all_lessons,
                    is_completed=True
                ).latest('completed_at').completed_at
            })
    
    context = {
        'completed_courses': completed_courses,
    }
    return render(request, 'accounts/certificates.html', context)
