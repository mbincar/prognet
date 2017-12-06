from django.test import LiveServerTestCase
from radish import pick
from selenium import webdriver


@pick
def get_browser():
    return webdriver.Chrome()


@pick
def get_live_server():
    live_server = LiveServerTestCase
    live_server.setUpClass()
    return live_server
