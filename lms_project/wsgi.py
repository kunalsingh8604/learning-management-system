"""
WSGI config for lms_project project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')
application = get_wsgi_application()

# Vercel expects the WSGI callable to be named `app`
app = application


def _bootstrap_vercel_sqlite():
    """Create tables (and demo data) for ephemeral SQLite on Vercel."""
    if not os.environ.get('VERCEL') or os.environ.get('DATABASE_URL'):
        return

    from django.core.management import call_command

    call_command('migrate', interactive=False, verbosity=0)

    from courses.models import Course

    if not Course.objects.exists():
        call_command('populate_demo', verbosity=0)


_bootstrap_vercel_sqlite()
