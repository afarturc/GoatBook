from django.contrib import admin
from app.models import Utilizador, Post, Comment, Like

# Register your models here.
admin.site.register(Utilizador)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
