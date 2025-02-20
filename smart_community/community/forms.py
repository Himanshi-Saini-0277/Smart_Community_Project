from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from community.models import Post, UserProfile
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image' ]

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(max_length=255, required=True)
    phone = forms.CharField(max_length=10, required=True)
    pincode = forms.CharField(max_length=6, required=True)
    town = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'phone', 'pincode', 'town', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create the user profile
            UserProfile.objects.create(
                user=user,
                username=self.cleaned_data['username'],
                full_name=self.cleaned_data['full_name'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone'],
                pincode=self.cleaned_data['pincode'],
                town=self.cleaned_data['town']
            )
        return user
