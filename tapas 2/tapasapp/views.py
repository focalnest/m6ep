from django.shortcuts import render, redirect, get_object_or_404
from .models import Dish 
from .models import Account
from django.contrib import messages


# Create your views here.

def home_view(request):
    account_id = request.session.get('account_id')
    if account_id:
        try:
            account = Account.objects.get(pk=account_id)
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
            request.session['account_id'] = account.pk 
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
            request.session['account_id'] = account.pk 
            messages.success(request, "Account created successfully!")
            return redirect('basic_list', pk=account.pk)
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
        if account.password == current:
            if new1 == new2:
                account.password = new1
                account.save()
                messages.success(request, "Password changed successfully!")
                return redirect('manage_account', pk=pk)
            else:
                messages.error(request, "Passwords do not match!")
        else:
            messages.error(request, "Password is incorrect!")
    return render(request, 'tapasapp/change_password.html', {'account': account})

def logout_view(request):
    return redirect('login')

def better_menu(request):
    dish_objects = Dish.objects.all()
    return render(request, 'tapasapp/better_list.html', {'dishes':dish_objects})

def add_menu(request):
    if(request.method=="POST"):
        dishname = request.POST.get('dname')
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.create(name=dishname, cook_time=cooktime, prep_time=preptime)
        return redirect('better_menu')
    else:
        return render(request, 'tapasapp/add_menu.html')

def view_detail(request, pk):
    d = get_object_or_404(Dish, pk=pk)
    return render(request, 'tapasapp/view_detail.html', {'d': d})

def delete_dish(request, pk):
    Dish.objects.filter(pk=pk).delete()
    return redirect('better_menu')

def update_dish(request, pk):
    if(request.method=="POST"):
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.filter(pk=pk).update(cook_time=cooktime, prep_time=preptime)
        return redirect('view_detail', pk=pk)
    else:
        d = get_object_or_404(Dish, pk=pk)
        return render(request, 'tapasapp/update_menu.html', {'d':d})