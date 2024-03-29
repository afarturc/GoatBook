from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from app.models import Post, Utilizador, Comment, Follow
from app.forms import FormSingup, FormLogin, CommentForm, ImageForm, PasswordForm, BioForm, EditPostForm, SearchForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse


# Create your views here.
# *Done
def home(request):
    if request.user.is_authenticated and request.user.username!="admin":
        ctx = {
            "friend":True,
            "posts": Post.objects.all().order_by("-date"),
            "user": get_object_or_404(Utilizador, username=request.user.username),
            "new_users": Utilizador.objects.all()[:5], #ALterar ainda
            "form_search": SearchForm(),
            "exist": True
        }

        return render(request, "home.html", ctx)
    else:
        ctx={
            "friend": False,
            "posts": Post.objects.all().order_by("-date"),
            "comments_count": Comment.objects.all().count(),
            "form_search": SearchForm(),
            "exist": False
        }
        return render(request, "home.html", ctx)

# *Done
def logout(request):
    if request.user.is_authenticated and request.user.username!="admin":
        auth.logout(request)
        return redirect("home")
    else:
        return redirect("login")

# *Done
def signup(request):
    if request.user.is_authenticated and request.user.username!="admin":
        return redirect("home")
    else:
        if request.method == "POST":
            formSignup = FormSingup(request.POST)
            if formSignup.is_valid():
                username = formSignup.cleaned_data["username"]
                email = formSignup.cleaned_data["email"]
                password = formSignup.cleaned_data["password"]
                confirmation = formSignup.cleaned_data["confirmation"]

                if password == confirmation:
                    if User.objects.filter(username=username).exists() or Utilizador.objects.filter(username=username).exists():
                        return render(request, "signup.html", {"messages": "Username already exists." , "formSignup": formSignup})
                    elif User.objects.filter(email=email).exists() or Utilizador.objects.filter(email=email).exists():
                        return render(request, "signup.html", {"messages": "Email already exists.", "formSignup": formSignup})
                    elif request.FILES:
                        photo = request.FILES["photo"]
                        User.objects.create_user(username=username, email=email, password=password)
                        Utilizador.objects.create(username=username, email=email, password=password, profile_pic=photo)
                        auth.login(request, User.objects.get(username=username))
                        return redirect("home")
                    else:
                        user = User.objects.create_user(username=username, password=password, email=email)
                        user.save()
                        Utilizador.objects.create(username=username, email=email, password=password)
                        auth.login(request, user)
                        return redirect("home")

                else:
                    return render(request, "signup.html", {"messages": "Passwords do not match.", "formSignup": formSignup, "form_search": SearchForm()})
            else:
                return render(request, "signup.html", {"messages": "Invalid credentials.", "formSignup": formSignup, "form_search": SearchForm()})
        else:
            return render(request, "signup.html", {"messages": "", "formSignup": FormSingup(), "form_search": SearchForm()})

# *Done
def login(request):
    if request.user.is_authenticated and request.user.username!="admin":
        return redirect("home")
    else:
        if request.method == "POST":
            formLogin = FormLogin(request.POST)
            if formLogin.is_valid():
                username = formLogin.cleaned_data["username"]
                password = formLogin.cleaned_data["password"]
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect("home")
                else:
                    return render(request, "login.html", {"messages": "Invalid credentials.", "formLogin": formLogin, "form_search": SearchForm()})
            else:
                return render(request, "login.html", {"messages": "Invalid credentials.", "formLogin": formLogin, "form_search": SearchForm()})
        else:
            return render(request, "login.html", {"messages": "", "formLogin": FormLogin(), "form_search": SearchForm()})

# *Done
def postadd(request):
    if request.user.is_authenticated and request.user.username!="admin":
        utilizador = get_object_or_404(Utilizador, username=request.user.username)
        if request.method == "POST" and request.FILES:
            caption = request.POST["caption"]
            photo = request.FILES["photo"]

            if caption and photo:
                Post.objects.create(user=utilizador, image=photo, caption=caption)
                return redirect("home")

        else:
            return redirect("home")
    else:
        return redirect("login")

#*Done
def postdetail(request, _id):
    post = get_object_or_404(Post, id=_id)
    ctx = {
        "post": post,
        "comments": Comment.objects.filter(post=_id),
        "exist_like" : False,
        "form_search": SearchForm()
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

#*Done
def postlike(request, _id):
    if request.user.is_authenticated and request.user.username!="admin":
        return redirect("postdetail", _id)
    else:
        return redirect("login")

#*Done
def postcomment(request, _id):
    if request.user.is_authenticated and request.user.username!="admin":
        redirect("postdetail", _id)
    else:
        return redirect("login")

def profile(request):
    if request.user.is_authenticated and request.user.username!="admin":
        user = get_object_or_404(Utilizador, username=request.user.username)
        try:
            posts = Post.objects.filter(user=user).order_by("-date")
        except ObjectDoesNotExist:
            posts = []

        ctx = {
            "user": user,
            "user_posts": user,
            "posts": posts,
            "following_count": Follow.objects.filter(user=user).count(),
            "followers_count": Follow.objects.filter(following=user).count(),
            "form_search": SearchForm()
        }

        return render(request, "profile.html", ctx)
    else:
        return redirect("login")

def profileUtilizador(request,username):
    print(username)
    user_posts = get_object_or_404(Utilizador, username=username)
    if request.user.is_authenticated and request.user.username!="admin":
        user = get_object_or_404(Utilizador, username=request.user.username)
    else:
        user = None
    try:
        posts = Post.objects.filter(user=user_posts).order_by("-date")
    except ObjectDoesNotExist:
        posts = []

    ctx = {
        "user_posts": user_posts,
        "posts": posts,
        "user": user,
        "is_follower": Follow.objects.filter(following=user_posts, user=user).exists(),
        "following_count": Follow.objects.filter(user=user_posts).count(),
        "followers_count": Follow.objects.filter(following=user_posts).count(),
        "form_search": SearchForm()
    }

    return render(request, "profile.html", ctx)

#*Done
def editProfile(request, username):
    if request.user.is_authenticated and request.user.username!="admin":
        if request.user.username != username:
            return redirect("profile")
        sucesso = False
        utilizador = Utilizador.objects.get(username=username)
        ctx={
            "user": utilizador,
            "form_search": SearchForm()
            }

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

# *Done
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

# *done
def commentdelete(request,_id, _id_comment):
    post = get_object_or_404(Post, id=_id)
    comment = get_object_or_404(Comment, id=_id_comment)
    if request.user.is_authenticated and request.user.username!="admin":
        if request.user.username == comment.user.username or request.user.username == post.user.username:
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
                "form_postedit": EditPostForm(),
                "user": Utilizador.objects.get(username=request.user.username),
                "form_search": SearchForm()
            }
            if request.method == "POST":
                form_postedit = EditPostForm(request.POST, request.FILES)
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

# *Done
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

def follow(request):
    if request.POST.get('action') == 'post':
        following = ''
        followers = ''
        user_id = request.POST.get('user_id')
        user_post_id = request.POST.get('user_posts_id')
        user = get_object_or_404(Utilizador, id=user_id)
        user_post = get_object_or_404(Utilizador, id=user_post_id)
        
        if Follow.objects.filter(user=user, following=user_post).exists():
            print("unfollow")
            Follow.objects.filter(user=user, following=user_post).delete()
            type = 'unfollow'
            following = Follow.objects.filter(user=user_post).count()
            followers = Follow.objects.filter(following=user_post).count()
        else:
            Follow.objects.create(user=user, following=user_post)
            type = 'follow'
            following = Follow.objects.filter(user=user_post).count()
            followers = Follow.objects.filter(following=user_post).count()
        
        return JsonResponse({'type': type, 'following': following, 'followers': followers})

def search(request):
    if request.method == "POST":
        form_search = SearchForm(request.POST)
        if form_search.is_valid():
            search = form_search.cleaned_data["search"]
            try:
                users = Utilizador.objects.filter(username__icontains=search)
            except ObjectDoesNotExist:
                users = list ()

            try:
                user = Utilizador.objects.get(username=request.user.username)
            except ObjectDoesNotExist:
                user = None
            
            result = []
            for result_user in users:
                following = Follow.objects.filter(user=result_user).count()
                followers = Follow.objects.filter(following=result_user).count()
                result.append((result_user,following,followers))

            ctx = {
                "result": result,
                "user": user,
                "form_search": form_search
            }
            return render(request,"searchresult.html",ctx)
        
    else:
        return redirect("searchresult")


def search_result(request):
    ctx={"form_search": SearchForm()}
    try:
        user = Utilizador.objects.get(username=request.user.username)
        ctx["user"]=user
    except ObjectDoesNotExist:
        user = None

    return render(request, "searchresult.html", ctx)

def error404(request, exception):
    user=None
    if request.user.is_authenticated and request.user.username!="admin":
        user = Utilizador.objects.get(username=request.user.username)
    ctx = {
        "form_search": SearchForm(),
        "exception": exception,
        "user": user
    }
    return render(request, '404.html',ctx)

def error500(request):
    user=None
    if request.user.is_authenticated and request.user.username!="admin":
        user = Utilizador.objects.get(username=request.user.username)
    ctx = {
        "form_search": SearchForm(),
        "user": user
    }
    return render(request, '404.html',ctx)