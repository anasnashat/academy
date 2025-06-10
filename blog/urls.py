from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Blog home and main pages
    path('', views.blog_home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('search/', views.search, name='search'),
    path('archives/', views.archives, name='archives'),
    path('contact/', views.contact, name='contact'),
    
    # Newsletter signup
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
    
    # Post detail
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    
    # Categories and tags
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('tag/<slug:slug>/', views.tag_detail, name='tag_detail'),
    
    # AJAX endpoints
    path('post/<slug:post_slug>/comment/', views.add_comment, name='add_comment'),
]
