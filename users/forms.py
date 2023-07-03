from django import forms


from .models import Profile


class Images(forms.Form):
    image = forms.ImageField()


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'date_of_birth', 'location', 'about_me', 'image')
