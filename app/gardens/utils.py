import random

from django.utils.text import slugify


def slugify_instance_name(instance, save=False, new_slug=None):
    """ Auto generate a slug for the instance """
    slug = new_slug if new_slug is not None else slugify(instance.name)
    inst_class = instance.__class__
    qs = inst_class.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        # autogenerate a new slug
        rand_int = random.randint(300_000, 500_000)
        slug = f"{slug}-{rand_int}"
        return slugify_instance_name(instance, save=save, new_slug=slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance