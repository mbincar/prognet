from allauth.account import forms

attrs = {'class': 'input is-large'}


class LoginForm(forms.LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs = attrs
        self.fields['login'].widget.attrs['placeholder'] = 'Username or email'
        self.fields['login'].widget.attrs['autofocus'] = ''
        self.fields['password'].widget.attrs = attrs
        self.fields['password'].widget.attrs['placholder'] = 'Your Password'
