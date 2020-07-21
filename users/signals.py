from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from django.contrib.auth.models import User

# Post save signal


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance,
                                   user_bio='This is the default bio')
    instance.profile.save()
