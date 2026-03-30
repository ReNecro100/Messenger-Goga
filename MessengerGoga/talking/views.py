from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, ChatMessage
from .forms import UserFormRegistration, UserFormLogin, ChatForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

# Create your views here.

from django.http import HttpResponse

@login_required(redirect_field_name="enter", login_url='enter')
def wsschat(request, room_name):
    return render(request, "wsschat.html", {"room_name": room_name, 'msgs': ChatMessage.objects.all(), 'itsname': request.user.username})

@login_required(redirect_field_name="enter", login_url='enter')
def new_chat(request):
    if request.method == 'POST':
        # Создаем форму с данными POST
        form = ChatForm(request.POST)
        if form.is_valid():
            # Сохраняем автора
            lechat = form.save(request)
            form = ChatForm()
            return redirect(f'wsschat/{lechat.chat_type.id}')
    else:
        # GET запрос - создаем пустую форму
        form = ChatForm()
    return render(request, "newchat.html", {"form": form})

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('wsschat/1')
    else:
        return redirect('log')

def secret(request):
    return HttpResponse("Как ты сюда попал???")

def reg(request):
    """
    Обрабатывает создание нового автора.
    GET: отображает пустую форму
    POST: сохраняет автора и перенаправляет на список авторов
    """
    if request.method == 'POST':
        # Создаем форму с данными POST
        form = UserFormRegistration(request.POST)
        if form.is_valid():
            # Сохраняем автора
            user = form.save()
            form = UserFormRegistration()
            messages.success(request, f'Теперь нужно залогиниться!')
            return redirect('log')
    else:
        # GET запрос - создаем пустую форму
        form = UserFormRegistration()
    
    return render(request, "reg.html", {"form": form})

def log(request):
    """
    Обрабатывает создание нового автора.
    GET: отображает пустую форму
    POST: сохраняет автора и перенаправляет на список авторов
    """
    request.session.set_expiry(1209600)
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('wsschat/1')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль!')
            form = UserFormLogin(request.POST)
    else:
        # GET запрос - создаем пустую форму
        form = UserFormLogin()
    
    return render(request, "log.html", {"form": form})
