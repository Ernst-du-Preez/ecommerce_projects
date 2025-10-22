# MariaDB/MySQL Setup Instructions

## 1. Install MariaDB or MySQL

### Windows:
- Download and install MariaDB from: https://mariadb.org/download/
- Or MySQL from: https://dev.mysql.com/downloads/installer/

### Linux:
```bash
sudo apt-get update
sudo apt-get install mariadb-server
sudo mysql_secure_installation
```

## 2. Create Database and User

Connect to MySQL/MariaDB:
```bash
mysql -u root -p
```

Run the following SQL commands:
```sql
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'ecommerce_password';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**IMPORTANT:** Change 'ecommerce_password' to a strong password and update it in settings.py!

## 3. Install Python MySQL Client

```bash
pip install mysqlclient
```

If you encounter issues on Windows, you may need to install the Microsoft C++ Build Tools or use:
```bash
pip install pymysql
```

And add this to `ecommerce_project/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

## 4. Migrate the Database

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 5. Update Settings

The database configuration in `settings.py` has been updated to:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'USER': 'ecommerce_user',
        'PASSWORD': 'ecommerce_password',  # Change this!
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
```

## 6. Optional: Export Data from SQLite (if you have existing data)

Before switching databases:
```bash
python manage.py dumpdata > data.json
```

After setting up MariaDB:
```bash
python manage.py migrate
python manage.py loaddata data.json
```
