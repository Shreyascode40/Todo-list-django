from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from account.forms import RegistrationForm
from todo.models import TodoItem
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.



def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect("account:login")
    else:
        form = UserCreationForm()

    return render(request, "account/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "account/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def home(request):
    return render(request, "home.html")