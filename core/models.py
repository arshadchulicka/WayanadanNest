from django.db import models



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class CompanyInfo(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    address = models.TextField()

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    state = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    phone = models.CharField(max_length=20)
    email = models.EmailField()

    google_map_embed = models.TextField(
        blank=True,
        null=True,
        help_text="Paste Google Maps iframe embed code"
    )

    def __str__(self):
        return self.name or "Company Info"



class Carousel(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)

    image = models.ImageField(upload_to='carousel/')
    
    discount_percentage = models.PositiveIntegerField(default=10)

    button_text = models.CharField(max_length=50, default='Book Now')
    button_link = models.CharField(max_length=200, default='/resorts/')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

