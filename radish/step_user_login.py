from hamcrest import assert_that, equal_to, contains_string
from radish import steps
from radish.stepmodel import Step
from selenium.webdriver import Chrome
from application.test.utils import wait_for_element


@steps
class LoginWithUsernameStep:
    """A user login with valid username and password"""

    def setup_user_data(self, step: Step):
        """I already sign up with the following data"""
        from allauth.account.models import EmailAddress
        from allauth.utils import get_user_model
        step.context.user_data = step.table[0]
        user = get_user_model()(username=step.table[0]['username'])
        user.set_password(step.table[0]['password'])
        user.save()
        EmailAddress.objects.create(
            user=user, email=step.table[0]['email'],
            primary=True, verified=True)

    def user_submit_login_data(self, step: Step):
        """I go to login page and login with my username"""
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

    def user_redirected_to_home_page(self, step: Step):
        """I should be redirected to home page"""
        current_url = str(step.context.browser.current_url).rstrip('/')
        assert_that(current_url, equal_to(step.context.base_url))


@steps
class LoginWithEmailStep:
    """A user login with valid email and password"""

    def user_submit_login_data(self, step: Step):
        """I go to login page and login with my email"""
        browser = step.context.browser
        step.context.browser.get(step.context.base_url + "/accounts/login/")
        find_by_id = Chrome.find_element_by_id.__name__
        login_input = wait_for_element(browser, find_by_id, 'id_login')
        password_input = wait_for_element(browser, find_by_id, 'id_password')
        button = wait_for_element(
            browser, 'find_element_by_tag_name', 'button')

        login_input.send_keys(step.context.user_data['email'])
        password_input.send_keys(step.context.user_data['password'])
        button.submit()


@steps
class LoginWithInvalidUsername:
    """A user login with invalid username"""

    def user_misspelled_username_on_login(self, step: Step):
        """I go to login page and misspelled username on sumbit data"""
        browser = step.context.browser
        step.context.browser.get(step.context.base_url + "/accounts/login/")
        find_by_id = Chrome.find_element_by_id.__name__
        login_input = wait_for_element(browser, find_by_id, 'id_login')
        password_input = wait_for_element(browser, find_by_id, 'id_password')
        button = wait_for_element(
            browser, 'find_element_by_tag_name', 'button')

        login_input.send_keys(step.context.user_data['username'] + "doe")
        password_input.send_keys(step.context.user_data['password'])
        button.submit()

    def notified_about_invalid_username_password(self, step: Step):
        """I should be notified about invalid username/password"""
        from django.shortcuts import reverse
        current_url = str(step.context.browser.current_url)
        base_url = step.context.base_url
        assert_that(
            current_url,
            equal_to(base_url + "/" + reverse('account_login')))
        assert_that(
            step.context.browser.body.text,
            contains_string("The username and/or "
                            "password you specified are not correct."))


@steps
class LoginWithInvalidEmail:
    """A user login with invalid email"""

    def user_misspelled_email_on_login(self, step: Step):
        """I go to login page and misspelled email on sumbit data"""
        browser = step.context.browser
        step.context.browser.get(step.context.base_url + "/accounts/login/")
        find_by_id = Chrome.find_element_by_id.__name__
        login_input = wait_for_element(browser, find_by_id, 'id_login')
        password_input = wait_for_element(browser, find_by_id, 'id_password')
        button = wait_for_element(
            browser, 'find_element_by_tag_name', 'button')

        login_input.send_keys(step.context.user_data['email'] + "doe")
        password_input.send_keys(step.context.user_data['password'])
        button.submit()

    def notified_about_invalid_email_password(self, step: Step):
        """I should be notified about invalid email/password"""
        from django.shortcuts import reverse
        current_url = str(step.context.browser.current_url)
        base_url = step.context.base_url
        assert_that(
            current_url,
            equal_to(base_url + "/" + reverse('account_login')))
        assert_that(
            step.context.browser.body.text,
            contains_string("The e-mail address and/or "
                            "password you specified are not correct."))


@steps
class LoginWithInvalidPassword:
    """A user login with valid username but invalid password"""

    def misspelled_password_on_login(self, step: Step):
        """I go to login page and misspelled password on login"""
        browser = step.context.browser
        step.context.browser.get(step.context.base_url + "/accounts/login/")
        find_by_id = Chrome.find_element_by_id.__name__
        login_input = wait_for_element(browser, find_by_id, 'id_login')
        password_input = wait_for_element(browser, find_by_id, 'id_password')
        button = wait_for_element(
            browser, 'find_element_by_tag_name', 'button')

        login_input.send_keys(step.context.user_data['username'])
        password_input.send_keys(step.context.user_data['password'] + "deo")
        button.submit()
