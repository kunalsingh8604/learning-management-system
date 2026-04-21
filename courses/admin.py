from django.contrib import admin
from .models import Course, Module, Lesson, Enrollment, Progress, Review, Certificate


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'level', 'is_published', 'created_at')
    list_filter = ('category', 'level', 'is_published')
    search_fields = ('title', 'description', 'instructor__username')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'duration_minutes')
    list_filter = ('module__course',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')
    list_filter = ('course', 'enrolled_at')


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'completed', 'completed_at')
    list_filter = ('completed',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'rating', 'created_at')
    list_filter = ('rating', 'course')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'certificate_id', 'issued_at')
    list_filter = ('course',)
