# Quick Reference Guide

## One-Time Setup (First Time Only)

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up database
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser
```

## Starting the Application (Every Time)

```bash
# 1. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 2. Start server
python manage.py runserver
```

**OR** just double-click:
- Windows: `START.bat`
- Mac/Linux: `START.sh`

## Important URLs

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/ | Main website |
| http://127.0.0.1:8000/admin/ | Admin panel |
| http://127.0.0.1:8000/api/ | API endpoints |
| http://127.0.0.1:8000/register/ | User registration |
| http://127.0.0.1:8000/login/ | User login |

## Common Commands

```bash
# Run the development server
python manage.py runserver

# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser/admin
python manage.py createsuperuser

# Run tests
python manage.py test

# Check for issues
python manage.py check

# Open Django shell
python manage.py shell

# Collect static files (for production)
python manage.py collectstatic
```

## File Structure

```
ecommerce_project/
├── START.bat              ← Windows quick start script
├── START.sh               ← Mac/Linux quick start script
├── README.md              ← Detailed documentation
├── INSTALL.md             ← Step-by-step installation guide
├── requirements.txt       ← Python dependencies
├── manage.py              ← Django management script
├── db.sqlite3            ← Database (created after setup)
├── venv/                 ← Virtual environment (created by you)
├── media/                ← Uploaded files (auto-created)
├── ecommerce/            ← Main application code
└── ecommerce_project/    ← Project settings
```

## Default Credentials

After running `createsuperuser`, you choose your own credentials.

Example:
- Username: admin
- Email: admin@example.com
- Password: (your choice)

## User Roles

1. **Buyer**: Any registered user can browse and purchase products
2. **Vendor**: Users who create stores can sell products
3. **Admin**: Superuser with full access to admin panel

## Quick Workflows

### As a New User (Buyer)
1. Go to http://127.0.0.1:8000/
2. Click "Register"
3. Create account
4. Browse products
5. Add to cart
6. Checkout

### As a Vendor
1. Login
2. Click "Create Store" (or go to Vendor Dashboard)
3. Fill in store details
4. Go to your store
5. Click "Add Product"
6. Manage products from Vendor Dashboard

### As Admin
1. Go to http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Manage all users, stores, products, orders

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| `python not found` | Install Python or add to PATH |
| `No module named 'django'` | Activate venv and run `pip install -r requirements.txt` |
| `Port 8000 in use` | Run `python manage.py runserver 8080` |
| `Database locked` | Close all terminals, restart |
| `Migration errors` | Run `python manage.py migrate` |
| Images not showing | Ensure `media/` exists and server is running |

## Environment Variables (Optional)

Create `.env` file in project root for:
```
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_SECRET=your_access_secret
```

## Email Configuration

By default, emails print to console. Check terminal for:
- Password reset links
- Order invoices

## Stopping the Server

Press `CTRL + C` in the terminal

## Deactivating Virtual Environment

```bash
deactivate
```

## Need More Help?

- Full documentation: See README.md
- Installation help: See INSTALL.md
- Database setup: See SETUP_MARIADB.md (for MySQL)
