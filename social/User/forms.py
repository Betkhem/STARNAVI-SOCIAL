from django import forms
from .models import UserModel

class UserModelForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields=(
            'first_name', 
            'last_name', 
            'bio', 
            'email',
            'username',
        )