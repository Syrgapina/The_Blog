from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from .forms import Images, Comments, Posts
from .models import NewPost, PostComment, LikePost


def hello(request):
    return HttpResponse("Hello, world!")


@csrf_exempt
def home(request):
    posts = NewPost.objects.all()
    # if request.method == 'POST':
    #
    return render(request, 'home.html', {'posts': posts})


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def add_post(request):
    if request.method == 'POST':
        form = Images(request.POST, request.FILES)
        if form.is_valid():
            new_post = NewPost(author=request.user, text=request.POST['text'], image=request.FILES['image'])
            new_post.save()
            return redirect('home')
    else:
        form = Images()
    return render(request, 'add_post.html', {'form': form})


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def remove_post(request, post_id):
    post = NewPost.objects.filter(id=post_id).first()
    if request.method == 'POST':
        post_el = NewPost.objects.get(id=post_id)
        post_el.delete()
        return redirect('home')
    return render(request, 'remove_post.html', {'post': post})


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def edit_post(request, post_id):
    post = NewPost.objects.filter(id=post_id).first()
    if request.method == 'POST':
        form = Posts(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('post_page', post_id=post_id)
    else:
        form = Posts(instance=post)
    context = {'post': post, 'form': form}
    return render(request, 'edit_post.html', context)


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def post_page(request, post_id):
    post = NewPost.objects.filter(id=post_id).first()
    post_comments = PostComment.objects.filter(post_id=post_id).all()
    if request.method == 'POST':
        form = Comments(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post_id = post_id
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_page', post_id=post_id)
    else:
        form = Comments()
    context = {'post': post, 'post_comments': post_comments, 'form': form}
    return render(request, 'post_page.html', context)


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def remove_comment(request, post_id, comment_id):
    if request.method == 'POST':
        post_comment = PostComment.objects.filter(id=comment_id).first()
        post_comment.delete()
        return redirect('post_page', post_id=post_id)
    return render(request, 'remove_comment.html')


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def edit_comment(request, post_id, comment_id):
    post_comment = PostComment.objects.filter(id=comment_id).first()
    if request.method == 'POST':
        form = Comments(request.POST, instance=post_comment)
        if form.is_valid():
            form.save()
        return redirect('post_page', post_id=post_id)
    else:
        form = Comments(instance=post_comment)
    context = {'post_comment': post_comment, 'form': form}
    return render(request, 'edit_comment.html', context)


@login_required(login_url=reverse_lazy('login'))
def like_post(request, post_id):
    username = request.user.username
    post = NewPost.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    if like_filter is None:
        new_like = LikePost.objects.create(post_id=post, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect(request, 'post_page.html')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
    return redirect(request, 'post_page.html')