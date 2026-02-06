# Django Migration Guide

## What Changed

✅ **Backend:** Node.js/Express → Django 5.0
✅ **Admin Panel:** Custom HTML → Django Admin (built-in, production-grade)
✅ **Database:** PostgreSQL (same, but now using Django ORM + migrations)
✅ **Frontend:** Stays exactly the same (all HTML/CSS/JS preserved)

## New Admin Panel

**URL:** https://agent-control-panel-production.up.railway.app/admin/

**Credentials:**
- Username: `root`
- Password: `root`

⚠️ **Change in production!**

## Features

The Django admin panel now provides:

- ✅ **Waitlist Management** - View, search, filter, export all signups
- ✅ **Agent Monitoring** - Full CRUD for agents (when implemented)
- ✅ **Activity Logs** - Search and filter agent actions
- ✅ **Metrics Dashboard** - View cost/token usage
- ✅ **User Management** - Full auth system ready
- ✅ **Export to CSV** - Built-in data export
- ✅ **Batch Actions** - Bulk operations
- ✅ **Search & Filters** - Powerful query interface

## Deployment

Railway will automatically:
1. Detect Python via `requirements.txt`
2. Install dependencies
3. Run migrations (`python manage.py migrate`)
4. Collect static files
5. Create admin user (root/root)
6. Start gunicorn server

## Database Connection

Make sure the web service has access to the database:

**Railway Variables:**
- `DATABASE_PRIVATE_URL` → Reference from `postgres` service

Railway sets this automatically for Python apps using the detected database.

## Local Development

```bash
# Create venv
python3 -m venv venv
source venv/bin/activate

# Install deps
pip install -r requirements.txt

# Set up env vars
cp .env.example.django .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create admin user
python manage.py create_admin

# Run server
python manage.py runserver
```

## API Endpoints (Same as Before)

- `POST /api/waitlist` - Add email to waitlist
- `GET /api/waitlist/count` - Get signup count  
- `GET /api/admin/waitlist` - Get full waitlist (admin only)

## Frontend Pages (Unchanged)

- `/` - Landing page
- `/dashboard` - Demo dashboard
- `/workflows.html` - Workflows
- `/pricing.html` - Pricing
- `/integrations.html` - Integrations
- `/admin/` - Django admin panel (NEW)

## What Got Better

1. **Professional Admin UI** - No more custom HTML, real data management
2. **Database Migrations** - Schema changes are tracked and versioned
3. **ORM** - Type-safe database queries, no raw SQL
4. **Built-in Auth** - User system ready for production
5. **Django Ecosystem** - Thousands of packages available
6. **Better Error Handling** - Django debug toolbar, logging
7. **API Framework** - Django REST Framework for future API expansion

## Old Files (Can Be Removed Later)

- `server.js` (Node backend)
- `db.js` (manual DB connection)
- `schema.sql` (replaced by Django migrations)
- `admin.html` (replaced by Django admin)
- `package.json`, `package-lock.json` (Node deps)
- `node_modules/` (Node packages)

Don't delete yet - keep for reference until Django deploy is confirmed working.
