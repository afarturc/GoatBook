from django.db import models
from django.contrib.auth import get_user_model

user=get_user_model()

class Utilizador (models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    bio = models.CharField(max_length=256, blank=True)
    email = models.EmailField(max_length=50)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, default= 'default.png')
    following = models.ManyToManyField("self", blank=True, related_name="followers", default=None)
    following_count = models.IntegerField(default=0)
    #post_count = models.IntegerField(default=0)

    def update_image(self, file):
        self.profile_pic.storage.delete(self.profile_pic.name)
        self.profile_pic = file

    def update_password(self, password):
        self.password = password

    def remove_follow(self, user):
        self.following.remove(user)    
        self.following_count -= 1
        super().save()

    def add_follow(self, user):
        self.following.add(user)
        self.following_count += 1
        super().save()

    

    # def get_post_count(self):
    #     return self.posts.count()
    
    def __str__(self):
        return self.username

class Post(models.Model):
    user = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    caption = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_pics', blank=True)
    likes = models.ManyToManyField(Utilizador, related_name='likes', blank=True, default=None)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption

    def delete(self):
        self.image.storage.delete(self.image.name)
        super().delete()
    
    def get_likes_count(self):
        return self.likes.count()
    
    def user_has_liked(self, user):
        return self.likes.filter(id=user.id).exists()

    def remove_like(self, user):
        self.likes.remove(user)    
        self.like_count -= 1
        super().save()

    def add_like(self, user):
        self.likes.add(user)
        self.like_count += 1
        super().save()
    
    def add_comment(self):
        self.comment_count += 1
        super().save()
    
    def remove_comment(self):
        self.comment_count -= 1
        super().save()

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
