import json
import requests
from behave import given, when, then, use_fixture
from playwright.sync_api import expect, sync_playwright
import Data
from Data.host_list import HOST_LIST
from Data.host_list import REQUEST_HOST_LIST
import urllib.parse



@when('user goes to lend page with "{host}"')
def step_def(context, host):
    host_url = HOST_LIST.get(host)
    context.page.goto(f"https://{host_url}/")
    # context.page.pause()
    context.page.get_by_label("Close").click()
    expect(context.page.locator(f'//h1')).to_be_visible()



@when('user fills correct data and sends feedback form')
def step_def(context):
    context.page.locator('//input[@id="register_input_name"]').fill("TEST")
    context.page.locator('//input[@id="register_input_email"]').fill("test12@qa.team")
    context.page.locator('//input[@id="register_input_phone"]').fill("347526911")



@when('user fills incorrect data to the feedback form')
def step_def(context):
    context.page.locator('//input[@id="register_input_name"]').fill("TEST 1234")
    context.page.locator('//input[@id="register_input_email"]').fill("test12qa.team")
    context.page.locator('//input[@id="register_input_phone"]').fill("347526911122")



@then('expected validation errors are under the form fields submit button is enabled')
def step_def(context):
    submit_button = context.page.locator('//form[@id="register"]/button[@type="submit"]')
    # Перевіряємо, що кнопка не натиснулась
    if submit_button.is_enabled():
        # Натискаємо кнопку і перевіряємо, що повідомлення про помилки все ще присутні
        submit_button.click()
        expect(context.page.get_by_text("Ім’я невірне")).to_be_visible()
        expect(context.page.get_by_text("Email невірний!")).to_be_visible()
        expect(context.page.get_by_text("Номер телефону невірний!")).to_be_visible()
    else:
        print("Submit button is disabled, not clicked.")



@when('user sees modall whith telegram button')
def step_def(context):
    context.page.wait_for_timeout(1000)
    context.page.wait_for_timeout(1000)
    telegram_button = context.page.frame_locator("internal:text=\"</div>\"i").get_by_role("button", name="icon Telegram")
    expect(telegram_button).to_be_visible()
    if telegram_button.is_visible():
        telegram_button.click()
    else:
        print("Telegram button is not visible.")



@when('user sees thanks modal')
def step_def(context):
    expect(context.page.get_by_text("Дякуємо, ми отримали заявку. Наші менеджери найближчим часом зв'яжуться з вами :")).to_be_visible()
    expect(context.page.get_by_text("Наші менеджери найближчим часом зв'яжуться з вами :)")).to_be_visible()



@then('user sees the transition page to Telegram')
def step_def(context):
    context.page.wait_for_timeout(5000)
    transition_page = context.page.locator('//a[@href="//telegram.org/"]')
    expect(transition_page).to_be_visible()
    print("Transition page to Telegram is visible.")



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
    context.page.locator(f'//form[@id="register"]/button[@type="submit"]').click()
    context.page.wait_for_timeout(500)

    # Перевірка на помилку
    if context.page.locator('//div[@class="swal2-icon swal2-error swal2-icon-show"]').is_visible():
        # Контекст локатора може відрізнятися, але вам потрібно перевірити видимість елемента
        error_message = "Знайдена помилка у формі! Такої пошти не існує"
        # print(error_message)
        assert False, error_message  # Використання асертації для падіння тесту з повідомленням про помилку

    assert second_request is not None, "Другий запит не був виконаний"  # Чекаємо, щоб запити були виконані

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

        assert 'TEST' in string_data, "Дані не містять 'TEST'"
        assert 'test12@qa.team' in string_data, "Дані не містять 'test12@qa.team'"
        assert '347526911' in string_data, "Дані не містять '347526911'"
        assert len(product_name_parse) not in range(0, 8), "Назва продукту має недопустиму довжину"
        assert len(product_id_parse) not in range(0, 8), "ID продукту має недопустиму довжину"

# ! Для реквест форм

@when('user goes to request page with "{host}"')
def step_def(context, host):
    host_url = REQUEST_HOST_LIST.get(host)
    context.page.goto(f"https://{host_url}/")
    context.page.get_by_label("Close").click()



@when('user fills correct data and sends request form')
def step_def(context):
    # context.page.pause()
    context.page.locator('//input[@id="header_input_name"]').fill("TEST")
    context.page.locator('//input[@id="header_input_phone"]').fill("347526911")
    context.page.locator('//input[@id="header_input_email"]').fill("test12@qa.team")


@then('intercept request form submission and check data on "{host}"')
def step_def(context, host):
    # Очікування другого запиту
    request_count = 0
    second_request = None
    host_url = REQUEST_HOST_LIST.get(host)

    def handle_request(request):
        nonlocal request_count, second_request
        if request.url == f'https://{host_url}/wp-admin/admin-ajax.php':
            request_count += 1
            if request_count == 2:
                second_request = request

    context.page.on('request', handle_request)
    context.page.locator(f'//form[@id="header"]/button[@type="submit"]').click()
    context.page.wait_for_timeout(500)

    # Перевірка на помилку
    if context.page.locator('//div[@class="swal2-icon swal2-error swal2-icon-show"]').is_visible():
        # Контекст локатора може відрізнятися, але вам потрібно перевірити видимість елемента
        error_message = "Знайдена помилка у формі! Такої пошти не існує"
        # print(error_message)
        assert False, error_message  # Використання асертації для падіння тесту з повідомленням про помилку

    assert second_request is not None, "Другий запит не був виконаний"  # Чекаємо, щоб запити були виконані

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

        assert 'TEST' in string_data, "Дані не містять 'TEST'"
        assert 'test12@qa.team' in string_data, "Дані не містять 'test12@qa.team'"
        assert '347526911' in string_data, "Дані не містять '347526911'"
        assert len(product_name_parse) not in range(0, 8), "Назва продукту має недопустиму довжину"
        assert len(product_id_parse) not in range(0, 8), "ID продукту має недопустиму довжину"


