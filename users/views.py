from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import ProfileEditForm, Images
from .models import Profile
from Daily_posts.models import NewPost


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Неправильно введен Логин или Пароль')
    return render(request, 'login.html', {'messages': messages.get_messages(request)})


@csrf_exempt
def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            messages.info(request, 'Пароли не совпадают. Попытайтесь снова')
            return redirect('registration')
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Пользователь с таким логином уже существует')
            return redirect('registration')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Введенная почта уже зарегистрирована другим пользователем')
            return redirect('registration')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            user = auth.authenticate(username=username,password=password)
            auth.login(request, user)

            user = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user)
            new_profile.save()
            return redirect('profile_settings')
    else:
        return render(request, 'registration.html', {'messages': messages.get_messages(request)})


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def profile_settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        user_profile.first_name = request.POST['first_name']
        user_profile.last_name = request.POST['last_name']
        user_profile.email = request.POST['email']
        user_profile.date_of_birth = request.POST['date_of_birth']
        user_profile.location = request.POST['location']
        user_profile.about_me = request.POST['about_me']
        form = Images(request.POST, request.FILES)
        if request.FILES.get('image') is None:
            user_profile.image = user_profile.image
        elif form.is_valid():
            user_profile.image = request.FILES.get('image')
            user_profile.save()
        return HttpResponseRedirect(reverse(viewname=profile, args=[user_profile.user.username]))
    return render(request, 'profile_settings.html', {'user_profile': user_profile})


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def profile(request, username):
    user = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user)
    posts = NewPost.objects.filter(author=user)
    if request.method == 'POST':
        auth.logout(request)
    return render(request, 'profile.html', {'user_profile': user_profile, 'posts': posts})


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def edit_profile(request, profile_id):
    user_profile = Profile.objects.get(id=profile_id)
    if request.method == 'POST':
        profile_form = ProfileEditForm(instance=user_profile, data=request.POST, files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()
        return HttpResponseRedirect(reverse(viewname=profile, args=[user_profile.user.username]))
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {'profile_form': profile_form, 'user_profile': user_profile}
    return render(request, 'edit_profile.html', context)


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def remove_profile_image(request, profile_id):
    if request.method == 'POST':
        user_profile = Profile.objects.get(id=profile_id)
        profile_image = user_profile.image
        profile_image.delete()
        return redirect('edit_profile')
    return render(request, 'remove_profile_image.html')


def remove_post(request, post_id):
    post = NewPost.objects.filter(id=post_id).first()
    if request.method == 'POST':
        post_el = NewPost.objects.get(id=post_id)
        post_el.delete()
        return redirect('home')
    return render(request, 'remove_post.html', {'post': post})

