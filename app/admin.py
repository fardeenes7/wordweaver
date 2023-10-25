from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from user.models import Profile, Activity
# Register your models here.


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class ActivityInline(admin.StackedInline):
    model = Activity
    can_delete = False
    verbose_name_plural = 'activity'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, ActivityInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_bio', 'get_image')
    list_select_related = ('profile',)
    def get_bio(self, instance):
        return instance.profile.bio
    get_bio.short_description = 'Bio'
    def get_image(self, instance):
        return instance.profile.image
    get_image.short_description = 'Image'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)