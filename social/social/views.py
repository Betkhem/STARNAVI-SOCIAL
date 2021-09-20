from django.shortcuts import render
from Post.models import PostModel, UserModel


def home_view(request):
    all_users = UserModel.objects.all()
    all_posts = PostModel.objects.all()
    context = {
        'all_posts':all_posts,
        'all_users':all_users,
    }
    return render(request, 'main/home_page.html', context)