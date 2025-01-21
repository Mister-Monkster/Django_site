from django.contrib import admin

from .models import User


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('username',  'email', 'is_verificated')
    exclude = ['password',]
