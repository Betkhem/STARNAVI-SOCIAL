from django.urls import path
from .views import list_posts, like_post, post_detail_view, Analitic_Posts_View

app_name = 'Post'

urlpatterns = [
    path('', list_posts, name='list_posts'),
    path('liked/',like_post , name='like_post'),
    path('<int:id>/', post_detail_view, name='post-detail'),
    path('analitics/date_from=<date_from>&date_to=<date_to>/', Analitic_Posts_View.as_view(), name='post_likes'),
]   