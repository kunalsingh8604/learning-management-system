# Learning Management System

Django LMS with student and instructor roles.

## Local development

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py populate_demo  # optional demo data
python manage.py runserver
```

Without `DATABASE_URL`, local development uses SQLite (`db.sqlite3`).

## Vercel deployment (required for login to work)

Vercel is **serverless**. Each request can run on a different machine, so **SQLite cannot store user accounts permanently**. You must connect a **PostgreSQL** database.

### 1. Create free PostgreSQL (Supabase)

1. Sign up at [https://supabase.com](https://supabase.com)
2. Create a new project
3. Go to **Project Settings → Database**
4. Under **Connection string**, choose **URI** and copy the string (use **Session pooler** mode)
5. Replace `[YOUR-PASSWORD]` with your database password

Example:
`postgresql://postgres.xxxxx:password@aws-0-ap-south-1.pooler.supabase.com:6543/postgres`

### 2. Add Vercel environment variables

In Vercel → your project → **Settings → Environment Variables**:

| Name | Value |
|------|--------|
| `DATABASE_URL` | Supabase connection string |
| `SECRET_KEY` | long random string |
| `DEBUG` | `False` |
| `CSRF_TRUSTED_ORIGINS` | `https://learning-management-system-theta-blush.vercel.app` |

Optional admin account (created automatically on deploy):

| Name | Value |
|------|--------|
| `ADMIN_USERNAME` | your username |
| `ADMIN_PASSWORD` | your password |
| `ADMIN_EMAIL` | your email |

### 3. Redeploy

Push to GitHub or click **Redeploy** in Vercel. Migrations run automatically on startup.

### 4. Test sign-up and login

1. Open your Vercel site
2. Register as Student or Instructor
3. Log out
4. Log in again with the same username and password

See `.env.example` for all supported variables.

## Other PostgreSQL providers

Any PostgreSQL host works — set `DATABASE_URL` to your connection string:

- [Supabase](https://supabase.com) (recommended, free)
- [Vercel Postgres](https://vercel.com/storage/postgres) (uses `POSTGRES_URL` automatically)
- [Railway](https://railway.app)
- [Render](https://render.com)
