from django.db import models
from django.utils import timezone


class PersonManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(hidden=False)


class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    last_name = models.CharField(max_length=100, editable=False)
    emergency_contact_name = models.CharField(blank=True, max_length=100)
    emergency_contact_phone_number = models.CharField(blank=True, max_length=20)
    media_permission = models.BooleanField(default=False, verbose_name="Do you give media permission?")
    hidden = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)

    objects = models.Manager()
    people = PersonManager()

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"
        ordering = ['last_name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.last_name = self.name.split(" ")[-1]
        super().save(*args, **kwargs)


class Signin(models.Model):
    is_signin = models.BooleanField(choices=[(True, "Sign in"), (False, "Sign out")], verbose_name="Sign in/out")
    date = models.DateTimeField(default=timezone.now)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Sign in/out"
        ordering = ['-date']

    def __str__(self):
        return f"{self.person} - {'Sign In' if self.is_signin else 'Sign Out'}"
