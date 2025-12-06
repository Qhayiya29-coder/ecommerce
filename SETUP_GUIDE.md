# Quick Setup Guide

## Step-by-Step Setup Instructions

### 1. Install Dependencies

```bash
cd ecommerce_project
pip install -r requirements.txt
```

Or manually:
```bash
pip install django pillow mysqlclient
```

### 2. Configure Database

Edit `ecommerce_project/settings.py` and update the database credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'USER': 'root',
        'PASSWORD': 'your_password',  # Change this
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 3. Create Database

```bash
mysql -u root -p
```

Then in MySQL:
```sql
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4;
exit;
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Setup Groups and Permissions

```bash
python manage.py setup_groups
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

### 7. Run Server

```bash
python manage.py runserver
```

### 8. Access the Application

- **Home Page**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Testing the Application

### Test Vendor Flow

1. Register a new account (select "Vendor")
2. Login with vendor credentials
3. Go to "My Stores" → Create a store
4. Add products to your store
5. Edit/Delete products as needed

### Test Buyer Flow

1. Register a new account (select "Buyer")
2. Login with buyer credentials
3. Browse products on home page
4. View product details
5. Add products to cart
6. View cart and checkout
7. Leave reviews for purchased products

### Test Password Reset

1. Go to login page
2. Click "Forgot Password?"
3. Enter your email
4. Check console for reset link (in development)
5. Click link and reset password

## Important Notes

- **Email**: In development, emails are printed to console. Check the terminal running `runserver` for email content.
- **Media Files**: Product images are stored in `media/products/` directory (already created).
- **Sessions**: Cart data persists for 24 hours in sessions.
- **Groups**: Run `setup_groups` command before testing to ensure proper permissions.

## Troubleshooting

### Database Connection Error
- Ensure MySQL/MariaDB is running
- Verify database credentials
- Check if database exists: `SHOW DATABASES;`

### Static Files Not Loading
- In development, Django serves static files automatically
- For production, run: `python manage.py collectstatic`

### Permission Errors
- Run `python manage.py setup_groups` to create groups
- Ensure users are assigned to correct groups (Vendors/Buyers)

### Import Errors
- Ensure you're in the `ecommerce_project` directory
- Verify all dependencies are installed: `pip list`

## Next Steps

1. Customize email settings for production
2. Configure production database
3. Set up proper static file serving
4. Configure security settings for production
5. Add more features as needed

