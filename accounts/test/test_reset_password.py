from allauth.account.models import EmailAddress
from allauth.utils import get_user_model
from django.core import mail
from django.shortcuts import reverse
from django.test import TestCase

from .. import forms


class ResetPasswordTestCase(TestCase):

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

    def test_reset_password_use_correct_template(self):
        response = self.client.get(reverse('account_reset_password'))
        self.assertTemplateUsed(response, 'account/password_reset.html')
        self.assertTemplateUsed(response, 'base-auth.html')

    def test_reset_password_form_is_valid(self):
        self.create_user(self.user_data)
        form = forms.ResetPasswordForm(data={
            'email': self.user_data['email']})
        self.assertTrue(form.is_valid())

    def test_form_is_invalid(self):
        form = forms.ResetPasswordForm(data={
            'email': self.user_data['email']})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(
            form.errors['email'],
            ['The e-mail address is not assigned to any user account'])

    def test_invalid_email_on_reset_password_flow(self):
        self.create_user(self.user_data)
        response = self.client.post(
            reverse('account_reset_password'),
            data={'email': self.user_data['email'] + 'doe'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/password_reset.html')
        self.assertFalse(response.context_data['form'].is_valid())
        self.assertFormError(
            response, 'form', 'email',
            "The e-mail address is not assigned to any user account")

    def test_unmatch_password_on_reset_password_flow(self):
        self.create_user(self.user_data)
        # Request new password
        response = self.client.post(
            reverse('account_reset_password'),
            data={'email': self.user_data['email']})
        self.assertRedirects(
            response, reverse('account_reset_password_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user_data['email']])
        body = mail.outbox[0].body
        self.assertGreater(body.find('http://'), 0)

        # Extract URL for password_reset_from_key view and accesst it
        url = body[body.find(
            str(reverse('account_reset_password'))):].split()[0]
        response = self.client.get(url)

        # Follow the redirect the actual password reset page with the key
        # hidden.
        url = response.url
        response = self.client.get(url)
        self.assertTemplateUsed('account_reset_password_from_key.html')
        self.assertFalse('token_fail' in response.context_data)

        # Try to submit unmatch new password
        response = self.client.post(url, data={
            'password1': self.user_data['password'] + 'new123',
            'password2': self.user_data['password'] + 'new321'})
        self.assertFalse(response.context_data['form'].is_valid())
        self.assertFormError(
            response, 'form', 'password2',
            'You must type the same password each time.')

    def test_valid_reset_password_flow(self):
        user = self.create_user(self.user_data)
        # Request new password
        response = self.client.post(
            reverse('account_reset_password'),
            data={'email': self.user_data['email']})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user_data['email']])
        self.assertRedirects(response, reverse('account_reset_password_done'))
        body = mail.outbox[0].body
        self.assertGreater(body.find('http://'), 0)

        # Extract URL for password_reset_from_key view and accesst it
        url = body[body.find(
            str(reverse('account_reset_password'))):].split()[0]
        response = self.client.get(url)

        # Follow the redirect the actual password reset page with the key
        # hidden.
        url = response.url
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'base-auth.html')
        self.assertTemplateUsed(
            response, 'account/password_reset_from_key.html')
        self.assertFalse('token_fail' in response.context_data)

        # Reset the password
        response = self.client.post(url, data={
            'password1': self.user_data['password'] + 'new123',
            'password2': self.user_data['password'] + 'new123'})
        self.assertRedirects(
            response,
            reverse('account_reset_password_from_key_done'))

        # Check the new password in effect
        user = get_user_model().objects.get(pk=user.pk)
        self.assertTrue(user.check_password(
            self.user_data['password'] + 'new123'))

        # Trying to reset the password against the same URL (or any other
        # invalid/obsolete URL) returns a bad token response
        response = self.client.post(url, data={
            'password1': self.user_data['password'] + 'new123',
            'password2': self.user_data['password'] + 'new123'})
        self.assertTemplateUsed(
            response, 'account/password_reset_from_key.html')
        self.assertTrue('token_fail' in response.context_data)

        # Same should happen when accessing the page directly
        response = self.client.get(url)
        self.assertTemplateUsed(
            response, 'account/password_reset_from_key.html')
        self.assertTrue('token_fail' in response.context_data)
