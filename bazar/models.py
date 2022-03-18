import uuid
import os

from PIL import Image

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static


# Create your models here.
class City(models.Model):
    city = models.CharField(max_length=50)
    slug = models.SlugField(verbose_name=_("Slug"), unique=True)
    description = models.TextField(blank=True, null=True)
    metadata = models.JSONField(verbose_name=_("Metadata"), blank=True, null=True, help_text=_("Metadata about city."))

    def __str__(self):
        return self.city


class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    profile_city = models.ForeignKey(City, verbose_name=_('Preferred City'), null=True, on_delete=models.CASCADE)
    preferred_contact = models.CharField(max_length=30, null=True, verbose_name=_('Preferred Contact'))
    metadata = models.JSONField(verbose_name=_("Metadata"), blank=True, null=True,
                                help_text=_("Metadata about profile."))

    def __str__(self):
        return str(self.user)


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(verbose_name=_("Slug"), unique=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name='subcat', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="listing_avatars", null=True, blank=True, verbose_name=_("Avatar"))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            imag = Image.open(self.avatar.path)

            if imag.width > 400 or imag.height > 300:
                output_size = (400, 300)
                imag.thumbnail(output_size)
                imag.save(self.avatar.path)

    @property
    def static_slug(self):
        return os.path.join('bazar', 'pics', self.slug +'.png')


class Listing(models.Model):
    DRAFT = 'D'
    OPEN = 'O'
    CLOSED = 'C'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    ]
    PURCHASE = 'P'
    SELL = 'S'
    REQUEST = 'R'
    DONATE = 'D'
    TYPE_CHOICES = [
        (PURCHASE, _('Purchase')),
        (SELL, _('Sell')),
        (REQUEST, _('Request')),
        (DONATE, _('Donate')),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    price = models.FloatField(validators=[MinValueValidator(0.0),])
    description = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=OPEN, verbose_name=_("Status"))
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=DONATE, verbose_name=_("Type"))
    photo = models.ImageField(upload_to="listing_photos", null=True, blank=True, verbose_name=_("Photo"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    viewed = models.IntegerField(default=0)
    metadata = models.JSONField(verbose_name=_("Metadata"), blank=True, null=True,
                                help_text=_("Metadata about listing."))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url

        return "/media/listing_photos/classifieds-default.jpg"


@receiver(post_save, sender='auth.User')
def create_user_profile(**kwargs):
    created = kwargs.get("created")
    instance = kwargs.get("instance")

    if created:
        Profile.objects.create(user=instance)


# @receiver(post_save, sender='auth.User')
# def create_token(**kwargs):
#     created = kwargs.get('created')
#     instance = kwargs.get('instance')
#
#     if created:
#         Token.objects.create(user=instance)
