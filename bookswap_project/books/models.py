from django.db import models
from django.conf import settings


class Book(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='books', verbose_name='Sahip')
    title = models.CharField(max_length=255, verbose_name='Kitap Adı')
    author = models.CharField(max_length=255, verbose_name='Yazar')
    edition = models.PositiveIntegerField(default=1, verbose_name='Baskı')
    publisher = models.CharField(max_length=255, verbose_name='Yayınevi')
    GENRE_CHOICES = [
    ('roman', 'Roman'),
    ('siir', 'Şiir'),
    ('tarih', 'Tarih'),
    ('bilim', 'Bilim'),
    ('felsefe', 'Felsefe'),
    ('biyografi', 'Biyografi'),
    ('cocuk', 'Çocuk'),
    ('fantastik', 'Fantastik'),
    ('korku', 'Korku'),
    ('dini', 'Dini'),
    ('egitim', 'Eğitim'),
    ('diger', 'Diğer'),
    ]

    page_count = models.PositiveIntegerField(verbose_name='Sayfa Sayısı')
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='diger', verbose_name='Tür')
    summary = models.TextField(blank=True, verbose_name='Özet')
    
    is_public = models.BooleanField(default=False, verbose_name='Takas Listesinde')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Eklenme Tarihi')

    class Meta:
        verbose_name = 'Kitap'
        verbose_name_plural = 'Kitaplar'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} — {self.author}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.owner.book_count = self.owner.books.count()
            self.owner.save(update_fields=['book_count'])

    def delete(self, *args, **kwargs):
        owner = self.owner
        super().delete(*args, **kwargs)
        owner.book_count = owner.books.count()
        owner.save(update_fields=['book_count'])
