import time
from urllib.parse import quote
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL  = "https://www.rottentomatoes.com"
WAIT_TIME = 10


class RottenTomatoesPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, WAIT_TIME)

    # ── Navigasi ──────────────────────────────────────────────────────────────

    def open_homepage(self):
        self.driver.get(BASE_URL)
        time.sleep(3)

    def open_url(self, path: str):
        safe_path = quote(path, safe="/?=&")
        self.driver.get(f"{BASE_URL}{safe_path}")
        time.sleep(3)

    def open_search(self, query: str):
        safe_query = quote(query, safe="")
        self.driver.get(f"{BASE_URL}/search?search={safe_query}")
        time.sleep(3)

    def open_movie_detail(self, slug: str):
        self.driver.get(f"{BASE_URL}/m/{slug}")
        time.sleep(3)

    def open_celebrity(self, slug: str):
        self.driver.get(f"{BASE_URL}/celebrity/{slug}")
        time.sleep(3)

    def open_tv_show(self, slug: str):
        self.driver.get(f"{BASE_URL}/tv/{slug}")
        time.sleep(3)

    def open_browse(self, category: str):
        self.driver.get(f"{BASE_URL}/browse/{category}/")
        time.sleep(3)

    # ── Getter dasar ──────────────────────────────────────────────────────────

    def get_page_title(self) -> str:
        return self.driver.title

    def get_page_source(self) -> str:
        """Page source dalam huruf kecil untuk pencarian kata kunci."""
        return self.driver.page_source.lower()

    def get_raw_page_source(self) -> str:
        return self.driver.page_source

    def get_current_url(self) -> str:
        return self.driver.current_url

    # ── Getter elemen ─────────────────────────────────────────────────────────

    def get_header(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "rt-header-nav")

    def get_movies_nav_links(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/movies']")

    def get_tv_nav_links(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/tv']")

    # ── Alert helper ──────────────────────────────────────────────────────────

    def dismiss_alert_if_present(self) -> bool:
        try:
            alert = self.driver.switch_to.alert
            alert.dismiss()
            return True
        except Exception:
            return False

    # ── Checker umum ──────────────────────────────────────────────────────────

    def is_page_loaded_without_server_error(self) -> bool:
        src = self.get_page_source()
        indicators = [
            "500 internal server error",
            "500 - internal server error",
            "<title>500</title>",
            "http error 500",
            "internal server error",
            "the server encountered an error",
        ]
        return not any(ind in src for ind in indicators)

    def has_error_page_indicator(self) -> bool:
        src = self.get_page_source()
        return any(kw in src for kw in ["404", "not found", "error", "oops"])

    def has_content_keywords(self, keywords: list) -> bool:
        """Cek keyword di seluruh page source (case-insensitive)."""
        src = self.get_page_source()
        return any(kw.lower() in src for kw in keywords)

    def is_on_domain(self) -> bool:
        return "rottentomatoes" in self.get_current_url()

    # ── Checker spesifik konten utama ─────────────────────────────────────────

    def has_score_element_in_main_content(self) -> bool:
        """
        Cek apakah elemen skor Tomatometer ada di konten utama halaman
        (bukan di footer atau meta tag).

        Selector yang digunakan menarget elemen score RT yang spesifik:
        - rt-button[slot='criticsScore']  : tombol skor kritikus
        - score-board                     : komponen skor RT (Web Component)
        - [data-qa='tomatometer']         : atribut data QA resmi RT
        - .mop-ratings-wrap               : wrapper rating di halaman film lama
        """
        selectors = [
            "[data-qa='tomatometer']",
            "score-board",
            "rt-button[slot='criticsScore']",
            ".mop-ratings-wrap__score",
            "[class*='tomatometer']",
        ]
        for selector in selectors:
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            if len(elements) > 0:
                return True
        return False

    def has_main_content_keyword(self, keyword: str) -> bool:
        """
        Cek apakah keyword ada di dalam elemen konten utama halaman.
        Tidak memeriksa header, footer, atau meta tag.

        Elemen yang diperiksa (dari yang paling spesifik ke paling umum):
        - main          : tag <main> HTML5
        - #main-content : ID konten utama umum
        - article       : tag artikel
        - .content      : class content umum
        Jika tidak ada elemen tersebut, fallback ke body.
        """
        keyword_lower = keyword.lower()

        main_selectors = ["main", "#main-content", "article", ".content", "body"]
        for selector in main_selectors:
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                text = elements[0].text.lower()
                return keyword_lower in text

        return keyword_lower in self.get_page_source()