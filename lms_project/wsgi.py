"""
WSGI config for lms_project project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')
application = get_wsgi_application()

# Vercel expects the WSGI callable to be named `app`
app = application


def _bootstrap_vercel_database():
    """Run migrations and seed data on Vercel cold starts."""
    if not os.environ.get('VERCEL'):
        return

    from django.contrib.auth import get_user_model
    from django.core.management import call_command

    from courses.models import Course

    call_command('migrate', interactive=False, verbosity=0)

    User = get_user_model()
    admin_username = os.environ.get('ADMIN_USERNAME')
    admin_password = os.environ.get('ADMIN_PASSWORD')
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')

    if admin_username and admin_password:
        user, _ = User.objects.get_or_create(
            username=admin_username,
            defaults={
                'email': admin_email,
                'is_staff': True,
                'is_superuser': True,
            },
        )
        user.email = admin_email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(admin_password)
        user.save()

    if not Course.objects.exists():
        call_command('populate_demo', verbosity=0)


_bootstrap_vercel_database()
