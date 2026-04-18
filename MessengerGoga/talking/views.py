from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, ChatMessage, Chat, ChatType
from django.db.models import Count, Subquery, OuterRef
from .forms import UserFormReg, UserFormEdit, UserFormLogin, ChatFormCreate, ChatFormEdit
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect

# Create your views here.

from django.http import HttpResponse

@csrf_protect
@login_required(redirect_field_name="log", login_url='log')
def wsschat(request, room_name):
    if request.method == 'POST' and 'non_member' in request.POST:
        chat = Chat.objects.get(id=int(room_name))
        chat.members.add(User.objects.get(id=request.POST['non_member']))
    if request.method == 'POST' and 'member' in request.POST:
        print()
        chats = Chat.objects.filter(
            chat_type=2,
            members__id__in=[request.POST['member'], request.user.id]
        ).annotate(
            member_count=Count('members')
        ).filter(
            member_count=2
        )
        try:
            return redirect(f'/wsschat/{chats[0].id}')
        except:
            chat_form = ChatFormCreate(data={
                "name": f"{request.user.username} - {User.objects.get(id=request.POST['member'])}",
                "description": f"ЛС пользователей {request.user.username} и {User.objects.get(id=request.POST['member'])}",
                "chat_type": ChatType.objects.get(id=2).id
                })
            #Pofiksitj
            print(chat_form.is_valid())
            print(chat_form.errors)
            if chat_form.is_valid():
                lechat = chat_form.save(request, commit=False)
                lechat.save()
                lechat.members.add(User.objects.get(id=request.POST['member']))
                lechat.members.add(request.user)
                return redirect(f'/wsschat/{lechat.id}')
    if request.method == 'POST' and 'leave_chat' in request.POST:
        membership = Chat.members.through.objects.get(
            chat_id=request.POST['leave_chat'],
            user_id=request.user.id
        )
        # Удалить
        membership.delete()
        return redirect(f'/wsschat/2')

    return render(request, "wsschat.html", {
        "room_name": room_name, 
        'current_user': request.user, 
        'current_chat': Chat.objects.get(id=int(room_name)),
        'my_chats': request.user.member_of.all(),
        'members_count': Chat.objects.get(id=int(room_name)).members.count(),
        'members': User.objects.filter(member_of=room_name),
        'non_members': User.objects.filter(
                            member_of__chat_type_id=2,           # чаты типа 2
                            member_of__members__id=request.user.id            # в чате есть пользователь 14
                        ).exclude(
                            id=request.user.id
                        ).exclude(
                            member_of__id=room_name
                        ).distinct()
    })

@login_required(redirect_field_name="log", login_url='log')
def new_chat(request):
    if request.method == 'POST':
        # Создаем форму с данными POST
        form = ChatFormCreate(request.POST)
        if form.is_valid():
            # Сохраняем автора
            lechat = form.save(request)
            lechat.members.add(request.user)
            form = ChatFormCreate()
            return redirect(f'wsschat/{lechat.id}')
    else:
        # GET запрос - создаем пустую форму
        form = ChatFormCreate()
    return render(request, "newchat.html", {"form": form})

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('/wsschat/2') #Pomeniatj idshnik pri zapuske v obraschenije <-VAZHNO SHO KAPEC
    else:
        return redirect('/log')

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
        form = UserFormReg(request.POST)
        if form.is_valid():
            # Сохраняем автора
            user = form.save()
            Chat.objects.get(id=2).members.add(user) #Pomeniatj idshnik pri zapuske v obraschenije <-VAZHNO SHO KAPEC
            form = UserFormReg()
            messages.success(request, f'Теперь нужно залогиниться!')
            return redirect('log')
    else:
        # GET запрос - создаем пустую форму
        form = UserFormReg()
    
    return render(request, "reg.html", {"form": form})

def log(request):
    request.session.set_expiry(1209600)
    if request.method == 'POST':
        form = UserFormLogin()
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('wsschat/2') #Pomeniatj idshnik pri zapuske v obraschenije <-VAZHNO SHO KAPEC
        else:
            messages.error(request, 'Неверное имя пользователя или пароль!')
            form = UserFormLogin(request.POST)
    else:
        # GET запрос - создаем пустую форму
        form = UserFormLogin()
    
    return render(request, "log.html", {"form": form})

@login_required(redirect_field_name="log", login_url='log')
def edit_user(request, userid):
    user = get_object_or_404(User, pk=userid)
    if request.user.id!=int(userid):
        return redirect('/wsschat/2') #Pomeniatj idshnik pri zapuske v obraschenije <-VAZHNO SHO KAPEC
    if request.method == 'POST':
        if 'save' in request.POST:
            # Создаем форму с данными POST
            form = UserFormEdit(request.POST, instance=user)
            if form.is_valid():
                # Сохраняем автора
                user = form.save()
                form = UserFormEdit(request.POST, instance=user)
        if 'delete_user' in request.POST:
            record = User.objects.get(id=request.user.id)
            record.delete()
            return redirect('/log')
        if 'log_out' in request.POST:
            logout(request)
            return redirect('/log')
    else:
        # GET запрос - создаем пустую форму
        form = UserFormEdit(instance=user)
    
    return render(request, "edituser.html", {"form": form})

@login_required(redirect_field_name="log", login_url='log')
def edit_chat(request, chatid):
    chat = get_object_or_404(Chat, pk=chatid)
    if request.user.id!=int(chat.chat_creator.id):
        return redirect('/wsschat/2') #Pomeniatj idshnik pri zapuske v obraschenije <-VAZHNO SHO KAPEC
    if request.method == 'POST':
        if 'save' in request.POST:
            form = ChatFormEdit(request.POST, instance=chat)
            if form.is_valid():
                chat = form.save()
                form = ChatFormEdit(request.POST, instance=chat)
        if 'delete_chat' in request.POST:
            record = Chat.objects.get(id=chat.id)
            record.delete()
            return redirect('/wsschat/2') #Pomeniatj idshnik pri zapuske v obraschenije <-VAZHNO SHO KAPEC
    else:
        # GET запрос - создаем пустую форму
        form = ChatFormEdit(instance=chat)

    return render(request, "editchat.html", {"form": form})