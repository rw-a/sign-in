from django.db import models
from django.db.models.functions import Upper
from django.contrib import admin
from django.utils import timezone


class PersonManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(hidden=False)


class Person(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    emergency_contact_name = models.CharField(max_length=100, blank=True,)
    emergency_contact_phone_number = models.CharField(max_length=20, blank=True)
    media_permission = models.BooleanField(default=False, verbose_name="Do you give media permission?")
    hidden = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)

    objects = models.Manager()
    people = PersonManager()

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"
        ordering = [Upper('last_name'), Upper('first_name')]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # sort by last name, then first name, ignoring all case
    @property
    @admin.display
    def name(self):
        return f"{self.first_name} {self.last_name}"


class Signin(models.Model):
    is_signin = models.BooleanField(choices=[(True, "Sign in"), (False, "Sign out")], verbose_name="Sign in/out")
    date = models.DateTimeField(default=timezone.now)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Sign in/out"
        ordering = ['-date']

    def __str__(self):
        return f"{self.person} - {'Sign In' if self.is_signin else 'Sign Out'}"
