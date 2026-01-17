from django.db import models
from django.conf import settings

class Resort(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    total_rooms = models.IntegerField()
    image = models.ImageField(upload_to='resorts/')
    is_active = models.BooleanField(default=True)

    def discounted_price(self):
        discount = settings.NEW_YEAR_DISCOUNT_PERCENT
        return self.price_per_night - (self.price_per_night * discount / 100)

    def __str__(self):
        return self.name
