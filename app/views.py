from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from app.models import User,Post

# Create your views here.

def home(request):
    return render(request, "home2.html")

def post(request):
    return render(request, "post.html")

def logout(request):
    return render(request, "logout.html")

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"messages": "Username already exists."})
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "signup.html", {"messages": "Passwords must match."})
        
        email = request.POST["email"]
        if User.objects.filter(email=email).exists():
            return render(request, "signup.html", {"messages": "Email already exists."})
        #pode nao ter imagem
        if "image" in request.FILES:
            image = request.FILES["image"]
            user = User(username=username, password=password, email=email, profile_pic=image)
        else:
            image = None
            user = User(username=username, password=password, email=email)
        
        user.save()
        return render(request, "home.html")

    else:
        return render(request, "signup.html", {"messages": ""})


