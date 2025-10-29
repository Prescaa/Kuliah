import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import pycountry

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Dashboard Analisis Biaya & Kualitas Universitas",
    layout="wide"
)

# 2. GAYA CSS KUSTOM (DARK MODE)
st.markdown("""
<style>
    .stApp { background-color: #222222; color: #E0E0E0; }
    [data-testid="stSidebar"] { background-color: #2A3F54; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, [data-testid="stSidebar"] label, [data-testid="stSidebar"] .st-bd { color: white; }
    [data-testid="stMetric"] {
        border-radius: 10px; padding: 20px; color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: none;
    }
    div[data-testid="stHorizontalBlock"]:nth-of-type(1) { gap: 20px; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(1) > div:nth-child(1) [data-testid="stMetric"] {
        background: linear-gradient(135deg, #7F7FD5, #86A8E7);
    }
    div[data-testid="stHorizontalBlock"]:nth-of-type(1) > div:nth-child(2) [data-testid="stMetric"] {
        background: linear-gradient(135deg, #FAD961, #F76B1C);
    }
    [data-testid="stMetric"] [data-testid="stMetricLabel"] { color: rgba(255, 255, 255, 0.85); }
    [data-testid="stMetric"] [data-testid="stMetricValue"] { color: white; font-size: 2.2rem; }
    .stPlotlyChart, [data-testid="stExpander"] {
        border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        overflow: hidden; background-color: #303030;
    }
    [data-testid="stExpander"] summary {
        background-color: #303030; border-radius: 10px; padding: 10px; color: white;
    }
    [data-testid="stExpander"] .st-emotion-cache-1h9usn1 { background-color: #303030; }
    [data-testid="stExpander"] .stDataFrame { background-color: #303030; }
    h1, h2, h3, h4, h5 { color: white; }
    [data-testid="stImage"] img { border-radius: 10px; }
    [data-testid="stImage"] { margin-bottom: 10px; }
    [data-testid="stCaption"] {
        color: #E0E0E0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. FUNGSI MEMUAT DATA
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()
        if 'Country' in df.columns: df['Country'] = df['Country'].astype(str)
        if 'Rank' in df.columns: df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
        cols_to_convert = ['Overall Score', 'Teaching', 'Research Environment',
                           'Research Quality', 'Industry Impact', 'International Outlook',
                           'Cost of Living Index', 'Rent Index', 'Groceries Index',
                           'Restaurant Price Index', 'Local Purchasing Power Index']
        for col in cols_to_convert:
            if col in df.columns: df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    except FileNotFoundError:
        st.error(f"File data CSV '{file_path}' tidak ditemukan."); return None
    except Exception as e:
        st.error(f"Terjadi error saat memuat data CSV: {e}"); return None

# 4. FUNGSI BANTU UNTUK PETA
@st.cache_data
def get_iso_alpha3(country_name):
    if pd.isna(country_name) or country_name == '': return None
    try:
        country_name_lower = country_name.lower()
        if country_name_lower == "usa": return "USA"
        if country_name_lower == "uk": return "GBR"
        if country_name == "South Korea": return "KOR"
        if country_name == "Taiwan": return "TWN"
        country = pycountry.countries.get(name=country_name)
        if country: return country.alpha_3
        country_fuzzy = pycountry.countries.search_fuzzy(country_name)
        if country_fuzzy: return country_fuzzy[0].alpha_3
        return None
    except Exception:
        return None

# 5. MUAT DATA
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMA_FILE_CSV = os.path.join(BASE_DIR, "Data_Universitas_Final.csv")
df = load_data(NAMA_FILE_CSV)

# 6. MEMBUAT DASHBOARD
if df is not None:
    st.image(os.path.join(os.path.dirname(__file__), "MIT.jpg"), use_container_width=True)
    st.title("Dashboard Kualitas Universitas & Biaya Hidup 2024")
    st.markdown("### About Us")
    st.markdown("""
    Dashboard ini dirancang untuk menjembatani kesenjangan informasi kritis yang dihadapi calon mahasiswa: menyeimbangkan desakan untuk kualitas akademik (skor peringkat, reputasi riset) dengan realitas biaya hidup (indeks sewa, daya beli lokal). Karena data kualitas dan biaya ini seringkali terpisah, misi kami adalah mengintegrasikan kedua set data tersebut ke dalam satu platform visual yang intuitif. Tujuannya adalah memberdayakan calon mahasiswa untuk menemukan "keseimbangan" optimal atau 'nilai terbaik' dari sebuah universitas, bukan sekadar mencari opsi termurah.
    """)
    st.divider()

    country_col = 'Country'
    score_col = 'Overall Score'
    cost_index_col = 'Cost of Living Index'
    rank_col = 'Rank'
    name_col = 'Name'
    rent_index_col = 'Rent Index'
    purchasing_power_col = 'Local Purchasing Power Index'
    teaching_col = 'Teaching'
    research_col = 'Research Environment'
    research_qual_col = 'Research Quality'
    industry_col = 'Industry Impact'
    available_cost_metrics = ['Cost of Living Index', 'Rent Index', 'Groceries Index',
                              'Restaurant Price Index', 'Local Purchasing Power Index']
    valid_cost_metrics = [col for col in available_cost_metrics if col in df.columns]

    st.sidebar.header("Filter Data")
    selected_countries = []
    if country_col in df.columns:
        unique_countries = sorted(df[country_col].dropna().unique())
        default_countries_list = ['United States', 'United Kingdom', 'Switzerland', 'China', 'Singapore', 'Canada', 'Japan', 'Germany', 'Hong Kong', 'Australia', 'France', 'Belgium', 'Netherlands', 'Denmark', 'South Korea']
        valid_default_countries = [c for c in default_countries_list if c in unique_countries]
        if not valid_default_countries:
            valid_default_countries = unique_countries[:15]
        selected_countries = st.sidebar.multiselect(
            "Pilih Negara:", 
            options=unique_countries, 
            default=valid_default_countries
        )
    else:
        st.sidebar.error(f"Kolom '{country_col}' tidak ditemukan.")

    selected_cost_metric = cost_index_col
    if valid_cost_metrics:
        selected_cost_metric = st.sidebar.selectbox(
            "Pilih Metrik Biaya untuk Sumbu X:",
            options=valid_cost_metrics,
            index=valid_cost_metrics.index(cost_index_col) if cost_index_col in valid_cost_metrics else 0
        )
    else:
        st.sidebar.error("Tidak ada kolom biaya yang valid ditemukan."); selected_cost_metric = None

    score_categories = {
        "Semua Kategori": (0, 101), "Sempurna (90+)": (90, 101), "Sangat Baik (70-89)": (70, 90),
        "Baik (50-69)": (50, 70), "Cukup (30-49)": (30, 50), "Berkembang (<30)": (0, 30)
    }
    selected_score_category = st.sidebar.selectbox(
        "Pilih Kategori Skor Keseluruhan:",
        options=list(score_categories.keys()),
        index=0
    )
    selected_rank_range = (1, 2000)
    if rank_col in df.columns:
        valid_ranks = df[rank_col].dropna()
        min_rank_val = int(valid_ranks.min()) if not valid_ranks.empty else 1
        max_rank_val = int(valid_ranks.max()) if not valid_ranks.empty else 2000
        selected_rank_range = st.sidebar.slider(
            "Rentang Peringkat (Rank):",
            min_value=min_rank_val, max_value=max_rank_val,
            value=(min_rank_val, max_rank_val)
        )
    else:
        st.sidebar.warning(f"Kolom '{rank_col}' tidak ditemukan untuk filter.")

    df_filtered = df.copy()
    if selected_countries and country_col in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[country_col].isin(selected_countries)]
    elif not selected_countries and country_col in df.columns:
        st.warning("Pilih setidaknya satu negara di sidebar untuk melihat data."); df_filtered = pd.DataFrame(columns=df.columns)

    if selected_score_category != "Semua Kategori" and score_col in df_filtered.columns:
        min_s, max_s = score_categories[selected_score_category]
        df_filtered = df_filtered.dropna(subset=[score_col])
        df_filtered = df_filtered[(df_filtered[score_col] >= min_s) & (df_filtered[score_col] < max_s)]
    elif score_col not in df_filtered.columns:
        st.warning(f"Kolom '{score_col}' tidak ditemukan untuk filter skor."); df_filtered = pd.DataFrame(columns=df.columns)

    if rank_col in df_filtered.columns:
        df_filtered = df_filtered.dropna(subset=[rank_col])
        df_filtered = df_filtered[(df_filtered[rank_col] >= selected_rank_range[0]) & (df_filtered[rank_col] <= selected_rank_range[1])]

    st.markdown("### Ringkasan & Analisis Biaya vs Kualitas (Sesuai Filter)")
    col_m1, col_m3 = st.columns(2)
    col_m1.metric("Jumlah Universitas", f"{len(df_filtered)}")
    median_cost_val = df_filtered[[country_col, selected_cost_metric]].drop_duplicates()[selected_cost_metric].median() if selected_cost_metric in df_filtered.columns and not df_filtered.empty else None
    col_m3.metric(f"Median {selected_cost_metric}", f"{median_cost_val:.1f}" if median_cost_val else "N/A")
    st.divider()

    display_title_country = f"{len(selected_countries)} Negara Terpilih" if selected_countries else "Global"
    st.markdown(f"#### Analisis Keseimbangan Skor Keseluruhan dan '{selected_cost_metric}' ({display_title_country})")
    vis1_col1, vis1_col2 = st.columns(2)
    global_avg_score = df[score_col].mean() if score_col in df.columns else None
    global_avg_cost = df[selected_cost_metric].mean() if selected_cost_metric in df.columns else None

    with vis1_col1:
        if selected_cost_metric in df_filtered.columns and score_col in df_filtered.columns and country_col in df_filtered.columns and not df_filtered.empty:
            score_text = f"{global_avg_score:.1f}" if global_avg_score is not None else 'N/A'
            cost_text = f"{global_avg_cost:.1f}" if global_avg_cost is not None else 'N/A'
            st.markdown(f"### Rata-rata Global: Skor Keseluruhan vs 'Cost of Living Index")
            fig_scatter_cost = px.scatter(df_filtered,
                                          x=selected_cost_metric, y=score_col, color=country_col,
                                          hover_data=[name_col, rank_col, country_col],
                                          title=f"Skor Keseluruhan vs '{selected_cost_metric}'",
                                          labels={selected_cost_metric: selected_cost_metric, score_col: "Skor Keseluruhan"},
                                          template="plotly_dark")
            if global_avg_score is not None: fig_scatter_cost.add_hline(y=global_avg_score, line_dash="dot", annotation_text="Rata-Rata Skor Global", annotation_position="bottom right")
            if global_avg_cost is not None: fig_scatter_cost.add_vline(x=global_avg_cost, line_dash="dot", annotation_text="Rata-Rata Biaya Global", annotation_position="bottom right")
            st.plotly_chart(fig_scatter_cost, use_container_width=True)
        else:
            st.warning("Data tidak cukup untuk Scatter Plot Skor vs Biaya.")

    with vis1_col2:
        st.markdown(f"##### Rata-rata Skor Keseluruhan per Negara (Terpilih)")
        if score_col in df_filtered.columns and country_col in df_filtered.columns and not df_filtered.empty:
                avg_score_by_country = df_filtered.groupby(country_col)[score_col].mean().sort_values(ascending=False).reset_index().head(30) 
                fig_avg_score_bar = px.bar(avg_score_by_country,
                                           x=country_col, y=score_col,
                                           title=f"Rata-rata Skor Keseluruhan di Negara Terpilih (Max 30)",
                                           labels={country_col: "Negara", score_col: "Rata-rata Skor"},
                                           template="plotly_dark")
                st.plotly_chart(fig_avg_score_bar, use_container_width=True)
        else:
            st.warning(f"Data tidak cukup atau kolom '{score_col}'/'{country_col}' tidak ada.")
    st.divider()

    st.markdown("#### Analisis Komponen & Peringkat")
    vis2_col1, vis2_col2 = st.columns(2)
    with vis2_col1:
        st.markdown(f"##### Top Universitas (Berdasarkan Skor Keseluruhan, Sesuai Filter)")
        num_top_univ = st.slider("Jumlah Top Universitas Ditampilkan:", 5, 25, 10, key='slider_top_univ')
        if score_col in df_filtered.columns and name_col in df_filtered.columns and not df_filtered.empty:
            top_n_univ = df_filtered.nlargest(num_top_univ, score_col).sort_values(score_col, ascending=True)
            fig_bar_top = px.bar(top_n_univ, x=score_col, y=name_col, orientation='h',
                                 title=f"Top {num_top_univ} Univ. (Sesuai Filter)",
                                 labels={name_col: "Universitas", score_col: "Skor Keseluruhan"},
                                 template="plotly_dark")
            fig_bar_top.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_bar_top, use_container_width=True)
        else:
            st.warning("Data tidak cukup atau kolom skor/nama tidak ditemukan.")

    with vis2_col2:
        st.markdown(f"##### Skor Keseluruhan vs Peringkat (Sesuai Filter)")
        if score_col in df_filtered.columns and rank_col in df_filtered.columns and not df_filtered.empty:
            fig_scatter_rank = px.scatter(df_filtered,
                                          x=rank_col, y=score_col, color=country_col,
                                          hover_data=[name_col, country_col],
                                          title=f"Hubungan Skor Keseluruhan vs Peringkat",
                                          labels={rank_col: "Peringkat (Rank)", score_col: "Skor Keseluruhan"},
                                          template="plotly_dark")
            st.plotly_chart(fig_scatter_rank, use_container_width=True)
        else:
            st.warning(f"Kolom '{score_col}' atau '{rank_col}' tidak ditemukan.")
    st.divider()

    st.markdown("#### Detail Biaya & Proporsi Negara")
    vis3_col1, vis3_col2 = st.columns(2)
    with vis3_col1:
        st.markdown("##### Proporsi Universitas per Negara (Global Top 10)")
        if country_col in df.columns:
            country_counts_global = df[country_col].value_counts().head(10)
            fig_pie_global = px.pie(country_counts_global, values=country_counts_global.values,
                                    names=country_counts_global.index,
                                    title="10 Negara dengan Universitas Terbanyak (Global)",
                                    template="plotly_dark")
            st.plotly_chart(fig_pie_global, use_container_width=True)
        else:
            st.warning(f"Kolom '{country_col}' tidak ditemukan.")

    with vis3_col2:
        st.markdown("##### Perbandingan Indeks Kunci Biaya (Negara Terpilih)")
        comparison_indices = [cost_index_col, rent_index_col, purchasing_power_col]
        valid_comparison_cols = [col for col in comparison_indices if col in df_filtered.columns]
        if country_col in df_filtered.columns and valid_comparison_cols and not df_filtered.empty:
            comparison_data = df_filtered[[country_col] + valid_comparison_cols].drop_duplicates(subset=[country_col])
            if not comparison_data.empty:
                comparison_melted = comparison_data.melt(id_vars=[country_col], value_vars=valid_comparison_cols,
                                                         var_name='Jenis Indeks', value_name='Nilai Indeks')
                fig_bar_comparison = px.bar(comparison_melted, x=country_col, y='Nilai Indeks',
                                            color='Jenis Indeks', barmode='group',
                                            title="Biaya Hidup, Sewa, Daya Beli (Semua Negara Terpilih)", 
                                            labels={country_col: "Negara", 'Nilai Indeks': "Nilai Indeks"},
                                            hover_data={'Jenis Indeks': True, 'Nilai Indeks': ':.1f'},
                                            template="plotly_dark")
                st.plotly_chart(fig_bar_comparison, use_container_width=True)
                st.caption("Biaya Hidup & Sewa: Makin rendah makin murah. Daya Beli: Makin tinggi makin terjangkau.")
            else:
                st.warning("Tidak ada data pembanding biaya untuk ditampilkan pada filter ini.")
        else:
            st.warning("Data tidak cukup atau kolom negara/indeks pembanding tidak ditemukan.")
    st.divider()

    st.markdown("### Peta Global: Biaya Hidup dan Jumlah Universitas")
    map_col1, map_col2 = st.columns(2)
    map_agg_data = pd.DataFrame()
    try:
        agg_functions = {'Name': ('count', 'univ_count')}
        if score_col in df.columns: agg_functions[score_col] = ('mean', 'avg_score')
        if cost_index_col in df.columns: agg_functions[cost_index_col] = (lambda x: x.iloc[0], 'avg_cost')
        final_agg_dict = {alias: pd.NamedAgg(column=col, aggfunc=func) for col, (func, alias) in agg_functions.items() if col in df.columns}
        if country_col in df.columns and final_agg_dict:
            map_agg_data = df.groupby(country_col).agg(**final_agg_dict).reset_index()
            map_agg_data['iso_alpha'] = map_agg_data[country_col].apply(get_iso_alpha3)
            map_agg_data = map_agg_data.dropna(subset=['iso_alpha'])
        else:
            st.warning("Kolom negara atau kolom agregasi tidak ditemukan untuk peta.")
    except Exception as e:
        st.error(f"Gagal mempersiapkan data agregat untuk peta: {e}")

    with map_col1:
        st.markdown(f"#### Peta '{selected_cost_metric}'")
        map_cost_col_dynamic = selected_cost_metric
        cost_map_plot_data = df[[country_col, map_cost_col_dynamic]].dropna(subset=[map_cost_col_dynamic]).drop_duplicates(subset=[country_col]).copy()
        cost_map_plot_data['iso_alpha'] = cost_map_plot_data[country_col].apply(get_iso_alpha3)
        cost_map_plot_data = cost_map_plot_data.dropna(subset=['iso_alpha'])
        if not cost_map_plot_data.empty:
            fig_map_cost = px.choropleth(cost_map_plot_data,
                                         locations="iso_alpha", color=map_cost_col_dynamic,
                                         hover_name=country_col,
                                         color_continuous_scale=px.colors.sequential.Plasma,
                                         title=f"{selected_cost_metric} per Negara",
                                         template="plotly_dark")
            fig_map_cost.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
            st.plotly_chart(fig_map_cost, use_container_width=True)
        else: st.warning(f"Tidak bisa membuat peta untuk '{selected_cost_metric}'.")

    with map_col2:
        st.markdown("#### Peta Jumlah Universitas")
        if not map_agg_data.empty and 'univ_count' in map_agg_data.columns:
            hover_data_map2 = []
            if 'avg_cost' in map_agg_data.columns: hover_data_map2.append('avg_cost')
            if 'avg_score' in map_agg_data.columns: hover_data_map2.append('avg_score')
            fig_map_count = px.choropleth(map_agg_data,
                                          locations="iso_alpha", color='univ_count',
                                          hover_name=country_col, hover_data=hover_data_map2,
                                          color_continuous_scale=px.colors.sequential.Viridis,
                                          title="Jumlah Universitas Terdaftar per Negara",
                                          template="plotly_dark")
            fig_map_count.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
            st.plotly_chart(fig_map_count, use_container_width=True)
        else: st.warning("Tidak bisa membuat peta jumlah universitas.")
    st.divider()

    st.markdown("### Insights & Rekomendasi")
    insight_cols_ready = all(col in df.columns for col in [
        country_col, score_col, cost_index_col, name_col,
        teaching_col, research_col, research_qual_col, industry_col
    ])
    if insight_cols_ready:
        global_avg_cost_insight = df[cost_index_col].mean()
        overperformers_df = df[(df[score_col] > 80) & (df[cost_index_col] < global_avg_cost_insight)].nlargest(3, score_col)[[name_col, country_col, score_col, cost_index_col]]
        overperformers_df.columns = ['Universitas', 'Negara', 'Skor', 'Biaya Hidup']
        overperformers_df = overperformers_df.reset_index(drop=True)
        underperformers_df = df[(df[score_col] < 60) & (df[cost_index_col] > 80)].nsmallest(3, score_col)[[name_col, country_col, score_col, cost_index_col]]
        underperformers_df.columns = ['Universitas', 'Negara', 'Skor', 'Biaya Hidup']
        underperformers_df = underperformers_df.reset_index(drop=True)
        generalist_df = df[(df[teaching_col] > 85) & (df[research_col] > 85) & (df[research_qual_col] > 85)].nlargest(3, score_col)[[name_col, country_col, teaching_col, research_col, research_qual_col]]
        generalist_df.columns = ['Universitas', 'Negara', 'Teaching', 'Research Env.', 'Research Q.']
        generalist_df = generalist_df.reset_index(drop=True)
        specialist_df = df[(df[industry_col] > 90) & (df[teaching_col] < 80)].nlargest(3, industry_col)[[name_col, country_col, industry_col, score_col]]
        specialist_df.columns = ['Universitas', 'Negara', 'Industry Impact', 'Skor (Overall)']
        specialist_df = specialist_df.reset_index(drop=True)

        st.markdown("#### A. Analisis 'Value for Money': Universitas Overperform vs Underperform")
        st.caption("Universitas Top 'Overperform' (Kualitas Tinggi, Biaya di Bawah Rata-rata)")
        st.dataframe(overperformers_df, use_container_width=True, hide_index=True)
        st.caption("Universitas Top 'Underperform' (Kualitas Rendah, Biaya Sangat Tinggi)")
        st.dataframe(underperformers_df, use_container_width=True, hide_index=True)
        st.markdown("**Rekomendasi (actionable):**")
        st.markdown("""
        Bagi calon mahasiswa, sangat disarankan untuk memfokuskan pencarian pada universitas 'Overperform'. Calon mahasiswa dapat menggunakan **Scatter Plot 'Skor vs Biaya'** di atas dan mencari universitas di **Kuadran Kiri Atas** (Skor tinggi, Biaya rendah) untuk menemukan 'hidden gems' lainnya. Sementara itu, bagi institusi yang berada di area 'Underperform' (biaya tinggi), mereka harus secara proaktif mempertimbangkan penawaran beasiswa atau program bantuan keuangan agar tetap kompetitif secara global.
        """)
        st.markdown("---")
        st.markdown("#### B. Analisis Fokus Universitas: 'Generalis' vs 'Spesialis Industri'")
        st.caption("Top 3 'Generalis (All-Rounder)' (Kuat di Pengajaran & Riset)")
        st.dataframe(generalist_df, use_container_width=True, hide_index=True)
        st.caption("Top 3 'Spesialis Industri' (Sangat Kuat di Industri, Skor Lain Bervariasi)")
        st.dataframe(specialist_df, use_container_width=True, hide_index=True)
        st.markdown("**Rekomendasi (actionable):**")
        st.markdown("""
        Rekomendasi ini membantu calon mahasiswa menyesuaikan pilihan universitas dengan tujuan karir. Calon mahasiswa yang mencari pendidikan yang seimbang dan kuat secara akademis, universitas 'Generalis (All-Rounder)' adalah pilihan yang solid. Namun, jika calon mahasiswa lebih fokus untuk langsung masuk ke dunia industri atau mencari keunggulan spesifik di bidang inovasi, universitas 'Spesialis Industri' dengan skor Industry Impact tinggi mungkin menawarkan nilai lebih, meskipun skor pengajaran atau penelitiannya tidak setinggi yang lain.
        """)
        st.divider()
    else:
        st.warning("Kolom data (Country, Overall Score, Teaching, Industry Impact, dll.) tidak ditemukan, tidak dapat membuat insights.")
        st.divider()

    with st.expander("Lihat Data Lengkap (Sesuai Filter)"):
        st.dataframe(df_filtered)
else:
    st.error("Gagal memuat data. Silakan periksa file CSV.")







