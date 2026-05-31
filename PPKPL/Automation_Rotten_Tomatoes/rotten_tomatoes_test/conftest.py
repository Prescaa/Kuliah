import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.rotten_tomatoes_page import RottenTomatoesPage


@pytest.fixture(scope="function")
def driver():
    options = Options()
    # options.add_argument("--headless")  # Komen ini agar browser terlihat saat testing
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(10)
    yield drv
    drv.quit()


@pytest.fixture(scope="function")
def rt_page(driver):
    return RottenTomatoesPage(driver)