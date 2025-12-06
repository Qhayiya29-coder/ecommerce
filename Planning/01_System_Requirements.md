# ExpressMarket - System Requirements Document

## 1. System Overview

ExpressMarket is a multi-vendor e-commerce platform that enables vendors to create stores, manage products, and sell to customers. The system facilitates the complete e-commerce lifecycle from product listing to order fulfillment.

## 2. User Types and Requirements

### 2.1 Customers (Buyers)

**Primary Goals:**
- Browse and search for products
- Purchase products from multiple vendors
- Manage orders and track order status
- Leave reviews for purchased products

**Key Requirements:**
1. **User Registration & Authentication**
   - Register as a customer with email and password
   - Login/logout functionality
   - Password reset via email (24-hour token expiration)
   - Session management

2. **Product Discovery**
   - Browse products on homepage
   - Search products by name/keywords
   - Filter products by category
   - View product details (images, descriptions, prices, vendor info)
   - View product ratings and reviews

3. **Shopping Cart Management**
   - Add products to cart with quantity selection
   - View cart contents
   - Update item quantities
   - Remove items from cart
   - Clear entire cart

4. **Checkout & Order Management**
   - Complete checkout with shipping information
   - View order confirmation
   - View order history
   - View individual order details
   - Filter orders by status (pending, processing, shipped, delivered, cancelled)
   - Receive order confirmation emails

5. **Product Reviews**
   - Leave reviews for purchased products (rating 1-5 stars + comment)
   - Edit own reviews
   - Delete own reviews
   - View all reviews for a product
   - See average product ratings

**Access Restrictions:**
- Cannot access vendor dashboard
- Cannot create/edit products
- Cannot create categories
- Can only review products they have purchased

### 2.2 Vendors (Sellers)

**Primary Goals:**
- Create and manage a store
- Add and manage products
- Track sales and orders
- Manage inventory

**Key Requirements:**
1. **Vendor Registration**
   - Register as vendor with business information
   - Provide business name, TIN (Tax Identification Number)
   - Upload business logo (optional)
   - Account verification status

2. **Store Management**
   - Create store with name, description
   - Set store location (address, city, region)
   - Store approval status
   - Store activation/deactivation

3. **Product Management**
   - Add products (name, description, price, image, category)
   - Edit existing products
   - Delete products
   - View all products in store
   - Product categorization

4. **Category Management**
   - Create product categories
   - Edit categories
   - Delete categories (only if no products assigned)
   - View all categories

5. **Dashboard & Analytics**
   - View total products count
   - View total orders received
   - View total sales revenue
   - View recent orders
   - View recent products

**Access Restrictions:**
- Cannot access customer shopping cart
- Cannot place orders as customer
- Cannot leave product reviews
- Cannot access other vendors' dashboards

### 2.3 Administrators

**Primary Goals:**
- Manage all users (customers and vendors)
- Manage all orders
- Monitor system activity
- Approve/reject vendor stores

**Key Requirements:**
1. **User Management**
   - View all users
   - Activate/deactivate user accounts
   - Verify vendor accounts
   - Manage user permissions

2. **Order Management**
   - View all orders across all vendors
   - Update order status
   - Cancel orders
   - View order analytics

3. **Product & Category Management**
   - View all products
   - Edit/delete any product
   - Manage categories globally
   - Moderate reviews

4. **Store Management**
   - Approve/reject vendor stores
   - Activate/deactivate stores
   - View store analytics

**Access:**
- Full access via Django Admin panel
- All CRUD operations on all models

### 2.4 Anonymous Users (Guests)

**Primary Goals:**
- Browse products
- View product details
- Search products

**Key Requirements:**
1. **Product Browsing**
   - View homepage with products
   - Search products
   - Filter by category
   - View product details

**Access Restrictions:**
- Cannot add to cart
- Cannot place orders
- Cannot leave reviews
- Must register/login to purchase

## 3. Functional Requirements

### 3.1 Authentication & Authorization
- User registration with type selection (Customer/Vendor)
- Secure password hashing (Django's PBKDF2)
- Session-based authentication
- Role-based access control (RBAC)
- Password reset with secure tokens
- Email verification (planned)

### 3.2 Product Management
- Product CRUD operations
- Image upload and storage
- Category assignment
- Product search and filtering
- Product pagination
- Related products display

### 3.3 Shopping Cart
- Session-based cart storage
- Add/update/remove items
- Quantity management
- Cart persistence across sessions (for logged-in users)
- Cart count display in navigation

### 3.4 Order Processing
- Order creation from cart
- Order number generation (unique, random)
- Order status tracking
- Order history for customers
- Order management for vendors
- Email notifications (order confirmation)

### 3.5 Review System
- Review submission (only for purchased products)
- Rating system (1-5 stars)
- Review editing/deletion (own reviews only)
- Average rating calculation
- Review pagination

### 3.6 Email System
- Order confirmation emails (HTML)
- Password reset emails (HTML)
- Email template rendering
- SMTP configuration support

## 4. Non-Functional Requirements

### 4.1 Performance
- Page load time < 2 seconds
- Database query optimization (select_related, prefetch_related)
- Image optimization and caching
- Pagination for large datasets

### 4.2 Security
- SQL injection prevention (Django ORM)
- XSS prevention (template auto-escaping)
- CSRF protection (Django middleware)
- Secure password storage
- Session security
- File upload validation
- Input validation and sanitization

### 4.3 Usability
- Responsive design (mobile-friendly)
- Intuitive navigation
- Clear error messages
- User feedback (success/error messages)
- Accessible UI (WCAG guidelines)

### 4.4 Scalability
- Database indexing on frequently queried fields
- Media file storage (local/cloud-ready)
- Session storage optimization
- Code modularity for easy extension

### 4.5 Reliability
- Error handling and logging
- Transaction management for critical operations
- Data validation at multiple levels
- Backup and recovery procedures

## 5. System Constraints

### 5.1 Technical Constraints
- Django 6.0 framework
- Python 3.12
- PostgreSQL database (production)
- SQLite database (development)
- Tailwind CSS for styling

### 5.2 Business Constraints
- Single currency (USD)
- Single country focus (Ethiopia - default)
- No payment gateway integration (manual payment)
- No inventory tracking (assumed unlimited stock)

## 6. Future Enhancements

1. **Payment Integration**
   - Payment gateway integration
   - Multiple payment methods
   - Payment status tracking

2. **Inventory Management**
   - Stock tracking
   - Low stock alerts
   - Out-of-stock handling

3. **Advanced Features**
   - Wishlist functionality
   - Product recommendations
   - Vendor analytics dashboard
   - Multi-currency support
   - Multi-language support
   - Mobile app (iOS/Android)

4. **Communication**
   - Vendor-customer messaging
   - Order status notifications (SMS/Email)
   - Newsletter subscriptions

5. **Marketing**
   - Discount codes/coupons
   - Promotional campaigns
   - Featured products
   - Vendor promotions

