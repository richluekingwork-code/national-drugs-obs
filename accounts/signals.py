from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, MoJ_User, LDEA_User, MoH_User, MoG_User, MoYS_User

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role.startswith('moj'):
            MoJ_User.objects.create(admin=instance)
        elif instance.role.startswith('ldea'):
            LDEA_User.objects.create(admin=instance)
        elif instance.role.startswith('moh'):
            MoH_User.objects.create(admin=instance)
        elif instance.role.startswith('mog'):
            MoG_User.objects.create(admin=instance)
        elif instance.role.startswith('moys'):
            MoYS_User.objects.create(admin=instance)