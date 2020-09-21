from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('book_title', 'book_author','book_label','book_int','text')

class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #htmlの表示を変更可能にします
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    class Meta:
       model = User
       fields = ("username", "password1", "password2",)

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       #htmlの表示を変更可能にします
       self.fields['username'].widget.attrs['class'] = 'form-control'
       self.fields['password'].widget.attrs['class'] = 'form-control'