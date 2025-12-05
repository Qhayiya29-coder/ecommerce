from django.db import models
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.utils.text import slugify



class Vendor(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    logo  = models.ImageField(upload_to = 'vendor/logs/')
    business_name = models.CharField(max_length = 100,null = False,blank = False)
    tin = models.CharField(max_length = 100,null = False,blank = False)
    rating = models.IntegerField(validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ])
    join_date = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.user.username






class Store(models.Model):
    """Vendor / Store model for multi-vendor e-commerce."""

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="store"
    )

    store_name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)


    address = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)

    rating = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.store_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.store_name
