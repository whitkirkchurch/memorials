from django.db import models

from sorl.thumbnail import ImageField
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from django.urls import reverse

from randomslugfield import RandomSlugField
from autoslug import AutoSlugField

import json


class Location(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=1024)
    description = MarkdownxField()
    slug = AutoSlugField(populate_from="name", unique=True, editable=True)

    @property
    def formatted_description(self):
        return markdownify(self.description)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("location", kwargs={"slug": self.slug})


class Tag(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=1024)
    description = MarkdownxField()
    slug = AutoSlugField(populate_from="name", unique=True, editable=True)

    @property
    def formatted_description(self):
        return markdownify(self.description)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tag", kwargs={"slug": self.slug})


class Memorial(models.Model):
    class Meta:
        ordering = ["pretty_name"]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    slug = RandomSlugField(
        length=4,
        exclude_upper=True,
        exclude_digits=True,
        exclude_vowels=True,
        help_text="A randomly generated set of letters used to uniquely identify this memorial.",
    )

    name = models.CharField(
        max_length=1024,
        help_text="If this memorial has a specific name, enter it here.",
        blank=True,
    )

    pretty_name = models.CharField(max_length=1024, editable=False)

    inscription = MarkdownxField(
        help_text="The exact text of the inscription on this memorial.", blank=True
    )

    description = MarkdownxField(
        help_text="Any additional information about this memorial (visible publicly).",
        blank=True,
    )

    notes = models.TextField(help_text="Private notes about this memorial.", blank=True)

    @property
    def formatted_inscription(self):
        return markdownify(self.inscription)

    @property
    def formatted_description(self):
        return markdownify(self.description)

    location = models.ForeignKey(
        "Location", on_delete=models.PROTECT, related_name="memorials"
    )

    location_detail = models.CharField(
        max_length=1024,
        blank=True,
        help_text="Additional information about this memorial's location, to help identify it if unclear or ambiguous.",
    )

    plot_reference = models.CharField(
        max_length=16, blank=True, help_text="This memorial's plot reference, if known"
    )

    names = models.ManyToManyField("Name", related_name="memorials")

    tags = models.ManyToManyField("Tag", related_name="memorials", blank=True)

    complete = models.BooleanField(
        help_text="Should this memorial's record be considered complete?",
    )

    published = models.BooleanField(
        help_text="Should this memorial be shown publicly?",
    )

    def save(self, *args, **kw):

        # If this is the first time we're saving this, pre-save before generating the pretty name
        if self._state.adding is False:
            self.pretty_name = self.generate_pretty_name()
        super(Memorial, self).save(*args, **kw)

    def __str__(self):
        return "{} ({})".format(self.pretty_name, self.location.name)

    def generate_pretty_name(self):
        if self.name:
            return self.name
        else:
            if self.names.all():
                return "Memorial to {}".format(self.names_on_memorial())
            else:
                return "Memorial to Unknown Person(s)"

    def names_on_memorial(self):

        if self.names.all():

            names_string = ""

            for name in self.names.all():

                if names_string != "":

                    names_string += ", "

                names_string += name.__str__()

            return names_string

        else:

            return None

    def get_absolute_url(self):
        return reverse("memorial", kwargs={"slug": self.slug})

    def get_json_url(self):
        return reverse("memorial-json", kwargs={"slug": self.slug})


class Name(models.Model):
    class Meta:
        ordering = ["family_name", "given_names"]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    slug = RandomSlugField(
        length=6,
        exclude_upper=True,
        exclude_digits=True,
        exclude_vowels=True,
        help_text="A randomly generated set of letters used to uniquely identify this person.",
    )

    import_key = models.UUIDField(
        null=True,
        editable=False,
        help_text="The UUID used to import this name record from the master import sheet, if present",
    )

    honorific = models.CharField(max_length=256, blank=True)
    given_names = models.CharField(max_length=1024)
    family_name = models.CharField(max_length=1024)

    date_of_birth = models.DateField(blank=True, null=True)

    date_of_death = models.DateField(blank=True, null=True)

    died_aged = models.IntegerField(
        help_text="If known, the age of this person when they died.",
        blank=True,
        null=True,
    )

    cwgc = models.CharField(
        verbose_name="CWGC Casualty",
        max_length=128,
        help_text="The Commonwealth War Graves Commission casualty number for this person.",
        blank=True,
    )

    service_number = models.CharField(
        verbose_name="Service Number",
        max_length=128,
        help_text="This person's service number.",
        blank=True,
    )

    wikidata = models.CharField(
        verbose_name="Wikidata ID",
        max_length=128,
        help_text="This person's Wikidata ID.",
        blank=True,
    )

    def __str__(self):
        return "{} {}".format(self.given_names, self.family_name)

    def get_absolute_url(self):
        return reverse("name", kwargs={"slug": self.slug})

    def get_json_url(self):
        return reverse("name-json", kwargs={"slug": self.slug})


class MemorialImage(models.Model):

    image = ImageField(upload_to="memorials")

    memorial = models.ForeignKey(
        "Memorial", on_delete=models.CASCADE, related_name="images"
    )

    def __str__(self):
        return "Image of {}".format(self.memorial)
