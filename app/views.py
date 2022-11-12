from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from app.models import Post, Utilizador, Comment, Like
from app.forms import PostForm, CommentForm, LikeForm, LikeFormDelete, ImageForm, PasswordForm, BioForm
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
# Done
def home(request):
    if request.user.is_authenticated and request.user.username!="admin":
        ctx = {
            "friend":True,
            "posts": Post.objects.all().order_by("-date"),
            "user": get_object_or_404(Utilizador, username=request.user.username),
            "new_users": Utilizador.objects.all()[:5], #ALterar ainda    
            "template": "layout.html",
        }

        return render(request, "home.html", ctx)
    else:
        ctx={   
            "friend": False,
            "template": "layout2.html",
            "posts": Post.objects.all().order_by("-date"),
        }
        return render(request, "home.html", ctx)

# Done
def logout(request):
    auth.logout(request)
    return redirect("home")
# Done
def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        email = request.POST["email"]

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
            image = request.FILES["image"]
            Utilizador.objects.create(username=username, password=password, email=email, profile_pic=image)
            user = User.objects.create_user(username=username, password=password, email=email, profile_pic=image)
            auth.login(request, user)
            return redirect("home")
        else:
            Utilizador.objects.create(username=username, password=password, email=email)
            user = User.objects.create_user(username=username, password=password, email=email)
            auth.login(request, user)
            return redirect("home")

    else:
        return render(request, "signup.html", {"messages": ""})

# Done
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {"messages": "Invalid credentials."})
    else:
        return render(request, "login.html", {"messages": ""})
        
# Done
def postadd(request):
    if request.user.is_authenticated and request.user.username!="admin":
        utilizador = get_object_or_404(Utilizador, username=request.user.username)
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data["image"]
                caption =  form.cleaned_data["caption"]
                
                if caption and image:
                    Post.objects.create(user=utilizador, image=image, caption=caption)
                    return redirect("home")

        else:
                ctx = {
                    "form": PostForm(),
                    "user": utilizador
                }
                return render(request, "postadd.html", ctx)
    else:
        return redirect("login")

#Done
def postdetail(request, _id):
    ctx = {
        "post": get_object_or_404(Post, id=_id),
        "comments": Comment.objects.filter(post=_id),
        "num_likes": Like.objects.filter(post=_id).count(),
        "num_comments": Comment.objects.filter(post=_id).count(),
    }
    post=get_object_or_404(Post, id=_id)
    if request.user.is_authenticated and request.user.username!="admin":
        user = get_object_or_404(Utilizador, username=request.user.username)
        ctx["user"]= user
        ctx["like_user"] = Like.objects.filter(user=user).count()
        if request.method == "POST":
            form_comment = CommentForm(request.POST)
            form_Like = LikeForm(request.POST)
            form_Like_delete = LikeFormDelete(request.POST)
            #Comentario
            if form_comment.is_valid():
                comment = form_comment.cleaned_data["comment"]
                Comment.objects.create(user=user, post=post, comment=comment)
                return redirect("postdetail", _id)
            #Like
            elif form_Like.is_valid():
                like = form_Like.cleaned_data["like"]
                Like.objects.create(user=user, post=post)
                return redirect("postdetail", _id)
            #Delete Like
            elif form_Like_delete.is_valid():
                like = Like.objects.filter(user=user, post=post)
                like.delete()
                return redirect("postdetail", _id)
        else:
            ctx["form_comment"] = CommentForm()
            ctx["form_Like"] = LikeForm()
            ctx["form_Like_delete"] = LikeFormDelete()

            return render(request, "postdetail.html", ctx)
            
    else:
        return render(request, "post.html", ctx)


def profile(request):

    if request.user.is_authenticated and request.user.username!="admin":
        print("User is authenticated")
        user = get_object_or_404(Utilizador, username=request.user.username)
        try:
            posts = Post.objects.filter(user=user).order_by("-date")
        except ObjectDoesNotExist:
            posts = []

        ctx = {
            "user": user,
            "posts": posts,
            "num_posts": len(posts),
            "template": "layout.html",
            #"num_followers": Follow.objects.filter(followed=user).count(),
            #"num_following": Follow.objects.filter(follower=user).count(),
        }

        return render(request, "profile.html", ctx)
    else:
        return redirect("login")

def profileUtilizador(request,username):
    try:
        user = get_object_or_404(Utilizador, username=username)
        posts = Post.objects.filter(user=user).order_by("-date")
    except ObjectDoesNotExist:
        posts = []

    ctx = {
        "user": user,
        "posts": posts,
        "num_posts": len(posts),
        "template": "layout2.html",
        #"num_followers": Follow.objects.filter(followed=user).count(),
        #"num_following": Follow.objects.filter(follower=user).count(),
    }

    return render(request, "profile.html", ctx)


def editProfile(request, username):
    user = get_object_or_404(User, username=username)
    if user.is_authenticated and request.user.username!="admin":
        sucesso = False
        utilizador = Utilizador.objects.get(username=username)
        ctx={"user": utilizador}

        if request.method == "POST" and 'image' in request.FILES:
            formImage= ImageForm(request.POST, request.FILES)
            if formImage.is_valid():
                file = formImage.cleaned_data["image"]
                if file:
                    utilizador.profile_pic = file
                    utilizador.update_image(file)
                    utilizador.save()
                    sucesso = True
            
        if request.method == "POST" and 'old_password' in request.POST and 'new_password' in request.POST and 'password_confirm' in request.POST:
            formPassword= PasswordForm(request.POST)
            if formPassword.is_valid():
                old_password = formPassword.cleaned_data["old_password"]
                new_password = formPassword.cleaned_data["new_password"]
                password_confirm = formPassword.cleaned_data["password_confirm"]
                if new_password != password_confirm:
                    sucesso = False
                else:

                    if user.check_password(old_password):
                        user.set_password(new_password)
                        user.save()

                        utilizador.update_password(new_password)
                        utilizador.save()
                        sucesso = True
                    else:
                        sucesso = False

        if request.method == "POST" and 'bio' in request.POST:
            formBio= BioForm(request.POST)
            if formBio.is_valid():
                bio = formBio.cleaned_data["bio"]
                if bio:
                    utilizador.bio = bio
                    utilizador.save()
                    sucesso = True
                        
        if not sucesso:
            ctx["formImage"] = ImageForm()
            ctx["formBio"] = BioForm()
            ctx["formPassword"] = PasswordForm()

            return render(request, "editProfile.html", ctx)
        
        return redirect("/profile")
    else:
        return redirect("login")