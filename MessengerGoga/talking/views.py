from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .forms import UserForm

# Create your views here.

from django.http import HttpResponse
  
def goga(request):
    return HttpResponse("МЕССЕНДЖЕР ГЕОРГИЙ")

def secret(request):
    return HttpResponse("Как ты сюда попал???")

def reg(request):
    """
    Обрабатывает создание нового автора.
    GET: отображает пустую форму
    POST: сохраняет автора и перенаправляет на список авторов
    """
    request.session.set_expiry(1209600)
    if request.method == 'POST':
        if 'reg' in request.POST:
            # Создаем форму с данными POST
            form = UserForm(request.POST)
            if form.is_valid():
                # Сохраняем автора
                user = form.save()
                form = UserForm()
                messages.success(request, f'Теперь нужно залогиниться!')
        if 'log' in request.POST:
            nm = request.POST.get('name')
            psswrd = request.POST.get('password')
            if User.objects.filter(name=nm, password=psswrd).exists():
                print(request.POST)
                return redirect('goga')
            else:
                form = UserForm()
    else:
        # GET запрос - создаем пустую форму
        form = UserForm()
    
    return render(request, 'reg.html', {'form': form})
