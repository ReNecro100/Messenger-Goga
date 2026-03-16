from django.shortcuts import render, redirect
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
    if request.method == 'POST':
        # Создаем форму с данными POST
        form = UserForm(request.POST)
        if form.is_valid():
            # Сохраняем автора
            user = form.save()
            return redirect('goga')
    else:
        # GET запрос - создаем пустую форму
        form = UserForm()
    
    return render(request, 'reg.html', {'form': form})
