from ftw.testbrowser import browser
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD


def visit(obj):
    browser.login(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
    browser.open(obj, view='sharing')


def visit_api(obj):
    browser.login(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
    browser.open(
        obj,
        view='sharing',
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })


def role_labels():
    return browser.css('#user-group-sharing-head th').text[1:]
