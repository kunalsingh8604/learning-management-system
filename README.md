# Learning Management System

Django LMS deployed on Vercel with PostgreSQL for persistent user accounts.

## Production database setup

Vercel serverless cannot use SQLite for production — `/tmp` SQLite resets and is not shared
between instances. Use **PostgreSQL** via `DATABASE_URL`.

### 1. Create a PostgreSQL database (Supabase — free)

1. Sign up at [supabase.com](https://supabase.com)
2. **New project** → set a database password
3. **Project Settings → Database → Connection string → URI**
4. Choose **Session pooler** (port `6543`)
5. Copy the URI and replace `[YOUR-PASSWORD]`

### 2. Set environment variables in Vercel

1. Open [vercel.com/dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to **Settings** (top navigation)
4. Click **Environment Variables** (left sidebar)
5. Add each variable below
6. Select **Production**, **Preview**, and **Development** environments
7. Click **Save**
8. Go to **Deployments** → latest deployment → **Redeploy**

| Variable | Value | Required |
|----------|-------|----------|
| `DATABASE_URL` | PostgreSQL connection string from Supabase | Yes |
| `ADMIN_PASSWORD` | Superuser password | Yes |
| `ADMIN_USERNAME` | Superuser username | Yes |
| `ADMIN_EMAIL` | Superuser email | Yes |
| `SECRET_KEY` | Long random string | Yes |
| `DEBUG` | `False` | Yes |
| `CSRF_TRUSTED_ORIGINS` | `https://your-app.vercel.app` | Yes |

### 3. Run setup locally (optional)

Test against your Supabase database before deploying:

```powershell
# Windows PowerShell
$env:DATABASE_URL="postgresql://postgres.xxx:PASSWORD@aws-0-region.pooler.supabase.com:6543/postgres"
$env:ADMIN_PASSWORD="your-secure-password"
python manage.py setup_production --username admin --email admin@example.com --demo
```

### 4. Deploy

Push to GitHub or redeploy on Vercel. On each cold start the app will:

- Run `migrate` against PostgreSQL
- Create/update the superuser from env vars
- Load demo courses if the database is empty

Registered users and login sessions **persist across redeploys** because data lives in PostgreSQL.

## Local development (SQLite)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Without `DATABASE_URL`, local dev uses `db.sqlite3`.

## Other PostgreSQL providers

Any provider works — set `DATABASE_URL`:

- [Supabase](https://supabase.com)
- [Vercel Postgres](https://vercel.com/storage/postgres) (auto-sets `POSTGRES_URL`)
- [Railway](https://railway.app)
- [Render](https://render.com)
