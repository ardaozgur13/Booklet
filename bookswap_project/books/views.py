from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book
from .forms import BookForm


def home_view(request):
    recent_books = Book.objects.filter(is_public=True).select_related('owner').order_by('-created_at')[:6]
    return render(request, 'books/home.html', {'recent_books': recent_books})


@login_required
def my_library_view(request):
    q = request.GET.get('q', '').strip()
    books = Book.objects.filter(owner=request.user)
    if q:
        books = (
            Book.objects.filter(owner=request.user, title__icontains=q) |
            Book.objects.filter(owner=request.user, author__icontains=q) |
            Book.objects.filter(owner=request.user, publisher__icontains=q)
        ).distinct()
    return render(request, 'books/my_library.html', {'books': books, 'q': q})


@login_required
def book_add_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            messages.success(request, f'"{book.title}" kitaplığınıza eklendi.')
            return redirect('books:my_library')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form, 'action': 'Ekle'})


@login_required
def book_edit_view(request, pk):
    book = get_object_or_404(Book, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kitap güncellendi.')
            return redirect('books:my_library')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form, 'action': 'Güncelle', 'book': book})


@login_required
def book_delete_view(request, pk):
    book = get_object_or_404(Book, pk=pk, owner=request.user)
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'"{title}" silindi.')
        return redirect('books:my_library')
    return render(request, 'books/book_confirm_delete.html', {'book': book})


@login_required
def book_toggle_public_view(request, pk):
    book = get_object_or_404(Book, pk=pk, owner=request.user)
    if request.method == 'POST':
        book.is_public = not book.is_public
        book.save(update_fields=['is_public'])
        status = 'takas listesine eklendi' if book.is_public else 'takas listesinden çıkarıldı'
        messages.success(request, f'"{book.title}" {status}.')
    return redirect('books:my_library')


def discover_view(request):
    books = Book.objects.filter(is_public=True).select_related('owner')
    q = request.GET.get('q', '').strip()
    city = request.GET.get('city', '').strip()
    genre = request.GET.get('genre', '').strip()
    if q:
        books = (
            Book.objects.filter(is_public=True, title__icontains=q) |
            Book.objects.filter(is_public=True, author__icontains=q)
        ).distinct()
    if city:
        books = books.filter(owner__city__icontains=city)
    if genre:
        books = books.filter(genre=genre)
    cities = Book.objects.filter(is_public=True).exclude(
        owner__city='').values_list('owner__city', flat=True).distinct().order_by('owner__city')
    genres = Book.GENRE_CHOICES
    return render(request, 'books/discover.html', {'books': books, 'q': q, 'city': city, 'cities': cities, 'genre': genre, 'genres': genres,})


@login_required
def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not book.is_public and book.owner != request.user:
        messages.error(request, 'Bu kitap görüntülenemiyor.')
        return redirect('books:discover')
    return render(request, 'books/book_detail.html', {'book': book})
