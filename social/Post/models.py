from django.db import models
from User.models import UserModel
from django.core.validators import FileExtensionValidator
from django.urls import reverse

# Create your models here.

class PostModel(models.Model):
    title = models.TextField()
    image = models.ImageField(upload_to='Post/static/images', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    liked = models.ManyToManyField(UserModel, blank=True, related_name='likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='Posts') # 

    def __str__(self):
        return str(self.title[:20])

    def num_likes(self):
        return self.liked.all().count()

    def num_comments(self):
        return self.comentpostmodel_set.all().count()


    def get_absolute_url(self):
        return reverse("Post:post-detail", kwargs={"id": self.id})

    
    class Meta:
        ordering = ('-created',)


class ComentPostModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


LIKE_CHOICES = (
    ('like', 'like'),
    ('unlike', 'unlike'),
)


class LikeModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    like = models.CharField(choices=LIKE_CHOICES, max_length=9)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.post} - {self.like}"