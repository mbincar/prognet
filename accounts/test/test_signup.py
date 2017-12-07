from allauth.account.models import EmailAddress
from allauth.utils import get_user_model
from django.core import mail
from django.shortcuts import reverse
from django.test import TestCase

from .. import forms


class SignupTestCase(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'john',
            'email': 'john@example.com',
            'password': 'studiocode'}
        self.user2_data = {
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'studiocode'
        }

    def create_user(self, user_data, verified=True):
        user = get_user_model()(username=user_data['username'])
        user.set_password(user_data['password'])
        user.save()
        EmailAddress.objects.create(
            user=user, email=user_data['email'],
            primary=True, verified=verified)
        return user

    def test_signup_form_is_valid(self):
        form = forms.SignupForm(data={
            'username': self.user_data['username'],
            'email': self.user_data['email'],
            'password1': self.user_data['password'],
            'password2': self.user_data['password']})
        self.assertTrue(form.is_valid())

    def test_signup_form_is_invalid_for_unmatch_password(self):
        form = forms.SignupForm(data={
            'username': self.user_data['username'],
            'email': self.user_data['email'],
            'password1': self.user_data['password'],
            'password2': self.user_data['password'] + 'false'})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(
            form.errors['password2'],
            ['You must type the same password each time.'])

    def test_signup_form_error_for_invalid_email_format(self):
        form = forms.SignupForm(data={
            'username': self.user_data['username'],
            'email': self.user_data['username'],
            'password1': self.user_data['password'],
            'password2': self.user_data['password']})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(
            form.errors['email'],
            ['Enter a valid email address.'])

    def test_signup_form_error_for_duplicate_username(self):
        self.create_user(user_data=self.user_data)
        form = forms.SignupForm(data={
            'username': self.user_data['username'],
            'email': self.user2_data['email'],
            'password1': self.user2_data['password'],
            'password2': self.user2_data['password']})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(
            form.errors['username'],
            ['A user with that username already exists.'])

    def test_signup_form_error_for_duplicate_email(self):
        self.create_user(user_data=self.user_data)
        form = forms.SignupForm(data={
            'username': self.user2_data['username'],
            'email': self.user_data['email'],
            'password1': self.user2_data['password'],
            'password2': self.user2_data['password']})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(
            form.errors['email'],
            ['A user is already registered with this e-mail address.'])

    def test_signup_view_use_correct_template(self):
        response = self.client.get(reverse('account_signup'))
        self.assertTemplateUsed('account/signup.html')

    def test_confirmation_email_is_sent_after_signup(self):
        response = self.client.post(reverse('account_signup'), data={
            'username': self.user_data['username'],
            'email': self.user_data['email'],
            'password1': self.user_data['password'],
            'password2': self.user_data['password']})
        self.assertRedirects(
            response,
            reverse('account_email_verification_sent'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user_data['email']])

    def test_user_not_login_right_after_signup(self):
        response = self.client.post(reverse('account_signup'), data={
            'username': self.user_data['username'],
            'email': self.user_data['email'],
            'password1': self.user_data['password'],
            'password2': self.user_data['password']})
        self.assertTrue(response.wsgi_request.user.is_anonymous())
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_django_message_is_sent_after_signup(self):
        response = self.client.post(reverse('account_signup'), data={
            'username': self.user_data['username'],
            'email': self.user_data['email'],
            'password1': self.user_data['password'],
            'password2': self.user_data['password']})
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Confirmation e-mail sent to %s.' % (self.user_data['email']))
