from django.db import models
from django.db.models.functions import Upper
from django.contrib import admin
from django.utils import timezone
from django.core.exceptions import ValidationError


class Session(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    sign_in_time = models.TimeField(help_text="The time when people can start signing in to this session.")
    sign_out_time = models.TimeField(help_text="The time when people can start signing out of this session.")
    end_time = models.TimeField(help_text="The time when everyone has left, and you can no longer sign in/out.")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class PersonManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(hidden=False)


class Person(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")

    emergency_contact_first_name = models.CharField(max_length=100, blank=True)
    emergency_contact_last_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone_number = models.CharField(max_length=20, blank=True)

    media_permission = models.BooleanField(default=False, verbose_name="Do you give media permission?")

    sessions = models.ManyToManyField(Session)

    hidden = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)

    objects = models.Manager()
    people = PersonManager()

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"
        # sort by last name, then first name, ignoring all case
        ordering = [Upper('last_name'), Upper('first_name')]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    @admin.display
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    @admin.display
    def emergency_contact_name(self):
        return f"{self.emergency_contact_first_name} {self.emergency_contact_last_name}"

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if Person.objects.filter(first_name__iexact=self.first_name,
                                 last_name__iexact=self.last_name).exclude(pk=self.pk).exists():
            raise ValidationError(f"{self.first_name} {self.last_name} already exists.")


class Signin(models.Model):
    is_signin = models.BooleanField(choices=[
        (True, "Sign in"),
        (False, "Sign out")
    ], verbose_name="Sign In/Out")

    date = models.DateTimeField(default=timezone.now)

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Sign In/Out"
        ordering = ('-date',)

    def __str__(self):
        return f"{self.person} - {'Sign In' if self.is_signin else 'Sign Out'}"
