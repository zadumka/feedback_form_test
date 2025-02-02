import json
import requests
from behave import given, when, then, use_fixture
from playwright.sync_api import expect, sync_playwright
import Data
from Data.host_list import HOST_LIST
import urllib.parse
from langdetect import detect


# @then('check all images have non-empty alt attributes')
# def step_def(context):
#     page = context.page  # Отримуємо сторінку з контексту тесту
#     images = page.locator('img')
#
#     all_alt_valid = True
#
#     for img in images.all():
#         alt_text = img.get_attribute('alt')
#         src = img.get_attribute('src')  # Отримуємо URL зображення
#
#         if not alt_text:
#             print(f"Image (URL: {src}) has an empty alt attribute.")
#             all_alt_valid = False
#         # else:
#         #     print(f"Image (URL: {src}) has alt text: {alt_text}")
#     # Перевірка, чи всі alt атрибути не пусті
#     assert all_alt_valid, "Some images have empty alt attributes."
#
#
#
#
# from langdetect import detect, DetectorFactory
#
# # Встановлюємо фіксоване зерно для детектора
# DetectorFactory.seed = 0
#
#
# @then('check all images alt text matches page language')
# def step_def(context):
#     page = context.page  # Отримуємо сторінку з контексту тесту
#     page_language = page.evaluate('document.documentElement.lang')
#
#     # Збір всіх зображень
#     images = page.query_selector_all('img')
#
#     for image in images:
#         alt_text = image.get_attribute('alt')
#         src = image.get_attribute('src')
#
#         # Перевіряємо, чи alt_text не порожній
#         if not alt_text:
#             # print("Зображення не має 'alt' тексту.")
#             continue
#
#         # Визначення мови alt_text
#         alt_language = detect(alt_text)
#
#         # Перевірка, чи мова 'alt' співпадає з мовою сайту
#         if alt_language != page_language:
#             print(
#                 f"Зображення за URL '{src}' з 'alt' текстом '{alt_text}' має мову {alt_language}, яка не відповідає мові сайту {page_language}.")




# @when('user fill form')
# def step_def(context):
#     context.page.locator('//button[text()="Open modal"]').click()
#     context.page.locator('//input[@id="modalForm_input_name"]').fill("TEST")
#     context.page.locator('//input[@id="modalForm_input_phone"]').fill("347526911")
#     context.page.locator('//input[@id="modalForm_input_email"]').fill("test12@qa.team")
#     context.page.locator('//span[@class="checkbox"]').check()
#
#
#
#
# @then('intercept form submission on "{host}"')
# def step_def(context, host):
#     # Очікування другого запиту
#     request_count = 0
#     second_request = None
#     host_url = HOST_LIST.get(host)
#
#     def handle_request(request):
#         nonlocal request_count, second_request
#         if request.url == f'https://{host_url}/wp-admin/admin-ajax.php':
#             request_count += 1
#             if request_count == 2:
#                 second_request = request
#
#
#     context.page.on('request', handle_request)
#     context.page.locator(f'//button[@type="submit"]').click()
#     context.page.wait_for_timeout(500)
#
#     # Перевірка на помилку
#     if context.page.locator('//div[@class="swal2-icon swal2-error swal2-icon-show"]').is_visible():
#         #context.page.get_by_role("heading", name="Помилка!").is_visible()
#         print("Знайдена помилка у формі! Такої пошти не існує")
#         return
#
#     assert second_request is not None  # Чекаємо, щоб запити були виконані
#
#     if second_request:
#         context.request_body = urllib.parse.parse_qs(second_request.post_data)
#         string_data = f'{context.request_body}'
#         # print(context.request_body)
#
#         # шукаємо строчку з назвою продукту
#         start_text = r'"product_name"\r\n\r\n'
#         end_text = r'\r\n------'
#         start_index = string_data.find(start_text) + len(start_text)
#         end_index = string_data.find(end_text, start_index)
#         product_name_parse = string_data[start_index:end_index]
#         print(f'product name is: {product_name_parse}')
#
#         # шукаємо строчку з айді продукту
#         start_text = r'"product_id"\r\n\r\n'
#         end_text = r'\r\n------'
#         start_index = string_data.find(start_text) + len(start_text)
#         end_index = string_data.find(end_text, start_index)
#         product_id_parse = string_data[start_index:end_index]
#         print(f'product id is: {product_id_parse}')
#
#         assert 'TEST' in string_data
#         assert 'test12@qa.team' in string_data
#         assert '347526911' in string_data
#         assert len(product_name_parse) not in range(0, 8)
#         assert len(product_id_parse) not in range(0, 8)




# @then('intercept form submission and check data on "{host}"')
# def step_def(context, host):
#     # Очікування другого запиту
#     request_count = 0
#     second_request = None
#     host_url = HOST_LIST.get(host)
#
#     def handle_request(request):
#         nonlocal request_count, second_request
#         if request.url == f'https://{host_url}/wp-admin/admin-ajax.php':
#             request_count += 1
#             if request_count == 2:
#                 second_request = request
#                 print(f"Intercepted second request for {host}")
#
#     context.page.on('request', handle_request)
#     context.page.locator(f'//form[@id="register"]/button[@type="submit"]').click()
#     context.page.wait_for_timeout(2000)  # Збільшуємо тайм-аут до 2000 мс, щоб переконатися, що запити виконані
#
#     # Перевірка на помилку
#     if context.page.locator('//div[@class="swal2-icon swal2-error swal2-icon-show"]').is_visible():
#         print("Знайдена помилка у формі! Такої пошти не існує")
#         return
#
#     assert second_request is not None, f"No second request intercepted for {host}"  # Чекаємо, щоб запити були виконані
#
#     if second_request:
#         context.request_body = urllib.parse.parse_qs(second_request.post_data)
#         string_data = f'{context.request_body}'
#         print(f"Request body for {host}: {string_data}")
#
#         # шукаємо строчку з назвою продукту
#         start_text = r'"product_name"\r\n\r\n'
#         end_text = r'\r\n------'
#         start_index = string_data.find(start_text) + len(start_text)
#         end_index = string_data.find(end_text, start_index)
#         product_name_parse = string_data[start_index:end_index]
#         print(f'Product name for {host} is: {product_name_parse}')
#
#         # шукаємо строчку з айді продукту
#         start_text = r'"product_id"\r\n\r\n'
#         end_text = r'\r\n------'
#         start_index = string_data.find(start_text) + len(start_text)
#         end_index = string_data.find(end_text, start_index)
#         product_id_parse = string_data[start_index:end_index]
#         print(f'Product ID for {host} is: {product_id_parse}')
#
#         assert 'TEST' in string_data
#         assert 'test12@qa.team' in string_data
#         assert '347526911' in string_data
#         assert len(product_name_parse) not in range(0, 8)
#         assert len(product_id_parse) not in range(0, 8)


# @when('user sees thanks modal')
# def step_def(context):
#     # expect(context.page.locator("//div[@aria-labelledby]")).to_be_visible()