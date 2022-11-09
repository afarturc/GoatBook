from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from app.models import Utilizador

# Create your views here.

def home(request):
    return render(request, "home2.html")

def post(request):
    return render(request, "post.html")

def logout(request):
    logout(request)
    return render(request, "logout.html")

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        email = request.POST["email"]
        if "image" in request.FILES:
            image = request.FILES["image"]
        else:
            image = None

        if User.objects.filter(username=username).exists():
            print("Username already exists")
            return render(request, "signup.html", {"messages": "Username already exists."})

        
            
        if password != confirmation:
            return render(request, "signup.html", {"messages": "Passwords must match."})

        if User.objects.filter(email=email).exists():
            print("Email already exists")
            return render(request, "signup.html", {"messages": "Email already exists."})

        if Utilizador.objects.filter(username=username).exists():
            return render(request, "signup.html", {"messages": "Username already exists."})

        if Utilizador.objects.filter(email=email).exists():
            return render(request, "signup.html", {"messages": "Email already exists."})
        

        Utilizador.objects.create(username=username, password=password, email=email, profile_pic=image)
        #create user
        user = User.objects.create_user(username=username, password=password, email=email)
        auth.login(request, user)
        return render(request, "home.html")

    else:
        return render(request, "signup.html", {"messages": ""})


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        

        print(username, password)

        user = auth.authenticate(username=username, password=password)

        print(user)
        if user is not None:
            auth.login(request, user)
            return render(request, "home.html")
        else:
            print("User does not exist")
            return render(request, "login.html", {"messages": "Invalid credentials."})
    else:
        return render(request, "login.html", {"messages": ""})

