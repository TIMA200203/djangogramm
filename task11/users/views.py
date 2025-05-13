from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, ProfileUpdateForm, UserLoginForm
from .models import User_Post, Profile, Follow, User
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_backends


def home(request):
    return render(request, 'users/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            backend = get_backends()[0]
            login(request, user, backend=f"{backend.__module__}.{backend.__class__.__name__}")
            Profile.objects.create(user=user)  
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/profile_update.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)   
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('profile')  
            else:
                form.add_error(None, "Неправильний логін або пароль.")
        else:

            form.add_error(None, "Будь ласка, виправте помилки.")
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'form': form})


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)

    if request.user != user_to_follow:
        existing_follow = Follow.objects.filter(follower=request.user, following=user_to_follow)

        if existing_follow.exists():
            existing_follow.delete()
            messages.success(request, "Відписано від користувача!")
        else:
            Follow.objects.create(follower=request.user, following=user_to_follow)
            messages.success(request, "Підписано на користувача!")

    return redirect(request.META.get('HTTP_REFERER', 'users_list'))


@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    messages.success(request, "Підписка скасована!")
    return redirect('users_list')


@login_required
def following_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    following = user.following.all()
    return render(request, "users/following_list.html", {"following": following})


@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        return redirect('profile')
    posts = User_Post.objects.filter(author=user)
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    return render(request, 'users/profile_user.html', {
        'user': user,
        'posts': posts,
        'is_following': is_following,
    })

@login_required
def users_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    users = User.objects.all()
    following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)

    return render(request, 'users/users_list.html', {
        'users': users,
        'following_ids': set(following_ids)
    })


@login_required
def following_list(request, user_id):

    user = get_object_or_404(User, id=user_id)

    following = Follow.objects.filter(follower=user).values_list('following', flat=True)
    users = User.objects.filter(id__in=following)

    return render(request, 'users/following_list.html', {'following': users})
