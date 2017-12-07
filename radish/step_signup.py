from io import StringIO

from hamcrest import assert_that, contains_string, equal_to, starts_with
from radish import steps
from selenium.webdriver import Chrome
from unittest.mock import patch
from application.test.utils import wait_for_element


@steps
class SignupWithDuplicateUsername:
    """A user sign up with duplicate username"""

    def setup_user_data(self, step):
        """I am new user with the following data"""
        step.context.user_data = step.table[0]

    def another_user_already_use_that_username(self, step):
        """Another user has already signup with the same username"""
        from allauth.account.models import EmailAddress
        from allauth.utils import get_user_model
        user = get_user_model()(username=step.table[0]['username'])
        user.set_password(step.table[0]['password'])
        user.save()
        EmailAddress.objects.create(
            user=user, email=step.table[0]['email'],
            primary=True, verified=True)

    def go_to_signup_page(self, step):
        """I go to home page and click sign on up link"""
        find_by_css = Chrome.find_element_by_css_selector.__name__
        step.context.browser.get(step.context.base_url)
        signup_link = wait_for_element(
            step.context.browser, find_by_css, 'p.control>a#signup_link')
        signup_link.click()

    def submit_invalid_data(self, step):
        """I submit my invalid data on sign up form"""
        find_by_id = Chrome.find_element_by_id.__name__
        find_by_tag = Chrome.find_element_by_tag_name.__name__
        browser = step.context.browser
        username_input = wait_for_element(browser, find_by_id, 'id_username')
        email_input = wait_for_element(browser, find_by_id, 'id_email')
        password1_input = wait_for_element(browser, find_by_id, 'id_password1')
        password2_input = wait_for_element(browser, find_by_id, 'id_password2')
        button = wait_for_element(browser, find_by_tag, 'button')

        username_input.send_keys(step.context.user_data['username'])
        email_input.send_keys(step.context.user_data['email'])
        password1_input.send_keys(step.context.user_data['password'])
        password2_input.send_keys(step.context.user_data['password'])
        button.submit()

    def notified_about_duplicate_username(self, step):
        """I should be notified about duplicate username"""
        from django.shortcuts import reverse
        current_url = step.context.browser.current_url
        base_url = step.context.base_url
        assert_that(
            current_url, equal_to(base_url + reverse('account_signup')))
        body = wait_for_element(
            step.context.browser, 'find_element_by_tag_name', 'body')
        assert_that(
            body.text,
            contains_string("A user with that username already exists."))


@steps
class SignupWithDuplicateEmail:
    """A user sign up with duplicate email"""

    def another_user_already_use_that_email(self, step):
        """Another user has already signup with the same email"""
        from allauth.account.models import EmailAddress
        from allauth.utils import get_user_model
        user = get_user_model()(username=step.table[0]['username'])
        user.set_password(step.table[0]['password'])
        user.save()
        EmailAddress.objects.create(
            user=user, email=step.table[0]['email'],
            primary=True, verified=True)

    def notified_about_duplicate_email(self, step):
        """I should be notified about duplicate email"""
        from django.shortcuts import reverse
        current_url = step.context.browser.current_url
        base_url = step.context.base_url
        assert_that(
            current_url, equal_to(base_url + reverse('account_signup')))
        body = wait_for_element(
            step.context.browser, 'find_element_by_tag_name', 'body')
        assert_that(
            body.text,
            contains_string("A user is already registered "
                            "with this e-mail address."))


@steps
class SignupWithUnmatchPassword:
    """A user sign up with unmatch password"""

    def submit_unmatch_password(self, step):
        """I submit unmatch password on sign up form"""
        find_by_id = Chrome.find_element_by_id.__name__
        find_by_tag = Chrome.find_element_by_tag_name.__name__
        browser = step.context.browser
        username_input = wait_for_element(browser, find_by_id, 'id_username')
        email_input = wait_for_element(browser, find_by_id, 'id_email')
        password1_input = wait_for_element(browser, find_by_id, 'id_password1')
        password2_input = wait_for_element(browser, find_by_id, 'id_password2')
        button = wait_for_element(browser, find_by_tag, 'button')

        username_input.send_keys(step.context.user_data['username'])
        email_input.send_keys(step.context.user_data['email'])
        password1_input.send_keys(step.context.user_data['password'])
        password2_input.send_keys(step.context.user_data['password'] + "deo")
        button.submit()

    def notified_about_unmatch_password(self, step):
        """ I should be notified about unmatch password"""
        from django.shortcuts import reverse
        current_url = step.context.browser.current_url
        base_url = step.context.base_url
        assert_that(
            current_url, equal_to(base_url + reverse('account_signup')))
        body = wait_for_element(
            step.context.browser, 'find_element_by_tag_name', 'body')
        assert_that(
            body.text,
            contains_string("You must type the same password each time."))


@steps
class SignupAndLoginAfterEmailVerification:
    """A user confirm email after sign up and login"""

    def submit_valid_data(self, step):
        """I submit my data on sign up form"""
        base_url = step.context.base_url
        find_by_id = Chrome.find_element_by_id.__name__
        find_by_tag = Chrome.find_element_by_tag_name.__name__
        browser = step.context.browser
        username_input = wait_for_element(browser, find_by_id, 'id_username')
        email_input = wait_for_element(browser, find_by_id, 'id_email')
        password1_input = wait_for_element(browser, find_by_id, 'id_password1')
        password2_input = wait_for_element(browser, find_by_id, 'id_password2')
        button = wait_for_element(browser, find_by_tag, 'button')

        username_input.send_keys(step.context.user_data['username'])
        email_input.send_keys(step.context.user_data['email'])
        password1_input.send_keys(step.context.user_data['password'])
        password2_input.send_keys(step.context.user_data['password'])

        with patch('sys.stdout', new=StringIO()) as fake_out:
            button.submit()
            mail_content = fake_out.getvalue()
            step.context.confirm_url = mail_content[mail_content.find(
                base_url + '/accounts/confirm-email/'):].split()[0]

    def get_confirmation_email(self, step):
        """I will receive a verification email"""
        assert_that(step.context.confirm_url, starts_with('http'))
        find_by_tag = Chrome.find_element_by_tag_name.__name__
        body = wait_for_element(step.context.browser, find_by_tag, 'body')
        assert_that(body.text, contains_string('Verify Your E-mail Address'))

    def confirm_email(self, step):
        """I confirm my email"""
        step.context.browser.quit()
        step.context.browser = Chrome()
        find_by_tag = Chrome.find_element_by_tag_name.__name__
        step.context.browser.get(step.context.confirm_url)
        button = wait_for_element(step.context.browser, find_by_tag, 'button')
        button.submit()
        step.context.browser = Chrome()


@steps
class SignUpAndLoginWithoutConfirmEmail:
    """ A user hasn't confirm email after sign up and login"""

    def did_not_confirm_email(self, step):
        """I didn't confirm my email"""
        step.context.browser.quit()
        step.context.browser = Chrome()

    def asked_to_confirm_email(self, step):
        """I should be asked to confirm my email"""
        find_by_tag = Chrome.find_element_by_tag_name.__name__
        body = wait_for_element(step.context.browser, find_by_tag, 'body')
        assert_that(body.text, contains_string('Verify Your E-mail Address'))
