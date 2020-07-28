import random
from django.utils.text import slugify

all_strings = 'ABCDEFGHIJKLMNOPQRSTWXYZabcdefghijklmnopqrstuvwxyz1234567890'


def unique_slug_generator(instance, new_slug=None):
    class_v = instance.__class__
    if new_slug is not None:
        slug = new_slug
    else:
        text_random = random.choice(all_strings)+str(random.randint(1, 30))+random.choice(all_strings)
        try:
            last_id = class_v.objects.all().latest('id')
        except Exception as e:
            last_id = 0
        slug = 2*text_random + str(last_id.id+1) + text_random
    qs_exists = class_v.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug = slug,
            randstr = random_string_generator(size=25)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
