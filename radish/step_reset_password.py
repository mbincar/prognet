from io import StringIO

from hamcrest import assert_that, contains_string, equal_to, starts_with
from radish import steps
from selenium.webdriver import Chrome
from unittest.mock import patch

from application.test.utils import wait_for_element


@steps
class ResetPasswordStep:
    """A user forgot password and reset it"""

    def forgot_password_on_login(self, step):
        """I forgot my password when trying to login"""
        from django.shortcuts import reverse
        step.context.browser.get(
            step.context.base_url + reverse('account_login'))
        find_by_link = Chrome.find_element_by_link_text.__name__
        browser = step.context.browser
        step.context.reset_link = wait_for_element(
            browser, find_by_link, 'Forgot Password?')

    def click_reset_link(self, step):
        """I click on reset password link"""
        step.context.reset_link.click()

    def redirected_to_reset_password_page(self, step):
        """I will be redirected to reset password page"""
        from django.shortcuts import reverse
        base_url = step.context.base_url
        current_url = step.context.browser.current_url
        assert_that(
            current_url,
            equal_to(base_url + reverse('account_reset_password')))

    def submit_email(self, step):
        """I submit my email on reset password form"""
        base_url = step.context.base_url
        browser = step.context.browser
        find_by_id = Chrome.find_element_by_id.__name__
        find_by_tag = Chrome.find_element_by_tag_name.__name__
        email_input = wait_for_element(browser, find_by_id, 'id_email')
        button = wait_for_element(browser, find_by_tag, 'button')

        email_input.send_keys(step.context.user_data['email'])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            button.submit()
            mail_content = fake_out.getvalue()
            step.context.reset_link = mail_content[mail_content.find(
                base_url + '/accounts/password/reset/key/'):].split()[0]

    def receive_email_for_reset_password(self, step):
        """I will receive an email with reset password link"""
        body = wait_for_element(
            step.context.browser, 'find_element_by_tag_name', 'body')
        reset_link = step.context.reset_link
        assert_that(
            body.text,
            contains_string("We have sent you an "
                            "e-mail. Please contact us if you do "
                            "not receive it within a few minutes."))
        assert_that(reset_link, starts_with('http'))

    def open_reset_password_link(self, step):
        """I open my reset password link and submit new password"""
        browser = step.context.browser
        browser.get(step.context.reset_link)
        find_by_id = Chrome.find_element_by_id.__name__
        find_by_tag = Chrome.find_element_by_tag_name.__name__
        password1_input = wait_for_element(browser, find_by_id, 'id_password1')
        password2_input = wait_for_element(browser, find_by_id, 'id_password2')
        button = wait_for_element(browser, find_by_tag, 'button')

        password1_input.send_keys(step.table[0]['new_password'])
        password2_input.send_keys(step.table[0]['new_password'])
        button.submit()
        body = wait_for_element(browser, find_by_tag, 'body')
        assert_that(
            body.text, contains_string('Your password is now changed.'))
        step.context.user_data['password'] = step.table[0]['new_password']

    def login_with_new_password(self, step):
        """I will be able to login with my new password"""
        browser = step.context.browser
        step.context.browser.get(step.context.base_url + "/accounts/login/")
        find_by_id = Chrome.find_element_by_id.__name__
        login_input = wait_for_element(browser, find_by_id, 'id_login')
        password_input = wait_for_element(browser, find_by_id, 'id_password')
        button = wait_for_element(
            browser, 'find_element_by_tag_name', 'button')

        login_input.send_keys(step.context.user_data['username'])
        password_input.send_keys(step.context.user_data['password'])
        button.submit()
        body = wait_for_element(browser, 'find_element_by_tag_name', 'body')
        current_url = str(step.context.browser.current_url).rstrip('/')
        assert_that(current_url, equal_to(step.context.base_url))


@steps
class ResetPasswordWrongEmailStep:
    """A user forgot username but submit wrong email on reset password"""

    def submit_email(self, step):
        """I submit wrong email address"""
        base_url = step.context.base_url
        browser = step.context.browser
        find_by_id = Chrome.find_element_by_id.__name__
        find_by_tag = Chrome.find_element_by_tag_name.__name__
        email_input = wait_for_element(browser, find_by_id, 'id_email')
        button = wait_for_element(browser, find_by_tag, 'button')

        email_input.send_keys(step.context.user_data['email'] + 'doe')
        button.submit()

    def notified_about_wrong_email(self, step):
        """I should be notified about it"""
        from django.shortcuts import reverse
        browser = step.context.browser
        base_url = step.context.base_url
        current_url = browser.current_url
        find_by_tag = Chrome.find_element_by_tag_name.__name__
        body = wait_for_element(browser, find_by_tag, 'body')
        assert_that(
            current_url,
            equal_to(base_url + reverse('account_reset_password')))
        assert_that(
            body.text,
            contains_string("The e-mail address is not "
                            "assigned to any user account"))


@steps
class ResetPasswordUnmatchPasswordStep:
    """A user forgot username but submit unmatch password on reset password"""

    def submit_unmatch_new_password(self, step):
        """I submit unmatch new password"""
        browser = step.context.browser
        browser.get(step.context.reset_link)
        find_by_id = Chrome.find_element_by_id.__name__
        find_by_tag = Chrome.find_element_by_tag_name.__name__
        password1_input = wait_for_element(browser, find_by_id, 'id_password1')
        password2_input = wait_for_element(browser, find_by_id, 'id_password2')
        button = wait_for_element(browser, find_by_tag, 'button')

        password1_input.send_keys(step.table[0]['new_password'])
        password2_input.send_keys(step.table[0]['new_password2'])
        button.submit()

    def notified_about_unmatch_password(self, step):
        """I should be notified about unmatch password for reset password"""
        browser = step.context.browser
        find_by_tag = Chrome.find_element_by_tag_name.__name__
        body = wait_for_element(browser, find_by_tag, 'body')
        assert_that(
            body.text,
            contains_string("You must type the same password each time."))


@steps
class ResetPasswordAlredyUsedLinkStep:
    """A user forgot username and try to use already used reset
    password link"""

    def request_reset_password_with_same_url(self, step):
        """I try to request reset password using the same url"""
        step.context.browser.get(step.context.reset_link)

    def notified_about_invalid_password_link(self, step):
        """I will be notified about invalid reset password link"""
        browser = step.context.browser
        find_by_tag = Chrome.find_element_by_tag_name.__name__
        body = wait_for_element(browser, find_by_tag, 'body')
        assert_that(body.text, contains_string("Bad Token"))
