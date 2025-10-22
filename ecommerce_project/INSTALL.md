# Installation Guide

This guide will help you install and run the e-commerce application step-by-step.

## Step 1: Install Python

### Windows:
1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. ✅ **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"

### Mac:
```bash
brew install python3
```

Or download from https://www.python.org/downloads/

### Linux:
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
```

### Verify Installation:
```bash
python --version
```
Should show Python 3.8 or higher.

## Step 2: Download the Project

**Option A: Using Git**
```bash
git clone <repository-url>
cd ecommerce_project
```

**Option B: Download ZIP**
1. Download the project ZIP file
2. Extract it to a folder
3. Open terminal/command prompt in that folder

## Step 3: Create a Virtual Environment

A virtual environment keeps the project dependencies isolated.

### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` at the start of your command prompt.

### Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

## Step 4: Install Required Packages

With your virtual environment activated, run:

```bash
pip install -r requirements.txt
```

This will install:
- Django (web framework)
- Django REST Framework (API support)
- Pillow (image handling)
- Tweepy (Twitter integration)
- And other dependencies

**Wait for the installation to complete.** This may take a few minutes.

### Troubleshooting Installation Issues:

**If you get SSL errors:**
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

**If pip is not found:**
```bash
python -m pip install -r requirements.txt
```

**If you're on an older system or get compilation errors, try:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 5: Set Up the Database

Run these commands to create the database:

```bash
python manage.py migrate
```

You should see several lines showing migrations being applied.

## Step 6: Create an Admin User

Create your admin account:

```bash
python manage.py createsuperuser
```

You will be asked for:
- Username: Choose any username
- Email: Your email (or leave blank)
- Password: Choose a password (it won't show as you type)
- Password (again): Repeat the password

## Step 7: Run the Server

Start the development server:

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## Step 8: Access the Application

Open your web browser and go to:

**Main Site**: http://127.0.0.1:8000/

**Admin Panel**: http://127.0.0.1:8000/admin/

Use the admin credentials you created in Step 6.

## Step 9: Create Sample Data (Optional)

1. Log in to the admin panel
2. Create a few sample users
3. Log in as a user and create a store
4. Add some products to your store

OR

1. Register a new account on the main site
2. Navigate to "Vendor Dashboard"
3. Click "Create Store"
4. Add products from your store page

## Common Problems and Solutions

### "python is not recognized"
- Reinstall Python and check "Add to PATH"
- Or use full path: `C:\Python311\python.exe` (adjust version)

### "pip is not recognized"
```bash
python -m pip install -r requirements.txt
```

### "No module named 'django'"
- Make sure virtual environment is activated (you should see `(venv)`)
- Run: `pip install -r requirements.txt`

### "Port 8000 is already in use"
```bash
python manage.py runserver 8080
```
Then access at: http://127.0.0.1:8080/

### Images not showing up
- Make sure the `media/` folder exists
- Make sure you're running the development server
- Upload images through the admin or vendor dashboard

### "ImportError: No module named ..."
```bash
pip list  # Check installed packages
pip install -r requirements.txt  # Reinstall dependencies
```

### Database is locked
- Close all terminals/command prompts
- Delete `db.sqlite3` file
- Run `python manage.py migrate` again
- Run `python manage.py createsuperuser` again

## Next Steps

Once the application is running:

1. **Explore as a Buyer**: Register an account and browse products
2. **Become a Vendor**: Create a store and add products
3. **Test the Cart**: Add items and checkout
4. **Try the API**: Access http://127.0.0.1:8000/api/

## Stopping the Server

Press `CTRL + C` in the terminal where the server is running.

## Deactivating the Virtual Environment

When you're done:
```bash
deactivate
```

## Running Again Later

1. Navigate to the project folder
2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
3. Run the server: `python manage.py runserver`

## Need Help?

Check the README.md file for more detailed information about features and configuration.
