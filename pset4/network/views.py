import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Post, Follows

def index(request):
    page_number = request.GET.get('page')

    return render(request, "network/index.html", {
        'posts': Paginator(Post.objects.order_by('-created_at'), 10).get_page(page_number),
        "title": "All Posts"
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def posts(request):
    if request.method == "POST":
        post = Post.objects.create(content=request.POST['content'], user=request.user)

    return HttpResponseRedirect(reverse('index'))

def profile(request, id):
    profile = User.objects.get(pk=id)
    page_number = request.GET.get('page')

    return render(request, 'network/profile.html', {
        "profile": profile,
        "posts": Paginator(profile.posts.all(), 10).get_page(page_number),
        'isFollowing': request.user.following.filter(following_user_id=profile).exists()
    })

@login_required
def followToggle(request, id):
    if request.method == "GET":
        return HttpResponseRedirect(reverse('index'))

    targetUser = User.objects.get(pk=id)

    if request.user.following.filter(following_user_id=targetUser).exists():
        request.user.following.get(following_user_id=targetUser).delete()
    else:
        Follows.objects.create(user_id=request.user, following_user_id=targetUser)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def following(request):
    # get followings ids only flattened to query posts over them
    following = request.user.following.all().values_list('following_user_id', flat=True).distinct()
    
    # guard
    if not following:
        return render(request, 'network/index.html', {"posts": None})

    page_number = request.GET.get('page')
    posts = Paginator(Post.objects.filter(user_id__in=following).order_by('-created_at'), 10).get_page(page_number)
    
    return render(request, 'network/index.html', {
        "posts": posts,
        "title": "following Posts"
    })

@login_required
def edit_post(request, id):
    if request.method == "POST":
        post = Post.objects.get(pk=id)

        if (post.user.id != request.user.id):
            return HttpResponse('Unauthorized', status=401)

        data = json.loads(request.body)

        print(data)

        post.content = data['content']
        post.save()

        return JsonResponse({
            'message': 'updated',
            'content': data['content']}
        , status=200)
    
    return JsonResponse({'message': 'something went wrong!'}, status=404)

@login_required
def toggle_like(request, id):
    if request.method == "POST":
        post = Post.objects.get(pk=id)

        if Post.objects.filter(pk=post.id, likedBy=request.user).exists():
            post.likedBy.remove(request.user)
        else:
            post.likedBy.add(request.user)
        
        return JsonResponse({
            'message': 'success',
            'likesCount': post.likesCount}
        , status=200)

    return JsonResponse({
            'message': 'something went wrong!'}
        , status=404)