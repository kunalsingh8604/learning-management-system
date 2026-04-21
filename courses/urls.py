from django.urls import path
from . import views

urlpatterns = [
    # Public - catalog (must be before slug patterns)
    path('', views.catalog_view, name='catalog'),

    # Student actions (specific paths before slug catch-all)
    path('my/courses/', views.my_courses_view, name='my_courses'),

    # Instructor - Create (specific path before slug catch-all)
    path('instructor/create/', views.create_course_view, name='create_course'),

    # Slug-based routes
    path('<slug:slug>/', views.course_detail_view, name='course_detail'),
    path('<slug:slug>/enroll/', views.enroll_view, name='enroll'),
    path('<slug:slug>/unenroll/', views.unenroll_view, name='unenroll'),
    path('<slug:slug>/certificate/', views.certificate_view, name='certificate'),
    path('<slug:slug>/edit/', views.edit_course_view, name='edit_course'),
    path('<slug:slug>/delete/', views.delete_course_view, name='delete_course'),
    path('<slug:slug>/manage/', views.manage_course_view, name='manage_course'),

    # Lesson views
    path('<slug:slug>/lesson/<int:lesson_id>/', views.lesson_view, name='lesson_view'),
    path('<slug:slug>/lesson/<int:lesson_id>/edit/', views.edit_lesson_view, name='edit_lesson'),
    path('<slug:slug>/lesson/<int:lesson_id>/delete/', views.delete_lesson_view, name='delete_lesson'),

    # Module actions
    path('<slug:slug>/module/<int:module_id>/delete/', views.delete_module_view, name='delete_module'),
    path('<slug:slug>/module/<int:module_id>/add-lesson/', views.add_lesson_view, name='add_lesson'),
]
