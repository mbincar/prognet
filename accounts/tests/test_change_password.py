from allauth.account.models import EmailAddress
from allauth.utils import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from .. import forms


class ChangePasswordTestCase(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'john',
            'email': 'john@example.com',
            'password': 'stdudiocode'}

    def create_user(self, user_data, verified=True):
        user = get_user_model()(username=user_data['username'])
        user.set_password(user_data['password'])
        user.save()
        EmailAddress.objects.create(
            user=user, email=user_data['email'],
            primary=True, verified=verified)
        return user

    def login_user(self, user_data):
        response = self.client.post(reverse('account_login'), data={
            'login': user_data['username'],
            'password': user_data['password']})
        return response

    def test_change_password_form_is_valid(self):
        user = self.create_user(self.user_data)
        form = forms.ChangePasswordForm(user=user, data={
            'oldpassword': self.user_data['password'],
            'password1': self.user_data['password'] + 'new123',
            'password2': self.user_data['password'] + 'new123'})
        self.assertTrue(form.is_valid())

    def test_change_password_invalid_for_wrong_old_password(self):
        user = self.create_user(self.user_data)
        form = forms.ChangePasswordForm(user=user, data={
            'oldpassword': self.user_data['password'] + 'new',
            'password1': self.user_data['password'] + 'new123',
            'password2': self.user_data['password'] + 'new123'})
        self.assertFalse(form.is_valid())

    # need rework
    # def test_change_password_invalid_if_newpassword_equalto_oldpassword(self):
    #     user = self.create_user(self.user_data)
    #     form = forms.ChangePasswordForm(user=user, data={
    #         'oldpassword': self.user_data['password'],
    #         'password1': self.user_data['password'],
    #         'password2': self.user_data['password']})
    #     self.assertFalse(form.is_valid())
