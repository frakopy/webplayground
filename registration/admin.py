from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):

    # Display specific columns to show in the panel
    list_display = ("user", "avatar", "bio", "link")


admin.site.register(Profile, ProfileAdmin)
