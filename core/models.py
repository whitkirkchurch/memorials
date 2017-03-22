from __future__ import unicode_literals

from django.db import models

from markitup.fields import MarkupField
import random_primary


class Location(models.Model):

    name = models.CharField(max_length=1024)
    description = models.TextField()

    def __str__(self):
        return self.name


class Memorial(random_primary.RandomPrimaryIdModel):

    name = models.CharField(
        max_length=1024,
        help_text='If this memorial has a specific name, enter it here.',
        blank=True
    )

    inscription = MarkupField(
        help_text='The exact text of the inscription on this memorial.',
        blank=True
    )

    location = models.ForeignKey(
        'Location',
        related_name='memorials'
    )

    def __str__(self):
        return '{} (at {})'.format(self.pretty_name(), self.location.name)

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


class Name(models.Model):

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
        related_name='names'
    )

    def __str__(self):
        return '{} {}'.format(self.given_names, self.family_name)
