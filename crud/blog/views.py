from django.http import request
from .forms import PostForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Hashtag, Post
from django.utils import timezone
from blog.forms import PostForm, CommentForm, HashtagForm

#메인페이지
def main(request):
    posts = Post.objects
    hashtags = Hashtag.objects
    return render(request, 'blog/main.html', {'posts':posts, 'hashtags':hashtags})

#글쓰기페이지
def write(request):
    return render(request, 'blog/create.html')

#글쓰기 함수
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form= form.save(commit=False)
            form.pub_date = timezone.now()
            form.save()
            form.save_m2m()
            return redirect('read')

    else:
        form=PostForm
        return render(request, 'blog/write.html', {'form':form})

#읽기페이지
def read(request):
    posts = Post.objects
    return render(request, 'blog/read.html', {'posts':posts})


#수정페이지
def edit(request):
    return render(request, 'blog/edit.html')

#수정 함수
def edit(request, id):
    post = get_object_or_404(Post, id = id)
    if request.method =="POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect('read')
        
    else:
        form= PostForm(instance=post)
        return render(request, 'blog/edit.html', {'form':form})


def delete(request, id):
    post = get_object_or_404(Post, id = id)
    post.delete()
    return redirect('read')

def detail(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post
            comment.text = form.cleaned_data['text']
            comment.save()
            return redirect('detail', id)

    else:
        form = CommentForm()
        return render(request, "blog/detail.html", {'post':post, 'form':form})

def hashtagform(request, hashtag=None):
    if request.method == 'POST':
        form = HashtagForm(request.POST, instance=hashtag)
        if form.is_valid():
            hashtag = form.save(commit=False)
            if Hashtag.objects.filter(name=form.cleaned_data['name']):
                form = HashtagForm()
                error_message = "이미 존재하는 해시태그 입니다."
                return render(request, 'blog/hashtag.html', {'form':form, "error_message":error_message})
            else:
                hashtag.name = form.cleaned_data['name']
                hashtag.save()
            return redirect('main')
    else:
        form = HashtagForm(instance=hashtag)
        return render(request, 'blog/hashtag.html', {'form':form})

def search(request, hashtag_id):
    hashtag=get_object_or_404(Hashtag, pk=hashtag_id)
    return render(request, 'blog/search.html', {'hashtag':hashtag})

