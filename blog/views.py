from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, Category, Tag, Comment
from .forms import CommentForm, PostSearchForm, NewsletterForm, ContactForm


def blog_home(request):
    """Blog homepage with featured posts and recent posts"""
    featured_posts = Post.published.filter(featured=True)[:3]
    recent_posts = Post.published.all()[:6]
    categories = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)[:5]
    popular_tags = Tag.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)[:10]
    
    context = {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'popular_tags': popular_tags,
        'page_title': 'Blog - Academy Learning Platform'
    }
    return render(request, 'blog/home.html', context)


def post_list(request):
    """List all published posts with pagination and filtering"""
    posts = Post.published.select_related('author', 'category').prefetch_related('tags')
    
    # Search functionality
    search_form = PostSearchForm(request.GET)
    if search_form.is_valid() and search_form.cleaned_data['query']:
        query = search_form.cleaned_data['query']
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    # Category filtering
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)
    
    # Tag filtering
    tag_slug = request.GET.get('tag')
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=tag)
    
    # Pagination
    paginator = Paginator(posts, 9)  # 9 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Sidebar data
    categories = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)
    popular_tags = Tag.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)[:15]
    recent_posts = Post.published.all()[:5]
    
    context = {
        'page_obj': page_obj,
        'posts': page_obj,
        'search_form': search_form,
        'categories': categories,
        'popular_tags': popular_tags,
        'recent_posts': recent_posts,
        'current_category': category_slug,
        'current_tag': tag_slug,
        'page_title': 'All Posts - Blog'
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    """Display single post with comments"""
    post = get_object_or_404(
        Post.published.select_related('author', 'category').prefetch_related('tags'),
        slug=slug
    )
    
    # Increment views count
    post.increment_views()
    
    # Get comments (only parent comments, replies are loaded via the template)
    comments = post.comments.filter(active=True, parent=None).select_related('author').prefetch_related('replies')
    
    # Comment form
    comment_form = CommentForm()
    
    # Handle comment submission
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            
            # Handle reply
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id, post=post)
                    comment.parent = parent_comment
                except Comment.DoesNotExist:
                    pass
            
            comment.save()
            messages.success(request, 'Your comment has been added successfully!')
            return redirect('blog:post_detail', slug=slug)
    
    # Related posts
    related_posts = post.get_related_posts()
    
    # Sidebar data
    categories = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)[:10]
    popular_tags = Tag.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)[:15]
    recent_posts = Post.published.exclude(id=post.id)[:5]
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts,
        'categories': categories,
        'popular_tags': popular_tags,
        'recent_posts': recent_posts,
        'page_title': post.title
    }
    return render(request, 'blog/post_detail.html', context)


def category_detail(request, slug):
    """List posts in a specific category"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.published.filter(category=category).select_related('author').prefetch_related('tags')
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Sidebar data
    categories = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)
    popular_tags = Tag.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)[:15]
    recent_posts = Post.published.all()[:5]
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'posts': page_obj,
        'categories': categories,
        'popular_tags': popular_tags,
        'recent_posts': recent_posts,
        'page_title': f'{category.name} - Blog'
    }
    return render(request, 'blog/category_detail.html', context)


def tag_detail(request, slug):
    """List posts with a specific tag"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.published.filter(tags=tag).select_related('author', 'category').prefetch_related('tags')
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Sidebar data
    categories = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)
    popular_tags = Tag.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)[:15]
    recent_posts = Post.published.all()[:5]
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
        'posts': page_obj,
        'categories': categories,
        'popular_tags': popular_tags,
        'recent_posts': recent_posts,
        'page_title': f'#{tag.name} - Blog'
    }
    return render(request, 'blog/tag_detail.html', context)


def search(request):
    """Search posts"""
    search_form = PostSearchForm(request.GET)
    posts = Post.objects.none()
    query = ''
    
    if search_form.is_valid() and search_form.cleaned_data['query']:
        query = search_form.cleaned_data['query']
        posts = Post.published.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct().select_related('author', 'category').prefetch_related('tags')
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Sidebar data
    categories = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)
    popular_tags = Tag.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)[:15]
    recent_posts = Post.published.all()[:5]
    
    context = {
        'page_obj': page_obj,
        'posts': page_obj,
        'search_form': search_form,
        'query': query,
        'categories': categories,
        'popular_tags': popular_tags,
        'recent_posts': recent_posts,
        'page_title': f'Search Results for "{query}"' if query else 'Search'
    }
    return render(request, 'blog/search.html', context)


@require_POST
@login_required
def add_comment(request, post_slug):
    """AJAX view to add comment"""
    post = get_object_or_404(Post, slug=post_slug)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            
            # Handle reply
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id, post=post)
                    comment.parent = parent_comment
                except Comment.DoesNotExist:
                    pass
            
            comment.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Comment added successfully!',
                'comment': {
                    'id': comment.id,
                    'content': comment.content,
                    'author': comment.author.username,
                    'created_at': comment.created_at.strftime('%B %d, %Y at %I:%M %p'),
                    'is_reply': comment.is_reply()
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def newsletter_signup(request):
    """Handle newsletter signup"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Here you would typically save to a newsletter model or send to an email service
            # For now, we'll just show a success message
            messages.success(request, 'Thank you for subscribing to our newsletter!')
            
            # Send confirmation email (optional)
            try:
                send_mail(
                    subject='Welcome to Academy Blog Newsletter',
                    message=f'Thank you for subscribing to our newsletter!',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )
            except:
                pass
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})
            
            return redirect('blog:home')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    
    return redirect('blog:home')


def contact(request):
    """Contact page"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Send email to admin
            try:
                send_mail(
                    subject=f'Contact Form: {subject}',
                    message=f'From: {name} <{email}>\n\nMessage:\n{message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
            except:
                messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')
            
            return redirect('blog:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'page_title': 'Contact Us - Blog'
    }
    return render(request, 'blog/contact.html', context)


def archives(request):
    """Blog archives page with posts grouped by month/year"""
    from django.db.models.functions import TruncMonth
    
    # Get posts grouped by month
    posts_by_month = Post.published.annotate(
        month=TruncMonth('published_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('-month')
    
    # Get all posts for the selected month
    selected_month = request.GET.get('month')
    posts = Post.objects.none()
    
    if selected_month:
        try:
            from datetime import datetime
            month_date = datetime.strptime(selected_month, '%Y-%m')
            posts = Post.published.filter(
                published_at__year=month_date.year,
                published_at__month=month_date.month
            ).select_related('author', 'category')
        except ValueError:
            pass
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts_by_month': posts_by_month,
        'page_obj': page_obj,
        'posts': page_obj,
        'selected_month': selected_month,
        'page_title': 'Archives - Blog'
    }
    return render(request, 'blog/archives.html', context)
