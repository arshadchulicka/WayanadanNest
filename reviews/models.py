from django.db import models
from django.contrib.auth.models import User
from resorts.models import Resort
from bookings.models import Booking

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE,related_name='reviews')

    # ✅ Allow null temporarily for migration safety
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    rating = models.PositiveIntegerField(
        choices=[(i, f"{i} Star") for i in range(1, 6)]
    )
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'resort')

    def __str__(self):
        return f"{self.user.username} - {self.resort.name}"

