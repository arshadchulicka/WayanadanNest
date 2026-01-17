
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Authentication / control
    phone = models.CharField(max_length=15, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_admin_approved = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=64, blank=True)
    # Profile details (NEW)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(
        upload_to='profiles/',
        default='profiles/default.png',
        blank=True
    )

    def __str__(self):
        return self.user.username

class OTP(models.Model):
    phone = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.phone} - {self.code}"
