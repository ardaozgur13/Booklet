from django import forms
from .models import BookExchange, Rating
from books.models import Book


class ExchangeRequestForm(forms.ModelForm):
    class Meta:
        model = BookExchange
        fields = ('offered_book',)
        labels = {'offered_book': 'Teklif Etmek İstediğiniz Kitap'}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['offered_book'].queryset = Book.objects.filter(owner=user)


class RatingForm(forms.ModelForm):
    SCORE_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    score = forms.ChoiceField(choices=SCORE_CHOICES, widget=forms.RadioSelect, label='Puan')

    class Meta:
        model = Rating
        fields = ('score', 'comment')
        labels = {'comment': 'Yorum (opsiyonel)'}
        widgets = {'comment': forms.Textarea(attrs={'rows': 3})}
