from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from base.models import Topic
from base.forms import UserForm
from django.contrib.auth.decorators import login_required


def registerPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    context = {
        'form': form,
        'legend': 'register'
    }
    return render(request, 'users/register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(
                request, 'There was a problem logging in. Check your email and password or create an account.')

    return render(request, 'users/login.html', {'legend': 'Login'})


def logoutPage(request):
    logout(request)
    return redirect('login')


def profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user': user,
        'rooms': rooms,
        'topics': topics,
        'room_messages': room_messages
    }
    return render(request, 'users/profile.html', context)


@login_required
def updateProfile(request):
    form = UserForm(instance=request.user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=request.user.id)
    else:
        form = UserForm(instance=request.user)

    context = {
        'form': form
    }

    return render(request, 'users/update_profile.html', context)
