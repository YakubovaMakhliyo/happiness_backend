from django.contrib.postgres.fields import ArrayField
from django.db.models import *

from scr.user.models import User


class Image(Model):
    image = ImageField(upload_to='restaurant/', blank=True, null=True)
    restaurant = ForeignKey('Restaurant', CASCADE, related_name='restaurant_images')

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        db_table = 'restaurant_image'

    def __str__(self):
        return f"{self.image} {self.restaurant}"


class Restaurant(Model):
    class StatusChoices(TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    description = TextField(null=True, blank=True)
    phone = CharField(max_length=255, unique=True)
    size_people = IntegerField(null=True, blank=True)
    license_image = ImageField(upload_to='restaurant/license', blank=True, null=True)
    address = ForeignKey('Address', CASCADE, related_name='restaurant')
    user = ForeignKey(User, CASCADE, related_name='restaurant')
    status = CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    services = ManyToManyField('Service', through='ServiceRestaurant')

    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'
        db_table = 'restaurant'

    def __str__(self):
        try:
            services = ', '.join(str(service) for service in self.services.all())
        except Exception as e:
            services = ""

        try:
            times = ', '.join(str(time) for time in self.time.all())
        except Exception as e:
            times = ""

        try:
            user_full_name = self.user.full_name
        except Exception as e:
            user_full_name = ""

        return (f"Restaurant: {self.name}, Address: {self.address}, Phone: {self.phone}, Size: {self.size_people},"
                f" Price: {self.price}, Status: {self.status}, User: {user_full_name}, Services: {services}, Times: {times}")


class Service(Model):
    name = CharField(max_length=255)
    image = ImageField(upload_to='service/', blank=True, null=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        db_table = 'service'

    def __str__(self):
        return f"{self.name} {self.image}"


class ServiceRestaurant(Model):
    service = ForeignKey('Service', CASCADE, related_name='restaurant_service')
    restaurant = ForeignKey('Restaurant', CASCADE, related_name='service_restaurant')

    class Meta:
        verbose_name = 'Service Restaurant'
        verbose_name_plural = 'Services Restaurant'
        db_table = 'restaurant_service'

    def __str__(self):
        f"{self.service} {self.restaurant}"
