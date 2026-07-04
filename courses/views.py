from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.utils import timezone
from .models import Course, Module, Lesson, Enrollment, Progress, Review, Certificate
from .forms import CourseForm, ModuleForm, LessonForm, ReviewForm


def home_view(request):
    """Landing page with featured courses."""
    featured_courses = Course.objects.filter(is_published=True)[:6]
    total_courses = Course.objects.filter(is_published=True).count()
    total_students = Enrollment.objects.values('student').distinct().count()
    context = {
        'featured_courses': featured_courses,
        'total_courses': total_courses,
        'total_students': total_students,
    }
    return render(request, 'home.html', context)


def catalog_view(request):
    """Browse all published courses with search and filter."""
    courses = Course.objects.filter(is_published=True)

    # Search
    query = request.GET.get('q', '')
    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(instructor__first_name__icontains=query) |
            Q(instructor__last_name__icontains=query)
        )

    # Category filter
    category = request.GET.get('category', '')
    if category:
        courses = courses.filter(category=category)

    # Level filter
    level = request.GET.get('level', '')
    if level:
        courses = courses.filter(level=level)

    context = {
        'courses': courses,
        'query': query,
        'selected_category': category,
        'selected_level': level,
        'categories': Course.CATEGORY_CHOICES,
        'levels': Course.LEVEL_CHOICES,
    }
    return render(request, 'courses/catalog.html', context)


def course_detail_view(request, slug):
    """View course details, modules, lessons, and reviews."""
    course = get_object_or_404(Course, slug=slug, is_published=True)
    modules = course.modules.prefetch_related('lessons').all()
    reviews = course.reviews.select_related('student').all()
    is_enrolled = False
    enrollment = None
    user_review = None

    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(student=request.user, course=course).first()
        is_enrolled = enrollment is not None
        user_review = Review.objects.filter(student=request.user, course=course).first()

    # Review form
    review_form = ReviewForm()
    if request.method == 'POST' and request.user.is_authenticated and is_enrolled:
        if 'submit_review' in request.POST:
            if user_review:
                review_form = ReviewForm(request.POST, instance=user_review)
            else:
                review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.student = request.user
                review.course = course
                review.save()
                messages.success(request, 'Review submitted successfully!')
                return redirect('course_detail', slug=slug)

    context = {
        'course': course,
        'modules': modules,
        'reviews': reviews,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'review_form': review_form,
        'user_review': user_review,
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
def enroll_view(request, slug):
    """Enroll a student in a course."""
    course = get_object_or_404(Course, slug=slug)
    if request.user.is_student:
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user, course=course
        )
        if created:
            messages.success(request, f'You have been enrolled in "{course.title}"!')
        else:
            messages.info(request, 'You are already enrolled in this course.')
    else:
        messages.warning(request, 'Only students can enroll in courses.')
    return redirect('course_detail', slug=slug)


@login_required
def unenroll_view(request, slug):
    """Unenroll a student from a course."""
    course = get_object_or_404(Course, slug=slug)
    enrollment = Enrollment.objects.filter(student=request.user, course=course)
    if enrollment.exists():
        enrollment.delete()
        # Also delete progress
        Progress.objects.filter(student=request.user, lesson__module__course=course).delete()
        messages.success(request, f'You have been unenrolled from "{course.title}".')
    return redirect('my_courses')


@login_required
def lesson_view(request, slug, lesson_id):
    """View a lesson and mark it as complete."""
    course = get_object_or_404(Course, slug=slug)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)

    # Get or create progress for this lesson
    progress, created = Progress.objects.get_or_create(
        student=request.user, lesson=lesson
    )

    # Mark as complete
    if request.method == 'POST' and 'mark_complete' in request.POST:
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()
        messages.success(request, f'Lesson "{lesson.title}" marked as complete!')

        # Check if all lessons are completed for certificate
        if enrollment.is_completed:
            cert, cert_created = Certificate.objects.get_or_create(
                student=request.user, course=course
            )
            if cert_created:
                messages.success(request, '🎉 Congratulations! You have completed the course and earned a certificate!')

        return redirect('lesson_view', slug=slug, lesson_id=lesson_id)

    # Get all lessons for navigation
    all_modules = course.modules.prefetch_related('lessons').all()
    completed_lessons = Progress.objects.filter(
        student=request.user,
        lesson__module__course=course,
        completed=True
    ).values_list('lesson_id', flat=True)

    context = {
        'course': course,
        'lesson': lesson,
        'progress': progress,
        'enrollment': enrollment,
        'all_modules': all_modules,
        'completed_lessons': list(completed_lessons),
    }
    return render(request, 'courses/lesson_view.html', context)


@login_required
def my_courses_view(request):
    """Show all courses the student is enrolled in."""
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course', 'course__instructor')
    return render(request, 'courses/my_courses.html', {'enrollments': enrollments})


@login_required
def certificate_view(request, slug):
    """View certificate for a completed course."""
    course = get_object_or_404(Course, slug=slug)
    certificate = get_object_or_404(Certificate, student=request.user, course=course)
    context = {
        'certificate': certificate,
        'course': course,
    }
    return render(request, 'courses/certificate.html', context)


# ============ INSTRUCTOR VIEWS ============

@login_required
def create_course_view(request):
    """Create a new course (instructors only)."""
    if not request.user.is_instructor:
        messages.warning(request, 'Only instructors can create courses.')
        return redirect('home')

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, f'Course "{course.title}" created successfully!')
            return redirect('manage_course', slug=course.slug)
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'action': 'Create'})


@login_required
def edit_course_view(request, slug):
    """Edit an existing course (owner only)."""
    course = get_object_or_404(Course, slug=slug, instructor=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f'Course "{course.title}" updated successfully!')
            return redirect('manage_course', slug=course.slug)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form, 'action': 'Edit', 'course': course})


@login_required
def delete_course_view(request, slug):
    """Delete a course (owner only)."""
    course = get_object_or_404(Course, slug=slug, instructor=request.user)
    if request.method == 'POST':
        title = course.title
        course.delete()
        messages.success(request, f'Course "{title}" has been deleted.')
        return redirect('instructor_dashboard')
    return render(request, 'courses/confirm_delete.html', {'course': course})


@login_required
def manage_course_view(request, slug):
    """Manage course content — add modules and lessons."""
    course = get_object_or_404(Course, slug=slug, instructor=request.user)
    modules = course.modules.prefetch_related('lessons').all()
    enrollments = course.enrollments.select_related('student').all()

    # Module form
    module_form = ModuleForm()
    if request.method == 'POST' and 'add_module' in request.POST:
        module_form = ModuleForm(request.POST)
        if module_form.is_valid():
            module = module_form.save(commit=False)
            module.course = course
            module.save()
            messages.success(request, f'Module "{module.title}" added!')
            return redirect('manage_course', slug=slug)

    context = {
        'course': course,
        'modules': modules,
        'module_form': module_form,
        'enrollments': enrollments,
    }
    return render(request, 'courses/manage_course.html', context)


@login_required
def add_lesson_view(request, slug, module_id):
    """Add a lesson to a module."""
    course = get_object_or_404(Course, slug=slug, instructor=request.user)
    module = get_object_or_404(Module, id=module_id, course=course)

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            messages.success(request, f'Lesson "{lesson.title}" added to {module.title}!')
            return redirect('manage_course', slug=slug)
    else:
        form = LessonForm()
    return render(request, 'courses/lesson_form.html', {
        'form': form,
        'course': course,
        'module': module,
        'action': 'Add',
    })


@login_required
def edit_lesson_view(request, slug, lesson_id):
    """Edit a lesson."""
    course = get_object_or_404(Course, slug=slug, instructor=request.user)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, f'Lesson "{lesson.title}" updated!')
            return redirect('manage_course', slug=slug)
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'courses/lesson_form.html', {
        'form': form,
        'course': course,
        'module': lesson.module,
        'action': 'Edit',
    })


@login_required
def delete_lesson_view(request, slug, lesson_id):
    """Delete a lesson."""
    course = get_object_or_404(Course, slug=slug, instructor=request.user)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    if request.method == 'POST':
        lesson.delete()
        messages.success(request, 'Lesson deleted.')
        return redirect('manage_course', slug=slug)
    return render(request, 'courses/confirm_delete.html', {'lesson': lesson, 'course': course})


@login_required
def delete_module_view(request, slug, module_id):
    """Delete a module and its lessons."""
    course = get_object_or_404(Course, slug=slug, instructor=request.user)
    module = get_object_or_404(Module, id=module_id, course=course)
    if request.method == 'POST':
        module.delete()
        messages.success(request, 'Module deleted.')
        return redirect('manage_course', slug=slug)
    return render(request, 'courses/confirm_delete.html', {'module': module, 'course': course})
