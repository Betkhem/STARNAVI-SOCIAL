from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.related import ForeignKey
from django.dispatch.dispatcher import receiver
from django.urls import reverse

# Create your models here.

class UserModel(AbstractUser): #UserModel - basically all info about user
    first_name = models.CharField(max_length=200, blank=True)
    last_name  = models.CharField(max_length=200, blank=True)
    email      = models.EmailField(max_length=200, blank=True, unique=True)
    bio        = models.TextField(default="no bio...", max_length=300)
    updated    = models.DateTimeField(auto_now=True)
    created    = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'


    def get_all_Post_authors(self):
        return self.Posts.all()


    def get_Post_number(self): #total amount of posts created
        return self.Posts.all().count()


    def get_all_Post_likes(self): #total amount of likes ever 
        likes = self.likemodel_set.all() #likemodel = LikeModel from Post/models.py
        amt_times_liked = 0
        for i in likes:
            if i.like == 'like':
                amt_times_liked += 1
        return amt_times_liked

    
    def get_like_count(self):
        post = self.Posts.all()
        amt_times_liked = 0
        for i in post:
            amt_times_liked += i.liked.all().count()
        return amt_times_liked


    def __str__(self):
        return f"{self.username}-{self.created.strftime('%d-%m-%Y')}"


    def get_absolute_url(self):
        return reverse("User:account-detail", kwargs={"id": self.id}) 
