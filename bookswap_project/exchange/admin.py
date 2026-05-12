from django.contrib import admin
from .models import BookExchange, Rating, Message


@admin.register(BookExchange)
class BookExchangeAdmin(admin.ModelAdmin):
    list_display = ('requester', 'offered_book', 'requested_book', 'status', 'is_completed', 'created_at')
    list_filter = ('status', 'is_completed')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('giver', 'receiver', 'score', 'exchange', 'created_at')
    list_filter = ('score',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'exchange', 'created_at', 'is_read')
    list_filter = ('is_read',)