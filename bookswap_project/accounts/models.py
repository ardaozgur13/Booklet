from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    GENDER_CHOICES = [('E', 'Erkek'), ('K', 'Kadın'), ('B', 'Belirtmek istemiyorum')]

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefon')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='Cinsiyet')
    city = models.CharField(max_length=100, blank=True, verbose_name='Şehir')
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, verbose_name='Profil Fotoğrafı')
    book_count = models.PositiveIntegerField(default=0, verbose_name='Kitap Sayısı')
    rating_average = models.FloatField(default=0.0, verbose_name='Puan Ortalaması')
    rating_count = models.PositiveIntegerField(default=0, verbose_name='Puanlanma Sayısı')

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'

    def __str__(self):
        return f'{self.first_name} {self.last_name} (@{self.username})'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.username

    def update_rating(self):
        from exchange.models import Rating
        ratings = Rating.objects.filter(receiver=self)
        count = ratings.count()
        self.rating_average = round(sum(r.score for r in ratings) / count, 1) if count else 0.0
        self.rating_count = count
        self.save(update_fields=['rating_average', 'rating_count'])
