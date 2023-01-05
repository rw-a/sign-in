from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone


class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    emergency_contact = models.CharField(max_length=10, validators=[MinLengthValidator(10)],
                                         help_text="Phone number should be of a friend/relative, "
                                                   "rather than the person themself.")
    media_permission = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"

    def __str__(self):
        return self.name


class Signin(models.Model):
    is_signin = models.BooleanField(choices=[(True, "Sign in"), (False, "Sign out")], verbose_name="Sign in/out")
    date = models.DateTimeField(default=timezone.now)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Sign in/out"

    def __str__(self):
        print(self.is_signin)
        return f"{self.is_signin} {self.person}"
