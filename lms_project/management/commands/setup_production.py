"""
Management command: set up the production database (run once after adding DATABASE_URL).
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Run migrations and create admin user for production (Neon/Vercel Postgres)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            default=os.environ.get('ADMIN_USERNAME', 'admin'),
            help='Admin username',
        )
        parser.add_argument(
            '--email',
            default=os.environ.get('ADMIN_EMAIL', 'admin@example.com'),
            help='Admin email',
        )
        parser.add_argument(
            '--password',
            default=os.environ.get('ADMIN_PASSWORD'),
            help='Admin password (or set ADMIN_PASSWORD env var)',
        )

    def handle(self, *args, **options):
        from django.core.management import call_command

        password = options['password']
        if not password:
            raise CommandError('Provide --password or set ADMIN_PASSWORD environment variable.')

        self.stdout.write('Running migrations...')
        call_command('migrate', interactive=False)

        User = get_user_model()
        username = options['username']
        email = options['email']

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
            f'{action} admin user "{username}". You can now log in on Vercel.'
        ))

        from courses.models import Course
        if not Course.objects.exists():
            self.stdout.write('Loading demo courses...')
            call_command('populate_demo')
