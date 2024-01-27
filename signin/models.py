from django.db import models
from django.db.models.functions import Upper, Concat
from django.db.models import Index, UniqueConstraint
from django.contrib import admin
from django.utils import timezone
from django.core.validators import RegexValidator
from simple_history.models import HistoricalRecords


class Session(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                '[a-z0-9_]',
                message="Only lower letters, numbers and underscores are allowed."
            )
        ])

    sign_in_time = models.TimeField(
        help_text="The time when you expect people to start signing in to this session."
    )
    sign_out_time = models.TimeField(
        help_text="The time when you expect people to be signing out of this session "
                  "instead of signing in."
    )
    end_time = models.TimeField(
        help_text="The time when you expect everyone to have left, and will no longer need anyone "
                  "to sign in/out."
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class ActivePersonManager(models.Manager):
    """
    Object manager which only returns people that are not hidden
    """
    def get_queryset(self):
        return super().get_queryset().filter(hidden=False)


class Person(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")

    emergency_contact_first_name = models.CharField(max_length=100, blank=True)
    emergency_contact_last_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone_number = models.CharField(max_length=20, blank=True)

    media_permission = models.BooleanField(
        default=False,
        verbose_name="Do you give media permission?"
    )

    sessions = models.ManyToManyField(Session)

    hidden = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)

    objects = models.Manager()
    actives = ActivePersonManager()

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"

        # sort by last name, then first name, ignoring all case
        ordering = [Upper('last_name'), Upper('first_name')]

        constraints = [
            UniqueConstraint(
                Concat(Upper("last_name"), Upper("first_name")),
                name="person_name",
                # violation_error_message="Person with this name already exists."
            )
        ]

        indexes = [
            Index(Upper('last_name'), name='idx_person_last_name')
        ]

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
        """
        Ensure names are in correct case (may break names with capital in the middle,
        e.g. MacDonald)
        """
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()
        super().save(*args, **kwargs)


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
