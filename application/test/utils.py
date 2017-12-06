import time
from selenium.common.exceptions import WebDriverException


def wait_for_element(browser, method_name, selector, max_wait=10):
    start_time = time.time()
    while True:
        try:
            elm = getattr(browser, method_name)(selector)
            return elm
        except WebDriverException as err:
            if time.time() - start_time > max_wait:
                raise err
            time.sleep(0.5)
