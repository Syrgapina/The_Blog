from django import forms
from .models import PostComment, NewPost


class Images(forms.Form):
    image = forms.ImageField()


class Posts(forms.ModelForm):
    class Meta:
        model = NewPost
        fields = '__all__'


class Comments(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = '__all__'
