from django import forms
from django.contrib.auth.models import User
from .models import PatentContent, DepositInfo

# login form
class LoginForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=18,widget=forms.TextInput(attrs={'class':'form-select','placeholder':'username'} ))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class':'form-select','placeholder':'password'} ))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


# registration form
class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=18, widget=forms.TextInput(attrs={'placeholder':'name on this platform'}))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder':'your password'}))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder':'first name'}))
    last_name = forms.CharField(max_length=20,  widget=forms.TextInput(attrs={'placeholder':'last name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'name@example.com'}))
    address = forms.CharField(max_length=20,  widget=forms.TextInput(attrs={'placeholder':'your address'}))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

DATE_ORDER = [('most recent', 'MOST RECENT'), ('least recent', "LEAST RECENT")]


# creates a list of all owners and adds the "any" option
OWNERS = [(owner.id, owner) for owner in list(User.objects.all())]
OWNERS.append(['any', 'any'])

# Search bar form
class SearchBarForm(forms.Form):

    search_filter = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class':'form-control text-center',
            'placeholder':'Search a Patent'
            }
    ))
        
    patent_order = forms.ChoiceField(
        choices=DATE_ORDER,
        required=False,
        initial='MOST RECENT',
        widget=forms.Select(attrs={
            'class':'form-select',
            'placeholder':'',
        }
    ))

    owner_filter = forms.ChoiceField(choices=OWNERS,
        required=False,
        initial='any',
        widget=forms.Select(attrs={
            'class':'form-select',
            'placeholder':''
        }
    ))
    


# new patent form
class NewPatentForm(forms.ModelForm):
    
    class Meta:
        model = PatentContent
        fields = ('title','sector', 'introduction', 'description', 'claims', 'image',)


        

# deposit info form
class DepositInfoForm(forms.ModelForm):

    class Meta:
        model = DepositInfo
        fields = ('currentAssignee', 'inventors')
    
    def __init__(self, *args, **kwargs):
        super(DepositInfoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'