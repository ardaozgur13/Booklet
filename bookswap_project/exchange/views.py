from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BookExchange, Rating, Message
from .forms import ExchangeRequestForm, RatingForm
from books.models import Book


@login_required
def exchange_request_view(request, book_pk):
    requested_book = get_object_or_404(Book, pk=book_pk, is_public=True)
    if requested_book.owner == request.user:
        messages.error(request, 'Kendi kitabınıza takas isteği gönderemezsiniz.')
        return redirect('books:discover')
    if not Book.objects.filter(owner=request.user).exists():
        messages.error(request, 'Önce kitaplığınıza kitap eklemelisiniz.')
        return redirect('books:book_add')
    if request.method == 'POST':
        form = ExchangeRequestForm(request.POST, user=request.user)
        if form.is_valid():
            if BookExchange.objects.filter(requester=request.user, requested_book=requested_book, status='pending').exists():
                messages.warning(request, 'Bu kitap için zaten bekleyen bir isteğiniz var.')
                return redirect('books:discover')
            exchange = form.save(commit=False)
            exchange.requester = request.user
            exchange.requested_book = requested_book
            exchange.save()
            messages.success(request, 'Takas isteğiniz gönderildi!')
            return redirect('exchange:outgoing')
    else:
        form = ExchangeRequestForm(user=request.user)
    return render(request, 'exchange/request_form.html', {'form': form, 'requested_book': requested_book})


@login_required
def incoming_view(request):
    exchanges = BookExchange.objects.filter(
        requested_book__owner=request.user, status='pending'
    ).select_related('requester', 'offered_book', 'requested_book')

    # Kabul edilmiş aktif takaslar (chat için)
    active_exchanges = BookExchange.objects.filter(
        status='accepted'
    ).filter(
        requested_book__owner=request.user
    ) | BookExchange.objects.filter(
        status='accepted', requester=request.user
    )
    active_exchanges = active_exchanges.distinct()

    unread_count = Message.objects.filter(
        exchange__in=active_exchanges, is_read=False
    ).exclude(sender=request.user).count()

    return render(request, 'exchange/incoming.html', {
        'exchanges': exchanges,
        'unread_count': unread_count,
    })


@login_required
def outgoing_view(request):
    exchanges = BookExchange.objects.filter(
        requester=request.user
    ).select_related('offered_book', 'requested_book', 'requested_book__owner')
    return render(request, 'exchange/outgoing.html', {'exchanges': exchanges})


@login_required
def accept_view(request, pk):
    exchange = get_object_or_404(BookExchange, pk=pk, requested_book__owner=request.user, status='pending')
    if request.method == 'POST':
        exchange.status = 'accepted'
        exchange.save(update_fields=['status'])
        messages.success(request, 'Takas isteği kabul edildi!')
        return redirect('exchange:incoming')
    return render(request, 'exchange/confirm_action.html', {'exchange': exchange, 'action': 'accept', 'action_label': 'Kabul Et'})


@login_required
def reject_view(request, pk):
    exchange = get_object_or_404(BookExchange, pk=pk, requested_book__owner=request.user, status='pending')
    if request.method == 'POST':
        exchange.status = 'rejected'
        exchange.save(update_fields=['status'])
        messages.success(request, 'Takas isteği reddedildi.')
        return redirect('exchange:incoming')
    return render(request, 'exchange/confirm_action.html', {'exchange': exchange, 'action': 'reject', 'action_label': 'Reddet'})


@login_required
def complete_view(request, pk):
    exchange = get_object_or_404(BookExchange, pk=pk, status='accepted')
    if request.user not in [exchange.requester, exchange.owner]:
        messages.error(request, 'Bu işlemi yapamazsınız.')
        return redirect('exchange:history')
    if request.method == 'POST':
        exchange.is_completed = True
        exchange.save(update_fields=['is_completed'])

        # Takas tamamlanınca her iki kitabı da public listeden kaldır
        exchange.offered_book.is_public = False
        exchange.offered_book.save(update_fields=['is_public'])

        exchange.requested_book.is_public = False
        exchange.requested_book.save(update_fields=['is_public'])

        messages.success(request, 'Takas tamamlandı olarak işaretlendi!')
        return redirect('exchange:history')
    return render(request, 'exchange/confirm_action.html', {
        'exchange': exchange, 'action': 'complete', 'action_label': 'Tamamlandı Olarak İşaretle'
    })

@login_required
def history_view(request):
    sent = BookExchange.objects.filter(requester=request.user, status__in=['accepted', 'rejected'])
    received = BookExchange.objects.filter(requested_book__owner=request.user, status__in=['accepted', 'rejected'])
    exchanges = (sent | received).distinct().select_related('requester', 'offered_book', 'requested_book', 'requested_book__owner')
    return render(request, 'exchange/history.html', {'exchanges': exchanges})


@login_required
def rate_view(request, pk):
    exchange = get_object_or_404(BookExchange, pk=pk, is_completed=True)
    if request.user not in [exchange.requester, exchange.owner]:
        messages.error(request, 'Bu takası puanlayamazsınız.')
        return redirect('exchange:history')
    if Rating.objects.filter(exchange=exchange, giver=request.user).exists():
        messages.info(request, 'Bu takası zaten puanladınız.')
        return redirect('exchange:history')
    receiver = exchange.owner if exchange.requester == request.user else exchange.requester
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.giver = request.user
            rating.receiver = receiver
            rating.exchange = exchange
            rating.score = int(form.cleaned_data['score'])
            rating.save()
            messages.success(request, f'{receiver.get_full_name()} için puanınız kaydedildi.')
            return redirect('exchange:history')
    else:
        form = RatingForm()
    return render(request, 'exchange/rate_form.html', {'form': form, 'exchange': exchange, 'receiver': receiver})

@login_required
def chat_view(request, pk):
    exchange = get_object_or_404(BookExchange, pk=pk, status='accepted')
    if request.user not in [exchange.requester, exchange.owner]:
        messages.error(request, 'Bu sohbete erişemezsiniz.')
        return redirect('exchange:history')

    # Karşı tarafın mesajlarını okundu işaretle
    Message.objects.filter(
        exchange=exchange, is_read=False
    ).exclude(sender=request.user).update(is_read=True)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                exchange=exchange,
                sender=request.user,
                content=content
            )
        return redirect('exchange:chat', pk=pk)

    chat_messages = exchange.messages.all()
    other_user = exchange.owner if exchange.requester == request.user else exchange.requester

    return render(request, 'exchange/chat.html', {
        'exchange': exchange,
        'chat_messages': chat_messages,
        'other_user': other_user,
    })