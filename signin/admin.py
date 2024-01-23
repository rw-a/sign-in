from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Person, Session, Signin


@admin.register(Session)
class SessionAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'code', 'sign_in_time', 'sign_out_time', 'end_time')


@admin.register(Person)
class PersonAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'emergency_contact_name', 'emergency_contact_phone_number',
                    'media_permission', 'person_sessions', 'hidden', 'pk')
    date_hierarchy = "date_added"
    actions = ('allow_media_permission', 'disallow_media_permission', 'hide', 'unhide')
    list_filter = ("hidden", "media_permission")

    @admin.display
    def person_sessions(self, obj: Person):
        return [session for session in obj.sessions.all()]

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
    list_display = ('person', 'session', 'is_signin', 'date')
    date_hierarchy = "date"
    list_filter = ('is_signin', 'session')


admin.site.site_header = "Sign In/Out System"
admin.site.site_title = "Sign In/Out"
