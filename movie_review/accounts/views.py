from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from accounts.models import UserProfile
from movies.models import Comment, Movie

# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def register_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        try:
            avatar = request.FILES['avatar']
        except MultiValueDictKeyError:
            avatar = None
        
        if password == password2:
            user = User.objects.create_user(
                username=username,
                password=password
            )
            user.first_name = firstname
            user.last_name = lastname
            user.email = email

            user.save()

            #create the user's profile
            profile = UserProfile(
                person=user,
                avatar=avatar
            )
            profile.save()
            login(request, user)
            return redirect('home')



    return render(request, 'register.html')

@login_required(login_url='login')
def user_profile(request):
    profile = UserProfile.objects.get(person=request.user)
    user_movies = Movie.objects.filter(owner=request.user)
    user_reviews = Comment.objects.filter(person=request.user)
    return render(request, 'profile.html',{
        'profile': profile,
        'user_movies': user_movies,
        'user_reviews': user_reviews
    })
