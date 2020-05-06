from django import forms
from .models import Account
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

def validate_id(value):
    account = Account.objects.filter(idnum=value)
    if account:
        raise ValidationError("This ID number is already used")
    else:
        return value
        
#https://medium.com/@himanshuxd/how-to-create-registration-login-webapp-with-django-2-0-fd33dc7a6c67
class UserForm(forms.ModelForm):
    
    first_name = forms.CharField(max_length=128, 
                widget=forms.TextInput(attrs={'class': 'validate'}), required = True)
    last_name = forms.CharField(max_length=128, 
                widget=forms.TextInput(attrs={'class': 'validate'}), required = True)
    password = forms.CharField(max_length=128,
                widget=forms.PasswordInput(attrs={'class': 'validate'}), required = True, 
               validators=[validate_password])
    username = forms.CharField(max_length=128, 
            widget=forms.TextInput(attrs={'class': 'validate'}), required = True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'validate'}), required=True)
    idnum = forms.CharField(widget=forms.NumberInput(attrs={'class': 'validate invalid'}), required=True, label = 'ID Number',
                validators=[validate_id])
   
   
    class Meta():
        model = Account
        fields = ('first_name', 'last_name', 'username','password','email','idnum')
        labels = {'first_name': 'First Name','last_name': 'Last Name','password': 'Password',
            'email': 'Email', 'idnum': 'ID Number'}

    def __init__(self,*args,**kwargs):
        username_err = kwargs.pop('username_err', None)
        pass_err = kwargs.pop('password_err', None)
        email_err = kwargs.pop('email_err', None)
        idnum_err = kwargs.pop('idnum_err', None)
        super(UserForm,self).__init__(*args,**kwargs)

        if username_err:
            self.fields['username'].widget.attrs.update({'class': 'invalid'})
        if idnum_err:
            self.fields['ID Number'].widget.attrs.update({'class': 'valid'})
        if pass_err:
            self.fields['password'].widget.attrs.update({'class': 'invalid'})
        if email_err:
            self.fields['email'].widget.attrs.update({'class': 'invalid'})

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Account
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'idnum')


