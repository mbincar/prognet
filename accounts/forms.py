from allauth.account import forms

attrs_login = {'class': 'input is-large'}
attrs_focus = {'class': 'input is-large', 'autofocus': ''}


class LoginForm(forms.LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs['class'] = attrs_login['class']
        self.fields['password'].widget.attrs['class'] = attrs_login['class']


class SignupForm(forms.SignupForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = attrs_login['class']
        self.fields['email'].widget.attrs['class'] = attrs_login['class']
        self.fields['password1'].widget.attrs['class'] = attrs_login['class']
        self.fields['password2'].widget.attrs['class'] = attrs_login['class']
