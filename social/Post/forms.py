from django import forms
from .models import PostModel, ComentPostModel

class PostModelForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    class Meta:
        model = PostModel
        fields = ['title', 'image']

class CommentPostModelForm(forms.ModelForm):
    comment = forms.CharField(label='',
        widget=forms.TextInput(attrs={'placeholder': 'Comment the post here'}))
    class Meta:
        model = ComentPostModel
        fields = ['comment']