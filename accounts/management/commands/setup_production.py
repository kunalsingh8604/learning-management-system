"""
Set up the production PostgreSQL database.

Runs migrations, creates/updates a superuser, and optionally loads demo courses.

Usage (local, pointing at Supabase/Postgres):
    set DATABASE_URL=postgresql://...
    set ADMIN_PASSWORD=your-secure-password
    python manage.py setup_production --username admin --email admin@example.com

On Vercel, this runs automatically on cold start when DATABASE_URL is set.
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = (
        'Run migrations and create a superuser for production PostgreSQL. '
        'Password is read from the ADMIN_PASSWORD environment variable.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            required=True,
            help='Superuser username (e.g. admin)',
        )
        parser.add_argument(
            '--email',
            required=True,
            help='Superuser email address',
        )
        parser.add_argument(
            '--demo',
            action='store_true',
            help='Load demo courses if the database is empty',
        )

    def handle(self, *args, **options):
        from django.core.management import call_command

        from lms_project.database import is_persistent

        if not is_persistent():
            raise CommandError(
                'DATABASE_URL is not set. Add your PostgreSQL connection string '
                '(Supabase, Vercel Postgres, Railway, etc.) before running this command.'
            )

        password = os.environ.get('ADMIN_PASSWORD', '').strip()
        if not password:
            raise CommandError(
                'Set the ADMIN_PASSWORD environment variable before running setup_production.'
            )

        username = options['username']
        email = options['email']

        self.stdout.write('Applying migrations...')
        call_command('migrate', interactive=False, verbosity=1)

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
            },
        )
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(
            f'{action} superuser "{username}" ({email}).'
        ))

        if options['demo']:
            from courses.models import Course
            if not Course.objects.exists():
                self.stdout.write('Loading demo courses...')
                call_command('populate_demo')

        self.stdout.write(self.style.SUCCESS(
            'Production database is ready. User accounts will persist across redeploys.'
        ))
