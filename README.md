# Learning Management System

Django LMS with student and instructor roles.

## Local development

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py populate_demo   # optional demo data
python manage.py runserver
```

Locally the app uses SQLite (`db.sqlite3`) when `DATABASE_URL` is not set.

## Deploy on Vercel (important)

Vercel’s filesystem is **read-only**, so **SQLite does not work** in production.
You must use a hosted PostgreSQL database (free options: [Neon](https://neon.tech) or [Supabase](https://supabase.com)).

### 1. Create a free Postgres database (Neon)

1. Sign up at [https://neon.tech](https://neon.tech)
2. Create a project
3. Copy the connection string (looks like  
   `postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require`)

### 2. Add environment variables in Vercel

In your Vercel project → **Settings → Environment Variables**, add:

| Name | Value |
|------|--------|
| `DATABASE_URL` | Your Neon/Supabase connection string |
| `SECRET_KEY` | A long random string (not the default insecure key) |
| `DEBUG` | `False` |
| `CSRF_TRUSTED_ORIGINS` | `https://learning-management-system-theta-blush.vercel.app` |

Redeploy after saving variables.

### 3. Run migrations against the remote database

On your machine (with the same `DATABASE_URL`):

```bash
# Windows PowerShell
$env:DATABASE_URL="postgresql://user:password@ep-xxx.../neondb?sslmode=require"
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_demo   # optional
```

### 4. Push and redeploy

Push these code changes to GitHub so Vercel rebuilds:

```bash
git add .
git commit -m "Use PostgreSQL on Vercel instead of SQLite"
git push
```

After deploy, open https://learning-management-system-theta-blush.vercel.app/

## Why the error happened

`OperationalError: unable to open database file` means Django tried to open
`/var/task/db.sqlite3` on Vercel. That path is not writable in serverless, so
SQLite cannot create or open the file. PostgreSQL via `DATABASE_URL` fixes this.
