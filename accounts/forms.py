from allauth.account import forms

attrs_login = {'class': 'form-control'}
attrs_focus = {'class': 'form-control', 'autofocus': ''}


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


class ResetPasswordForm(forms.ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = attrs_login['class']


class ResetPasswordKeyForm(forms.ResetPasswordKeyForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = attrs_login['class']
        self.fields['password2'].widget.attrs['class'] = attrs_login['class']


class ChangePasswordForm(forms.ChangePasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['oldpassword'].widget.attrs['class'] = attrs_login['class']
        self.fields['password1'].widget.attrs['class'] = attrs_login['class']
        self.fields['password2'].widget.attrs['class'] = attrs_login['class']


class SetPasswordForm(forms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = attrs_login['class']
        self.fields['password2'].widget.attrs['class'] = attrs_login['class']
