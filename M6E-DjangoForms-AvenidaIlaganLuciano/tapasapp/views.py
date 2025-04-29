from django.shortcuts import render, redirect, get_object_or_404
from .models import Dish, Account
from django.contrib import messages


# Create your views here.

def home_view(request):
    account_pk = request.session.get('account_pk')
    if account_pk:
        try:
            account = Account.objects.get(pk=account_pk)
            return redirect('basic_list', pk=account.pk)
        except Account.DoesNotExist:
            pass
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        try:
            account = Account.objects.get(username=username, password=password)
            request.session['account_pk'] = account.pk 
            return redirect('basic_list', pk=account.pk)
        except Account.DoesNotExist:
            messages.error(request, "That login is invalid!")
            return render(request, 'tapasapp/login.html') 
    return render(request, 'tapasapp/login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        if Account.objects.filter(username=username).exists():
            messages.error(request, "Account already exists!")
            return render(request, 'tapasapp/signup.html')
        else:
            account = Account.objects.create(username=username, password=password)
            request.session['account_pk'] = account.pk 
            messages.success(request, "Account created successfully!")
            return redirect('login')
    return render(request, 'tapasapp/signup.html')

def basic_list_view(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'tapasapp/basic_list.html', {'account': account})

def manage_account_view(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'tapasapp/manage_account.html', {'account': account})

def delete_account_view(request, pk):
    account = get_object_or_404(Account, pk=pk)
    account.delete()
    messages.success(request, "Account deleted successfully!")
    return redirect('login')

def change_password_view(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        current = request.POST['current']
        new1 = request.POST['new1']
        new2 = request.POST['new2']
        if account.password == current and new1 == new2:
            account.password = new1
            account.save()
            return redirect('manage_account', pk=pk)
        else:
            messages.error(request, "Your password is either incorrect or your new passwords don't match!")
    return render(request, 'tapasapp/change_password.html', {'account': account})

def logout_view(request):
    return redirect('login')