# A - Imports
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, CustomerDetailed

# B - Auto-create Profile when new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# C - Auto-save Profile when User is updated
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.customerdetailed_profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)

# D - Auto-fill team field in CustomerDetailed from Profile
@receiver(post_save, sender=CustomerDetailed)
def assign_team_from_profile(sender, instance, created, **kwargs):
    if created and not instance.team:
        try:
            profile = instance.created_by.customerdetailed_profile
            instance.team = profile.role
            instance.save(update_fields=["team"])
        except Profile.DoesNotExist:
            pass


