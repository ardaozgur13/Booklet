from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'edition', 'publisher', 'page_count', 'genre', 'summary', 'cover_image')        
        widgets = {
            'edition': forms.NumberInput(attrs={'min': 1}),
            'page_count': forms.NumberInput(attrs={'min': 1}),
            'summary': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Kitap hakkında kısa bir özet…'}),
        }
