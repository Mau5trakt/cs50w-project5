from django import forms
from .models import CustomUser


class RegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input'

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email']

        labels = {
            'email': "The email of you spotify account"
        }

        help_texts = {
            'username': None
        }

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords don\'t match')

        def clean_email(self):
            data = self.cleaned_data['email']
            if CustomUser.objects.filter(email=data).exists():
                raise forms.ValidationError('email already in use')
            return data

        def clean_username(self):
            username = self.cleaned_data['username']
            if CustomUser.objects.filter(username__iexact=username).exists():
                raise forms.ValidationError('Username already in use')
            return username

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input'

    username = forms.CharField()
    # Widget to render the input with password type
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        help_texts = {
            'username': None,
            'password': None
        }

    def clean_username(self):
        username = self.cleaned_data['username']