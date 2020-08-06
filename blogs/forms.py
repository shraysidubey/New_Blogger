from django.contrib.auth.models import User
from blogs.models import blog,UserProfile
from django import forms
from django import forms
from django import forms
from blogs.models import blog

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)


class BlogForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    body = forms.CharField(max_length=5000)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = blog
        fields = ('title', 'body',)



