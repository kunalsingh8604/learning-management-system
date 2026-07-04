from django.conf import settings
from django.db import connection


def deployment(request):
    persistent = getattr(settings, 'PERSISTENT_DATABASE', False)

    if persistent:
        try:
            connection.ensure_connection()
            persistent = connection.vendor == 'postgresql'
        except Exception:
            persistent = False

    return {
        'persistent_database': persistent,
        'is_vercel': getattr(settings, 'IS_VERCEL', False),
    }
