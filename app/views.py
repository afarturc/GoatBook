from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from app.models import Post, Utilizador, Comment, Like
from app.forms import PostForm, CommentForm, LikeForm, LikeFormDelete

# Create your views here.

def home(request):
    if request.user.is_authenticated and request.user.username!="admin":
        new_users = Utilizador.objects.all()[:5]
        profile = Utilizador.objects.filter(username=request.user.username)
        posts = Post.objects.all().order_by("-date")
        return render(request, "home.html", {"profile": profile, "posts": posts, "new_users": new_users})
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
        if request.FILES:
            image = request.FILES["image"]
        else:
            image = None

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"messages": "Username already exists."})

        elif password != confirmation:
            return render(request, "signup.html", {"messages": "Passwords must match."})

        elif User.objects.filter(email=email).exists():
            print("Email already exists")
            return render(request, "signup.html", {"messages": "Email already exists."})

        elif Utilizador.objects.filter(username=username).exists():
            return render(request, "signup.html", {"messages": "Username already exists."})

        elif Utilizador.objects.filter(email=email).exists():
            return render(request, "signup.html", {"messages": "Email already exists."})
        
        elif request.FILES:
            Utilizador.objects.create(username=username, password=password, email=email, profile_pic=image)
            user = User.objects.create_user(username=username, password=password, email=email)
            auth.login(request, user)
            return redirect("home")
        else:
            Utilizador.objects.create(username=username, password=password, email=email)
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
    if user.is_authenticated and request.user.username!="admin":
        utilizador = Utilizador.objects.get(username=request.user.username)
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = request.FILES["image"]
                caption = request.POST["caption"]

                if caption and image:
                    Post.objects.create(user=utilizador, image=image, caption=caption)
                    return redirect("home")

        else:
                form=PostForm()
                return render(request, "postadd.html", {"form": form, "user": utilizador})
    else:
        return redirect("login")


## EM PROGRESSO
def postdetail(request, _id):
    post_id = Post.objects.get(id=_id)
    comments = Comment.objects.filter(post=post_id)
    num_comments = len(comments)
    likes = Like.objects.filter(post=post_id)
    num_likes = len(likes)
    if request.user.is_authenticated and request.user.username!="admin":
        user = Utilizador.objects.get(username=request.user.username)
        like_user = len(Like.objects.filter(user=user))
        print(like_user)
        #Comentarios
        if request.method == "POST":
            form_comment = CommentForm(request.POST)
            form_Like = LikeForm(request.POST)
            form_Like_delete = LikeFormDelete(request.POST)
            if form_comment.is_valid():
                comment = form_comment.cleaned_data["comment"]
                Comment.objects.create(user=user, post=post_id, comment=comment)
                return redirect("postdetail", _id)
            elif form_Like.is_valid():
                like = form_Like.cleaned_data["like"]
                Like.objects.create(user=user, post=post_id)
                return redirect("postdetail", _id)
            elif form_Like_delete.is_valid():
                like = Like.objects.filter(user=user, post=post_id)
                like.delete()
                return redirect("postdetail", _id)
        else:
            form_comment = CommentForm()
            form_Like = LikeForm()
            form_Like_delete = LikeFormDelete()
            return render(request, "post.html", {
                "post": post_id, 
                "comments": comments,
                "num_comments": num_comments, 
                "likes": likes, 
                "num_likes": num_likes, 
                "form_comment": form_comment, 
                "form_Like": form_Like , 
                "form_Like_delete": form_Like_delete,
                "like_user": like_user})
            
    else:
        return render(request, "post2.html", {"post": post_id, "comments": comments, "num_comments": num_comments , "likes": likes, "num_likes": num_likes})

def comment(request, _id):
    if request.user.is_authenticated and request.user.username!="admin":
        post = Post.objects.get(id=_id)
        user = Utilizador.objects.get(username=request.user.username)
        comments = Comment.objects.filter(post=post)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = request.POST["comment"]
            Comment.objects.create(user=user, post=post, comment=comment)
            return redirect("postdetail", _id)
        else:
            return render(request, "post.html", {"post": post, "user": user, "comments": comments, "form": form})
    else:
        return redirect("login")


def like (request,_id):
    if request.user.is_authenticated and request.user.username!="admin":
        post = Post.objects.get(id=_id)
        user = Utilizador.objects.get(username=request.user.username)
        likes = Like.objects.filter(post=post)
        form = LikeForm(request.POST)
        if form.is_valid():
            Like.objects.create(user=user, post=post)
            return redirect("postdetail", _id)
        else:
            return render(request, "post.html", {"post": post, "user": user, "likes": likes, "form": form})
    else:
        return redirect("login")