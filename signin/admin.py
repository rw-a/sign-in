from django.contrib import admin
from .models import Person, Signin


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'emergency_contact', 'media_permission', 'pk')
    date_hierarchy = "date_added"
    ordering = ("name",)


@admin.register(Signin)
class SigninAdmin(admin.ModelAdmin):
    list_display = ('person', 'is_signin', 'date')
    date_hierarchy = "date"
    ordering = ("date",)
