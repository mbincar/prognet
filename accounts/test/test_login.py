from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.account.views import LoginView
from allauth.utils import get_user_model
from django.core import mail
from django.shortcuts import reverse
from django.test import TestCase, RequestFactory

from .. import forms


class LoginTestCase(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'john',
            'email': 'john@example.com',
            'password': 'studiocode'}

    def create_user(self, user_data, verified=True):
        user = get_user_model()(username=user_data['username'])
        user.set_password(user_data['password'])
        user.save()
        EmailAddress.objects.create(
            user=user, email=user_data['email'],
            primary=True, verified=verified)
        return user

    def test_login_view_use_correct_template(self):
        response = self.client.get(reverse('account_login'))
        self.assertTemplateUsed(response, 'account/login.html')

    def test_email_verification_is_mandatory(self):
        self.create_user(user_data=self.user_data, verified=False)
        response = self.client.post(reverse('account_login'), data={
            'login': self.user_data['username'],
            'password': self.user_data['password']})
        self.assertTrue(response.wsgi_request.user.is_anonymous())
        self.assertFalse(response.wsgi_request.user.is_authenticated())
        self.assertRedirects(
            response, reverse('account_email_verification_sent'))

    def test_login_with_username(self):
        self.create_user(user_data=self.user_data)
        response = self.client.post(reverse('account_login'), data={
            'login': self.user_data['username'],
            'password': self.user_data['password']})
        self.assertFalse(response.wsgi_request.user.is_anonymous())
        self.assertTrue(response.wsgi_request.user.is_authenticated())

    def test_login_with_email(self):
        self.create_user(user_data=self.user_data)
        response = self.client.post(reverse('account_login'), data={
            'login': self.user_data['email'],
            'password': self.user_data['password']})
        self.assertFalse(response.wsgi_request.user.is_anonymous())
        self.assertTrue(response.wsgi_request.user.is_authenticated())

    def test_valid_loginform_data(self):
        self.create_user(self.user_data)
        form = forms.LoginForm(data={
            'login': self.user_data['username'],
            'password': self.user_data['password']})
        self.assertTrue(form.is_valid())

    def test_invalid_username_passowrd_loginform_data(self):
        self.create_user(self.user_data)
        form = forms.LoginForm(data={
            'login': self.user_data['username'],
            'password': self.user_data['password'] + 'false'})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.non_field_errors()), 1)
        self.assertEqual(
            form.non_field_errors()[0],
            'The username and/or password you specified are not correct.')

    def test_invalid_email_password_loginform_data(self):
        self.create_user(self.user_data)
        form = forms.LoginForm(data={
            'login': self.user_data['email'],
            'password': self.user_data['password'] + 'false'})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.non_field_errors()), 1)
        self.assertEqual(
            form.non_field_errors()[0],
            'The e-mail address and/or password you specified are not correct.')

    def test_django_message_on_valid_login(self):
        self.create_user(self.user_data)
        response = self.client.post(reverse('account_login'), data={
            'login': self.user_data['username'],
            'password': self.user_data['password']})
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Successfully signed in as %s.' % (self.user_data['username']))

    def test_redirect_to_login_root_for_required_login_root(self):
        self.create_user(self.user_data)
        response = self.client.get(reverse('account_change_password'))
        self.assertRedirects(response, reverse(
            'account_login') + "?next=%s" % (reverse('account_change_password')))
