# ============================================================
# KELOMPOK 1: HOMEPAGE — Negatif
# ============================================================

def test_TC_HOME_01_NEG_url_tidak_valid_menampilkan_halaman_error(rt_page):
    """Memastikan URL path tidak valid menampilkan halaman error, bukan server crash."""
    rt_page.open_url("/halaman_yang_tidak_ada_sama_sekali_xyz")
    assert rt_page.has_error_page_indicator(), \
        "Halaman error tidak tampil untuk URL tidak valid"


def test_TC_HEAD_02_NEG_url_karakter_khusus_tidak_crash(rt_page):
    """Memastikan URL dengan karakter khusus tidak menyebabkan crash browser."""
    rt_page.open_url("/!@#$%^&*()")
    assert rt_page.get_current_url() is not None, \
        "Browser crash saat mengakses URL dengan karakter khusus"


def test_TC_NAV_03_NEG_akses_root_tetap_di_domain(rt_page):
    """Memastikan akses path root tidak redirect ke luar domain."""
    rt_page.open_url("/")
    assert rt_page.get_current_url().startswith("https://www.rottentomatoes.com"), \
        "Redirect tidak terduga ke luar domain rottentomatoes.com"


def test_TC_NAV_04_NEG_link_tv_shows_tidak_ada_di_halaman_error(rt_page):
    """
    Memastikan halaman 404 menampilkan indikator error, bukan konten beranda normal.

    CATATAN PERBAIKAN: RT adalah Single Page App — elemen <a href='/tv'> tetap
    ada di DOM bahkan di halaman 404 (header di-render oleh JS). Oleh karena itu,
    assertion diubah dari "cek jumlah link == 0" menjadi "cek halaman menampilkan
    indikator error", yang merupakan tujuan test yang sesungguhnya.
    """
    rt_page.open_url("/halaman_tidak_ada_xyz_abc_999")
    assert rt_page.has_error_page_indicator(), \
        "Halaman 404/error seharusnya tampil untuk URL yang tidak ada"


# ============================================================
# KELOMPOK 2: SEARCH — Negatif
# ============================================================

def test_TC_SRCH_05_NEG_pencarian_kosong_tidak_crash(rt_page):
    """Memastikan pencarian dengan query kosong tidak menyebabkan crash atau error 500."""
    rt_page.open_search("")
    assert rt_page.get_current_url() is not None, \
        "Browser crash saat melakukan pencarian kosong"
    assert rt_page.is_page_loaded_without_server_error(), \
        "Server error 500 terdeteksi saat pencarian kosong"


def test_TC_SRCH_06_NEG_pencarian_karakter_khusus_tidak_crash(rt_page):
    """Memastikan pencarian dengan karakter khusus tidak menyebabkan error 500."""
    rt_page.open_search("%21%40%23%24%25")  # fully encoded: !@#$%
    assert rt_page.is_page_loaded_without_server_error(), \
        "Server error 500 saat pencarian karakter khusus"


def test_TC_SRCH_07_NEG_pencarian_judul_tidak_ada_tampilkan_pesan(rt_page):
    """Memastikan pencarian judul yang tidak ada menampilkan pesan no results."""
    rt_page.open_search("xyznonexistentmovie123456789abc")
    assert rt_page.has_content_keywords(
        ["no results", "no result", "0 result", "couldn't find"]
    ), "Pesan 'no results' tidak tampil untuk pencarian yang tidak ada hasilnya"


def test_TC_SRCH_08_NEG_pencarian_teks_sangat_panjang_tidak_crash(rt_page):
    """Memastikan pencarian dengan string sangat panjang tidak menyebabkan crash."""
    long_query = "a" * 500
    rt_page.open_search(long_query)
    assert rt_page.get_current_url() is not None, \
        "Browser crash saat melakukan pencarian dengan input sangat panjang"


def test_TC_SRCH_19_NEG_pencarian_angka_saja_tidak_crash(rt_page):
    """Memastikan pencarian hanya angka tidak menyebabkan error 500."""
    rt_page.open_search("123456789")
    assert rt_page.is_page_loaded_without_server_error(), \
        "Server error saat pencarian dengan angka saja"


# ============================================================
# KELOMPOK 3: MOVIE DETAIL — Negatif
# ============================================================

def test_TC_MOV_09_NEG_id_film_tidak_valid_menampilkan_error(rt_page):
    """Memastikan ID film tidak valid menampilkan halaman error 404."""
    rt_page.open_movie_detail("this_movie_does_not_exist_xyz_abc_999")
    assert rt_page.has_error_page_indicator(), \
        "Halaman error tidak tampil untuk ID film yang tidak valid"


def test_TC_MOV_10_NEG_skor_tomatometer_tidak_ada_di_film_tidak_valid(rt_page):
    """
    Memastikan skor Tomatometer pada konten film tidak tampil di halaman film tidak valid.

    CATATAN PERBAIKAN: Kata 'tomatometer' muncul di footer/meta RT bahkan di halaman 404.
    Solusi: cek elemen skor spesifik menggunakan CSS selector pada konten utama film,
    bukan seluruh page source.
    """
    rt_page.open_movie_detail("this_movie_does_not_exist_xyz_abc_999")
    assert not rt_page.has_score_element_in_main_content(), \
        "Elemen skor Tomatometer pada konten film seharusnya tidak ada di halaman tidak valid"


def test_TC_MOV_11_NEG_judul_film_tidak_tampil_untuk_slug_salah(rt_page):
    """Memastikan judul film 'Inception' tidak tampil jika slug film salah/tidak valid."""
    rt_page.open_movie_detail("this_movie_does_not_exist_xyz_abc_999")
    title = rt_page.get_page_title().lower()
    has_in_src = rt_page.has_content_keywords(["inception"])
    assert "inception" not in title and not has_in_src, \
        "Judul 'Inception' seharusnya tidak tampil di halaman film yang tidak valid"


def test_TC_MOV_12_NEG_sinopsis_tidak_ada_di_film_tidak_valid(rt_page):
    """
    Memastikan sinopsis film tidak tampil di halaman film dengan slug tidak valid.

    CATATAN PERBAIKAN: Kata 'description' hadir di meta tag HTML setiap halaman.
    Solusi: hapus 'description' dari keyword dan hanya cek kata kunci konten film
    yang benar-benar spesifik (batman, gotham, joker, synopsis).
    """
    rt_page.open_movie_detail("this_movie_does_not_exist_xyz_abc_999")
    assert not rt_page.has_content_keywords(
        ["synopsis", "batman", "gotham", "joker"]
    ), "Sinopsis/deskripsi film seharusnya tidak ditemukan di halaman film yang tidak valid"


# ============================================================
# KELOMPOK 4: BROWSE & SELEBRITI — Negatif
# ============================================================

def test_TC_BRW_13_NEG_kategori_browse_tidak_valid_tidak_crash(rt_page):
    """Memastikan kategori browse tidak valid tidak menyebabkan server error."""
    rt_page.open_browse("invalid_category_xyz")
    assert rt_page.is_page_loaded_without_server_error(), \
        "Server error 500 untuk kategori browse yang tidak valid"


def test_TC_BRW_14_NEG_slug_tvshow_tidak_valid_tidak_server_error(rt_page):
    """Memastikan slug TV show tidak valid tidak menyebabkan server error 500."""
    rt_page.open_tv_show("nonexistent_show_xyz_abc_123")
    assert rt_page.is_page_loaded_without_server_error(), \
        "Server error 500 untuk slug TV show yang tidak valid"


def test_TC_CEL_15_NEG_slug_selebriti_tidak_valid_tampilkan_error(rt_page):
    """Memastikan slug selebriti tidak valid menampilkan halaman error."""
    rt_page.open_celebrity("nonexistent_person_xyz_abc")
    assert rt_page.has_error_page_indicator(), \
        "Halaman error tidak tampil untuk slug selebriti yang tidak ada"


# ============================================================
# KELOMPOK 5: TV SHOW DETAIL — Negatif
# ============================================================

def test_TC_TV_16_NEG_konten_tvshow_tidak_ada_untuk_slug_tidak_valid(rt_page):
    """
    Memastikan konten TV show tidak ditemukan di elemen utama untuk slug tidak valid.

    CATATAN PERBAIKAN: Kata 'breaking' bisa muncul di bagian lain halaman (misalnya
    headline berita di sidebar RT). Solusi: cek elemen konten utama TV show, bukan
    seluruh page source. Halaman invalid menampilkan error indicator, bukan konten show.
    """
    rt_page.open_tv_show("nonexistent_show_xyz_abc_999")
    assert rt_page.has_error_page_indicator() or \
        not rt_page.has_main_content_keyword("breaking"), \
        "Konten TV show 'breaking' seharusnya tidak ditemukan di halaman tidak valid"


def test_TC_TV_17_NEG_skor_tidak_tampil_di_tvshow_tidak_valid(rt_page):
    """
    Memastikan elemen skor tidak tampil pada konten TV show yang tidak valid.

    CATATAN PERBAIKAN: Tanda '%' dan 'tomatometer' bisa muncul di mana saja di halaman
    RT (footer, sidebar, meta). Solusi: cek elemen skor pada konten utama show.
    """
    rt_page.open_tv_show("nonexistent_show_xyz_abc_999")
    assert not rt_page.has_score_element_in_main_content(), \
        "Elemen skor pada konten show seharusnya tidak tampil di halaman tidak valid"


def test_TC_TV_18_NEG_judul_tvshow_tidak_tampil_untuk_slug_tidak_valid(rt_page):
    """
    Memastikan judul TV show tidak tampil di konten utama halaman slug tidak valid.

    CATATAN PERBAIKAN: Kata 'office' bisa muncul di link navigasi atau footer RT.
    Solusi: cek elemen judul pada konten utama, atau konfirmasi halaman adalah error page.
    """
    rt_page.open_tv_show("nonexistent_show_xyz_abc_999")
    assert rt_page.has_error_page_indicator() or \
        not rt_page.has_main_content_keyword("the office"), \
        "Judul 'The Office' seharusnya tidak ditemukan di konten utama halaman tidak valid"


def test_TC_DOM_20_NEG_beranda_parameter_tidak_valid_tidak_server_error(rt_page):
    """Memastikan beranda dengan parameter URL tidak valid tidak menyebabkan server error 500."""
    rt_page.open_url("/?q=%21%40%23%24%25%5E%26")
    assert rt_page.is_page_loaded_without_server_error(), \
        "Server error 500 saat mengakses beranda dengan parameter URL tidak valid"