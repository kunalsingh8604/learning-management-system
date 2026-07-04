from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, InstructorRegistrationForm, CustomLoginForm, ProfileUpdateForm
from courses.models import Enrollment, Course


def register_student(request):
    """Register a new student account."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your student account has been created.')
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register.html', {
        'form': form,
        'role': 'Student',
    })


def register_instructor(request):
    """Register a new instructor account."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = InstructorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your instructor account has been created.')
            return redirect('dashboard')
    else:
        form = InstructorRegistrationForm()
    return render(request, 'accounts/register.html', {
        'form': form,
        'role': 'Instructor',
    })


def login_view(request):
    """Log in an existing user."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Log out the current user."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard(request):
    """Redirect to role-specific dashboard."""
    if request.user.is_instructor:
        return redirect('instructor_dashboard')
    return redirect('student_dashboard')


@login_required
def student_dashboard(request):
    """Dashboard for students showing enrolled courses and progress."""
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course', 'course__instructor')
    context = {
        'enrollments': enrollments,
        'total_enrolled': enrollments.count(),
    }
    return render(request, 'accounts/student_dashboard.html', context)


@login_required
def instructor_dashboard(request):
    """Dashboard for instructors showing their courses and stats."""
    courses = Course.objects.filter(instructor=request.user).prefetch_related('enrollments')
    total_students = sum(course.enrollments.count() for course in courses)
    context = {
        'courses': courses,
        'total_courses': courses.count(),
        'total_students': total_students,
    }
    return render(request, 'accounts/instructor_dashboard.html', context)


@login_required
def profile_view(request):
    """View and update user profile."""
    enrollments = []
    if request.user.is_student:
        enrollments = Enrollment.objects.filter(student=request.user).select_related('course', 'course__instructor')

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form, 'enrollments': enrollments})
