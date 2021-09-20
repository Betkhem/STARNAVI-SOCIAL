from django.contrib import admin
from .models import PostModel, ComentPostModel, LikeModel

# Register your models here.

admin.site.register(PostModel)
admin.site.register(ComentPostModel)
admin.site.register(LikeModel)