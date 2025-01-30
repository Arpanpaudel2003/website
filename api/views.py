from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, RegisterForm, CommentForm
from .models import Post
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

@login_required(login_url='login')
def blog(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        posts = Post.objects.filter(para__icontains=search_query) 
    else:
        posts = Post.objects.all()
    
    form = PostForm()
    
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/blog")
    
    context = {'posts': posts, 'form': form, 'search_query': search_query}
    return render(request, 'blog.html', context)

@login_required(login_url='login')
def deletePost(request, pk):
    item = Post.objects.get(id=pk)
    
    if request.method == "POST":
        item.delete()
        return redirect('/blog')
    
    context = {'item': item}
    return render(request, 'delete.html', context)

@login_required(login_url='login')
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("/blog")
    
    context = {'form': form}
    return render(request, "update_post.html", context)

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    
    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #messages.success(request, "Login Successfully")
            return redirect('blog')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    #messages.info(request, "Logout Successfully")
    return redirect('login')
        