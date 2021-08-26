from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .forms import RegisterForm

# Create your views here.


def login_view(req):
    if req.method == "POST":
        form = AuthenticationForm(request=req, data=req.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request=req, username=username, password=password)
            if user is not None:
                login(req, user)
        return redirect("home")
    else : 
        form = AuthenticationForm()
        return render(req, 'login.html', {'form':form})

def logout_view(req):
    logout(req)
    return redirect("home")

def regiseter_view(req):
    if req.method == "POST":
        form = RegisterForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
        return redirect("home")
    else : 
        form = RegisterForm()
        return render(req, 'signup.html', {'form':form})