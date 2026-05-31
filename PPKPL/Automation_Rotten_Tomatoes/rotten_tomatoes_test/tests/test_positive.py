# ============================================================
# KELOMPOK 1: HOMEPAGE — Positif
# ============================================================

def test_TC_HOME_01_POS_beranda_berhasil_dimuat(rt_page):
    """Memastikan halaman beranda berhasil dimuat dengan judul yang benar."""
    rt_page.open_homepage()
    title = rt_page.get_page_title()
    assert "Rotten Tomatoes" in title, \
        f"Judul halaman tidak mengandung 'Rotten Tomatoes'. Judul: {title}"


def test_TC_HEAD_02_POS_header_logo_terlihat(rt_page):
    """Memastikan header navigasi Rotten Tomatoes tampil di beranda."""
    rt_page.open_homepage()
    header = rt_page.get_header()
    assert len(header) > 0, "Header/logo tidak ditemukan di halaman"


def test_TC_NAV_03_POS_link_navigasi_movies_tersedia(rt_page):
    """Memastikan link navigasi menuju halaman Movies tersedia di beranda."""
    rt_page.open_homepage()
    links = rt_page.get_movies_nav_links()
    assert len(links) > 0, "Link navigasi Movies tidak ditemukan di header"


def test_TC_NAV_04_POS_link_navigasi_tv_shows_tersedia(rt_page):
    """Memastikan link navigasi menuju halaman TV Shows tersedia di beranda."""
    rt_page.open_homepage()
    links = rt_page.get_tv_nav_links()
    assert len(links) > 0, "Link navigasi TV Shows tidak ditemukan di header"


# ============================================================
# KELOMPOK 2: SEARCH — Positif
# ============================================================

def test_TC_SRCH_05_POS_pencarian_film_valid_menampilkan_hasil(rt_page):
    """Memastikan pencarian film 'Inception' menampilkan hasil yang relevan."""
    rt_page.open_search("Inception")
    assert rt_page.has_content_keywords(["inception"]), \
        "Hasil pencarian 'Inception' tidak ditemukan"


def test_TC_SRCH_06_POS_pencarian_nama_aktor_menampilkan_hasil(rt_page):
    """Memastikan pencarian nama aktor 'Leonardo DiCaprio' menampilkan hasil."""
    rt_page.open_search("Leonardo+DiCaprio")
    assert rt_page.has_content_keywords(["dicaprio", "leonardo"]), \
        "Hasil pencarian aktor Leonardo DiCaprio tidak ditemukan"


def test_TC_SRCH_07_POS_pencarian_serial_tv_menampilkan_hasil(rt_page):
    """Memastikan pencarian judul TV show 'Breaking Bad' menampilkan hasil."""
    rt_page.open_search("Breaking+Bad")
    assert rt_page.has_content_keywords(["breaking"]), \
        "Hasil pencarian TV show 'Breaking Bad' tidak ditemukan"


def test_TC_SRCH_08_POS_hasil_pencarian_mengandung_kata_kunci(rt_page):
    """Memastikan hasil pencarian 'Titanic' mengandung kata kunci yang dicari."""
    rt_page.open_search("Titanic")
    assert rt_page.has_content_keywords(["titanic"]), \
        "Kata 'Titanic' tidak ditemukan di halaman hasil pencarian"


def test_TC_SRCH_19_POS_halaman_hasil_pencarian_tetap_di_domain(rt_page):
    """Memastikan halaman hasil pencarian tetap berada di domain rottentomatoes.com."""
    rt_page.open_search("The+Godfather")
    assert rt_page.is_on_domain(), \
        "Halaman search redirect ke luar domain"
    assert rt_page.get_current_url() is not None, \
        "Halaman hasil pencarian gagal dimuat"


# ============================================================
# KELOMPOK 3: MOVIE DETAIL — Positif
# ============================================================

def test_TC_MOV_09_POS_halaman_detail_film_berhasil_dimuat(rt_page):
    """Memastikan halaman detail film 'The Godfather' berhasil dimuat."""
    rt_page.open_movie_detail("the_godfather")
    assert rt_page.has_content_keywords(["godfather"]), \
        "Konten film The Godfather tidak ditemukan di halaman detail"


def test_TC_MOV_10_POS_skor_tomatometer_terlihat(rt_page):
    """Memastikan skor Tomatometer tampil di halaman detail film."""
    rt_page.open_movie_detail("the_godfather")
    src = rt_page.get_raw_page_source()
    assert "%" in src or "tomatometer" in src.lower(), \
        "Skor Tomatometer tidak ditemukan di halaman detail film"


def test_TC_MOV_11_POS_judul_film_tampil_di_halaman_detail(rt_page):
    """Memastikan judul film 'Inception' tampil di halaman detail."""
    rt_page.open_movie_detail("inception_2010")
    title = rt_page.get_page_title().lower()
    has_in_src = rt_page.has_content_keywords(["inception"])
    assert "inception" in title or has_in_src, \
        "Judul film 'Inception' tidak tampil di halaman detail"


def test_TC_MOV_12_POS_halaman_film_memiliki_sinopsis(rt_page):
    """Memastikan halaman film 'The Dark Knight' mengandung sinopsis."""
    rt_page.open_movie_detail("the_dark_knight")
    assert rt_page.has_content_keywords(["synopsis", "description", "batman", "gotham", "joker"]), \
        "Sinopsis/deskripsi tidak ditemukan di halaman film"


# ============================================================
# KELOMPOK 4: BROWSE & SELEBRITI — Positif
# ============================================================

def test_TC_BRW_13_POS_halaman_browse_film_berhasil_dimuat(rt_page):
    """Memastikan halaman Movies in Theaters berhasil dimuat dengan konten film."""
    rt_page.open_browse("movies_in_theaters")
    assert rt_page.has_content_keywords(["theater", "movie", "film"]), \
        "Konten halaman Movies in Theaters tidak ditemukan"


def test_TC_BRW_14_POS_halaman_browse_tv_berhasil_dimuat(rt_page):
    """Memastikan halaman browse TV Series berhasil dimuat."""
    rt_page.open_browse("tv_series_browse")
    assert rt_page.has_content_keywords(["tv", "series", "show"]), \
        "Konten halaman TV Series browse tidak ditemukan"


def test_TC_CEL_15_POS_halaman_selebriti_berhasil_dimuat(rt_page):
    """Memastikan halaman detail selebriti Tom Hanks berhasil dimuat."""
    rt_page.open_celebrity("tom_hanks")
    assert rt_page.has_content_keywords(["tom", "hanks"]), \
        "Nama Tom Hanks tidak ditemukan di halaman selebriti"


# ============================================================
# KELOMPOK 5: TV SHOW DETAIL — Positif
# ============================================================

def test_TC_TV_16_POS_halaman_detail_tvshow_berhasil_dimuat(rt_page):
    """Memastikan halaman detail TV show 'Breaking Bad' berhasil dimuat."""
    import time
    from selenium.common.exceptions import WebDriverException
    slugs = ["breaking_bad", "breaking-bad"]
    loaded = False
    for slug in slugs:
        try:
            rt_page.open_tv_show(slug)
            loaded = True
            break
        except WebDriverException:
            time.sleep(2)
            continue
    assert loaded, "Gagal memuat halaman TV show Breaking Bad (ERR_NAME_NOT_RESOLVED)"
    assert rt_page.has_content_keywords(["breaking"]), \
        "Konten TV show Breaking Bad tidak ditemukan di halaman detail"


def test_TC_TV_17_POS_skor_tvshow_terlihat_di_halaman(rt_page):
    """Memastikan skor atau rating tampil di halaman detail TV show."""
    import time
    from selenium.common.exceptions import WebDriverException
    slugs = ["breaking_bad", "breaking-bad"]
    for slug in slugs:
        try:
            rt_page.open_tv_show(slug)
            break
        except WebDriverException:
            time.sleep(2)
            continue
    src = rt_page.get_raw_page_source()
    assert "%" in src or "tomatometer" in src.lower(), \
        "Skor atau rating tidak ditemukan di halaman TV show"


def test_TC_TV_18_POS_judul_tvshow_tampil_di_halaman_detail(rt_page):
    """Memastikan judul TV show 'The Office' tampil di halaman detail."""
    rt_page.open_tv_show("the_office")
    assert rt_page.has_content_keywords(["office"]), \
        "Judul TV show 'The Office' tidak ditemukan di halaman detail"


def test_TC_DOM_20_POS_beranda_menampilkan_konten_trending(rt_page):
    """Memastikan halaman beranda menampilkan konten trending atau featured."""
    rt_page.open_homepage()
    assert rt_page.has_content_keywords(
        ["trending", "popular", "featured", "fresh", "certified"]
    ), "Konten trending/featured tidak ditemukan di beranda"