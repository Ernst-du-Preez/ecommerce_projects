

A full-featured Django e-commerce platform with vendor management, product listings, shopping cart, and order processing.

## Features

- 🛍️ **Product Management**: Browse and search products from multiple vendors
- 🏪 **Vendor Dashboard**: Create stores and manage products
- 🛒 **Shopping Cart**: Add products to cart and checkout
- 📧 **Email Invoices**: Automatic invoice generation and email delivery
- ⭐ **Product Reviews**: Users can review purchased products
- 🔐 **Authentication**: User registration, login, and password reset
- 🎨 **REST API**: Full API with JWT authentication
- 🐦 **Twitter Integration**: Optional product/store announcements (configurable)

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

## Quick Start

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd ecommerce_project
```

Or download and extract the ZIP file.

### 2. Create a Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages:
- Django 5.0+
- Django REST Framework
- Pillow (for image handling)
- Tweepy (for Twitter integration)
- And other dependencies

### 4. Set Up the Database

Run migrations to create the database:

```bash
python manage.py migrate
```

### 5. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 6. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

## Default Setup

The project comes configured with:
- **SQLite database** (no additional setup required)
- **Console email backend** (emails print to terminal/console)
- **Media files** stored in `media/` directory
- **DEBUG mode** enabled for development

## Project Structure

```
ecommerce_project/
├── ecommerce/              # Main application
│   ├── models.py          # Database models (Store, Product, Review, Purchase)
│   ├── views.py           # View functions and API endpoints
│   ├── urls.py            # URL routing
│   ├── forms.py           # Django forms
│   ├── serializers.py     # API serializers
│   └── templates/         # HTML templates
├── ecommerce_project/     # Project settings
│   ├── settings.py        # Django settings
│   └── urls.py            # Root URL configuration
├── media/                 # Uploaded files (created automatically)
├── db.sqlite3            # SQLite database (created after migration)
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Using the Application

### As a Buyer

1. **Register**: Click "Register" and create an account
2. **Browse Products**: View available products on the homepage
3. **Add to Cart**: Click "Add to Cart" on products you want to purchase
4. **Checkout**: View your cart and complete the purchase
5. **Review**: Leave reviews on products you've purchased

### As a Vendor

1. **Create a Store**: After logging in, go to "Vendor Dashboard" → "Create Store"
2. **Add Products**: In your store detail page, click "Add Product"
3. **Manage**: Edit or delete your stores from the vendor dashboard
4. **View Products**: See all your products listed in the vendor dashboard

### As an Admin

Access the admin panel at: **http://127.0.0.1:8000/admin/**

Use your superuser credentials to:
- Manage users, stores, products, and orders
- Moderate reviews
- View system data

## API Endpoints

The application includes a REST API with JWT authentication:

### Authentication
- `POST /api/v1/auth/login/` - Obtain JWT token
- `POST /api/v1/auth/refresh/` - Refresh JWT token

### API Resources
- `GET /api/stores/` - List all stores
- `GET /api/products/` - List all products
- `GET /api/reviews/` - List all reviews

API documentation available at: **http://127.0.0.1:8000/api/**

## Email Configuration

By default, emails are printed to the console for development. Check your terminal where you run `manage.py runserver` to see:
- Password reset links
- Order invoices

To configure real email delivery, edit `settings.py` and update the `EMAIL_BACKEND` settings.

## Database Migration (Optional)

The project is configured to use SQLite by default. To migrate to MySQL/MariaDB:

1. Install MySQL/MariaDB
2. Install the MySQL client: `pip install mysqlclient`
3. Follow instructions in `SETUP_MARIADB.md`
4. Update `settings.py` database configuration

## Twitter Integration (Optional)

To enable Twitter announcements for new stores/products:

1. Create a `.env` file in the project root
2. Add your Twitter API credentials:
   ```
   TWITTER_API_KEY=your_api_key
   TWITTER_API_SECRET=your_api_secret
   TWITTER_ACCESS_TOKEN=your_access_token
   TWITTER_ACCESS_SECRET=your_access_secret
   ```
3. Install python-dotenv: `pip install python-dotenv`

Without configuration, the app works normally without Twitter features.

## Common Issues

### Import Errors

If you get `ModuleNotFoundError`, make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### Database Errors

If you get database errors, run migrations:
```bash
python manage.py migrate
```

### Media Files Not Showing

Make sure you're running the development server and the `media/` directory exists.

### Port Already in Use

If port 8000 is busy, use a different port:
```bash
python manage.py runserver 8080
```

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

After modifying models:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files (for production)

```bash
python manage.py collectstatic
```

## Security Notes

⚠️ **This is a development setup. Before deploying to production:**

1. Set `DEBUG = False` in `settings.py`
2. Change `SECRET_KEY` to a secure random value
3. Configure `ALLOWED_HOSTS` properly
4. Use HTTPS (enable SSL settings)
5. Use a production database (PostgreSQL/MySQL)
6. Configure a real email backend
7. Set up proper static file serving
8. Review all security settings in `settings.py`

## Support

For issues or questions:
1. Check the console/terminal for error messages
2. Verify all dependencies are installed: `pip list`
3. Ensure migrations are up to date: `python manage.py migrate`

## License

This project is provided as-is for educational purposes.

## Version

- Django: 5.2.6
- Python: 3.8+
- Last Updated: October 2025
