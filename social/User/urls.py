from django.urls import path
from .views import account_view, account_detail_view, RegisterView, LoginView, UserView, Logout, LastUserLoginView

app_name = 'User'

urlpatterns = [
    path('sign_up', RegisterView.as_view(), name='sign_up_page'),
    path('sign_in', LoginView.as_view(), name='sign_in_page'),
    path('log_out', Logout.as_view(), name='log_out_page'),

    path('account', account_view, name='account_page'),
    path('<int:id>/', account_detail_view, name='account-detail'),
    path('lastuser_login/<int:pk>', LastUserLoginView.as_view(), name='user_activity'),
]