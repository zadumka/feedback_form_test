import json
import requests
from behave import given, when, then, use_fixture
from playwright.sync_api import expect, sync_playwright

# https://da-m-lp-ua.goit.global/
# https://html-m-lp-ua.goit.global/

@when('user goes to lend page')
def step_def(context):
    context.page.goto("https://html-m-lp-ua.goit.global/")
    context.page.pause()
    context.page.get_by_label("Close").click()
    expect(context.page.locator(f'//h1')).to_be_visible()



@then('user fills and sends feedback form')
def step_def(context):
    context.page.locator('//button[text()="Зареєструватися"]').nth(1).click()
    context.page.locator('//input[@name="name"]').nth(1).fill("TEST")
    context.page.locator('//input[@name="email"]').nth(1).fill("test12@qa.team")
    context.page.locator('//input[@name="phone"]').nth(1).fill("347526911")
    context.page.locator(f'//button[@type="submit"]').nth(1).click()



@when('user sees modall whith telegram button')
def step_def(context):
    context.page.wait_for_timeout(1000)
    expect(context.page.locator('//div[contains(@class, "leeloo-lgt-form-wrapper")]')).to_be_visible()
    telegram_button = context.page.frame_locator("internal:text=\"</div>\"i").get_by_role("button", name="icon Telegram")
    if telegram_button.is_visible():
        telegram_button.click()
    else:
        print("Telegram button is not visible.")



@then('user sees the transition page to Telegram')
def step_def(context):
    transition_page = context.page.locator('//a[@href="//telegram.org/"]')
    try:
        expect(transition_page).to_be_visible()
        print("Transition page to Telegram is visible.")
    except AssertionError:
        print("Transition page to Telegram is not visible.")



# from email.parser import BytesParser
# from io import BytesIO
# import urllib.parse
#
#
# @then('intercept form submission and check data')
# def step_def(context):
#     with context.page.expect_request(
#             f'https://da-m-lp-ua.goit.global/wp-admin/admin-ajax.php') as request_info:
#         context.page.wait_for_timeout(1000)
#         context.page.locator(f'//button[@type="submit"]').nth(1).click()
#
#         raw_data = request_info.value.post_data
#         # Перетворюємо рядок у байти
#         byte_data = BytesIO(raw_data.encode('utf-8'))
#         # Парсимо form-data
#         message = BytesParser().parse(byte_data)
#
#         form_data = {}
#         for part in message.walk():
#             if part.get_content_disposition() == 'form-data':
#                 name = part.get_param('name', header='content-disposition')
#                 form_data[name] = part.get_payload(decode=True).decode('utf-8')
#
#         print(form_data)
#
#         assert form_data['name'] == "Test"
#         assert form_data['email'] == "test12@qa.team"
#         assert form_data['phone'] == "347526911"
#         assert form_data['product_name'] != ""
#         assert form_data['product_id'] != ""