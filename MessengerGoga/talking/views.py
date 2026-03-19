from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

# Create your views here.

from django.http import HttpResponse
  
@login_required(redirect_field_name="enter", login_url='enter')
def chatroom(request):
    return render(request, 'chatting_room.html')

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
        elif 'log' in request.POST:
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('room')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль!')
                form = UserForm(request.POST)
    else:
        # GET запрос - создаем пустую форму
        form = UserForm()
    
    return render(request, 'reg.html', {'form': form})
