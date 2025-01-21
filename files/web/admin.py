from django.contrib import admin
from web.models import *


@admin.register(Posts)
class Posts(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('title', 'author', 'text')

@admin.register(Comments)
class Comments(admin.ModelAdmin):
    list_display = ('author', 'text')

@admin.register(Category)
class Category(admin.ModelAdmin):
    display = 'category'
    prepopulated_fields = {"slug": ('category',)}

@admin.register(Ban_words)
class Ban_words(admin.ModelAdmin):
    display = 'word'

