from django.urls import path
from . import views

urlpatterns = [
    # Public views
    path('', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('category/<slug:slug>/', views.category_courses, name='category_courses'),
    path('search/', views.search_courses, name='search_courses'),
    
    # User dashboard
    path('my-courses/', views.my_courses, name='my_courses'),
    path('learn/<int:course_id>/', views.course_learn, name='course_learn'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    
    # AJAX endpoints
    path('ajax/update-progress/', views.update_lesson_progress, name='update_lesson_progress'),
    path('ajax/add-review/<int:course_id>/', views.add_course_review, name='add_course_review'),
    path('ajax/add-comment/<int:course_id>/', views.add_comment, name='add_comment'),
]