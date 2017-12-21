from radish import steps
from selenium.webdriver import Chrome
from application.test.utils import wait_for_element


@steps
class LoginUserChangePassword:
    """A login user change password"""
    def change_password(self, step):
        """I go to change password link and submit new password"""
        from django.shortcuts import reverse
        change_password_link = \
            step.context.base_url + reverse('account_change_password')
        browser = step.context.browser
        browser.get(change_password_link)
        find_by_id = Chrome.find_element_by_id.__name__
        find_by_tag = Chrome.find_element_by_tag_name.__name__
        old_password_input = wait_for_element(
            browser, find_by_id, 'id_oldpassword')
        password1_input = wait_for_element(browser, find_by_id, 'id_password1')
        password2_input = wait_for_element(browser, find_by_id, 'id_password2')
        button = wait_for_element(browser, find_by_tag, 'button')

        old_password_input.send_keys(step.context.user_data['password'])
        password1_input.send_keys(step.table[0]['new_password'])
        password2_input.send_keys(step.table[0]['new_password'])
        button.submit()
        step.context.user_data['password'] = step.table[0]['new_password']

    def logout(self, step):
        """I logout"""
        from django.shortcuts import reverse
        logout_link = step.context.base_url + reverse('account_logout')
        step.context.browser.get(logout_link)
