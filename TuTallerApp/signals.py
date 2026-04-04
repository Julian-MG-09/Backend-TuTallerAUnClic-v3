from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Rol


@receiver(post_migrate)
def crear_roles(sender, **kwargs):
    roles = ["cliente", "empresa", "admin"]

    for r in roles:
        Rol.objects.get_or_create(nombre=r)