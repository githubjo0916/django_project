from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

def post_new(request):
    if request.method == "POST":
        #print(type(request)) #<class 'django.core.handlers.wsgi.WSGIRequest'>
        #print(request.POST)
        #[25/Nov/2022 15:55:34] "GET /blog/post/new/ HTTP/1.1" 200 1359
        #<QueryDict: {'csrfmiddlewaretoken': ['q2vyelWyfnuLUthd1zWlxcBuAEJ7NicSaenlCkqvZSm8LKwm9UbR5jb1nG9bFSoj'], 'title': ['test'], 'text': ['test']}>
        #[25/Nov/2022 15:55:39] "POST /blog/post/new/ HTTP/1.1" 302 0
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form':form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST": #수정한 내용을 쓰고 save 버튼을 눌렀을 때
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form':form})