from django.shortcuts import get_object_or_404, redirect, render
from .models import Blog
from django.utils import timezone

# Create your views here.

def home(req):
    blogs = Blog.objects.all()
    return render(req, 'home.html', {'blogs':blogs})

def detail(req, id):
    blog = get_object_or_404(Blog, pk=id)
    return render(req, 'detail.html', {'blog':blog})

def create(req):
    if req.method =="POST":
        new_blog = Blog()
        new_blog.title = req.POST['title']
        new_blog.writer = req.POST['writer']
        new_blog.pub_date = timezone.now()
        new_blog.body = req.POST['body']
        new_blog.save()
        return redirect('detail', str(new_blog.id))
    else :
        return render(req, 'new.html')

def update(req, id):
    if req.method =="POST":
        update_blog = get_object_or_404(Blog, pk=id)
        update_blog.title = req.POST['title']
        update_blog.writer = req.POST['writer']
        update_blog.body = req.POST['body']
        update_blog.save()
        return redirect('detail', str(update_blog.id))
    else :
        edit_blog = get_object_or_404(Blog, pk=id)
        return render(req, 'edit.html', {'blog':edit_blog})

def delete(req, id):
    delete_blog = get_object_or_404(Blog, pk=id)
    delete_blog.delete()
    return redirect('home')