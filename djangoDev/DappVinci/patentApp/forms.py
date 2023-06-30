from django import forms
from django.contrib.auth.models import User

# login form
class LoginForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=18,widget=forms.TextInput(attrs={'class':'form-select','placeholder':'username'} ))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class':'form-select','placeholder':'password'} ))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
