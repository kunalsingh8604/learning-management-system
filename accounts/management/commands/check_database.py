"""Check whether the production PostgreSQL database is configured and reachable."""

from django.core.management.base import BaseCommand
from django.db import connection

from lms_project.database import resolve_database_url


class Command(BaseCommand):
    help = 'Verify PostgreSQL connection (run before deploying to Vercel)'

    def handle(self, *args, **options):
        url = resolve_database_url()

        if not url:
            self.stdout.write(self.style.ERROR(
                'No database URL found. Set DATABASE_URL (or connect Vercel Postgres).'
            ))
            self.stdout.write(
                'Vercel: Dashboard -> Project -> Storage -> Create Database -> Postgres -> Redeploy'
            )
            return

        masked = url.split('@')[-1] if '@' in url else '(configured)'
        self.stdout.write(f'Database URL host: {masked}')

        try:
            connection.ensure_connection()
            self.stdout.write(self.style.SUCCESS(
                f'Connected to {connection.vendor} — accounts will persist across redeploys.'
            ))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f'Connection failed: {exc}'))
