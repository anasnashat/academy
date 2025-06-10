from django.contrib import admin
from .models import Category, Course, Section, Lesson, Purchase, LessonProgress, CourseReview, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_ar', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'instructor', 'price', 'difficulty_level', 'is_active', 'is_featured']
    list_filter = ['category', 'difficulty_level', 'is_active', 'is_featured']
    search_fields = ['title', 'title_ar']

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'is_active']
    list_filter = ['course', 'is_active']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'lesson_type', 'order', 'is_preview', 'is_active']
    list_filter = ['lesson_type', 'is_preview', 'is_active']

admin.site.register(Purchase)
admin.site.register(LessonProgress)
admin.site.register(CourseReview)
admin.site.register(Comment)
