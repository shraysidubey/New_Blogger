from django.contrib.auth.models import User
from blogs.models import blog,UserProfile, Comment_on_blog
from django import forms
from django import forms
from django import forms
from blogs.models import blog

class UserForm(forms.ModelForm):                                                  #create form for registration
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User                                                             #using User django model
        fields = ('username', 'email', 'password')                               #include or visible fields in form


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user','follows',)


class BlogForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    body = forms.CharField(max_length=5000)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = blog
        fields = ('title', 'body',)

class Comment_on_blogForm(forms.ModelForm):
    comment = forms.CharField(max_length=500)

    class Meta:
        model = Comment_on_blog
        fields = ('comment',)


