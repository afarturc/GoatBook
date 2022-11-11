from django.db import models
from django.contrib.auth import get_user_model

user=get_user_model()

class Utilizador (models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    bio = models.CharField(max_length=256, blank=True)
    email = models.EmailField(max_length=50)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, default= 'default.jpeg')
    following = models.ManyToManyField("self", blank=True, related_name="followers", symmetrical=False)

    def __str__(self):
        return self.username

class Post(models.Model):
    user = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    caption = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_pics', blank=True)
    likes = models.ManyToManyField(Utilizador, related_name='likes', blank=True, default=None)
    comments = models.ManyToManyField(Utilizador, related_name='comments', blank=True, default=None)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption

    class Meta:
        ordering = ['-date']

class Like(models.Model):
    user = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-date']

class Comment(models.Model):
    user = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['-date']

