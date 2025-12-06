# Django ECommerce Application

A complete Django eCommerce application with vendor and buyer functionality, authentication, sessions, and email integration.

## Features

- **Authentication System**: User registration with vendor/buyer account types
- **Password Reset**: Token-based password reset with email integration
- **Vendor Features**: Create and manage stores, add/edit/delete products
- **Buyer Features**: Browse products, shopping cart, checkout, order management
- **Review System**: Product reviews with verified purchase badges
- **Session Management**: Cart persistence across sessions
- **Email Integration**: Order invoices and password reset emails
- **Admin Panel**: Full admin interface for all models

## Project Structure

```
ecommerce_project/
├── ecommerce_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── ecommerce/
│   ├── models.py (Store, Product, Cart, CartItem, Order, OrderItem, Review, ResetToken)
│   ├── views.py (All views for authentication, stores, products, cart, orders, reviews)
│   ├── forms.py (All form classes with validation)
│   ├── urls.py (URL routing)
│   ├── admin.py (Admin configuration)
│   ├── templates/ecommerce/ (All HTML templates)
│   ├── static/ecommerce/ (CSS and JavaScript files)
│   └── management/commands/ (Management commands)
├── media/products/ (Product images)
└── manage.py
```

## Installation & Setup

### Prerequisites

- Python 3.8+
- MySQL/MariaDB
- pip

### Step 1: Install Dependencies

```bash
pip install django pillow mysqlclient
```

### Step 2: Database Setup

1. Create MySQL database:

```sql
mysql -u root -p
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4;
exit;
```

2. Update database settings in `ecommerce_project/settings.py`:

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

### Step 3: Run Migrations

```bash
cd ecommerce_project
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Groups and Permissions

```bash
python manage.py setup_groups
```

### Step 5: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 6: Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Email Configuration

### Development (Console Backend)

The default configuration uses console email backend (emails printed to console). This is already configured in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Production (Gmail SMTP)

For production, update `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'  # Use App Password, not regular password
DEFAULT_FROM_EMAIL = 'your_email@gmail.com'
```

## Usage Guide

### For Vendors

1. **Register** as a vendor account
2. **Create a Store** from "My Stores" menu
3. **Add Products** to your store
4. **Manage Products** (edit, delete, view)

### For Buyers

1. **Register** as a buyer account
2. **Browse Products** from the home page
3. **View Product Details** and add to cart
4. **Manage Cart** (view, remove items)
5. **Checkout** to place orders
6. **Leave Reviews** for purchased products

## Testing Checklist

- [ ] Register as vendor and buyer
- [ ] Vendor creates store and adds products
- [ ] Buyer browses and adds to cart
- [ ] Cart persists across sessions
- [ ] Checkout creates order and sends email
- [ ] Buyer leaves review (verified if purchased)
- [ ] Password reset works with email
- [ ] Stock reduces after purchase
- [ ] Permissions prevent unauthorized access
- [ ] Admin panel shows all data

## Key Features Implementation

### Session Management
- Cart stored in both database and session (backup)
- Session expiry after 24 hours
- Session cleared on logout

### Email Functionality
- Password reset emails with secure tokens
- Order invoice emails
- Token expiry (30 minutes)

### Permissions
- Vendors: Create/edit/delete stores and products
- Buyers: Browse, cart, checkout, review
- Authentication required for all actions except browse

### Review Verification
- Auto-check if buyer purchased product
- Display verified badge
- One review per buyer per product

### Stock Management
- Check stock before adding to cart
- Reduce stock on checkout
- Display "Out of Stock" for zero stock

### Security
- Password hashing (Django default)
- CSRF protection
- Token-based password reset
- Permission checks on all sensitive views

## Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin/` using your superuser credentials.

All models are registered with custom admin classes:
- StoreAdmin
- ProductAdmin
- CartAdmin, CartItemAdmin
- OrderAdmin, OrderItemAdmin
- ReviewAdmin
- ResetTokenAdmin

## Troubleshooting

### Database Connection Issues
- Ensure MySQL/MariaDB is running
- Verify database credentials in settings.py
- Check database exists: `SHOW DATABASES;`

### Static Files Not Loading
- Run `python manage.py collectstatic` (for production)
- Ensure `STATICFILES_DIRS` is configured in settings.py

### Media Files Not Loading
- Ensure `MEDIA_ROOT` and `MEDIA_URL` are configured
- Check `media/products/` directory exists
- Verify URL configuration includes media files in DEBUG mode

### Email Not Sending
- Check email backend configuration
- For Gmail: Use App Password, not regular password
- Check console for email output in development mode

## License

This project is created for educational purposes.

