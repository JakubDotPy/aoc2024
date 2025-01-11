import os

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def setup_driver(cookie_value):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.get('https://adventofcode.com')
    driver.add_cookie(
        {'name': 'session', 'value': cookie_value.lstrip('session='), 'domain': 'adventofcode.com'}
    )
    return driver


def crop_image(input_path, output_path, crop_box=(0, 0, 640, 621)):
    with Image.open(input_path) as img:
        cropped = img.crop(crop_box)
        cropped.save(output_path)


def take_screenshot(driver, url, selector, output_name):
    driver.get(url)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )
    element.screenshot(output_name)
    crop_image(output_name, output_name)


def main():
    os.makedirs('screenshots', exist_ok=True)
    cookie = os.getenv('COOKIE')
    driver = setup_driver(cookie)
    try:
        take_screenshot(
            driver,
            'https://adventofcode.com/2024',
            'body > main > pre',
            'screenshots/aoc-screenshot.png',
        )
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
