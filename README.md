# ExpressMarket - Multi-Vendor E-Commerce Platform

ExpressMarket is a full-featured multi-vendor e-commerce platform built with Django. It allows vendors to create stores, add products, and manage their inventory, while customers can browse products, add them to cart, and place orders.

## Features

### Customer Features
- **User Registration & Authentication**: Separate registration for customers and vendors
- **Product Browsing**: Browse products by category with search functionality
- **Shopping Cart**: Session-based shopping cart to add/remove products
- **Checkout Process**: Complete checkout with shipping information
- **Order Management**: View order history and track order status
- **Product Details**: Detailed product pages with images and descriptions

### Vendor Features
- **Vendor Dashboard**: Comprehensive dashboard with sales statistics
- **Store Management**: Create and manage store information
- **Product Management**: Add, edit, and delete products
- **Order Tracking**: View orders received for their products
- **Sales Analytics**: Track total sales, orders, and items sold

### Admin Features
- **Django Admin**: Full admin interface for managing all aspects of the platform
- **Order Management**: View and manage all orders
- **User Management**: Manage customers and vendors

## Technology Stack

- **Backend**: Django 6.0
- **Database**: SQLite (development)
- **Frontend**: HTML, CSS (Tailwind CSS 4.1)
- **Build Tools**: PostCSS, Autoprefixer
- **Image Handling**: Pillow
- **Authentication**: Django's built-in authentication system

## Project Structure

```
expressmarket/
├── accounts/          # User authentication and registration
├── core_ecommerce/    # Main e-commerce functionality (cart, checkout, orders)
├── customer/          # Customer profile management
├── product/           # Product and category models
├── vendor/            # Vendor and store management
├── templates/         # HTML templates
├── static/            # Static files (CSS, images)
└── expressmarket/     # Project settings and configuration
```

## Installation

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Node.js and npm (for Tailwind CSS)

### Setup Instructions

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd /path/to/practical-proj
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**:
   ```bash
   # On Linux/Mac:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

4. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   If requirements.txt doesn't exist, install manually:
   ```bash
   pip install django pillow
   ```

5. **Install Node.js dependencies** (for Tailwind CSS):
   ```bash
   cd expressmarket
   npm install
   ```

6. **Set up Tailwind CSS**:
   ```bash
   # The Tailwind configuration is already set up in tailwind.config.js
   # To build CSS for development (with watch mode):
   npm run build-css
   
   # Or for production (minified):
   npm run build-css-prod
   ```
   
   **Note**: The `build-css` command runs in watch mode and will automatically rebuild CSS when you make changes. Keep this running in a separate terminal while developing.

7. **Run database migrations**:
   ```bash
   cd expressmarket
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

9. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

10. **Run the development server**:
    ```bash
    python manage.py runserver
    ```
    
    **Important**: Make sure to run Tailwind CSS in watch mode in a separate terminal:
    ```bash
    cd expressmarket
    npm run build-css
    ```

11. **Access the application**:
    - Main site: http://127.0.0.1:8000/
    - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### For Customers

1. **Register as a Customer**:
   - Go to Register page
   - Select "Customer" as user type
   - Fill in registration form

2. **Browse Products**:
   - View products on the homepage
   - Filter by category
   - Search for specific products

3. **Add to Cart**:
   - Click on a product to view details
   - Select quantity and click "Add to Cart"
   - View cart from navigation menu

4. **Checkout**:
   - Go to cart page
   - Click "Proceed to Checkout"
   - Fill in shipping information
   - Place order

5. **View Orders**:
   - Click "My Orders" in navigation
   - View order history and details

### For Vendors

1. **Register as a Vendor**:
   - Go to Register page
   - Select "Vendor" as user type
   - Fill in vendor registration form (includes business name, TIN, logo)

2. **Create Store**:
   - After login, you'll be redirected to vendor dashboard
   - Click "Create Store"
   - Fill in store information

3. **Add Products**:
   - Click "Add Product" from dashboard or product list
   - Fill in product details (name, description, price, image, category)
   - Save product

4. **Manage Products**:
   - View all products in "My Products"
   - Edit or delete products as needed

5. **View Dashboard**:
   - Access vendor dashboard to see:
     - Total products
     - Total orders
     - Total sales
     - Recent orders

## URL Structure

### Main URLs
- `/` - Homepage (product listing)
- `/accounts/login/` - Login page
- `/accounts/register/` - Registration page
- `/accounts/logout/` - Logout

### Customer URLs
- `/cart/` - Shopping cart
- `/cart/add/<product_id>/` - Add product to cart
- `/cart/update/<product_id>/` - Update cart item quantity
- `/cart/remove/<product_id>/` - Remove item from cart
- `/checkout/` - Checkout page
- `/orders/` - My orders list
- `/orders/<order_id>/` - Order details

### Vendor URLs
- `/vendor/dashboard/` - Vendor dashboard
- `/vendor/store/create/` - Create/Edit store
- `/vendor/products/` - Product list
- `/vendor/products/create/` - Create product
- `/vendor/products/<id>/edit/` - Edit product
- `/vendor/products/<id>/delete/` - Delete product

### Product URLs
- `/product/<slug>/` - Product detail page

## Database Models

### User Models
- **User**: Custom user model with user_type (customer/vendor)
- **Customer**: Customer profile with shipping/billing addresses
- **Vendor**: Vendor profile with business information

### E-Commerce Models
- **Product**: Product information (name, price, image, category, vendor)
- **Category**: Product categories
- **Order**: Customer orders with shipping information
- **OrderItem**: Individual items in an order

### Vendor Models
- **Store**: Vendor store information
- **Vendor**: Vendor business details

## Development

### Running Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating Superuser
```bash
python manage.py createsuperuser
```

### Running Tests
```bash
python manage.py test
```

### Static Files
Static files are served from `static/` directory. CSS is compiled using Tailwind CSS.

### Tailwind CSS Development

The project uses Tailwind CSS 4.1 for styling. Here's how to work with it:

**File Structure:**
- `static/src/input.css` - Source CSS file with Tailwind directives
- `static/css/output.css` - Compiled CSS (generated, do not edit directly)
- `tailwind.config.js` - Tailwind configuration
- `postcss.config.js` - PostCSS configuration

**Development Workflow:**

1. **Start Tailwind in watch mode** (in a separate terminal):
   ```bash
   cd expressmarket
   npm run build-css
   ```
   This will watch for changes and automatically rebuild the CSS.

2. **Make changes to HTML templates** - Tailwind classes will be automatically detected and included in the output CSS.

3. **For production builds** (minified CSS):
   ```bash
   npm run build-css-prod
   ```

**Tailwind Configuration:**
The `tailwind.config.js` is configured to scan all HTML templates in the project:
- `./templates/**/*.html`
- `./**/templates/**/*.html`
- `./**/*.html`

This ensures all Tailwind classes used in templates are included in the final CSS.

## Environment Variables

For production, you should set:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: List of allowed hostnames
- `DATABASE_URL`: Database connection string (if using external database)

## Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Configure `ALLOWED_HOSTS` properly
- Use environment variables for sensitive data
- Implement proper file upload restrictions
- Use HTTPS in production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for educational purposes.

## Support

For issues and questions, please open an issue in the repository.

