from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'owner', 'edition', 'publisher', 'page_count', 'is_public', 'created_at')
    list_filter = ('is_public', 'publisher')
    search_fields = ('title', 'author', 'owner__username')
    list_editable = ('is_public',)
