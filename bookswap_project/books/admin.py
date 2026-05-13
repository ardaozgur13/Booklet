from django.contrib import admin
from django.utils.html import format_html
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('cover_preview', 'title', 'author', 'owner', 'genre', 'edition', 'publisher', 'page_count', 'is_public', 'created_at')
    list_filter = ('is_public', 'genre', 'publisher')
    search_fields = ('title', 'author', 'owner__username')
    list_editable = ('is_public',)

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="width:36px;height:50px;object-fit:cover;border-radius:3px;">', obj.cover_image.url)
        return '—'
    cover_preview.short_description = 'Kapak'