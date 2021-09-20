from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import PostModel, LikeModel
from User.models import UserModel
from .forms import PostModelForm, CommentPostModelForm

import json
from User.serializers import LikeSerializer
from rest_framework import generics

# Create your views here.


def list_posts(request):
    if request.user.is_authenticated == False:
        return redirect("home_page")
    all_posts = PostModel.objects.all()
    user = UserModel.objects.get(username=request.user.username)
    post_form = PostModelForm()
    comment_form = CommentPostModelForm()

    if 'name_for_post_form' in request.POST:
        print(request.POST)
        post_form = PostModelForm(request.POST, request.FILES)
        if post_form.is_valid():
            obj_form = post_form.save(commit=False) # form is not saved yet
            obj_form.author = user
            obj_form.save()
            post_form = PostModelForm()
    
    if 'name_for_comment_form' in request.POST:
        print(request.POST)
        comment_form = CommentPostModelForm(request.POST)
        if comment_form.is_valid():
            obj_form = comment_form.save(commit=False) # form is not saved yet
            obj_form.user = user
            obj_form.post = PostModel.objects.get(id=request.POST.get('id2'))
            obj_form.save()
            comment_form = CommentPostModelForm()
    
    context = {
        'all_posts':all_posts,
        'account':user,
        'post_form':post_form,
        'comment_form':comment_form,
    }
    print(user)
    return render(request, "Post/list_posts.html", context)


def like_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('id')
        post = PostModel.objects.get(id=post_id)
        account = UserModel.objects.get(username=user.username) #username=request.user.username
        if account in post.liked.all():
            post.liked.remove(account)
        else:
            post.liked.add(account)

        like,created = LikeModel.objects.get_or_create(user=account, post_id=post_id) 
        #created is boolen value, if created =True it means that the post didn't exist before, it was created
        if not created:
            if like.like=='Like':
                like.like='Unlike'
            else:
                like.like = 'Like'
        else:
            like.like = 'Like'

            post.save()
            like.save()
        # like."like" is value of LikeModel

    return redirect("Post:list_posts")


def post_detail_view(request, id):
    obj = get_object_or_404(PostModel, id=id)
    context = {
        "postname": obj.title,
        "post":obj,
    }
    return render(request, "Post/post_info.html", context)


# Example url: /api/analitics/?date_from=2020-02-02&date_to=2020-02-15
class Analitic_Posts_View(generics.ListAPIView):
    serializer_class = LikeSerializer
#Example url: http://127.0.0.1:8000/Post/analitics/date_from%3D2021-09-19&date_to%3D2021-09-2/

    def get(self, request, *args, **kwargs):
        likes_analitic = LikeModel.objects.filter(created__range=[kwargs['date_from'], kwargs['date_to']])
        if len(likes_analitic) > 0:
            mimetype = 'application/json'
            return HttpResponse(f'likes by period: {len(likes_analitic)}')
        else:
            return HttpResponse("no likes on this period")


