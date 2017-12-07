from hamcrest import assert_that, equal_to
from radish import steps
from radish.stepmodel import Step
from selenium.webdriver import Chrome
from application.test.utils import wait_for_element


@steps
class LoginStep:
    """A user that already sign up and confirm email login"""

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
        """I go to login page and submit my login data"""
        browser = step.context.browser
        step.context.browser.get(step.context.base_url + "/accounts/login/")
        find_by_id = Chrome.find_element_by_id.__name__
        login_input = wait_for_element(browser, find_by_id, 'id_login')
        password_input = wait_for_element(browser, find_by_id, 'id_password')
        button = wait_for_element(browser, 'find_element_by_tag_name', 'button')

        login_input.send_keys(step.context.user_data['username'])
        password_input.send_keys(step.context.user_data['password'])
        button.submit()

    def user_redirected_to_home_page(self, step: Step):
        """I should be redirected to the home page"""
        current_url = str(step.context.browser.current_url).rstrip('/')
        assert_that(current_url, equal_to(step.context.base_url))