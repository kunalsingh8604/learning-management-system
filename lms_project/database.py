"""Production database configuration for Django."""

import os
from pathlib import Path

import dj_database_url

# Environment variable names checked in priority order (first match wins).
DATABASE_URL_KEYS = (
    'DATABASE_URL',
    'SUPABASE_DATABASE_URL',
    'POSTGRES_URL',
    'POSTGRES_URL_NON_POOLING',
)


def resolve_database_url() -> str | None:
    """Return a normalized PostgreSQL connection URL, or None for local SQLite."""
    for key in DATABASE_URL_KEYS:
        value = os.environ.get(key, '').strip()
        if not value:
            continue
        # Django/psycopg expect postgresql:// not postgres://
        if value.startswith('postgres://'):
            value = 'postgresql://' + value[len('postgres://'):]
        return value
    return None


def build_databases(*, base_dir: Path, is_vercel: bool) -> dict:
    """
    Build Django DATABASES setting.

    - DATABASE_URL set → PostgreSQL (persistent, required for Vercel production)
    - Local dev, no URL → SQLite file in project root
    - Vercel, no URL → ephemeral SQLite in /tmp (demo only; data resets)
    """
    database_url = resolve_database_url()

    if database_url:
        return {
            'default': dj_database_url.config(
                default=database_url,
                engine='django.db.backends.postgresql',
                conn_max_age=0,
                conn_health_checks=True,
                ssl_require='sslmode=disable' not in database_url,
            )
        }

    if is_vercel:
        return {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': '/tmp/db.sqlite3',
            }
        }

    return {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': base_dir / 'db.sqlite3',
        }
    }


def is_persistent() -> bool:
    """True when connected to external PostgreSQL (accounts survive redeploys)."""
    return resolve_database_url() is not None
