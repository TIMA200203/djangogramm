from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post_in_site, PostImage, Tag_For_Pots
from posts.forms import PostForm
from django.http import JsonResponse
from users.models import Follow
from users.views import follow_user


@login_required
def feed(request):
    posts = Post_in_site.objects.all().order_by('-created_at')
    following_ids = set(Follow.objects.filter(follower=request.user).values_list('following_id', flat=True))

    return render(request, 'posts/feed.html', {
        'posts': posts,
        'following_ids': following_ids
    })


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post_in_site, id=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post_in_site, id=post_id)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({'likes': post.likes.count(), 'liked': liked})

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            for image in images:
                PostImage.objects.create(post=post, image=image)

            return redirect('profile') 
    else:
        form = PostForm()

    return render(request, 'posts/add_post.html', {'form': form})

@login_required
def news_feed(request):
    following_users = Follow.objects.filter(follower=request.user).values_list("following", flat=True)
    posts = Post_in_site.objects.filter(user__in=following_users).order_by("-created_at")
    return render(request, 'posts/news_feed.html', {'posts': posts})


@login_required
def posts_following_list(request):
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    posts = Post_in_site.objects.filter(user__in=following_users).order_by('-created_at')
    return render(request, 'posts/posts_following_list.html', {'posts': posts})
