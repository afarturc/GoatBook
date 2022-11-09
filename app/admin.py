from django.contrib import admin
from app.models import User, Post, Comment, Like

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
