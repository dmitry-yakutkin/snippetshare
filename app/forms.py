from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=30)
    password = forms.CharField(
        label='password', widget=forms.PasswordInput(), max_length=30)


class RegisterForm(forms.Form):
    username = forms.CharField(label='username', max_length=30)
    email = forms.EmailField(label='email', max_length=40)
    password = forms.CharField(
        label='password', widget=forms.PasswordInput(), max_length=30)


class MessageForm(forms.Form):
    text = forms.CharField(
        label='text', widget=forms.Textarea(), max_length=200)
