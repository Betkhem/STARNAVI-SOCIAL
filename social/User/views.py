from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import response
from .models import UserModel
from .forms import UserModelForm
from django.contrib.auth.decorators import login_required
#rest_framework imports
import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, LastUserLoginSerializer
import jwt, datetime
from rest_framework import generics

# Create your views here.

# Example url /api/analitics/?date_from=2020-02-02&date_to=2020-02-15


@login_required
def account_view(request):
    if request.user.is_authenticated == False:
        return(HttpResponse("Sign up or sign in first"))
    else:
        user_instance = UserModel.objects.get(username=request.user.username)
        form = UserModelForm(request.POST or None, instance=user_instance)
        Success = False
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                Success = True
        
        context = {
            'user':user_instance,
            'form':form,
            'success':Success,
        }
    return render(request, "User/account.html", context)



def account_detail_view(request, id):
    obj = get_object_or_404(UserModel, id=id)
    context = {
        "username": obj.username
    }
    return render(request, "User/account_info.html", context)


# Authefication part.


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) #expresion inside the bracets will raise an error if data isn't valid
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = UserModel.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not faund')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        #return via coockies
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt':token
        }
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError: #Expiration time is automatically verified in jwt.decode() and raises jwt.ExpiredSignatureError if the expiration time is in the past
            raise AuthenticationFailed('Unauthenticated')

        user = UserModel.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class Logout(APIView):
    def post(self, request): #removing the cookie
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'success'
        }
        return response


class LastUserLoginView(generics.RetrieveAPIView):
    queryset = UserModel.objects.all()
    serializer_class = LastUserLoginSerializer

