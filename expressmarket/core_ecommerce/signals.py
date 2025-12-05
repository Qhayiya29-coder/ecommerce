from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Order, OrderItem


# In-memory tracking to prevent duplicate emails (simple approach)
_invoice_sent_orders = set()


@receiver(post_save, sender=OrderItem)
def send_order_invoice_on_item_created(sender, instance, created, **kwargs):
    """
    Send invoice email when an order item is created for a new order.
    This ensures all order items exist before sending the email.
    Only sends email once per order, even if multiple items are created.
    """
    if created:
        order = instance.order
        order_id = order.id
        
        # Check if we've already queued/sent invoice for this order
        if order_id in _invoice_sent_orders:
            return
        
        # Only send email for orders created recently (within last 5 minutes)
        # This prevents sending emails for old orders when items are added later
        time_diff = timezone.now() - order.created_at
        if time_diff > timedelta(minutes=5):
            return
        
        # Mark that we're processing this order
        _invoice_sent_orders.add(order_id)
        
        # Use on_commit to ensure all items in the transaction are saved
        def send_email():
            try:
                # Refresh order from DB to get latest data
                order.refresh_from_db()
                
                # Get all order items
                order_items = order.items.all()
                
                # Skip if no items (shouldn't happen, but safety check)
                if not order_items.exists():
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f'Order {order.order_number} has no items, skipping invoice email')
                    # Remove from tracking so we can retry if needed
                    _invoice_sent_orders.discard(order_id)
                    return
                
                # Prepare email context
                context = {
                    'order': order,
                    'order_items': order_items,
                    'site_name': getattr(settings, 'SITE_NAME', 'ExpressMarket'),
                    'site_domain': getattr(settings, 'SITE_DOMAIN', 'localhost:8000'),
                }
                
                # Render email template
                subject = f'Order Confirmation - {order.order_number}'
                html_message = render_to_string('emails/order_invoice.html', context)
                plain_message = render_to_string('emails/order_invoice.txt', context)
                
                # Send email
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@expressmarket.com'),
                    recipient_list=[order.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                
                import logging
                logger = logging.getLogger(__name__)
                logger.info(f'Invoice email sent successfully for order {order.order_number}')
            except Exception as e:
                # Log the error but don't break the order creation
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f'Failed to send invoice email for order {order.order_number}: {str(e)}')
                # Remove from tracking on error so we can retry if needed
                _invoice_sent_orders.discard(order_id)
        
        # Use on_commit to ensure all database operations are complete
        transaction.on_commit(send_email)

