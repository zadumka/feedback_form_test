import json
import requests
from behave import given, when, then, use_fixture
from playwright.sync_api import expect, sync_playwright

# https://da-m-lp-ua.goit.global/
# https://html-m-lp-ua.goit.global/

@when('user goes to lend page')
def step_def(context):
    context.page.goto("https://da-m-lp-ua.goit.global/")
    context.page.pause()
    context.page.get_by_label("Close").click()
    expect(context.page.locator(f'//h1')).to_be_visible()



@then('user fills and sends feedback form')
def step_def(context):
    context.page.locator('//button[@data-modal-open]').nth(1).click()
    context.page.locator('//input[@name="name"]').nth(1).fill("TEST")
    context.page.locator('//input[@name="email"]').nth(1).fill("test12@qa.team")
    context.page.locator('//input[@name="phone"]').nth(1).fill("347526911")
    # context.page.locator(f'//button[@type="submit"]').nth(1).click()



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


# @then('intercept form submission and check data')
# def step_def(context):
#     with context.page.expect_request(
#             f'https://da-m-lp-ua.goit.global/wp-admin/admin-ajax.php') as request_info:
#         context.page.wait_for_timeout(1000)
#         # context.page.locator(f'//button[@type="submit"]').nth(1).click()
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


from io import BytesIO
import pprint
from email.parser import BytesParser
from email.policy import default


@then('intercept form submission and check data')
def step_def(context):
    requests = []
    # context.page.wait_for_timeout(1000)
    context.page.locator(f'//button[@type="submit"]').nth(1).click()

    try:
        print("Waiting for the request...")
        with context.page.expect_request(f'https://da-m-lp-ua.goit.global/wp-admin/admin-ajax.php',
                                         timeout=60000) as request_info:
            requests.append(request_info)
        print(request_info)

        # context.page.wait_for_timeout(2000)  # Додаткове очікування для завершення запиту

        if not requests:
            print("No requests captured")
            return

        # Вибираємо останній запит
        request = requests[-1]
        raw_data = request.post_data
        content_type = request.headers.get('Content-Type', '')
        boundary = content_type.split('boundary=')[-1].strip()

        byte_data = BytesIO(raw_data)
        content = byte_data.read().decode('utf-8')

        form_data = {}
        parts = content.split(f'--{boundary}')

        for part in parts:
            if 'Content-Disposition' in part:
                name_start = part.find('name="') + len('name="')
                name_end = part.find('"', name_start)
                name = part[name_start:name_end]
                payload_start = part.find('\r\n\r\n') + len('\r\n\r\n')
                payload_end = part.rfind(f'\r\n--{boundary}')
                payload = part[payload_start:payload_end].strip()
                form_data[name] = payload

        pprint.pprint(form_data)

        assert form_data.get('name') == "Test"
        assert form_data.get('phone') == "+380347526911"
        assert form_data.get('email') == "test12@qa.team"
        assert form_data.get('product_name') != ""
        assert form_data.get('product_id') != ""

    except Exception as e:
        print(f"Error occurred: {e}")


