from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm, LoginForm


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Hesabınız oluşturuldu!')
            return redirect('books:my_library')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('books:my_library')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect(request.GET.get('next', 'books:my_library'))
            messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('books:home')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'profile_user': request.user})


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profiliniz güncellendi.')
            return redirect('accounts:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})


def user_profile_view(request, pk):
    profile_user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'accounts/profile.html', {'profile_user': profile_user})

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Hesabınız silindi.')
        return redirect('books:home')
    return render(request, 'accounts/delete_account.html')