from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from allauth.account.signals import user_logged_in
from django.contrib.auth import logout

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



@receiver(user_logged_in)
def check_google_login(sender, request, user, **kwargs):
    profile = user.profile

    if not profile.is_email_verified or not profile.is_admin_approved:
        logout(request)
        raise Exception("Account not approved or email not verified")
