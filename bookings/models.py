from django.db import models
from django.contrib.auth.models import User
from resorts.models import Resort

# bookings/models.py
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE)

    check_in = models.DateField()
    check_out = models.DateField()

    room_count = models.PositiveIntegerField(default=1)
    days = models.PositiveIntegerField(default=1)

    original_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0   # ✅ IMPORTANT
    )

    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0   # ✅ IMPORTANT
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0   # ✅ IMPORTANT
    )

    status = models.CharField(
        max_length=20,
        choices=[('PENDING', 'PENDING'), ('PAID', 'PAID')],
        default='PENDING'
    )
