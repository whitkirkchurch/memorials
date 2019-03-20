from django.db import models

from sorl.thumbnail import ImageField
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

import string
import random

from django.db.utils import IntegrityError
from django.db import transaction

from django.urls import reverse

from randomslugfield import RandomSlugField


class Location(models.Model):

    name = models.CharField(max_length=1024)
    description = models.TextField()

    def __str__(self):
        return self.name


class Memorial(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    slug = RandomSlugField(
        length=4,
        exclude_upper=True,
        exclude_digits=True,
        exclude_vowels=True
    )

    name = models.CharField(
        max_length=1024,
        help_text='If this memorial has a specific name, enter it here.',
        blank=True
    )

    inscription = MarkdownxField(
        help_text='The exact text of the inscription on this memorial.',
        blank=True
    )

    @property
    def formatted_inscription(self):
        return markdownify(self.inscription)

    location = models.ForeignKey(
        'Location',
        on_delete=models.PROTECT,
        related_name='memorials'
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )

    cwgc = models.CharField(
        verbose_name='CWGC Casualty',
        max_length=128,
        help_text='If known, the entry number of this casualty with the Commonwealth War Graves Commission.',
        blank=True
    )

    complete = models.BooleanField(
        help_text='Should this memorial\'s record be considered complete?',
    )

    def __str__(self):
        return '{} ({})'.format(self.pretty_name(), self.location.name)

    def pretty_name(self):
        if self.name:
            return self.name
        else:
            if self.names.all():
                return 'Memorial to {}'.format(self.names_on_memorial())
            else:
                return 'Memorial to Unknown Person(s)'

    def names_on_memorial(self):

        if self.names.all():

            names_string = ''

            for name in self.names.all():

                if names_string != '':

                    names_string += ', '

                names_string += name.__str__()

            return names_string

        else:

            return None

    def get_absolute_url(self):
        return reverse('memorial', kwargs={'slug':self.slug})


class Name(models.Model):

    honorific = models.CharField(max_length=256, blank=True)
    given_names = models.CharField(max_length=1024)
    family_name = models.CharField(max_length=1024)

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )
    date_of_death = models.DateField(
        blank=True,
        null=True
    )

    memorial = models.ForeignKey(
        'Memorial',
        on_delete=models.CASCADE,
        related_name='names'
    )

    def __str__(self):
        return '{} {}'.format(self.given_names, self.family_name)


class MemorialImage(models.Model):

    image = ImageField(
        upload_to='memorials'
    )

    memorial = models.ForeignKey(
        'Memorial',
        on_delete=models.CASCADE,
        related_name='images'
    )

    def __str__(self):
        return 'Image of {}'.format(self.memorial)
