"""
Django shell script to test email configuration and verify SMTP credentials
Run this directly: python test_email.py
Or in Django shell: python manage.py shell < test_email.py
"""

import os
import sys
import django
import smtplib
from email.mime.text import MIMEText

# Setup Django - Add the expressmarket directory to Python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXPRESSMARKET_DIR = os.path.join(BASE_DIR, 'expressmarket')
sys.path.insert(0, EXPRESSMARKET_DIR)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expressmarket.settings')

# Configure Django
django.setup()

from django.core.mail import send_mail, send_mass_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from core_ecommerce.models import Order, OrderItem

print("=" * 60)
print("Testing Email Configuration & Credentials")
print("=" * 60)

# Try to get a real order from database
test_order = None
test_email = 'aleludago@gmail.com'  # Fallback email

try:
    test_order = Order.objects.select_related('customer').prefetch_related('items__product').first()
    if test_order:
        test_email = test_order.email
        print(f"\n📦 Found order in database: {test_order.order_number}")
        print(f"   Using order email: {test_email}")
    else:
        print(f"\n⚠ No orders found in database. Using fallback email: {test_email}")
except Exception as e:
    print(f"\n⚠ Could not fetch order from database: {str(e)}")
    print(f"   Using fallback email: {test_email}")

# Check email settings
print("\n1. Checking Email Settings:")
print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"   EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Not set')}")
print(f"   EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'Not set')}")
print(f"   EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Not set')}")
print(f"   EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'Not set')}")
email_password = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
password_display = '***' + email_password[-4:] if email_password and len(email_password) > 4 else 'Not set'
print(f"   EMAIL_HOST_PASSWORD: {password_display}")
print(f"   DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not set')}")

# Test SMTP Connection and Credentials
print("\n2. Testing SMTP Connection & Credentials...")
print("   Attempting to connect to Gmail SMTP server...")

try:
    email_host = getattr(settings, 'EMAIL_HOST', 'smtp.gmail.com')
    email_port = getattr(settings, 'EMAIL_PORT', 587)
    email_user = getattr(settings, 'EMAIL_HOST_USER', '')
    email_password = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
    use_tls = getattr(settings, 'EMAIL_USE_TLS', True)
    
    if not email_user or not email_password:
        print("   ✗ ERROR: EMAIL_HOST_USER or EMAIL_HOST_PASSWORD not set!")
        print("   Please check your .env file.")
        sys.exit(1)
    
    # Create SMTP connection
    print(f"   Connecting to {email_host}:{email_port}...")
    server = smtplib.SMTP(email_host, email_port, timeout=10)
    
    # Start TLS if needed
    if use_tls:
        print("   Starting TLS...")
        server.starttls()
    
    # Login with credentials
    print(f"   Attempting to authenticate as {email_user}...")
    server.login(email_user, email_password)
    
    print("   ✓ SUCCESS! SMTP credentials are CORRECT!")
    print("   ✓ Connection established and authentication successful!")
    
    # Close connection
    server.quit()
    print("\n   Proceeding to test actual email sending...\n")
    
except smtplib.SMTPAuthenticationError as e:
    print(f"   ✗ AUTHENTICATION FAILED!")
    print(f"   Error: {str(e)}")
    print("\n   Possible issues:")
    print("   - App Password is incorrect")
    print("   - 2-Step Verification is not enabled on your Google account")
    print("   - App Password was not generated correctly")
    print("   - Email address is incorrect")
    sys.exit(1)
    
except smtplib.SMTPConnectError as e:
    print(f"   ✗ CONNECTION FAILED!")
    print(f"   Error: {str(e)}")
    print("\n   Possible issues:")
    print("   - Internet connection problem")
    print("   - Firewall blocking SMTP port 587")
    print("   - Gmail SMTP server is down")
    sys.exit(1)
    
except smtplib.SMTPException as e:
    print(f"   ✗ SMTP ERROR!")
    print(f"   Error: {str(e)}")
    print("\n   This is a general SMTP error. Check your credentials and network.")
    sys.exit(1)
    
except Exception as e:
    print(f"   ✗ UNEXPECTED ERROR!")
    print(f"   Error: {str(e)}")
    print(f"   Error Type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 1: Simple text email
print("\n3. Testing Simple Text Email (Actual SMTP Send)...")
try:
    result = send_mail(
        subject='Test Email - Simple Text',
        message='This is a test email to verify email configuration is working correctly.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[test_email],
        fail_silently=False,
    )
    print(f"   ✓ Email sent successfully to {test_email}! (Result: {result})")
except Exception as e:
    print(f"   ✗ Error sending email: {str(e)}")

# Test 2: HTML email
print("\n4. Testing HTML Email (Actual SMTP Send)...")
try:
    html_content = """
    <html>
        <body>
            <h2>Test HTML Email</h2>
            <p>This is a <strong>test email</strong> with HTML content.</p>
            <p>If you can see this formatted, HTML emails are working!</p>
        </body>
    </html>
    """
    
    result = send_mail(
        subject='Test Email - HTML Content',
        message='This is the plain text version.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[test_email],
        html_message=html_content,
        fail_silently=False,
    )
    print(f"   ✓ HTML email sent successfully to {test_email}! (Result: {result})")
except Exception as e:
    print(f"   ✗ Error sending HTML email: {str(e)}")

# Test 3: Email with template (like order invoice)
print("\n5. Testing Email with Template (Order Invoice Style)...")
try:
    # Use real order if available, otherwise create mock
    if test_order:
        order = test_order
        order_items = list(order.items.all())
        print(f"   Using real order: {order.order_number} with {len(order_items)} items")
    else:
        # Fallback to mock order data
        from decimal import Decimal
        print("   No real order found, using mock order data")
        order = type('Order', (), {
            'order_number': 'TEST123456',
            'created_at': timezone.now(),
            'get_status_display': lambda: 'Pending',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': test_email,
            'phone': '123-456-7890',
            'shipping_address': '123 Test Street',
            'city': 'Test City',
            'region': 'Test Region',
            'postal_code': '12345',
            'country': 'Ethiopia',
            'subtotal': Decimal('100.00'),
            'shipping_cost': Decimal('0.00'),
            'total': Decimal('100.00'),
        })()
        
        from decimal import Decimal
        order_items = [
            type('OrderItem', (), {
                'product': type('Product', (), {'name': 'Test Product'})(),
                'quantity': 2,
                'price': Decimal('50.00'),
                'subtotal': Decimal('100.00'),
            })()
        ]
    
    context = {
        'order': order,
        'order_items': order_items,
        'site_name': getattr(settings, 'SITE_NAME', 'ExpressMarket'),
        'site_domain': getattr(settings, 'SITE_DOMAIN', 'localhost:8000'),
    }
    
    html_message = render_to_string('emails/order_invoice.html', context)
    plain_message = render_to_string('emails/order_invoice.txt', context)
    
    result = send_mail(
        subject=f'Test Order Invoice - {order.order_number}',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[test_email],
        html_message=html_message,
        fail_silently=False,
    )
    print(f"   ✓ Template email sent successfully to {test_email}! (Result: {result})")
except Exception as e:
    print(f"   ✗ Error sending template email: {str(e)}")
    import traceback
    traceback.print_exc()

# Test 4: Using EmailMessage for more control
print("\n6. Testing EmailMessage (Advanced)...")
try:
    email = EmailMessage(
        subject='Test Email - EmailMessage',
        body='This is a test using EmailMessage class for more control.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_email],
        reply_to=[test_email],
    )
    email.send()
    print(f"   ✓ EmailMessage sent successfully to {test_email}!")
except Exception as e:
    print(f"   ✗ Error sending EmailMessage: {str(e)}")

print("\n" + "=" * 60)
print("Email Testing Complete!")
print("=" * 60)
print(f"\n✓ If credentials test passed, emails should be sent to your inbox.")
print(f"  Check the recipient email inbox: {test_email}")
if test_order:
    print(f"  (Using email from order: {test_order.order_number})")
print("\n⚠ If emails are not received:")
print("  - Check spam/junk folder")
print("  - Verify EMAIL_BACKEND is set to 'django.core.mail.backends.smtp.EmailBackend'")
print("  - Ensure .env file has correct credentials")
print("  - Check Gmail account for security alerts")

