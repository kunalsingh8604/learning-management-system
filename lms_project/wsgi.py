"""
WSGI config for lms_project project.
"""

import logging
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')
application = get_wsgi_application()

# Vercel expects the WSGI callable to be named `app`
app = application

logger = logging.getLogger(__name__)


def _bootstrap_vercel_database():
    """
    On Vercel cold starts:
    - With DATABASE_URL → run setup_production (migrate + superuser + demo)
    - Without DATABASE_URL → migrate ephemeral SQLite + demo only
    """
    if not os.environ.get('VERCEL'):
        return

    try:
        from django.core.management import call_command

        from lms_project.database import is_persistent

        if is_persistent():
            admin_username = os.environ.get('ADMIN_USERNAME', '').strip()
            admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com').strip()
            admin_password = os.environ.get('ADMIN_PASSWORD', '').strip()

            if admin_username and admin_password:
                call_command(
                    'setup_production',
                    username=admin_username,
                    email=admin_email,
                    demo=True,
                    verbosity=0,
                )
            else:
                call_command('migrate', interactive=False, verbosity=0)
                from courses.models import Course
                if not Course.objects.exists():
                    call_command('populate_demo', verbosity=0)
        else:
            call_command('migrate', interactive=False, verbosity=0)
            from courses.models import Course
            if not Course.objects.exists():
                call_command('populate_demo', verbosity=0)
    except Exception:
        logger.exception('Vercel database bootstrap failed')


_bootstrap_vercel_database()
