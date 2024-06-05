from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SocialUser, FriendRequest

class SocialUserAdmin(UserAdmin):
    model = SocialUser
    list_display = ('email', 'name', 'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'timestamp')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)
    
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'status', 'timestamp']
    list_filter = ['status', 'timestamp']
    search_fields = ['from_user__email', 'to_user__email']

admin.site.register(SocialUser, SocialUserAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)