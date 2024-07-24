import json
import requests
from behave import given, when, then, use_fixture
from playwright.sync_api import expect, sync_playwright
import Data
from Data.host_list import HOST_LIST
import urllib.parse


@when('user goes to lend page with "{host}"')
def step_def(context, host):
    host_url = HOST_LIST.get(host)
    context.page.goto(f"https://{host_url}/")
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



@when('user sees thanks modall')
def step_def(context):
    expect(context.page.locator("//div[@aria-labelledby]")).to_be_visible()




@then('user sees the transition page to Telegram')
def step_def(context):
    transition_page = context.page.locator('//a[@href="//telegram.org/"]')
    try:
        expect(transition_page).to_be_visible()
        print("Transition page to Telegram is visible.")
    except AssertionError:
        print("Transition page to Telegram is not visible.")




@then('intercept form submission and check data on "{host}"')
def step_def(context, host):
    # Очікування другого запиту
    request_count = 0
    second_request = None
    host_url = HOST_LIST.get(host)

    def handle_request(request):
        nonlocal request_count, second_request
        if request.url == f'https://{host_url}/wp-admin/admin-ajax.php':
            request_count += 1
            if request_count == 2:
                second_request = request


    context.page.on('request', handle_request)

    # Виконання дій на сторінці
    context.page.locator(f'//button[@type="submit"]').nth(1).click()
    context.page.wait_for_timeout(500)
    assert second_request is not None # Чекаємо, щоб запити були виконані

    if second_request:
        context.request_body = urllib.parse.parse_qs(second_request.post_data)
        string_data = f'{context.request_body}'
        # print(context.request_body)

        # шукаємо строчку з назвою продукту
        start_text = r'"product_name"\r\n\r\n'
        end_text = r'\r\n------'
        start_index = string_data.find(start_text) + len(start_text)
        end_index = string_data.find(end_text, start_index)
        product_name_parse = string_data[start_index:end_index]
        print(f'product name is: {product_name_parse}')

        # шукаємо строчку з айді продукту
        start_text = r'"product_id"\r\n\r\n'
        end_text = r'\r\n------'
        start_index = string_data.find(start_text) + len(start_text)
        end_index = string_data.find(end_text, start_index)
        product_id_parse = string_data[start_index:end_index]
        print(f'product id is: {product_id_parse}')

        assert 'TEST' in string_data
        assert 'test12@qa.team' in string_data
        assert '347526911' in string_data
        assert len(product_name_parse) not in range(0, 8)
        assert len(product_id_parse) not in range(0, 8)