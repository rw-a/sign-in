from django.contrib import admin
from .models import Person, Signin


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'emergency_contact_name', 'emergency_contact_phone_number',
                    'media_permission', 'hidden', 'pk')
    date_hierarchy = "date_added"
    actions = ('resave', 'allow_media_permission', 'disallow_media_permission', 'hide', 'unhide')

    @admin.action(description='Resave selected people (refreshes last names)')
    def resave(self, request, queryset):
        for obj in queryset:
            obj.save()

    @admin.action(description='Set selected people to give media permission')
    def allow_media_permission(self, request, queryset):
        for obj in queryset:
            obj.media_permission = True
            obj.save()

    @admin.action(description='Set selected people to revoke media permission')
    def disallow_media_permission(self, request, queryset):
        for obj in queryset:
            obj.media_permission = False
            obj.save()

    @admin.action(description='Set selected people to hidden')
    def hide(self, request, queryset):
        for obj in queryset:
            obj.hidden = True
            obj.save()

    @admin.action(description='Set selected people to not hidden')
    def unhide(self, request, queryset):
        for obj in queryset:
            obj.hidden = False
            obj.save()


@admin.register(Signin)
class SigninAdmin(admin.ModelAdmin):
    list_display = ('person', 'is_signin', 'date')
    date_hierarchy = "date"


admin.site.site_header = "Sign In/Out System"
admin.site.site_title = "Sign In/Out"
