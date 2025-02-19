from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from community.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image' ]

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=10, required=True)
    password = forms.CharField(max_length=255, required=True)
    postal_code = forms.CharField(max_length=6, required=True)
    postal_area = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone_number', 'postal_area', 'postal_code', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
