# ExpressMarket - Security and Access Control Document

## 1. Authentication System

### 1.1 User Authentication
- **Framework**: Django's built-in authentication system
- **Password Storage**: PBKDF2 hashing algorithm (Django default)
- **Session Management**: Database-backed sessions
- **Session Timeout**: Default Django session timeout (2 weeks)
- **Password Requirements**:
  - Minimum length enforced by Django
  - Password validation in forms
  - No password reuse restrictions (can be added)

### 1.2 User Registration
- **Customer Registration**: 
  - Username, email, password
  - User type: 'customer'
  - No email verification required (can be added)
  
- **Vendor Registration**:
  - Username, email, password
  - Business name, TIN (Tax Identification Number)
  - Logo upload (optional)
  - User type: 'vendor'
  - Default rating: 1 (new vendors)

### 1.3 Password Reset
- **Token Generation**: Secure, time-limited tokens
- **Token Expiration**: 24 hours
- **Email Delivery**: HTML email with reset link
- **Security**: One-time use tokens (Django default)
- **Rate Limiting**: Not implemented (can be added)

## 2. Authorization and Access Control

### 2.1 Role-Based Access Control (RBAC)

#### 2.1.1 User Types
```
User (AbstractUser)
├── Customer (user_type='customer')
│   ├── Can browse products
│   ├── Can add to cart
│   ├── Can place orders
│   ├── Can leave reviews (for purchased products)
│   └── Cannot access vendor features
│
└── Vendor (user_type='vendor')
    ├── Can create/manage store
    ├── Can create/manage products
    ├── Can create/manage categories
    ├── Can view vendor dashboard
    └── Cannot access customer cart/orders
```

### 2.2 View-Level Access Control

#### 2.2.1 Decorators Used
- `@login_required`: Requires authentication
- `@method_decorator(login_required)`: For class-based views
- Custom `vendor_required` decorator: For vendor-only views

#### 2.2.2 Access Control Matrix

| Feature | Anonymous | Customer | Vendor | Admin |
|---------|-----------|----------|--------|-------|
| Browse Products | ✅ | ✅ | ✅ | ✅ |
| View Product Details | ✅ | ✅ | ✅ | ✅ |
| Add to Cart | ❌ | ✅ | ❌ | ✅ |
| Place Order | ❌ | ✅ | ❌ | ✅ |
| View Orders | ❌ | ✅ (own) | ❌ | ✅ (all) |
| Leave Review | ❌ | ✅ (purchased) | ❌ | ✅ |
| Edit Review | ❌ | ✅ (own) | ❌ | ✅ |
| Vendor Dashboard | ❌ | ❌ | ✅ | ✅ |
| Create Store | ❌ | ❌ | ✅ | ✅ |
| Add Product | ❌ | ❌ | ✅ | ✅ |
| Manage Categories | ❌ | ❌ | ✅ | ✅ |
| Admin Panel | ❌ | ❌ | ❌ | ✅ |

### 2.3 Object-Level Permissions

#### 2.3.1 Order Access
- Customers can only view their own orders
- Vendors can view orders for their products
- Admins can view all orders

**Implementation:**
```python
# In views
order = get_object_or_404(Order, id=order_id, customer=request.user)
```

#### 2.3.2 Review Access
- Users can only edit/delete their own reviews
- Reviews can only be created for purchased products

**Implementation:**
```python
# Check purchase
has_purchased = OrderItem.objects.filter(
    order__customer=request.user,
    product=product
).exists()
```

#### 2.3.3 Product Management
- Vendors can only edit/delete their own products
- Admins can edit/delete any product

**Implementation:**
```python
# In vendor views
product = get_object_or_404(Product, id=product_id, vendor__user=request.user)
```

#### 2.3.4 Store Management
- Vendors can only manage their own store
- One store per vendor (OneToOne relationship)

## 3. Security Measures

### 3.1 Input Validation

#### 3.1.1 Form Validation
- **Client-side**: HTML5 validation (required, type, min, max)
- **Server-side**: Django form validation
- **Model-level**: Field constraints (max_length, validators)

#### 3.1.2 Data Sanitization
- **XSS Prevention**: Django template auto-escaping
- **SQL Injection**: Django ORM (parameterized queries)
- **File Uploads**: 
  - File type validation (images only)
  - File size limits (can be configured)
  - Secure file storage paths

### 3.2 CSRF Protection
- **Middleware**: Django CSRF middleware enabled
- **Forms**: CSRF tokens in all POST forms
- **AJAX**: CSRF token in headers (if using AJAX)

### 3.3 Session Security
- **Session Cookie**: HttpOnly, Secure (in production)
- **Session Storage**: Database-backed
- **Session Fixation**: Django handles automatically
- **Session Timeout**: Configurable via settings

### 3.4 Password Security
- **Hashing**: PBKDF2 with SHA256
- **Salt**: Automatic per-user salt
- **Minimum Length**: Enforced by Django
- **Password Reset**: Secure token-based

### 3.5 File Upload Security
- **Allowed Types**: Images only (JPEG, PNG, GIF)
- **Storage Path**: Media directory with unique filenames
- **File Size**: No explicit limit (can be added)
- **Virus Scanning**: Not implemented (can be added)

### 3.6 Email Security
- **SMTP**: TLS encryption (EMAIL_USE_TLS=True)
- **Credentials**: Stored in environment variables (.env)
- **Email Content**: HTML sanitization via Django templates

## 4. Data Protection

### 4.1 Sensitive Data
- **Passwords**: Hashed, never stored in plain text
- **Email Addresses**: Stored but not publicly displayed
- **Payment Information**: Not stored (no payment integration)
- **Personal Information**: 
  - Shipping addresses stored in orders
  - Accessible only to order owner and admins

### 4.2 Data Encryption
- **At Rest**: Database encryption (PostgreSQL supports)
- **In Transit**: HTTPS (required in production)
- **Passwords**: Hashed with PBKDF2

### 4.3 Data Access Logging
- **Django Admin**: Built-in logging
- **Application Logs**: Python logging module
- **Error Tracking**: Django error logging
- **Audit Trail**: Not implemented (can be added)

## 5. Security Headers (Production)

### 5.1 Recommended Headers
```python
# In settings.py (production)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 5.2 Content Security Policy
- Not implemented (can be added via middleware)

## 6. Access Control Implementation

### 6.1 View Decorators
```python
# Login required
@login_required
def my_view(request):
    pass

# Vendor required
def vendor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_vendor:
            messages.error(request, 'Vendor access required')
            return redirect('core_ecommerce:home')
        return view_func(request, *args, **kwargs)
    return wrapper
```

### 6.2 Template-Level Access Control
```django
{% if user.is_authenticated %}
    {% if user.is_vendor %}
        <!-- Vendor content -->
    {% else %}
        <!-- Customer content -->
    {% endif %}
{% else %}
    <!-- Anonymous content -->
{% endif %}
```

### 6.3 URL Protection
- All sensitive URLs require authentication
- Vendor URLs check `is_vendor` property
- Order URLs filter by `customer=request.user`

## 7. Security Best Practices

### 7.1 Implemented
✅ Password hashing
✅ CSRF protection
✅ XSS prevention (auto-escaping)
✅ SQL injection prevention (ORM)
✅ Session security
✅ Role-based access control
✅ Input validation
✅ Secure file uploads

### 7.2 Recommended for Production
⚠️ HTTPS enforcement
⚠️ Rate limiting
⚠️ Email verification
⚠️ Two-factor authentication (2FA)
⚠️ Password complexity requirements
⚠️ Account lockout after failed attempts
⚠️ Security headers
⚠️ Content Security Policy
⚠️ Regular security audits
⚠️ Dependency updates
⚠️ Database backups
⚠️ Error logging and monitoring

## 8. Vulnerability Mitigation

### 8.1 Common Vulnerabilities Addressed

1. **SQL Injection**: Prevented by Django ORM
2. **XSS (Cross-Site Scripting)**: Prevented by template auto-escaping
3. **CSRF (Cross-Site Request Forgery)**: Prevented by CSRF tokens
4. **Session Hijacking**: Mitigated by secure session cookies
5. **Password Attacks**: Mitigated by password hashing
6. **File Upload Attacks**: Mitigated by file type validation
7. **Privilege Escalation**: Prevented by role-based access control

### 8.2 Security Testing
- Manual testing of access control
- Form validation testing
- Session management testing
- Password reset flow testing
- File upload security testing

## 9. Compliance Considerations

### 9.1 Data Privacy
- User data collection: Username, email, shipping addresses
- Data storage: Database with access controls
- Data retention: Indefinite (can be configured)
- User rights: Users can delete accounts (via admin)

### 9.2 GDPR Considerations (Future)
- User consent for data collection
- Right to access personal data
- Right to deletion
- Data portability
- Privacy policy page

