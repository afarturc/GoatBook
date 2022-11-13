from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from app.models import Post, Utilizador, Comment
from app.forms import PostForm, CommentForm, ImageForm, PasswordForm, BioForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse


# Create your views here.
# Done
def home(request):
    if request.user.is_authenticated and request.user.username!="admin":
        ctx = {
            "friend":True,
            "posts": Post.objects.all().order_by("-date"),
            "user": get_object_or_404(Utilizador, username=request.user.username),
            "new_users": Utilizador.objects.all()[:5], #ALterar ainda    
        }

        return render(request, "home.html", ctx)
    else:
        ctx={   
            "friend": False,
            "posts": Post.objects.all().order_by("-date"),
            "comments_count": Comment.objects.all().count(),
        }
        return render(request, "home.html", ctx)

# Done
def logout(request):
    if request.user.is_authenticated and request.user.username!="admin":
        auth.logout(request)
        return redirect("home")
    else:
        return redirect("login")

# Done
def signup(request):
    if request.user.is_authenticated and request.user.username!="admin":
        return redirect("home")
    else:
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
    if request.user.is_authenticated and request.user.username!="admin":
        return redirect("home")
    else:
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
            caption = request.POST["caption"]
            photo = request.FILES["photo"]

            if caption and photo:
                Post.objects.create(user=utilizador, image=photo, caption=caption)
                return redirect("home")

        else:
                ctx = {
                    "user": utilizador
                }
                return render(request, "home.html", ctx)
    else:
        return redirect("login")

#Done
def postdetail(request, _id):
    post = get_object_or_404(Post, id=_id)
    ctx = {
        "post": post,
        "comments": Comment.objects.filter(post=_id),
        "exist_like" : False
    }
    post=get_object_or_404(Post, id=_id)
    if request.user.is_authenticated and request.user.username!="admin":
        user = get_object_or_404(Utilizador, username=request.user.username)
        ctx["user"]= user
        if request.method == "POST":
            form_comment = CommentForm(request.POST)
            if form_comment.is_valid():
                comment = form_comment.cleaned_data["comment"]
                Comment.objects.create(user=user, post=post, comment=comment)
                post.add_comment()
                return redirect("postdetail", _id)
        else:
            ctx["form_comment"] = CommentForm()
            ctx["exist_like"] = True

            return render(request, "postdetail.html", ctx)
    else:
        return render(request, "postdetail.html", ctx)

def postlike(request, _id):
    if request.user.is_authenticated and request.user.username!="admin":
        return redirect("postdetail", _id)
    else:
        return redirect("login")

def postcomment(request, _id):
    if request.user.is_authenticated and request.user.username!="admin":
        redirect("postdetail", _id)
    else:
        return redirect("login")

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
        #"num_followers": Follow.objects.filter(followed=user).count(),
        #"num_following": Follow.objects.filter(follower=user).count(),
    }

    return render(request, "profile.html", ctx)

#Done
def editProfile(request, username):
    if request.user.is_authenticated and request.user.username!="admin":
        if request.user.username != username:
            return redirect("profile")
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

                    if request.user.check_password(old_password):
                        request.user.set_password(new_password)
                        request.user.save()

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

            return render(request, "profileedit.html", ctx)
        
        return redirect("/profile")
    else:
        return redirect("login")

def postdelete(request, _id):
    post = get_object_or_404(Post, id=_id)
    if request.user.is_authenticated and request.user.username!="admin":
        if request.user.username == post.user.username:
            post.delete()
            return redirect("profile")
        else:
            return redirect("postdetail", _id)
    else:
        return redirect("login")

def commentdelete(request,_id, _id_comment):
    post = get_object_or_404(Post, id=_id)
    comment = get_object_or_404(Comment, id=_id_comment)
    if request.user.is_authenticated and request.user.username!="admin":
        if request.user.username == comment.user.username:
            post.remove_comment()
            comment.delete()
            return redirect("postdetail", comment.post.id)
        else:
            return redirect("postdetail", comment.post.id)
    else:
        return redirect("login")

def postedit(request,_id):
    post = get_object_or_404(Post, id=_id)
    if request.user.is_authenticated and request.user.username!="admin":
        if request.user.username == post.user.username:
            ctx = {
                "post": post,
                "form_postedit": PostForm(),
                "user": Utilizador.objects.get(username=request.user.username),
            }
            if request.method == "POST":
                form_postedit = PostForm(request.POST, request.FILES)
                ctx["form_postedit"]=form_postedit
                if form_postedit.is_valid():
                    caption = form_postedit.cleaned_data["caption"]
                    image = form_postedit.cleaned_data["image"]

                    if image :
                        post.image = image
                        sucesso = True
                    if caption:
                        post.caption = caption
                        sucesso = True
                    if sucesso:
                        post.save()
                        return redirect("postdetail", _id)
                    
            else:
                return render(request, "postedit.html", ctx)
        else:
            return redirect("postdetail", _id)
    else:
        return redirect("login")
        

def like(request):
    if request.POST.get('action') == 'post':
        type = ''
        result = ''
        post_id = request.POST.get('post_id')
        user_id = request.POST.get('user_id')
        user = get_object_or_404(Utilizador, id=user_id)
        post = get_object_or_404(Post, id=post_id)
        if post.likes.filter(id=user_id).exists():
            post.remove_like(user)
            type = 'unlike'
            result = post.like_count
        else:
            type = 'like'
            post.add_like(user)
            result = post.like_count
        return JsonResponse({'result': result, 'type': type})
