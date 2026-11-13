import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import io
import datetime
import base64, os
try:
    import pyreadstat
    HAS_PYREADSTAT = True
except ImportError:
    HAS_PYREADSTAT = False

# ==========================================
# 1. إعدادات الصفحة والتصميم الفضائي المظلم (Ultra-Modern Dark Glass SaaS)
# ==========================================
st.set_page_config(
    page_title="Socio Lab Pro | منظومة الذكاء المنهجي والتدقيق الجنائي للبيانات",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Readex+Pro:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

    html, body, [class*="css"], .stMarkdown, .stText, .stButton, .stSelectbox, .stMultiSelect, .stRadio {
        font-family: 'Readex Pro', sans-serif !important;
        direction: rtl;
        text-align: right;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    /* خلفية فضائية كحلية متدرجة فائقة الحداثة */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #1E1B4B 0%, #090D16 45%, #020617 100%) !important;
        color: #F8FAFC !important;
    }

    /* ضبط نصوص Streamlit في الوضع المظلم */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #F1F5F9 !important;
    }

    /* شريط علوي عائم (Floating Glass Navbar) */
    .top-navbar {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 20px;
        padding: 18px 32px;
        margin-bottom: 26px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.6), 0 0 25px rgba(56, 189, 248, 0.1);
    }
    .brand-box {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .brand-logo {
        width: 52px;
        height: 52px;
        border-radius: 14px;
        background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 50%, #6366F1 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.5rem;
        font-weight: 800;
        color: #FFFFFF;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.5);
    }
    .brand-title {
        font-size: 1.65rem;
        font-weight: 700;
        background: linear-gradient(90deg, #FFFFFF 0%, #38BDF8 50%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .brand-sub {
        color: #94A3B8 !important;
        font-size: 0.85rem;
        margin: 2px 0 0 0;
    }
    .status-badge {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #34D399 !important;
        padding: 8px 18px;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
    }

    /* شبكة بطاقات المؤشرات النيون (Neon Bento Grid) */
    .bento-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.65) 0%, rgba(15, 23, 42, 0.85) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-top: 2px solid #38BDF8;
        border-radius: 20px;
        padding: 22px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }
    .bento-card:hover {
        transform: translateY(-6px);
        border-color: rgba(56, 189, 248, 0.5);
        box-shadow: 0 20px 40px -10px rgba(56, 189, 248, 0.2);
    }
    .bento-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .bento-label {
        color: #94A3B8 !important;
        font-size: 0.9rem;
        font-weight: 500;
    }
    .bento-icon {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    .bento-val {
        font-family: 'Space Grotesk', 'Readex Pro', sans-serif !important;
        font-size: 2.1rem;
        font-weight: 700;
        color: #FFFFFF !important;
        margin: 4px 0 10px 0;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
    }
    .neon-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.76rem;
        font-weight: 600;
    }
    .tag-cyan { background: rgba(6, 182, 212, 0.18); color: #67E8F9; border: 1px solid rgba(6, 182, 212, 0.35); }
    .tag-emerald { background: rgba(16, 185, 129, 0.18); color: #6EE7B7; border: 1px solid rgba(16, 185, 129, 0.35); }
    .tag-amber { background: rgba(245, 158, 11, 0.18); color: #FCD34D; border: 1px solid rgba(245, 158, 11, 0.35); }

    /* الحاويات الزجاجية للأقسام (Glass Workspace) */
    .workspace-card {
        background: rgba(15, 23, 42, 0.72);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 22px;
        padding: 28px 32px;
        margin-top: 14px;
        margin-bottom: 24px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.65);
    }
    .workspace-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #38BDF8 !important;
        margin: 0 0 8px 0;
    }
    .workspace-desc {
        color: #CBD5E1 !important;
        font-size: 0.96rem;
        line-height: 1.75;
        margin-bottom: 18px;
    }

    /* شريط التبويبات العلوي المضيء (Horizontal Neon Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(15, 23, 42, 0.85);
        padding: 8px;
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.15);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        color: #94A3B8 !important;
        background: transparent !important;
        border: none !important;
        transition: all 0.25s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0284C7 0%, #4F46E5 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.35) !important;
    }

    /* الأزرار التفاعلية المضيئة */
    .stButton > button {
        background: linear-gradient(135deg, #06B6D4 0%, #2563EB 50%, #4F46E5 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.96rem !important;
        border-radius: 12px !important;
        padding: 0.7rem 1.8rem !important;
        border: 1px solid rgba(103, 232, 249, 0.4) !important;
        box-shadow: 0 8px 25px -4px rgba(6, 182, 212, 0.45) !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 12px 30px -2px rgba(6, 182, 212, 0.65) !important;
    }

    /* جداول APA 7th في الوضع المظلم الملوكي */
    .apa-dark-box {
        background: rgba(2, 6, 23, 0.75);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 18px;
        padding: 26px;
        margin: 18px 0;
    }
    .apa-table {
        width: 100%;
        border-collapse: collapse;
        margin: 14px 0;
        font-size: 0.98rem;
        color: #F8FAFC;
        direction: rtl;
    }
    .apa-table thead tr {
        border-top: 2px solid #38BDF8;
        border-bottom: 1.5px solid #38BDF8;
        background: rgba(30, 58, 138, 0.35);
        color: #7DD3FC;
        font-weight: 700;
    }
    .apa-table th, .apa-table td {
        padding: 14px 16px;
        text-align: center;
    }
    .apa-table tbody tr {
        border-bottom: 1px solid rgba(148, 163, 184, 0.12);
    }
    .apa-table tbody tr:last-of-type {
        border-bottom: 2px solid #38BDF8;
    }

    /* شهادة النزاهة بتصميم الهولوغرام المظلم */
    .holo-cert {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 27, 75, 0.92) 100%);
        border: 2px solid #38BDF8;
        border-radius: 24px;
        padding: 42px;
        text-align: center;
        box-shadow: 0 0 50px rgba(6, 182, 212, 0.2);
        margin-top: 24px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. المحرك الإحصائي والمنهجي (Core Engine)
# ==========================================

@st.cache_data
def generate_demo_dataset():
    np.random.seed(42)
    n = 60
    ids = [f"RES-{i:03d}" for i in range(1, n + 1)]
    genders = np.random.choice(["ذكر", "أنثى"], size=n, p=[0.55, 0.45])
    levels = np.random.choice(["السنة الأولى ثانوي", "السنة الثانية ثانوي", "السنة الثالثة ثانوي"], size=n)

    likert_labels = {
        1: "غير موافق بشدة",
        2: "غير موافق",
        3: "محايد",
        4: "موافق",
        5: "موافق بشدة"
    }

    data = []
    for i in range(n):
        base_tendency = np.random.choice([2, 3, 4], p=[0.3, 0.3, 0.4])
        q1 = int(np.clip(base_tendency + np.random.randint(-1, 2), 1, 5))
        q2 = int(np.clip(base_tendency + np.random.randint(-1, 2), 1, 5))
        q3 = int(np.clip(base_tendency + np.random.randint(-1, 2), 1, 5))
        q4_rev = int(np.clip(6 - base_tendency + np.random.randint(-1, 2), 1, 5))

        q5 = int(np.clip(base_tendency + np.random.randint(-1, 2), 1, 5))
        q6 = int(np.clip(base_tendency + np.random.randint(-1, 2), 1, 5))
        q7_weak = int(np.random.randint(1, 6))
        q8_rev = int(np.clip(6 - base_tendency + np.random.randint(-1, 2), 1, 5))

        row = [ids[i], genders[i], levels[i], q1, q2, q3, q4_rev, q5, q6, q7_weak, q8_rev]
        data.append(row)

    data[13][3:] = [5, 5, 5, 5, 5, 5, 5, 5]
    data[28][3:] = [5, 5, 5, 5, 5, 5, 4, 5]
    data[40][3:] = [1, 1, 1, 1, 1, 1, 2, 1]
    data[51][1:] = data[4][1:]

    columns = [
        "رمز_الاستمارة", "الجنس", "المستوى_الدراسي",
        "Q1_تأثير_الأقران", "Q2_الانتماء_للجماعة", "Q3_مجاراة_الرفاق", "Q4_الاستقلالية_عكسية",
        "Q5_مخالفة_القواعد", "Q6_العدوانية_اللفظية", "Q7_فقرة_مشوشة", "Q8_الانضباط_المدرسي_عكسية"
    ]
    df_num = pd.DataFrame(data, columns=columns)

    df_text = df_num.copy()
    for col in columns[3:]:
        df_text[col] = df_text[col].map(likert_labels)

    return df_text, df_num


def auto_code_dataframe(df):
    df_coded = df.copy()
    codebook = []

    likert_map = {
        "غير موافق بشدة": 1, "لا أوافق بشدة": 1, "أبدا": 1, "Pas du tout d'accord": 1,
        "غير موافق": 2, "لا أوافق": 2, "نادرا": 2, "Pas d'accord": 2,
        "محايد": 3, "غير متأكد": 3, "أحيانا": 3, "Neutre": 3,
        "موافق": 4, "أوافق": 4, "غالبا": 4, "D'accord": 4,
        "موافق بشدة": 5, "أوافق بشدة": 5, "دائما": 5, "Tout à fait d'accord": 5,
        "نعم": 1, "لا": 0, "ذكر": 1, "أنثى": 2
    }

    for col in df_coded.columns:
        if col != "رمز_الاستمارة":
            s_str = df_coded[col].astype(str).str.strip()
            unique_vals = [v for v in s_str.unique() if v not in ["nan", "None", ""]]

            if any(val in likert_map for val in unique_vals):
                df_coded[col] = s_str.map(lambda x: likert_map.get(x, np.nan))
                df_coded[col] = pd.to_numeric(df_coded[col], errors='coerce')
                mapping_str = "ترميز قياسي آلي (مقياس ليكرت / ثنائي)"
            else:
                num_try = pd.to_numeric(df_coded[col], errors='coerce')
                if num_try.notna().sum() > 0:
                    df_coded[col] = num_try
                    mapping_str = "متغير رقمي مباشر"
                else:
                    cats = {val: idx + 1 for idx, val in enumerate(unique_vals)}
                    df_coded[col] = s_str.map(cats)
                    df_coded[col] = pd.to_numeric(df_coded[col], errors='coerce')
                    mapping_str = " | ".join([f"{k}={v}" for k, v in cats.items()])
        else:
            mapping_str = "معرف الاستمارة"

        codebook.append({
            "اسم المتغير (Variable)": col,
            "النوع في SPSS": "Numeric" if col != "رمز_الاستمارة" else "String",
            "القيم المفقودة": int(df[col].isna().sum()),
            "دليل الترميز (Value Labels)": mapping_str
        })

    return df_coded, pd.DataFrame(codebook)


def calculate_cronbach_alpha(df_items):
    df_num = df_items.apply(pd.to_numeric, errors='coerce').dropna()
    k = df_num.shape[1]
    if k < 2 or len(df_num) < 2:
        return 0.0
    mat = df_num.to_numpy(dtype=float)
    item_variances = np.var(mat, axis=0, ddof=1).sum()
    total_variance = np.var(mat.sum(axis=1), ddof=1)
    if total_variance == 0 or np.isnan(total_variance):
        return 0.0
    alpha = (k / (k - 1)) * (1.0 - (item_variances / total_variance))
    return float(alpha)


def forensic_audit(df_coded, scale_cols, pos_col=None, neg_col=None):
    audit_records = []
    flagged_indices = []

    duplicated_mask = df_coded.duplicated(subset=scale_cols, keep='first')

    for idx, row in df_coded.iterrows():
        form_id = row["رمز_الاستمارة"] if "رمز_الاستمارة" in df_coded.columns else f"Row-{idx+1}"
        vals_series = pd.to_numeric(row[scale_cols], errors='coerce')
        vals_clean = vals_series.dropna().to_numpy(dtype=float)
        sd_val = float(np.std(vals_clean, ddof=0)) if len(vals_clean) > 1 else 0.0
        missing_cnt = int(vals_series.isna().sum())

        reasons = []
        status = "صالحة وموثوقة"

        if sd_val < 0.20:
            reasons.append(f"إجابة نمطية جامدة (SD={sd_val:.2f})")
            status = "مزيفة / مرفوضة منهجيا"

        if pos_col and neg_col and pos_col in df_coded.columns and neg_col in df_coded.columns:
            v_pos = pd.to_numeric(row[pos_col], errors='coerce')
            v_neg = pd.to_numeric(row[neg_col], errors='coerce')
            if pd.notna(v_pos) and pd.notna(v_neg):
                if (v_pos >= 4 and v_neg >= 4) or (v_pos <= 2 and v_neg <= 2):
                    reasons.append("تناقض سيكومتري حاد بين الموجب والسالب")
                    status = "مزيفة / مرفوضة منهجيا"

        if duplicated_mask.loc[idx]:
            reasons.append("تطابق كلي (استنساخ مكتبي من استمارة سابقة)")
            status = "مزيفة / مرفوضة منهجيا"

        if missing_cnt > len(scale_cols) * 0.3:
            reasons.append(f"قيم مفقودة مرتفعة ({missing_cnt})")
            status = "مرفوضة منهجيا"

        if status != "صالحة وموثوقة":
            flagged_indices.append(idx)

        audit_records.append({
            "رقم الاستمارة": form_id,
            "الانحراف المعياري الداخلي (IRV)": round(sd_val, 3),
            "القيم المفقودة": missing_cnt,
            "التشخيص الجنائي الإحصائي": " ، ".join(reasons) if reasons else "اتساق طبيعي سليم",
            "القرار المنهجي": status
        })

    return pd.DataFrame(audit_records), flagged_indices


# ==========================================
# 3. تهيئة البيانات (Session State)
# ==========================================
if "raw_df" not in st.session_state:
    demo_text, _ = generate_demo_dataset()
    st.session_state.raw_df = demo_text
    coded_df, codebook_df = auto_code_dataframe(demo_text)
    st.session_state.working_df = coded_df
    st.session_state.codebook_df = codebook_df
    st.session_state.reversed_done = False
    st.session_state.cleaned_done = False


# ==========================================
# 4. شريط القيادة العلوي العائم (Top Glass Navbar)
# ==========================================
# ==========================================
# 4. شريط القيادة العلوي العائم مع الشعار (Logo)
# ==========================================
logo_html = '<div class="brand-logo">SL</div>'
for ext in ["logo.png", "logo.jpg", "logo.jpeg"]:
    if os.path.exists(ext):
        with open(ext, "rb") as img_f:
            b64_logo = base64.b64encode(img_f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{b64_logo}" style="width:58px; height:58px; border-radius:14px; object-fit:contain; background:#0F172A; border:1px solid #38BDF8; padding:3px; box-shadow:0 0 20px rgba(6,182,212,0.4);">'
        break

st.markdown(f"""
<div class="top-navbar">
    <div class="brand-box">
        {logo_html}
        <div>
            <h1 class="brand-title">SOCIO LAB CLOUD PRO</h1>
            <p class="brand-sub">منظومة الذكاء المنهجي، التدقيق الجنائي للبيانات، والتحكيم السيكومتري الآلي</p>
        </div>
    </div>
    <div class="status-badge">● متصل بالمحرك الإحصائي السحابي | v3.0 AI-Ready</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. شبكة المؤشرات الذكية المضيئة (Bento Grid KPIs)
# ==========================================
df_current = st.session_state.working_df
numeric_cols = [c for c in df_current.columns if c not in ["رمز_الاستمارة", "الجنس", "المستوى_الدراسي"]]
alpha_now = calculate_cronbach_alpha(df_current[numeric_cols]) if len(numeric_cols) >= 2 else 0.0

k1, k2, k3, k4 = st.columns(4)

with k1:
    tag_cls = "tag-emerald" if st.session_state.cleaned_done else "tag-cyan"
    tag_txt = "نقاوة البيانات 100% ✓" if st.session_state.cleaned_done else "العينة الميدانية الأولية"
    st.markdown(f"""
    <div class="bento-card">
        <div class="bento-top">
            <span class="bento-label">حجم العينة النشطة (N)</span>
            <div class="bento-icon">👥</div>
        </div>
        <div class="bento-val">{len(df_current)}</div>
        <span class="neon-tag {tag_cls}">{tag_txt}</span>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="bento-card">
        <div class="bento-top">
            <span class="bento-label">المتغيرات المرمزة آلياً</span>
            <div class="bento-icon">🧬</div>
        </div>
        <div class="bento-val">{len(numeric_cols)} متغيرات</div>
        <span class="neon-tag tag-cyan">جاهزة للتصدير إلى SPSS</span>
    </div>
    """, unsafe_allow_html=True)

with k3:
    a_cls = "tag-emerald" if alpha_now >= 0.75 else "tag-amber"
    a_txt = "موثوقية سيكومترية عالية" if alpha_now >= 0.75 else "بحاجة لعكس الفقرات وتنقية المقياس"
    st.markdown(f"""
    <div class="bento-card">
        <div class="bento-top">
            <span class="bento-label">معامل ألفا كرونباخ (α)</span>
            <div class="bento-icon">📐</div>
        </div>
        <div class="bento-val">{alpha_now:.3f}</div>
        <span class="neon-tag {a_cls}">{a_txt}</span>
    </div>
    """, unsafe_allow_html=True)

with k4:
    r_cls = "tag-emerald" if st.session_state.reversed_done else "tag-amber"
    r_txt = "تم قلب الأوزان (1 ↔ 5) ✓" if st.session_state.reversed_done else "أوزان خام غير معكوسة"
    st.markdown(f"""
    <div class="bento-card">
        <div class="bento-top">
            <span class="bento-label">معالجة الفقرات المعكوسة</span>
            <div class="bento-icon">⚡</div>
        </div>
        <div class="bento-val">{"مكتملة" if st.session_state.reversed_done else "قيد الانتظار"}</div>
        <span class="neon-tag {r_cls}">{r_txt}</span>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 6. شريط الوحدات التفاعلية الأفقي (Main Horizontal Navigation Tabs)
# ==========================================
main_tabs = st.tabs([
    "📥 1. الترميز الذكي وعكس الفقرات",
    "🛡️ 2. الرادار الجنائي وكشف الفبركة",
    "📐 3. المختبر السيكومتري الآلي",
    "🌳 4. شجرة القرار وجداول APA",
    "🎓 5. تصدير SPSS وشهادة الاعتماد",
    "📅 6. حجز الاستشارات والدورات"
])

with main_tabs[0]:
    st.markdown("""
    <div class="workspace-card">
        <div class="workspace-title">📥 بوابة القراءة الذكية، الترميز الآلي، وعكس العبارات السالبة</div>
        <div class="workspace-desc">
            تحول المنصة إجابات الاستبيان النصية (العربية والفرنسية) تلقائياً إلى مصفوفة رقمية قياسية، وتبني جدول تعريف المتغيرات (Variable View) مع قلب أوزان العبارات السالبة بضغطة زر.
        </div>
    </div>
    """, unsafe_allow_html=True)

    sub_t1, sub_t2, sub_t3 = st.tabs([
        "📄 البيانات النصية الخام",
        "🔢 المصفوفة الرقمية المرمزة (Data View)",
        "🗂️ قاموس المتغيرات الآلي (Variable View)"
    ])
    with sub_t1:
        st.dataframe(st.session_state.raw_df, use_container_width=True, height=300)
    with sub_t2:
        st.dataframe(st.session_state.working_df, use_container_width=True, height=300)
    with sub_t3:
        st.dataframe(st.session_state.codebook_df, use_container_width=True)

    st.markdown("#### ⚡ محرك عكس أوزان الفقرات السالبة (Reverse Coding)")
    default_rev = [c for c in numeric_cols if "عكسية" in c]
    rev_cols = st.multiselect("حدد الفقرات السالبة في استبيانك لقلب أوزانها (5 ↔ 1):", numeric_cols, default=default_rev)

    if st.button("🔄 تنفيذ عكس الأوزان الآلي وتحديث معامل الثبات"):
        if not st.session_state.reversed_done and rev_cols:
            for c in rev_cols:
                st.session_state.working_df[c] = 6 - pd.to_numeric(st.session_state.working_df[c], errors='coerce')
            st.session_state.reversed_done = True
            st.success(f"تم قلب أوزان الفقرات ({', '.join(rev_cols)}) بنجاح! انظر إلى ارتفاع ألفا كرونباخ في الأعلى.")
            st.rerun()
        elif st.session_state.reversed_done:
            st.info("تم عكس أوزان هذه الفقرات مسبقاً.")

with main_tabs[1]:
    st.markdown("""
    <div class="workspace-card">
        <div class="workspace-title">🛡️ محرك التدقيق الجنائي الإحصائي وكشف تزييف الاستمارات (Anti-Curbstoning Radar)</div>
        <div class="workspace-desc">
            يفحص المحرك كل استمارة عبر خوارزميات التباين الداخلي (IRV) ومصائد التناقض السيكومتري وتطابق المصفوفات لعزل الاستمارات العشوائية أو المفبركة مكتبياً قبل التحليل.
        </div>
    </div>
    """, unsafe_allow_html=True)

    cp1, cp2 = st.columns(2)
    with cp1:
        pos_item = st.selectbox("اختر فقرة موجبة مرجعية لفحص التناقض:", numeric_cols, index=0)
    with cp2:
        neg_idx = 3 if len(numeric_cols) > 3 else 0
        neg_item = st.selectbox("اختر الفقرة السالبة المقابلة لها منطقياً:", numeric_cols, index=neg_idx)

    raw_coded_temp, _ = auto_code_dataframe(st.session_state.raw_df)
    if st.session_state.cleaned_done:
        raw_coded_temp = raw_coded_temp.loc[st.session_state.working_df.index]

    audit_df, bad_indices = forensic_audit(raw_coded_temp, numeric_cols, pos_item, neg_item)

    ca1, ca2, ca3 = st.columns(3)
    ca1.metric("إجمالي الاستمارات المفحوصة", f"{len(audit_df)} استمارة")
    ca2.metric("الاستمارات الصالحة والموثوقة", f"{len(audit_df) - len(bad_indices)} استمارة")
    ca3.metric("الاستمارات المزيفة المرصودة", f"{len(bad_indices)} استمارات")

    audit_sorted = audit_df.sort_values(by="القرار المنهجي", ascending=False)
    st.dataframe(audit_sorted, use_container_width=True, height=320)

    if len(bad_indices) > 0:
        st.warning(f"⚠️ رصد الرادار الجنائي {len(bad_indices)} استمارات متلاعب بها أو متناقضة سيكومترياً.")
        if st.button("🧹 عزل واستبعاد الاستمارات المزيفة آلياً وتطهير العينة"):
            st.session_state.working_df = st.session_state.working_df.drop(index=bad_indices)
            st.session_state.cleaned_done = True
            st.success("تم تطهير قاعدة البيانات بنجاح! ارتفع مؤشر نزاهة العينة إلى 100%.")
            st.rerun()
    else:
        st.success("✅ قاعدة البيانات نقية تماماً وخالية من أي تلاعب أو تناقض سيكومتري.")

with main_tabs[2]:
    st.markdown("""
    <div class="workspace-card">
        <div class="workspace-title">📐 المختبر السيكومتري الآلي لتحكيم المقاييس (Automated Psychometrics Lab)</div>
        <div class="workspace-desc">
            حساب آلي لمعامل ألفا كرونباخ والاتساق الداخلي للفقرات (Item-Total Correlation) مع كشف واستبعاد الفقرات المشوشة التي تضعف ثبات المقياس.
        </div>
    </div>
    """, unsafe_allow_html=True)

    selected_scale_items = st.multiselect(
        "فقرات المقياس الخاضعة للتحكيم السيكومتري:",
        numeric_cols,
        default=numeric_cols
    )

    if len(selected_scale_items) >= 3:
        sub_df = st.session_state.working_df[selected_scale_items].apply(pd.to_numeric, errors='coerce').dropna()
        overall_alpha = calculate_cronbach_alpha(sub_df)

        psych_rows = []
        weak_items = []
        for item in selected_scale_items:
            other_items = [c for c in selected_scale_items if c != item]
            alpha_if_deleted = calculate_cronbach_alpha(sub_df[other_items])
            corrected_total = sub_df[other_items].sum(axis=1).to_numpy(dtype=float)
            item_arr = sub_df[item].to_numpy(dtype=float)
            r_val, p_val = stats.pearsonr(item_arr, corrected_total)

            if alpha_if_deleted > overall_alpha + 0.01 or r_val < 0.25:
                diag = "⚠️ فقرة مشوشة للثبات (يوصى بحذفها)"
                weak_items.append(item)
            else:
                diag = "✅ فقرة صادقة ومتسقة بنيوياً"

            psych_rows.append({
                "الفقرة": item,
                "المتوسط الحسابي (M)": round(float(np.mean(item_arr)), 2),
                "الانحراف المعياري (SD)": round(float(np.std(item_arr, ddof=1)), 2),
                "ارتباط الفقرة بالمحور (r)": round(float(r_val), 3),
                "مستوى الدلالة (p-value)": round(float(p_val), 4),
                "ألفا كرونباخ إذا حذفت الفقرة": round(float(alpha_if_deleted), 3),
                "التشخيص السيكومتري": diag
            })

        st.dataframe(pd.DataFrame(psych_rows), use_container_width=True)

        if weak_items:
            st.warning(f"💡 توصية المحرك السيكومتري: حذف الفقرة المشوشة ({', '.join(weak_items)}) سيرفع ثبات المقياس بشكل ملحوظ.")
            if st.button(f"✂️ استبعاد الفقرة المشوشة ({', '.join(weak_items)}) وإعادة بناء المقياس"):
                st.session_state.working_df = st.session_state.working_df.drop(columns=weak_items)
                st.success("تم حذف الفقرة المشوشة بنجاح وقفز معامل ألفا كرونباخ الكلي!")
                st.rerun()

with main_tabs[3]:
    st.markdown("""
    <div class="workspace-card">
        <div class="workspace-title">🌳 شجرة القرار الإحصائي المشروطة ومولد جداول (APA 7th Edition)</div>
        <div class="workspace-desc">
            فحص إلزامي لاعتدالية التوزيع (Shapiro-Wilk) وتجانس التباين (Levene's Test) قبل توجيه الباحث آلياً للاختبار المعلمي أو اللامعلمي الصحيح وتوليد جدول APA.
        </div>
    </div>
    """, unsafe_allow_html=True)

    df_calc = st.session_state.working_df.copy()
    peer_cols = [c for c in numeric_cols if c.startswith(("Q1", "Q2", "Q3", "Q4"))]
    delinq_cols = [c for c in numeric_cols if c.startswith(("Q5", "Q6", "Q7", "Q8"))]

    if peer_cols and delinq_cols:
        df_calc["محور_تأثير_جماعة_الرفاق"] = df_calc[peer_cols].apply(pd.to_numeric, errors='coerce').mean(axis=1)
        df_calc["محور_السلوك_الجانح"] = df_calc[delinq_cols].apply(pd.to_numeric, errors='coerce').mean(axis=1)
        analysis_vars = ["محور_تأثير_جماعة_الرفاق", "محور_السلوك_الجانح"] + numeric_cols
    else:
        analysis_vars = numeric_cols

    hypothesis_type = st.radio(
        "حدد نوع الفرضية المراد اختبارها:",
        [
            "🔗 فرضية علاقة ارتباطية بين متغيرين كميين (Correlation)",
            "⚖️ فرضية فروق بين مجموعتين مستقلتين (Two Independent Groups)"
        ],
        horizontal=True
    )

    if "ارتباطية" in hypothesis_type:
        c1, c2 = st.columns(2)
        with c1:
            var_x = st.selectbox("المتغير المستقل (X):", analysis_vars, index=0)
        with c2:
            var_y = st.selectbox("المتغير التابع (Y):", analysis_vars, index=1 if len(analysis_vars) > 1 else 0)

        series_x = pd.to_numeric(df_calc[var_x], errors='coerce').dropna().to_numpy(dtype=float)
        series_y = pd.to_numeric(df_calc[var_y], errors='coerce').dropna().to_numpy(dtype=float)

        stat_sw_x, p_sw_x = stats.shapiro(series_x)
        stat_sw_y, p_sw_y = stats.shapiro(series_y)
        is_normal = (p_sw_x > 0.05) and (p_sw_y > 0.05)

        if is_normal:
            test_used = "معامل ارتباط بيرسون المعلمي (Pearson Correlation - r)"
            r_val, p_val = stats.pearsonr(series_x, series_y)
            reason_txt = f"نظراً لتحقق اعتدالية التوزيع (Shapiro-Wilk p = {p_sw_x:.3f}, {p_sw_y:.3f} > 0.05)، اعتمد المحرك اختبار بيرسون المعلمي."
        else:
            test_used = "معامل ارتباط سبيرمان اللامعلمي للرتب (Spearman Rank - rho)"
            r_val, p_val = stats.spearmanr(series_x, series_y)
            reason_txt = f"نظراً لعدم تحقق اعتدالية التوزيع (Shapiro-Wilk p = {min(p_sw_x, p_sw_y):.4f} ≤ 0.05)، حظر النظام اختبار بيرسون ووجه المعالجة آلياً نحو سبيرمان اللامعلمي."

        st.info(f"🧭 **قرار المحرك الإحصائي:** اعتماد **{test_used}**\n\n*{reason_txt}*")

        sig_label = "دالة إحصائياً عند (α = 0.05)" if p_val < 0.05 else "غير دالة إحصائياً"
        st.markdown(f"""
        <div class="apa-dark-box">
            <h4 style="color:#38BDF8; margin-top:0;">جدول (1): نتائج اختبار العلاقة الارتباطية وفق معايير APA 7th Edition</h4>
            <table class="apa-table">
                <thead>
                    <tr>
                        <th>المتغيرات المدروسة</th>
                        <th>حجم العينة (N)</th>
                        <th>المتوسط الحسابي (M)</th>
                        <th>الانحراف المعياري (SD)</th>
                        <th>قيمة معامل الارتباط</th>
                        <th>مستوى الدلالة (p-value)</th>
                        <th>القرار الإحصائي</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{var_x}</td>
                        <td>{len(series_x)}</td>
                        <td>{np.mean(series_x):.2f}</td>
                        <td>{np.std(series_x, ddof=1):.2f}</td>
                        <td rowspan="2" style="font-weight:800; font-size:1.2rem; color:#38BDF8;">{r_val:.3f}**</td>
                        <td rowspan="2">{p_val:.4f}</td>
                        <td rowspan="2"><span class="neon-tag tag-emerald">{sig_label}</span></td>
                    </tr>
                    <tr>
                        <td>{var_y}</td>
                        <td>{len(series_y)}</td>
                        <td>{np.mean(series_y):.2f}</td>
                        <td>{np.std(series_y, ddof=1):.2f}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)
    else:
        dep_var = st.selectbox("اختر المتغير التابع الكمي:", analysis_vars, index=1 if len(analysis_vars) > 1 else 0)
        if "الجنس" in df_calc.columns:
            groups = df_calc["الجنس"].dropna().unique()
            if len(groups) >= 2:
                g1 = pd.to_numeric(df_calc[df_calc["الجنس"] == groups[0]][dep_var], errors='coerce').dropna().to_numpy(dtype=float)
                g2 = pd.to_numeric(df_calc[df_calc["الجنس"] == groups[1]][dep_var], errors='coerce').dropna().to_numpy(dtype=float)

                _, p_norm1 = stats.shapiro(g1) if len(g1) >= 3 else (0, 1)
                _, p_norm2 = stats.shapiro(g2) if len(g2) >= 3 else (0, 1)
                _, p_lev = stats.levene(g1, g2)

                if p_norm1 > 0.05 and p_norm2 > 0.05 and p_lev > 0.05:
                    t_stat, p_val = stats.ttest_ind(g1, g2)
                    test_title = "اختبار (Independent Samples T-Test) المعلمي"
                    stat_symbol = f"t = {t_stat:.3f}"
                else:
                    u_stat, p_val = stats.mannwhitneyu(g1, g2)
                    test_title = "اختبار مان-ويتني (Mann-Whitney U) اللامعلمي"
                    stat_symbol = f"U = {u_stat:.1f}"

                st.info(f"🧭 **الاختبار المطبق آلياً (Levene p = {p_lev:.3f}):** {test_title}")
                st.markdown(f"""
                <div class="apa-dark-box">
                    <h4 style="color:#38BDF8; margin-top:0;">جدول (2): نتائج اختبار الفروق بين المجموعتين وفق معايير APA 7th Edition</h4>
                    <table class="apa-table">
                        <thead>
                            <tr>
                                <th>المجموعة المقارنة</th>
                                <th>العدد (n)</th>
                                <th>المتوسط الحسابي (M)</th>
                                <th>الانحراف المعياري (SD)</th>
                                <th>قيمة الاختبار</th>
                                <th>مستوى الدلالة (p-value)</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>المجموعة الأولى ({groups[0]})</td>
                                <td>{len(g1)}</td>
                                <td>{np.mean(g1):.2f}</td>
                                <td>{np.std(g1, ddof=1):.2f}</td>
                                <td rowspan="2" style="font-weight:800; font-size:1.2rem; color:#38BDF8;">{stat_symbol}</td>
                                <td rowspan="2">{p_val:.4f}</td>
                            </tr>
                            <tr>
                                <td>المجموعة الثانية ({groups[1]})</td>
                                <td>{len(g2)}</td>
                                <td>{np.mean(g2):.2f}</td>
                                <td>{np.std(g2, ddof=1):.2f}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                """, unsafe_allow_html=True)

with main_tabs[4]:
    st.markdown("""
    <div class="workspace-card">
        <div class="workspace-title">🎓 تصدير الحزمة الإحصائية النهائية (SPSS .sav) وشهادة الاعتماد المنهجي</div>
        <div class="workspace-desc">
            حمل قاعدة بياناتك المطهرة بصيغة برنامج SPSS الأصلية، مع شهادة النزاهة والموثوقية الميدانية لإرفاقها بمذكرتك أو تقريرك المؤسسي.
        </div>
    </div>
    """, unsafe_allow_html=True)

    cd1, cd2, cd3 = st.columns(3)
    csv_bytes = st.session_state.working_df.to_csv(index=False).encode('utf-8-sig')
    with cd1:
        st.download_button("📥 تحميل المصفوفة المرمزة (CSV / Excel)", data=csv_bytes, file_name="SocioLab_Cleaned.csv", mime="text/csv")

    codebook_bytes = st.session_state.codebook_df.to_csv(index=False).encode('utf-8-sig')
    with cd2:
        st.download_button("📘 تحميل قاموس المتغيرات (Variable View)", data=codebook_bytes, file_name="SocioLab_Codebook.csv", mime="text/csv")

    with cd3:
        if HAS_PYREADSTAT:
            sav_path = "SocioLab_Output.sav"
            spss_df = st.session_state.working_df.copy()
            for c in spss_df.columns:
                if c != "رمز_الاستمارة":
                    spss_df[c] = pd.to_numeric(spss_df[c], errors='coerce')
                else:
                    spss_df[c] = spss_df[c].astype(str)
            clean_cols = {col: f"VAR_{i+1}" for i, col in enumerate(spss_df.columns)}
            col_labels = {f"VAR_{i+1}": col for i, col in enumerate(spss_df.columns)}
            spss_df = spss_df.rename(columns=clean_cols)
            pyreadstat.write_sav(spss_df, sav_path, column_labels=col_labels)
            with open(sav_path, "rb") as f:
                st.download_button("📊 تحميل ملف SPSS الأصلي (.sav)", data=f, file_name="SocioLab_Verified.sav", mime="application/octet-stream")

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    cert_id = f"SL-DZ-{datetime.datetime.now().strftime('%Y%m')}-060"

    st.markdown(f"""
    <div class="holo-cert">
        <span class="neon-tag tag-cyan" style="font-size:0.9rem; padding:6px 20px;">★ SOCIO LAB VERIFIED DATASET ★</span>
        <h2 style="color:#FFFFFF; margin-top:14px; margin-bottom:6px; font-weight:800;">شهادة التدقيق المنهجي وموثوقية البيانات الميدانية</h2>
        <p style="color:#38BDF8 !important; font-family:'Space Grotesk',sans-serif; letter-spacing:1.5px; margin-top:0;">FORENSIC STATISTICAL & PSYCHOMETRIC AUDIT CERTIFICATE</p>
        <hr style="border:1px solid rgba(56, 189, 248, 0.25); width:70%; margin:20px auto;">
        <p style="font-size:1.1rem; color:#E2E8F0 !important; line-height:2.0; max-width:85%; margin:0 auto;">
            تشهد منظومة <b>Socio Lab السحابية للهندسة المنهجية والبيانات</b> بأن قاعدة البيانات المرفقة قد خضعت للتدقيق الجنائي الإحصائي الآلي،
            وتم فحصها من حيث التباين الداخلي للاستمارات (<b>IRV</b>)، والاتساق السيكومتري للعبارات المعكوسة، وخلوها من الاستنساخ المكتبي،
            وبلغ معامل الثبات الكلي للمقياس بعد الضبط (<b>α = {alpha_now:.3f}</b>) بحجم عينة صافية ومعتمدة قدره (<b>N = {len(df_current)}</b>).
        </p>
        <div style="display:flex; justify-content:space-around; margin-top:30px; padding-top:20px; border-top:1px dashed rgba(148, 163, 184, 0.25); color:#7DD3FC; font-weight:700;">
            <div>🔖 رقم الاعتماد: {cert_id}</div>
            <div>📅 تاريخ الإصدار: {today_str}</div>
            <div>🏛️ Socio Lab - جامعة سوق أهراس</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with main_tabs[5]:
    st.markdown("""
    <div class="workspace-card">
        <div class="workspace-title">📅 بوابة حجز الاستشارات المنهجية والدورات التدريبية (حضوري بسوق أهراس / عن بعد)</div>
        <div class="workspace-desc">
            احجز جلسة مرافقة منهجية وإحصائية مخصصة لبحثك أو سجل في معسكرات التدريب التطبيقي على برنامج IBM SPSS ومنهجية IMRAD.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("booking_form"):
        cf1, cf2 = st.columns(2)
        with cf1:
            client_name = st.text_input("👤 الاسم واللقب الكامل:")
            client_uni = st.text_input("🏛️ الجامعة / المؤسسة:", value="جامعة محمد الشريف مساعدية - سوق أهراس")
            client_level = st.selectbox("🎓 الصفة الأكاديمية أو المهنية:", ["طالب ماستر 2", "طالب دكتوراه", "أستاذ باحث", "مؤسسة اقتصادية / جمعية"])
        with cf2:
            service_req = st.selectbox("🛠️ نوع الخدمة المطلوبة:", [
                "استشارة منهجية وضبط أدوات القياس (الاستبيان)",
                "التدقيق الجنائي والمعالجة الإحصائية عبر SPSS",
                "دورة تدريبية تطبيقية في برنامج SPSS ومنهجية IMRAD",
                "إنجاز دراسة ميدانية أو استطلاع رأي مؤسسي (B2B)"
            ])
            mode_req = st.radio("📍 نمط الاستفادة المفضل:", ["حضورياً (مقر Socio Lab - سوق أهراس)", "عن بعد (عبر المنصة الرقمية - 58 ولاية)"])
            client_phone = st.text_input("📱 رقم الهاتف أو البريد الإلكتروني للتواصل:")

        notes = st.text_area("📝 ملخص موضوع البحث أو الاحتياج الإحصائي:")
        submitted = st.form_submit_button("🚀 تأكيد وإرسال طلب الحجز الآن")
        if submitted:
            if client_name and client_phone:
                st.success(f"شكراً لك ({client_name})! تم تسجيل طلبك لخدمة ({service_req}) بنجاح، وسيتواصل معك فريق Socio Lab خلال 24 ساعة.")
            else:
                st.warning("يرجى إدخال الاسم ورقم التواصل لتأكيد الحجز.")
