"""TPW_Project1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls), # user: admin, password: admin
    path("", views.home, name="home"),

    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("profile/", views.profile, name="profile"),
    path("profile/<str:username>", views.profileUtilizador, name="profile"),
    path("profile/<str:username>/edit", views.editProfile, name="editProfile"),

    path("postadd/", views.postadd, name="postadd"),
    path("post/<int:_id>/", views.postdetail, name="postdetail"),
    path("post/<int:_id>/like/", views.postlike, name="like"),
    path("post/<int:_id>/comment/", views.postcomment, name="comment"),
    path("post/<int:_id>/delete/", views.postdelete, name="deletepost"),
    path("post/<int:_id>/edit/", views.postedit, name="edit"),
    path("like/", views.like, name="like_post"),
    

    path("post/<int:_id>/comment/<int:_id_comment>/delete/", views.commentdelete, name="deletecomment"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)