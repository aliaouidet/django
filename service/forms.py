from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.contrib.auth.forms import UserCreationForm

from ArtyProd import settings
from .models import BlogComment, Project, User


from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

from django.contrib.auth import get_user_model
class blogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content']
User = get_user_model()
from .models import Article
class ProjectForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter project title', 'class': 'form-control'})
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Enter project description', 'class': 'form-control', 'rows': 5})
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'placeholder': 'Select start date', 'class': 'form-control datepicker'})
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'placeholder': 'Select end date', 'class': 'form-control datepicker'})
    )

    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date']
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

from .models import Comment
class CommentForm(forms.ModelForm):
    text = forms.CharField(max_length=30, required=True, widget=forms.Textarea(attrs={'placeholder': 'Enter your comment', 'class': 'form-control mb-3','id':'comment','cols':'30','rows':'5'}))

    class Meta:
        model = Comment
        fields = ('text',)
class CustomRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your first name', 'class': 'form-input'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your last name', 'class': 'form-input'}))
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'placeholder': 'Upload your photo', 'class': 'form-input'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-input'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'form-input'}))
    password1 = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'form-input', 'id': 'password'}))
    password2 = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'class': 'form-input', 'id': 're_password'}))


    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'photo','email', 'phone', 'password1', 'password2')
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)


class EmailLoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()
        return email

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your first name', 'class': 'form-input'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your last name', 'class': 'form-input'}))
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'placeholder': 'Upload your photo', 'class': 'form-input'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-input'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'form-input'}))
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your username', 'class': 'form-input'}))
    password1 = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'form-input', 'id': 'password'}))
    password2 = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'class': 'form-input', 'id': 're_password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'photo', 'email', 'phone', 'username', 'password1', 'password2']

