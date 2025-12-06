from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from ecommerce.models import Store, Product


class Command(BaseCommand):
    help = 'Create groups and assign permissions for Vendors and Buyers'

    def handle(self, *args, **options):
        # Get content types
        store_ct = ContentType.objects.get_for_model(Store)
        product_ct = ContentType.objects.get_for_model(Product)

        # Create Vendors group
        vendors_group, created = Group.objects.get_or_create(name='Vendors')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Vendors group'))
        else:
            self.stdout.write('Vendors group already exists')

        # Get vendor permissions
        vendor_permissions = Permission.objects.filter(
            content_type__in=[store_ct, product_ct],
            codename__in=[
                'add_store', 'change_store', 'delete_store',
                'add_product', 'change_product', 'delete_product',
                'view_store', 'view_product'
            ]
        )

        # Assign permissions to Vendors group
        vendors_group.permissions.set(vendor_permissions)
        self.stdout.write(self.style.SUCCESS(f'Assigned {vendor_permissions.count()} permissions to Vendors group'))

        # Create Buyers group
        buyers_group, created = Group.objects.get_or_create(name='Buyers')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Buyers group'))
        else:
            self.stdout.write('Buyers group already exists')

        # Buyers don't need special permissions (they use custom views)
        # But we can add view permissions if needed
        buyer_permissions = Permission.objects.filter(
            content_type__in=[store_ct, product_ct],
            codename__in=['view_store', 'view_product']
        )
        buyers_group.permissions.set(buyer_permissions)
        self.stdout.write(self.style.SUCCESS(f'Assigned {buyer_permissions.count()} permissions to Buyers group'))

        self.stdout.write(self.style.SUCCESS('\nGroups and permissions setup completed successfully!'))

