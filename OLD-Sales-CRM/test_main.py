# test_main.py

from config import credentials, base_url
from locators import locators

# Test credentials
def test_credentials():
    assert credentials['email'] == 'chandana.rj@icompaas.in'
    assert credentials['password'] == 'Chandu@15033'

# Test base URL
def test_base_url():
    assert base_url == "https://dev-sc.theoneloan.com"

# Test locators
def test_locators():
    assert 'google_oauth_button' in locators
    assert 'email_input' in locators
    assert locators['google_oauth_button'][0] == 'xpath'
