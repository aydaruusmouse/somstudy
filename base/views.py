from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from .models import Room, Topic, Message
from .forms import roomForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import userForm
# rooms= [
#     {'id':1, 'name': 'Lets learn Javascript'},
#     {'id':2, 'name': 'Lets learn Python'},
#     {'id':3, 'name': 'Lets learn Django'},
#     {'id':4, 'name': 'Lets learn Node js'},
#     {'id':5, 'name': 'Lets learn React'},
# ]

def home(request):
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    rooms= Room.objects.filter(Q(topic__name__icontains= q) |
                               Q(description__icontains= q)
                               )
    room_count= rooms.count()
    topics= Topic.objects.all()
    recent_messages= Message.objects.filter(Q(room__topic__name__icontains= q))
    context= {'rooms': rooms, 'topics': topics, 'room_count': room_count,
              'recent_messages': recent_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room= Room.objects.get(pk= pk)
    room_messages= room.message_set.all().order_by('-created')
    participants= room.participants.all()
    if request.method == 'POST':
       message= Message.objects.create(
        user= request.user,
        room= room,
        body= request.POST.get('message')
        )
        
    # room= None
    # for i in rooms:
    #     if i['id']== int(pk):
    #        room = i
    context= {'room': room, 'messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)



def userProfile(request, pk):
    user= User.objects.get(id= pk)
    rooms= user.room_set.all()
    recent_messages= user.message_set.all()
    topics= Topic.objects.all()
    context= {'user': user, 'rooms': rooms, 'recent_messages': recent_messages, 'topics': topics}
    
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form= roomForm()
    topics= Topic.objects.all()
    context= {'form': form, 'topics': topics}
    
    if request.method== 'POST':
        if request.POST:
            # form= roomForm(request.POST)
            topic_name= request.POST.get('topic')
            topic, created= Topic.objects.get_or_create(name= topic_name)
            Room.objects.create(
                host= request.user,
                topic= topic,
                name= request.POST.get('name'),
                description= request.POST.get('description')
            )
            # if form.is_valid():
            #    room= form.save(commit= False)
            #    room.host= request.user
            #    room.save()
            #    return redirect('home')
            # else:
            #     return HttpResponse('Form is not valid')
            return redirect('home')
    return render(request, 'base/create-room.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
  topics= Topic.objects.all()
  room= Room.objects.get(id=pk)
  if request.user != room.host:
     HttpResponse('You are not authorized to create room')
  form= roomForm(instance=room)
  if request.method== 'POST':
     topic_name= request.POST.get('topic')
     topic, created= Topic.objects.get_or_create(name= topic_name)
     room.name= request.POST.get('name')
     room.topic= topic
     room.description= request.POST.get('description')
     room.save()   
    #  form= roomForm(request.POST, instance=room)
    #  if form.is_valid():
    #     form.save()
     return redirect('home')
  context= {'form': form, 'topics': topics, 'room':room}
  
  return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def roomDelete(request, pk):
    room= Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context={'obj':room}
    return render(request, 'base/room_delete.html', context)

def loginUser(request):
    if request.user.is_authenticated:
       return redirect('home')
    page= 'login'
    username= request.POST.get('username')
    password= request.POST.get('password')

    
    if username== '' and password== '':
       messages.error(request, 'Please enter username and password')
    
    if username and password:
        user= authenticate(username= username, password= password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    context={'page': page}
    return render(request, 'base/user_login-register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    page= 'register';
    form= UserCreationForm()
    if request.method == 'POST':
       form= UserCreationForm(request.POST)
       if form.is_valid():
          user= form.save(commit= False)
          user.username= user.username.lower()
          user.save()
          login(request, user)
          return redirect('home')
    else:
          messages.error(request, 'error accur during registeration')
    context = {'page': page, 'form': form}
    return render(request, 'base/user_login-register.html', context)

# def sendMessage(request):
#     if request.method == 'POST':
       
#    return render(request, 'base/room.html')

# Delete Message
def DeleteMessage(request, pk):
    message= Message.objects.get(id=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context={'obj':message}
    return render(request, 'base/room_delete.html', context)
@login_required(login_url='login')
def updateUser(request):
    user= request.user
    form= userForm(instance=user)
    if request.method == 'POST':
       form= userForm(request.POST, instance=user)
       if form.is_valid():
          form.save()
          return redirect('profile', user.id)
    context= {'form': form}
    return render(request, 'base/edit-user.html', context)

def topicPage(request):
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    topics= Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    room_messages= Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages':room_messages})