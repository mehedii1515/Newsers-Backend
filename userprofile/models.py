from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .constants import ROLE_CHOICES

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)

@receiver(post_save, sender=User)
def set_role(sender, instance, *args, **kwargs):
    if UserProfile.objects.filter(user=instance).exists():
        return
    profile = UserProfile(user=instance, role="viewer")
    profile.save()