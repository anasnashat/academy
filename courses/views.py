from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import Category, Course, Section, Lesson, Purchase, LessonProgress, CourseReview, Comment

# ===== PUBLIC VIEWS =====

def course_list(request):
    """Display all courses with filtering options"""
    courses = Course.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    # Filtering
    category_slug = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    search = request.GET.get('search')
    
    selected_category_obj = None
    if category_slug:
        selected_category_obj = Category.objects.filter(slug=category_slug).first()
        courses = courses.filter(category__slug=category_slug)
    
    if difficulty:
        courses = courses.filter(difficulty_level=difficulty)
    
    if search:
        courses = courses.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(courses, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'courses': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'selected_category_obj': selected_category_obj,
        'selected_difficulty': difficulty,
        'search_query': search,
    }
    return render(request, 'courses/course_list.html', context)

def course_detail(request, course_id):
    """Display course details and sections"""
    course = get_object_or_404(Course, id=course_id, is_active=True)
    sections = course.sections.filter(is_active=True).prefetch_related('lessons')
    reviews = course.reviews.all()[:5]
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Check if user has purchased the course
    has_purchased = False
    if request.user.is_authenticated:
        has_purchased = Purchase.objects.filter(
            user=request.user, 
            course=course, 
            is_completed=True
        ).exists()
    
    context = {
        'course': course,
        'sections': sections,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'has_purchased': has_purchased,
    }
    return render(request, 'courses/course_detail.html', context)

def category_courses(request, slug):
    """Display courses by category"""
    category = get_object_or_404(Category, slug=slug)
    courses = Course.objects.filter(category=category, is_active=True)
    
    # Pagination
    paginator = Paginator(courses, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'courses': page_obj,
    }
    return render(request, 'courses/category_courses.html', context)

# ===== USER DASHBOARD VIEWS =====

@login_required
def my_courses(request):
    """Display user's purchased courses"""
    purchases = Purchase.objects.filter(
        user=request.user, 
        is_completed=True
    ).select_related('course')
    
    context = {
        'purchases': purchases,
    }
    return render(request, 'courses/my_courses.html', context)

@login_required
def course_learn(request, course_id):
    """Course learning interface"""
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    # Check if user has purchased the course
    purchase = get_object_or_404(
        Purchase, 
        user=request.user, 
        course=course, 
        is_completed=True
    )
    
    sections = course.sections.filter(is_active=True).prefetch_related('lessons')
    
    # Get current lesson (first incomplete or first lesson)
    current_lesson = None
    for section in sections:
        for lesson in section.lessons.filter(is_active=True):
            progress = LessonProgress.objects.filter(
                user=request.user, 
                lesson=lesson
            ).first()
            
            if not progress or not progress.is_completed:
                current_lesson = lesson
                break
        if current_lesson:
            break
    
    # If all lessons completed, show first lesson
    if not current_lesson and sections:
        first_section = sections.first()
        if first_section.lessons.filter(is_active=True).exists():
            current_lesson = first_section.lessons.filter(is_active=True).first()
    
    context = {
        'course': course,
        'sections': sections,
        'current_lesson': current_lesson,
    }
    return render(request, 'courses/course_learn.html', context)

@login_required
def lesson_detail(request, lesson_id):
    """Display specific lesson content"""
    lesson = get_object_or_404(Lesson, id=lesson_id, is_active=True)
    course = lesson.section.course
    
    # Check if user has purchased the course or lesson is preview
    if not lesson.is_preview:
        get_object_or_404(
            Purchase, 
            user=request.user, 
            course=course
        )
    
    # Get or create lesson progress
    progress, created = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'progress_percentage': 0}
    )
    
    # Get all sections for navigation
    sections = course.sections.filter(is_active=True).prefetch_related('lessons')
    
    # Get all lessons in order for navigation
    all_lessons = []
    for section in sections.order_by('order'):
        for section_lesson in section.lessons.filter(is_active=True).order_by('order'):
            all_lessons.append(section_lesson)
    
    # Find current lesson index and get next/previous
    current_index = None
    for i, l in enumerate(all_lessons):
        if l.id == lesson.id:
            current_index = i
            break
    
    next_lesson = None
    prev_lesson = None
    
    if current_index is not None:
        if current_index > 0:
            prev_lesson = all_lessons[current_index - 1]
        if current_index < len(all_lessons) - 1:
            next_lesson = all_lessons[current_index + 1]
    
    # Get completed lesson IDs for the sidebar
    completed_lesson_ids = LessonProgress.objects.filter(
        user=request.user,
        lesson__in=all_lessons,
        is_completed=True
    ).values_list('lesson_id', flat=True)
    
    context = {
        'lesson': lesson,
        'course': course,
        'sections': sections,
        'progress': progress,
        'next_lesson': next_lesson,
        'prev_lesson': prev_lesson,
        'completed_lesson_ids': list(completed_lesson_ids),
    }
    return render(request, 'courses/lesson_detail.html', context)

# ===== AJAX VIEWS =====

@login_required
def update_lesson_progress(request):
    """Update lesson progress via AJAX"""
    if request.method == 'POST':
        lesson_id = request.POST.get('lesson_id')
        progress_percentage = request.POST.get('progress_percentage', 0)
        is_completed = request.POST.get('is_completed') == 'true'
        
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            progress, created = LessonProgress.objects.get_or_create(
                user=request.user,
                lesson=lesson
            )
            
            progress.progress_percentage = int(progress_percentage)
            progress.is_completed = is_completed
            
            if is_completed:
                from django.utils import timezone
                progress.completed_at = timezone.now()
            
            progress.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Progress updated successfully'
            })
            
        except Lesson.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Lesson not found'
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required
def add_course_review(request, course_id):
    """Add or update course review"""
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        
        # Check if user has purchased the course
        if not Purchase.objects.filter(
            user=request.user, 
            course=course, 
            is_completed=True
        ).exists():
            messages.error(request, 'You must purchase the course to leave a review.')
            return redirect('course_detail', course_id=course_id)
        
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')
        
        if rating and review_text:
            review, created = CourseReview.objects.update_or_create(
                course=course,
                user=request.user,
                defaults={
                    'rating': int(rating),
                    'review': review_text
                }
            )
            
            if created:
                messages.success(request, 'Review added successfully!')
            else:
                messages.success(request, 'Review updated successfully!')
        else:
            messages.error(request, 'Please provide both rating and review text.')
    
    return redirect('course_detail', course_id=course_id)

@login_required
def add_comment(request, course_id):
    """Add comment to course"""
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        
        if content:
            comment_data = {
                'course': course,
                'user': request.user,
                'content': content,
            }
            
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment_data['parent'] = parent_comment
            
            Comment.objects.create(**comment_data)
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Comment content cannot be empty.')
    
    return redirect('course_detail', course_id=course_id)

# ===== SEARCH VIEW =====

def search_courses(request):
    """Advanced course search"""
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    
    courses = Course.objects.filter(is_active=True)
    
    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(title_ar__icontains=query) |
            Q(description__icontains=query) |
            Q(description_ar__icontains=query)
        )
    
    if category_id:
        courses = courses.filter(category_id=category_id)
    
    if difficulty:
        courses = courses.filter(difficulty_level=difficulty)
    
    if price_min:
        courses = courses.filter(price__gte=price_min)
    
    if price_max:
        courses = courses.filter(price__lte=price_max)
    
    # Pagination
    paginator = Paginator(courses, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'courses': page_obj,
        'query': query,
        'categories': Category.objects.all(),
    }
    return render(request, 'courses/search_results.html', context)
