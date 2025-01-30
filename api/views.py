from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, RegisterForm
from .models import Post
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

def blog(request):
    # Get the search query from GET parameters
    search_query = request.GET.get('search', '')
    
    # Filter posts based on the search query if provided
    if search_query:
        posts = Post.objects.filter(para__icontains=search_query)  # Adjust to your field
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

def deletePost(request, pk):
    item = Post.objects.get(id=pk)
    
    if request.method == "POST":
        item.delete()
        return redirect('/blog')
    
    context = {'item': item}
    return render(request, 'delete.html', context)


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

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request, "Register Successfully")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request,'register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successfully")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Logout Successfully")
    return redirect('home')
        