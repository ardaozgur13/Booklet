from django.db import models
from django.conf import settings


class BookExchange(models.Model):
    STATUS_CHOICES = [('pending', 'Beklemede'), ('accepted', 'Kabul Edildi'), ('rejected', 'Reddedildi')]

    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_exchanges', verbose_name='Takas İsteyen')
    offered_book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='offered_in_exchanges', verbose_name='Teklif Edilen Kitap')
    requested_book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='requested_in_exchanges', verbose_name='İstenen Kitap')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Durum')
    is_completed = models.BooleanField(default=False, verbose_name='Tamamlandı')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='İstek Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    class Meta:
        verbose_name = 'Kitap Takası'
        verbose_name_plural = 'Kitap Takasları'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.requester} → {self.offered_book.title} ↔ {self.requested_book.title}'

    @property
    def owner(self):
        return self.requested_book.owner

    def requester_rated(self):
        return Rating.objects.filter(exchange=self, giver=self.requester).exists()

    def owner_rated(self):
        return Rating.objects.filter(exchange=self, giver=self.owner).exists()

class Message(models.Model):
    exchange = models.ForeignKey(BookExchange, on_delete=models.CASCADE, related_name='messages', verbose_name='Takas')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages', verbose_name='Gönderen')
    content = models.TextField(verbose_name='Mesaj')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Tarih')
    is_read = models.BooleanField(default=False, verbose_name='Okundu')

    class Meta:
        verbose_name = 'Mesaj'
        verbose_name_plural = 'Mesajlar'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender.username} → {self.exchange} ({self.created_at:%d.%m.%Y %H:%M})'
    
class Rating(models.Model):
    giver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_ratings', verbose_name='Puanı Veren')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_ratings', verbose_name='Puanı Alan')
    exchange = models.ForeignKey(BookExchange, on_delete=models.CASCADE, related_name='ratings', verbose_name='İlgili Takas')
    score = models.PositiveIntegerField(verbose_name='Puan')
    comment = models.TextField(blank=True, verbose_name='Yorum')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Tarih')

    class Meta:
        verbose_name = 'Puanlama'
        verbose_name_plural = 'Puanlamalar'
        unique_together = ('giver', 'exchange')

    def __str__(self):
        return f'{self.giver} → {self.receiver}: {self.score}/5'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.receiver.update_rating()
