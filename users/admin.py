from django.contrib import admin
from .models import UserProfile, TeacherCode
from django.contrib.auth.models import User

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)

@admin.register(TeacherCode)
class TeacherCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_used')