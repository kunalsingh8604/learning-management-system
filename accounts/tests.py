from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from courses.models import Course, Enrollment


class ProfileEnrolledCoursesTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.student = self.User.objects.create_user(
            username='student1',
            email='student1@example.com',
            password='testpass123',
            role='student',
        )
        self.instructor = self.User.objects.create_user(
            username='instructor1',
            email='instructor1@example.com',
            password='testpass123',
            role='instructor',
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='A course for testing enrollment.',
            instructor=self.instructor,
            is_published=True,
        )
        Enrollment.objects.create(student=self.student, course=self.course)

    def test_profile_page_shows_enrolled_courses(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Enrolled Courses')
        self.assertContains(response, self.course.title)
