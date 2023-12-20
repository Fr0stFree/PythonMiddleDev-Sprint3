from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_admin')
    list_filter = ('is_admin', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
