from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.order_by(
        '-created', '-updated').filter(
            Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()[:4]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)).order_by('-created')
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
    }
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        body = request.POST.get('body')
        Message.objects.create(
            user=request.user,
            room=room,
            body=body
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants
    }
    return render(request, 'base/room.html', context)


@login_required
def createRoom(request):
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')
    else:
        form = RoomForm()
    context = {
        'form': form,
        'topics': topics,
        'legend': 'Create'
    }
    return render(request, 'base/room_form.html', context)


@login_required
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('room', pk=room.id)
    else:
        form = RoomForm(instance=room)

    context = {
        'form': form,
        'topics': topics,
        'room': room,
        'legend': 'Update'
    }
    return render(request, 'base/room_form.html', context)


@login_required
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {
        'obj': room
    }
    return render(request, 'base/delete.html', context)


@login_required
def deleteRoomMessage(request, pk):
    room_message = Message.objects.get(id=pk)
    if request.method == 'POST':
        room_message.delete()
        return redirect('home')

    context = {
        'obj': room_message
    }

    return render(request, 'base/delete.html', context)


def topicPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {
        'topics': topics,
    }
    return render(request, 'base/topics.html', context)


def activityPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)).order_by('-created')
    context = {
        'room_messages': room_messages,
    }
    return render(request, 'base/activity.html', context)
