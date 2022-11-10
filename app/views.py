from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from app.models import Post, Utilizador

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        profile = Utilizador.objects.filter(username=request.user.username)
        posts = Post.objects.all()
        return render(request, "home.html", {"profile": profile, "posts": posts})
        return render(request, "home.html")
    else:
        posts = Post.objects.all()
        print(posts)
        return render(request, "home2.html", {"posts": posts})

def post(request):
    return render(request, "post.html")

def logout(request):
    auth.logout(request)
    return redirect("home")

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
        return redirect("home")

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
            return redirect("home")
        else:
            print("User does not exist")
            return render(request, "login.html", {"messages": "Invalid credentials."})
    else:
        return render(request, "login.html", {"messages": ""})

def postadd(request):
    user = User.objects.get(username=request.user.username)
    if user.is_authenticated:
        print("User is authenticated")
        utilizador = Utilizador.objects.get(username=request.user.username)
        if request.method == "POST":
            caption = request.POST["caption"]
            image = request.FILES["image"]
            Post.objects.create(user=utilizador, caption=caption, image=image)
            return redirect("post.html")
        else:
            return render(request, "postadd.html", {"messages": ""})
    else:
        return redirect("login")