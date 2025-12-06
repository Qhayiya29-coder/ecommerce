# ExpressMarket - Error Handling and Failure Recovery

## 1. Error Handling Strategy

### 1.1 Error Categories

#### 1.1.1 User Input Errors
- **Form Validation Errors**: Invalid data submission
- **Missing Required Fields**: Required fields not filled
- **Invalid Data Types**: Wrong data format (e.g., non-numeric in number field)
- **File Upload Errors**: Invalid file types, oversized files

#### 1.1.2 Authentication/Authorization Errors
- **Unauthenticated Access**: User not logged in
- **Unauthorized Access**: User lacks required permissions
- **Session Expired**: Session timeout
- **Invalid Credentials**: Wrong username/password

#### 1.1.3 Business Logic Errors
- **Cart Empty**: Attempting checkout with empty cart
- **Product Out of Stock**: Product unavailable (if implemented)
- **Duplicate Review**: Attempting to review same product twice
- **Invalid Order Status**: Invalid status transition

#### 1.1.4 System Errors
- **Database Errors**: Connection failures, query errors
- **File System Errors**: Media file access failures
- **Email Errors**: SMTP failures, email delivery issues
- **External Service Errors**: Third-party API failures

## 2. Error Handling Implementation

### 2.1 Form Validation Errors

#### 2.1.1 Client-Side Validation
```html
<!-- HTML5 validation -->
<input type="email" required minlength="3" maxlength="100">
```

#### 2.1.2 Server-Side Validation
```python
# Django form validation
if form.is_valid():
    # Process form
else:
    # Display errors
    for field, errors in form.errors.items():
        messages.error(request, f"{field}: {errors}")
```

#### 2.1.3 Error Display
- **Template**: Error messages displayed near form fields
- **Styling**: Red text, error icons
- **User Feedback**: Clear error descriptions

### 2.2 Authentication Errors

#### 2.2.1 Unauthenticated Access
```python
@login_required
def protected_view(request):
    # View logic
    pass
```

**Error Handling:**
- Redirect to login page
- Store intended URL for redirect after login
- Display message: "Please log in to access this page"

#### 2.2.2 Invalid Credentials
```python
# In login view
if form.is_valid():
    user = form.get_user()
    if user is not None:
        login(request, user)
    else:
        messages.error(request, "Invalid username or password")
```

### 2.3 Authorization Errors

#### 2.3.1 Vendor-Only Access
```python
def vendor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_vendor:
            messages.error(request, 'Vendor access required')
            return redirect('core_ecommerce:home')
        return view_func(request, *args, **kwargs)
    return wrapper
```

#### 2.3.2 Object Ownership
```python
# Check ownership before allowing edit/delete
order = get_object_or_404(Order, id=order_id, customer=request.user)
if order.customer != request.user:
    messages.error(request, 'You can only edit your own orders')
    return redirect('core_ecommerce:my_orders')
```

### 2.4 Business Logic Errors

#### 2.4.1 Empty Cart Checkout
```python
def post(self, request):
    cart_items, total = get_cart_items(request)
    if not cart_items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('core_ecommerce:cart')
    # Continue checkout
```

#### 2.4.2 Duplicate Review Prevention
```python
existing_review = ProductReview.objects.filter(
    product=product, 
    user=request.user
).first()
if existing_review:
    messages.info(request, 'You have already reviewed this product.')
    return redirect('product:product_detail', slug=product.slug)
```

### 2.5 Database Errors

#### 2.5.1 Transaction Management
```python
from django.db import transaction

@transaction.atomic
def create_order(request):
    try:
        order = Order.objects.create(...)
        # Create order items
        for item in cart_items:
            OrderItem.objects.create(...)
        return order
    except Exception as e:
        # Rollback transaction
        logger.error(f"Order creation failed: {str(e)}")
        messages.error(request, 'Order creation failed. Please try again.')
        return redirect('core_ecommerce:cart')
```

#### 2.5.2 Database Connection Errors
- **Handling**: Django automatically retries connections
- **Logging**: Database errors logged to Django error log
- **User Feedback**: Generic error message (don't expose DB details)

### 2.6 File Upload Errors

#### 2.6.1 File Validation
```python
def clean_image(self):
    image = self.cleaned_data.get('image')
    if image:
        # Check file size (e.g., 5MB limit)
        if image.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Image file too large (max 5MB)')
        # Check file type
        if not image.content_type.startswith('image/'):
            raise forms.ValidationError('File must be an image')
    return image
```

#### 2.6.2 File System Errors
```python
try:
    product.image.save(filename, file)
except IOError as e:
    logger.error(f"File upload failed: {str(e)}")
    messages.error(request, 'Failed to upload image. Please try again.')
```

### 2.7 Email Errors

#### 2.7.1 Email Sending Failures
```python
try:
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[email],
        fail_silently=False,  # Raise exception on failure
    )
except Exception as e:
    logger.error(f"Email sending failed: {str(e)}")
    # Don't break order creation if email fails
    # Order is still created, just email not sent
```

#### 2.7.2 Email Template Errors
- **Handling**: Template errors caught and logged
- **Fallback**: Plain text email if HTML fails
- **User Impact**: Order still created, email may be delayed

## 3. Error Messages and User Feedback

### 3.1 Message Types

#### 3.1.1 Success Messages
```python
messages.success(request, 'Order placed successfully!')
```
- **Display**: Green background, checkmark icon
- **Location**: Top of page
- **Duration**: Auto-dismiss after 5 seconds

#### 3.1.2 Error Messages
```python
messages.error(request, 'Invalid input. Please check your form.')
```
- **Display**: Red background, error icon
- **Location**: Top of page or near form
- **Duration**: Until user dismisses or page reload

#### 3.1.3 Warning Messages
```python
messages.warning(request, 'Your cart is empty.')
```
- **Display**: Yellow background, warning icon
- **Location**: Top of page
- **Duration**: Auto-dismiss after 5 seconds

#### 3.1.4 Info Messages
```python
messages.info(request, 'You have already reviewed this product.')
```
- **Display**: Blue background, info icon
- **Location**: Top of page
- **Duration**: Auto-dismiss after 5 seconds

### 3.2 Error Message Best Practices
- **Clear and Specific**: Tell user exactly what went wrong
- **Actionable**: Suggest what user can do to fix it
- **Non-Technical**: Avoid exposing system internals
- **Consistent**: Use same language and tone throughout

## 4. Exception Handling

### 4.1 Global Exception Handling

#### 4.1.1 404 Not Found
```python
# Django automatically handles 404s
# Custom 404 page can be created: templates/404.html
```

#### 4.1.2 500 Internal Server Error
```python
# Django automatically handles 500s
# Custom 500 page can be created: templates/500.html
# Errors logged to Django error log
```

#### 4.1.3 403 Forbidden
```python
# Django automatically handles 403s
# Custom 403 page can be created: templates/403.html
```

### 4.2 Custom Exception Handling

#### 4.2.1 Custom Exceptions
```python
class InsufficientStockError(Exception):
    pass

class DuplicateReviewError(Exception):
    pass
```

#### 4.2.2 Exception Handling in Views
```python
try:
    # Business logic
    process_order()
except InsufficientStockError as e:
    messages.error(request, str(e))
    return redirect('core_ecommerce:cart')
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}", exc_info=True)
    messages.error(request, 'An unexpected error occurred. Please try again.')
    return redirect('core_ecommerce:home')
```

## 5. Logging and Monitoring

### 5.1 Logging Configuration

#### 5.1.1 Log Levels
- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failures
- **CRITICAL**: Critical errors requiring immediate attention

#### 5.1.2 Logging Implementation
```python
import logging

logger = logging.getLogger(__name__)

# In views/signals
logger.info(f'Order {order.order_number} created successfully')
logger.warning(f'Order {order.order_number} has no items')
logger.error(f'Failed to send email: {str(e)}', exc_info=True)
```

### 5.2 What to Log

#### 5.2.1 User Actions
- Login/logout events
- Order creation
- Product creation/editing
- Review submission

#### 5.2.2 System Events
- Email sending (success/failure)
- File uploads
- Database operations (errors only)
- External API calls

#### 5.2.3 Errors
- All exceptions with stack traces
- Validation failures
- Authentication failures
- Authorization failures

## 6. Failure Recovery Strategies

### 6.1 Database Failures

#### 6.1.1 Connection Loss
- **Automatic**: Django connection pool handles reconnection
- **Manual**: Retry logic for critical operations
- **Fallback**: Queue operations for later processing

#### 6.1.2 Transaction Failures
```python
@transaction.atomic
def critical_operation():
    try:
        # Multiple database operations
        create_order()
        create_order_items()
        clear_cart()
    except Exception as e:
        # Automatic rollback
        logger.error(f"Transaction failed: {str(e)}")
        raise  # Re-raise to trigger rollback
```

### 6.2 Email Service Failures

#### 6.2.1 SMTP Failures
- **Strategy**: Don't break order creation
- **Implementation**: Email sending in try-except block
- **Recovery**: Queue emails for retry (can be implemented)
- **User Impact**: Order created, email may be delayed

#### 6.2.2 Email Template Errors
- **Strategy**: Fallback to plain text
- **Implementation**: Try HTML, fallback to text
- **Recovery**: Log error, send basic email

### 6.3 File System Failures

#### 6.3.1 Media Storage Failures
- **Strategy**: Validate before saving
- **Implementation**: Check permissions, disk space
- **Recovery**: Use default image or skip image
- **User Impact**: Product created without image

### 6.4 Session Failures

#### 6.4.1 Session Expiration
- **Strategy**: Redirect to login
- **Implementation**: Django middleware handles
- **Recovery**: User logs in again
- **User Impact**: Cart may be lost (can persist to database)

#### 6.4.2 Session Data Loss
- **Strategy**: Store critical data in database
- **Implementation**: Move cart to database on login
- **Recovery**: Restore from database
- **User Impact**: Minimal if implemented

## 7. Data Integrity

### 7.1 Referential Integrity
- **Database Constraints**: Foreign keys with CASCADE
- **Application Logic**: Validate relationships before operations
- **Recovery**: Prevent orphaned records

### 7.2 Data Validation
- **Multiple Levels**: Form → Model → Database
- **Consistency Checks**: Validate data at each level
- **Recovery**: Reject invalid data, show errors

### 7.3 Backup and Recovery

#### 7.3.1 Database Backups
- **Strategy**: Regular automated backups
- **Frequency**: Daily (recommended)
- **Storage**: Off-site backup storage
- **Recovery**: Restore from latest backup

#### 7.3.2 Media File Backups
- **Strategy**: Regular file system backups
- **Frequency**: Daily (recommended)
- **Storage**: Cloud storage (AWS S3, etc.)
- **Recovery**: Restore from backup

## 8. Error Prevention

### 8.1 Input Validation
- **Client-Side**: HTML5 validation
- **Server-Side**: Django form validation
- **Database**: Field constraints

### 8.2 Business Rule Enforcement
- **Cart Validation**: Check cart not empty before checkout
- **Review Validation**: Check purchase before review
- **Order Validation**: Validate order status transitions

### 8.3 System Health Checks
- **Database**: Connection health checks
- **Email Service**: SMTP connectivity checks
- **File System**: Disk space monitoring
- **Application**: Regular health check endpoints

## 9. Disaster Recovery Plan

### 9.1 Recovery Objectives
- **RTO (Recovery Time Objective)**: 4 hours
- **RPO (Recovery Point Objective)**: 24 hours (daily backups)

### 9.2 Recovery Procedures

#### 9.2.1 Database Recovery
1. Identify failure point
2. Restore from latest backup
3. Apply any transaction logs
4. Verify data integrity
5. Restart application

#### 9.2.2 Application Recovery
1. Identify issue
2. Check logs for errors
3. Restart application server
4. Verify functionality
5. Monitor for issues

#### 9.2.3 Media File Recovery
1. Identify missing files
2. Restore from backup
3. Verify file integrity
4. Update database references if needed

## 10. Testing Error Scenarios

### 10.1 Test Cases

#### 10.1.1 Form Validation
- Empty required fields
- Invalid data types
- Data exceeding max length
- Invalid file uploads

#### 10.1.2 Authentication
- Invalid credentials
- Expired sessions
- Unauthorized access attempts

#### 10.1.3 Business Logic
- Empty cart checkout
- Duplicate reviews
- Invalid order operations

#### 10.1.4 System Failures
- Database connection loss
- Email service failures
- File system errors

### 10.2 Error Testing Tools
- Manual testing
- Django test framework
- Error injection
- Load testing

