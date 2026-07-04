from django.conf import settings


def deployment(request):
    return {
        'persistent_database': getattr(settings, 'PERSISTENT_DATABASE', True),
        'is_vercel': getattr(settings, 'IS_VERCEL', False),
    }
