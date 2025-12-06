# ExpressMarket - System Architecture Document

## 1. System Overview

ExpressMarket is a multi-vendor e-commerce platform built using Django, following the Model-View-Template (MVT) architectural pattern. The system is designed to be modular, scalable, and maintainable.

## 2. Architecture Pattern

### 2.1 MVT (Model-View-Template) Pattern

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP Request
       ▼
┌─────────────────────────────────────┐
│         Django Framework            │
│  ┌──────────┐  ┌─────────────────┐ │
│  │   URLs   │→ │     Views       │ │
│  └──────────┘  └────────┬────────┘ │
│                          │          │
│                          ▼          │
│                    ┌──────────┐    │
│                    │  Models  │    │
│                    └────┬─────┘    │
│                         │          │
│                         ▼          │
│                    ┌──────────┐    │
│                    │Database  │    │
│                    └──────────┘    │
│                          │          │
│                          ▼          │
│                    ┌──────────┐    │
│                    │Templates │    │
│                    └────┬─────┘    │
└─────────────────────────┼──────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │   Browser   │
                   └─────────────┘
```

## 3. Application Structure

### 3.1 Django Apps Organization

```
expressmarket/
├── accounts/          # User authentication & registration
├── core_ecommerce/     # Main e-commerce logic (cart, checkout, orders)
├── customer/          # Customer profile management
├── product/           # Product & category management
├── vendor/            # Vendor & store management
└── expressmarket/     # Project settings & configuration
```

### 3.2 App Responsibilities

#### 3.2.1 accounts/
- **Purpose**: User authentication and registration
- **Models**: User (custom AbstractUser)
- **Views**: Login, Logout, Registration, Password Reset
- **Forms**: UserTypeForm, AuthenticationForm
- **URLs**: Authentication-related routes

#### 3.2.2 core_ecommerce/
- **Purpose**: Core shopping functionality
- **Models**: Order, OrderItem
- **Views**: Cart management, Checkout, Order history
- **Forms**: CheckoutForm
- **Signals**: Order email notifications
- **Context Processors**: Cart count

#### 3.2.3 customer/
- **Purpose**: Customer-specific data
- **Models**: Customer profile
- **Views**: Customer profile management
- **Forms**: CustomerUserCreationForm

#### 3.2.4 product/
- **Purpose**: Product and category management
- **Models**: Product, Category, ProductReview
- **Views**: Product detail, Category management, Review management
- **Forms**: CategoryForm, ReviewForm
- **URLs**: Product and category routes

#### 3.2.5 vendor/
- **Purpose**: Vendor and store management
- **Models**: Vendor, Store
- **Views**: Vendor dashboard, Store management, Product management
- **Forms**: VendorUserCreationForm, StoreForm, ProductForm
- **URLs**: Vendor-specific routes

## 4. Database Schema

### 4.1 Entity Relationship Diagram

```
User (AbstractUser)
├── user_type (customer/vendor)
├── is_verified
└── OneToOne → Customer
└── OneToOne → Vendor
    └── OneToOne → Store

Store
├── owner (FK → User)
├── store_name
├── description
└── location fields

Product
├── vendor (FK → Vendor)
├── category (FK → Category)
├── name, description, price
└── image

Category
├── name, slug
└── description

ProductReview
├── product (FK → Product)
├── user (FK → User)
├── rating, comment
└── timestamps

Order
├── customer (FK → User)
├── order_number
├── status
├── shipping info
└── totals

OrderItem
├── order (FK → Order)
├── product (FK → Product)
├── quantity, price
└── subtotal
```

### 4.2 Database Relationships

- **User → Customer**: OneToOne
- **User → Vendor**: OneToOne
- **Vendor → Store**: OneToOne
- **Vendor → Product**: OneToMany
- **Category → Product**: OneToMany
- **Product → ProductReview**: OneToMany
- **User → ProductReview**: OneToMany
- **User → Order**: OneToMany
- **Order → OrderItem**: OneToMany
- **Product → OrderItem**: OneToMany

## 5. Data Flow

### 5.1 User Registration Flow

```
User → Select User Type → Registration Form → Create User
                                              ↓
                                    Create Customer/Vendor
                                              ↓
                                    Redirect to Login
```

### 5.2 Order Creation Flow

```
Customer → Add to Cart → View Cart → Checkout Form
                                            ↓
                                    Create Order
                                            ↓
                                    Create OrderItems
                                            ↓
                                    Clear Cart
                                            ↓
                                    Send Email (Signal)
                                            ↓
                                    Order Success Page
```

### 5.3 Product Review Flow

```
Customer → Purchase Product → View Product → Write Review
                                                    ↓
                                            Check Purchase
                                                    ↓
                                            Create Review
                                                    ↓
                                            Update Product Rating
```

## 6. Technology Stack

### 6.1 Backend
- **Framework**: Django 6.0
- **Language**: Python 3.12
- **Database**: 
  - Development: SQLite
  - Production: PostgreSQL
- **ORM**: Django ORM

### 6.2 Frontend
- **Templating**: Django Templates
- **Styling**: Tailwind CSS 4.1
- **Build Tools**: PostCSS, Autoprefixer
- **JavaScript**: Vanilla JS (minimal)

### 6.3 Additional Libraries
- **Image Processing**: Pillow
- **Environment Variables**: python-decouple
- **Database Driver**: psycopg2-binary (PostgreSQL)

## 7. Security Architecture

### 7.1 Authentication Layer
- Django's authentication system
- Session-based authentication
- Password hashing (PBKDF2)

### 7.2 Authorization Layer
- Role-based access control (RBAC)
- View-level decorators
- Object-level permissions

### 7.3 Security Middleware
- CSRF protection
- XSS prevention (auto-escaping)
- SQL injection prevention (ORM)

## 8. File Structure

### 8.1 Media Files
```
media/
├── products/          # Product images
└── vendor/
    └── logs/          # Vendor logos
```

### 8.2 Static Files
```
static/
├── css/
│   └── output.css    # Compiled Tailwind CSS
└── src/
    └── input.css     # Tailwind source
```

### 8.3 Templates
```
templates/
├── base.html          # Base template
├── accounts/         # Authentication templates
├── cart/             # Cart templates
├── checkout/         # Checkout templates
├── emails/           # Email templates
├── home/             # Homepage templates
├── orders/           # Order templates
├── product/          # Product templates
└── vendor/           # Vendor templates
```

## 9. API Design (Future)

### 9.1 RESTful API Structure
```
/api/v1/
├── /auth/            # Authentication endpoints
├── /products/        # Product endpoints
├── /orders/          # Order endpoints
├── /reviews/         # Review endpoints
└── /vendor/          # Vendor endpoints
```

## 10. Deployment Architecture

### 10.1 Development Environment
```
Developer Machine
├── Django Development Server
├── SQLite Database
├── Local Media Storage
└── Console Email Backend
```

### 10.2 Production Environment (Recommended)
```
Load Balancer
    ↓
Web Server (Gunicorn/uWSGI)
    ↓
Django Application
    ↓
PostgreSQL Database
    ↓
Media Storage (S3/Cloud Storage)
    ↓
SMTP Server (Email Service)
```

## 11. Scalability Considerations

### 11.1 Database Optimization
- Indexes on frequently queried fields
- select_related() and prefetch_related() for queries
- Database connection pooling

### 11.2 Caching Strategy (Future)
- Redis for session storage
- Memcached for query caching
- CDN for static/media files

### 11.3 Horizontal Scaling
- Stateless application design
- Session storage in database/Redis
- Media files in cloud storage

## 12. Monitoring and Logging

### 12.1 Application Logging
- Python logging module
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Log rotation and archival

### 12.2 Error Tracking (Future)
- Sentry or similar error tracking
- Performance monitoring
- User activity tracking

## 13. Development Workflow

### 13.1 Version Control
- Git for source control
- Feature branches
- Commit conventions

### 13.2 Testing Strategy
- Unit tests for models
- Integration tests for views
- Manual testing for UI/UX

### 13.3 Deployment Process
1. Code review
2. Run tests
3. Database migrations
4. Static file collection
5. Server restart
6. Health checks

## 14. Future Architecture Enhancements

### 14.1 Microservices (Future)
- Separate services for:
  - User service
  - Product service
  - Order service
  - Payment service
  - Notification service

### 14.2 Message Queue (Future)
- Celery for async tasks
- Redis/RabbitMQ as message broker
- Background job processing

### 14.3 API Gateway (Future)
- REST API for mobile apps
- GraphQL API (optional)
- API rate limiting
- API authentication (JWT)

