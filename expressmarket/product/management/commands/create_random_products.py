from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import SimpleUploadedFile
from product.models import Product, Category
from vendor.models import Vendor
from accounts.models import User
import random
import string
from decimal import Decimal


class Command(BaseCommand):
    help = 'Creates 100 random products with random data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Number of products to create (default: 100)',
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Ensure we have categories
        categories = self._ensure_categories()
        
        # Ensure we have vendors
        vendors = self._ensure_vendors()
        
        if not categories:
            self.stdout.write(self.style.ERROR('No categories available. Please create categories first.'))
            return
        
        if not vendors:
            self.stdout.write(self.style.ERROR('No vendors available. Please create vendors first.'))
            return
        
        # Product name templates
        product_names = [
            'Premium', 'Deluxe', 'Standard', 'Professional', 'Advanced',
            'Classic', 'Modern', 'Elegant', 'Stylish', 'Luxury',
            'Smart', 'Digital', 'Wireless', 'Portable', 'Compact'
        ]
        
        product_types = [
            'Laptop', 'Smartphone', 'Headphones', 'Watch', 'Camera',
            'Tablet', 'Speaker', 'Keyboard', 'Mouse', 'Monitor',
            'Charger', 'Cable', 'Case', 'Stand', 'Bag',
            'Shirt', 'Pants', 'Shoes', 'Jacket', 'Hat',
            'Book', 'Pen', 'Notebook', 'Desk', 'Chair'
        ]
        
        descriptions = [
            'High quality product with excellent features.',
            'Perfect for everyday use with modern design.',
            'Durable and reliable product built to last.',
            'Stylish and functional design for modern lifestyle.',
            'Premium quality with outstanding performance.',
            'Innovative design meets practical functionality.',
            'Comfortable and ergonomic design for long-term use.',
            'Elegant and sophisticated product for discerning customers.',
        ]
        
        created_count = 0
        
        for i in range(count):
            # Generate random product name
            name = f"{random.choice(product_names)} {random.choice(product_types)} {i+1}"
            
            # Generate random description
            description = random.choice(descriptions)
            if random.choice([True, False]):
                description += f" Features include {random.choice(['wireless connectivity', 'long battery life', 'premium materials', 'advanced technology', 'eco-friendly design'])}."
            
            # Generate random price between 10.00 and 9999.99
            price = Decimal(str(random.uniform(10.00, 9999.99))).quantize(Decimal('0.01'))
            
            # Random category and vendor
            category = random.choice(categories)
            vendor = random.choice(vendors)
            
            # Create a simple dummy image
            # Create a minimal 1x1 pixel PNG image
            image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82'
            image_file = SimpleUploadedFile(
                name=f"product_{i+1}.png",
                content=image_content,
                content_type='image/png'
            )
            
            try:
                product = Product.objects.create(
                    name=name,
                    description=description,
                    price=price,
                    image=image_file,
                    category=category,
                    vendor=vendor
                )
                created_count += 1
                if (i + 1) % 10 == 0:
                    self.stdout.write(f'Created {i + 1}/{count} products...')
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'Failed to create product {i+1}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} products!')
        )

    def _ensure_categories(self):
        """Ensure we have at least some categories, create default ones if needed"""
        categories = list(Category.objects.all())
        
        if not categories:
            self.stdout.write('No categories found. Creating default categories...')
            default_categories = [
                'Electronics',
                'Clothing',
                'Home & Garden',
                'Books',
                'Sports & Outdoors',
                'Toys & Games',
                'Health & Beauty',
                'Automotive',
                'Food & Beverages',
                'Office Supplies'
            ]
            
            for cat_name in default_categories:
                Category.objects.get_or_create(name=cat_name)
            
            categories = list(Category.objects.all())
            self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} categories.'))
        
        return categories

    def _ensure_vendors(self):
        """Ensure we have at least one vendor, create a test vendor if needed"""
        vendors = list(Vendor.objects.all())
        
        if not vendors:
            self.stdout.write('No vendors found. Creating a test vendor...')
            
            # Create a test user for the vendor
            username = 'test_vendor'
            email = 'test_vendor@example.com'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'user_type': 'vendor'
                }
            )
            
            if created:
                user.set_password('testpass123')
                user.save()
            
            # Create vendor with a dummy logo
            logo_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82'
            logo_file = SimpleUploadedFile(
                name='vendor_logo.png',
                content=logo_content,
                content_type='image/png'
            )
            
            vendor, created = Vendor.objects.get_or_create(
                user=user,
                defaults={
                    'business_name': 'Test Vendor Store',
                    'tin': 'TEST123456',
                    'rating': 4,
                    'logo': logo_file
                }
            )
            
            vendors = [vendor]
            self.stdout.write(self.style.SUCCESS('Created test vendor.'))
        
        return vendors

