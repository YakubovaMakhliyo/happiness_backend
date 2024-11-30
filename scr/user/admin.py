from django.contrib import admin

from scr.user.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'username', 'email', 'phone', 'is_active', 'is_staff', 'is_admin')
    search_fields = ('full_name', 'username', 'email', 'phone')
    ordering = ('-id',)


admin.site.register(User, UserAdmin)
