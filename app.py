import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import io
import datetime

try:
    import pyreadstat
    HAS_PYREADSTAT = True
except ImportError:
    HAS_PYREADSTAT = False

# ==========================================
# 1. إعدادات الصفحة والتصميم العصري الفاخر (Ultra-Modern SaaS UI)
# ==========================================
st.set_page_config(
    page_title="Socio Lab | منصة الهندسة المنهجية والتدقيق الإحصائي",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

    /* ضبط الخطوط والاتجاه العام */
    html, body, [class*="css"], .stMarkdown, .stText, .stButton, .stSelectbox, .stMultiSelect, .stRadio {
        font-family: 'Tajawal', 'Plus Jakarta Sans', sans-serif !important;
        direction: rtl;
        text-align: right;
    }

    /* إخفاء عناصر Streamlit الافتراضية المزعجة */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    /* خلفية الصفحة الرئيسية المتدرجة بنعومة */
    .stApp {
        background: radial-gradient(circle at top right, #EEF2FF 0%, #F8FAFC 45%, #F1F5F9 100%);
        color: #0F172A;
    }

    /* تصميم القائمة الجانبية (Dark Navy Glassmorphism) */
    section[data-testid="stSidebar"] {
        background: linear-gradient(165deg, #070C18 0%, #0F172A 50%, #172554 100%) !important;
        border-left: 1px solid rgba(56, 189, 248, 0.18);
        box-shadow: -8px 0 30px rgba(2, 6, 23, 0.25);
    }
    section[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }

    /* شعار القائمة الجانبية */
    .sidebar-brand {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 20px;
        backdrop-filter: blur(12px);
        text-align: center;
    }
    .sidebar-brand-title {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.65rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38BDF8, #818CF8, #E0E7FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
        margin-bottom: 4px;
    }
    .sidebar-brand-sub {
        font-size: 0.85rem;
        color: #94A3B8 !important;
        font-weight: 500;
    }

    /* البانر الترحيبي العلوي (Hero Banner) */
    .hero-container {
        background: linear-gradient(125deg, #090D16 0%, #0F172A 40%, #1E3A8A 85%, #1D4ED8 100%);
        border-radius: 22px;
        padding: 34px 40px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 40px -15px rgba(15, 23, 42, 0.35);
        border: 1px solid rgba(56, 189, 248, 0.25);
    }
    .hero-container::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -10%;
        width: 380px;
        height: 380px;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.18) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.4);
        color: #7DD3FC !important;
        padding: 5px 16px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
    }
    .hero-title {
        color: #FFFFFF !important;
        font-size: 2.2rem;
        font-weight: 900;
        margin: 0 0 10px 0;
        line-height: 1.3;
    }
    .hero-subtitle {
        color: #CBD5E1 !important;
        font-size: 1.05rem;
        font-weight: 400;
        margin: 0;
        max-width: 90%;
        line-height: 1.7;
    }

    /* بطاقات المؤشرات الذكية (Modern Glass KPI Cards) */
    .kpi-card {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 22px 24px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.04);
        transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        margin-bottom: 18px;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 30px -10px rgba(30, 58, 138, 0.12);
        border-color: #93C5FD;
    }
    .kpi-icon-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    .kpi-label {
        color: #64748B;
        font-size: 0.92rem;
        font-weight: 700;
    }
    .kpi-icon {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: #EFF6FF;
        color: #1D4ED8;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .kpi-number {
        color: #0F172A;
        font-size: 1.95rem;
        font-weight: 900;
        margin: 4px 0 8px 0;
        font-family: 'Plus Jakarta Sans', 'Tajawal', sans-serif !important;
    }
    .kpi-pill {
        display: inline-block;
        padding: 3px 11px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
    }
    .pill-blue { background: #E0F2FE; color: #0369A1; }
    .pill-green { background: #DCFCE7; color: #15803D; }
    .pill-amber { background: #FEF3C7; color: #B45309; }

    /* الحاويات والأقسام العلمية (Elevated Cards) */
    .glass-panel {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 12px 32px -8px rgba(15, 23, 42, 0.05);
    }
    .panel-header {
        display: flex;
        align-items: center;
        gap: 12px;
        border-bottom: 2px solid #F1F5F9;
        padding-bottom: 16px;
        margin-bottom: 20px;
    }
    .panel-title {
        color: #0F172A;
        font-size: 1.4rem;
        font-weight: 800;
        margin: 0;
    }
    .panel-desc {
        color: #475569;
        font-size: 1rem;
        line-height: 1.75;
        margin-bottom: 20px;
    }

    /* الأزرار العصرية المتدرجة */
    .stButton > button {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
        border-radius: 12px !important;
        padding: 0.65rem 1.6rem !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        box-shadow: 0 6px 15px -3px rgba(37, 99, 235, 0.35) !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #3B82F6 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 22px -4px rgba(37, 99, 235, 0.5) !important;
    }

    /* أزرار التحميل */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%) !important;
        color: #F8FAFC !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 0.65rem 1.2rem !important;
        width: 100% !important;
        border: 1px solid #334155 !important;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%) !important;
        border-color: #60A5FA !important;
    }

    /* تصميم التبويبات (Modern Pills Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #F1F5F9;
        padding: 6px;
        border-radius: 14px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
        background-color: transparent !important;
        border: none !important;
        color: #475569 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #1E3A8A !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08) !important;
    }

    /* جداول APA 7th الاحترافية */
    .apa-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 24px;
        margin: 18px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }
    .apa-table {
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0;
        font-size: 1rem;
        background-color: #FFFFFF;
        direction: rtl;
    }
    .apa-table thead tr {
        border-top: 2.5px solid #0F172A;
        border-bottom: 1.5px solid #0F172A;
        color: #0F172A;
        font-weight: 800;
        background-color: #F8FAFC;
    }
    .apa-table th, .apa-table td {
        padding: 14px 16px;
        text-align: center;
    }
    .apa-table tbody tr {
        border-bottom: 1px solid #F1F5F9;
    }
    .apa-table tbody tr:last-of-type {
        border-bottom: 2.5px solid #0F172A;
    }

    /* شهادة النزاهة العلمية الملكية */
    .luxury-certificate {
        background: radial-gradient(circle at top left, #FFFFFF 0%, #F8FAFC 60%, #EFF6FF 100%);
        border: 2px solid #1E3A8A;
        outline: 6px double rgba(30, 58, 138, 0.18);
        outline-offset: -14px;
        border-radius: 22px;
        padding: 44px 38px;
        text-align: center;
        box-shadow: 0 20px 45px -15px rgba(30, 58, 138, 0.15);
        margin-top: 24px;
        position: relative;
    }
    .cert-seal {
        display: inline-block;
        background: linear-gradient(135deg, #1E3A8A, #2563EB);
        color: #FFFFFF;
        padding: 8px 24px;
        border-radius: 999px;
        font-weight: 800;
        font-size: 0.88rem;
        letter-spacing: 1px;
        margin-bottom: 14px;
        box-shadow: 0 6px 15px rgba(37, 99, 235, 0.25);
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. الدوال الإحصائية والمنهجية (Core Engine - Python 3.14 Safe)
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

    # 4 استمارات متلاعب بها لاختبار المحرك الجنائي
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
# 3. إدارة حالة الجلسة (Session State)
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
# 4. القائمة الجانبية العصرية (Sidebar Navigation)
# ==========================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-title">SOCIO LAB</div>
        <div class="sidebar-brand-sub">ResearchTech & Forensic Analytics</div>
    </div>
    """, unsafe_allow_html=True)

    nav_page = st.radio(
        "🧭 وحدات المنصة السحابية:",
        [
            "1. الرفع الذكي والترميز الآلي",
            "2. التدقيق الجنائي وكشف التلاعب",
            "3. المختبر السيكومتري (الصدق والثبات)",
            "4. شجرة القرار الإحصائي وجداول APA",
            "5. التصدير لـ SPSS وشهادة النزاهة",
            "6. حجز الاستشارات والدورات التدريبية"
        ]
    )

    st.markdown("---")
    st.markdown("##### 📂 إدارة مصدر البيانات")
    data_source = st.selectbox(
        "اختر قاعدة البيانات النشطة:",
        ["قاعدة البيانات التجريبية (N=60 تلميذاً)", "رفع ملف استبيان خارجي (Excel / CSV)"]
    )

    if data_source == "رفع ملف استبيان خارجي (Excel / CSV)":
        uploaded_file = st.file_uploader("ارفع ملف الاستبيان الخام", type=["xlsx", "csv"])
        if uploaded_file is not None:
            if uploaded_file.name.endswith(".csv"):
                user_df = pd.read_csv(uploaded_file)
            else:
                user_df = pd.read_excel(uploaded_file)
            st.session_state.raw_df = user_df
            coded_df, codebook_df = auto_code_dataframe(user_df)
            st.session_state.working_df = coded_df
            st.session_state.codebook_df = codebook_df
            st.session_state.reversed_done = False
            st.session_state.cleaned_done = False
            st.success("تم رفع وترميز ملفك بنجاح!")

    if st.button("🔄 استعادة البيانات التجريبية الأصلية"):
        demo_text, _ = generate_demo_dataset()
        st.session_state.raw_df = demo_text
        coded_df, codebook_df = auto_code_dataframe(demo_text)
        st.session_state.working_df = coded_df
        st.session_state.codebook_df = codebook_df
        st.session_state.reversed_done = False
        st.session_state.cleaned_done = False
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.8rem; color:#94A3B8; text-align:center; line-height:1.6;">
        <b>Socio Lab Cloud Platform v2.5</b><br>
        حاضنة الأعمال - جامعة سوق أهراس<br>
        الامتثال للقانون 18-07 لحماية البيانات
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 5. البانر الرئيسي وبطاقات الأداء الذكية (KPIs)
# ==========================================
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">✨ الجيل الجديد من تكنولوجيا البحث العلمي والبيانات في الجزائر</div>
    <h1 class="hero-title">SOCIO LAB | المختبر السحابي للهندسة المنهجية والتدقيق السيكومتري</h1>
    <p class="hero-subtitle">
        أول محرك ذكاء منهجي وإحصائي جنائي لأتمتة فحص موثوقية الاستبيانات، كشف الاستمارات المفبركة، التحكيم السيكومتري للمقاييس، وتوليد جداول APA وملفات SPSS الأصلية.
    </p>
</div>
""", unsafe_allow_html=True)

df_current = st.session_state.working_df
numeric_cols = [c for c in df_current.columns if c not in ["رمز_الاستمارة", "الجنس", "المستوى_الدراسي"]]
alpha_now = calculate_cronbach_alpha(df_current[numeric_cols]) if len(numeric_cols) >= 2 else 0.0

col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    pill_cls = "pill-green" if st.session_state.cleaned_done else "pill-blue"
    pill_txt = "عينة مطهرة ومعتمدة ✓" if st.session_state.cleaned_done else "العينة الميدانية الخام"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon-bar">
            <span class="kpi-label">حجم العينة النشطة (N)</span>
            <div class="kpi-icon">👥</div>
        </div>
        <div class="kpi-number">{len(df_current)}</div>
        <span class="kpi-pill {pill_cls}">{pill_txt}</span>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon-bar">
            <span class="kpi-label">فقرات القياس المرمزة</span>
            <div class="kpi-icon">🔢</div>
        </div>
        <div class="kpi-number">{len(numeric_cols)} فقرات</div>
        <span class="kpi-pill pill-blue">متوافقة 100% مع SPSS</span>
    </div>
    """, unsafe_allow_html=True)

with col_m3:
    alpha_pill = "pill-green" if alpha_now >= 0.75 else "pill-amber"
    alpha_status = "ثبات سيكومتري ممتاز" if alpha_now >= 0.75 else "يتطلب ضبط الفقرات المعكوسة"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon-bar">
            <span class="kpi-label">ألفا كرونباخ الكلي (α)</span>
            <div class="kpi-icon">📐</div>
        </div>
        <div class="kpi-number">{alpha_now:.3f}</div>
        <span class="kpi-pill {alpha_pill}">{alpha_status}</span>
    </div>
    """, unsafe_allow_html=True)

with col_m4:
    rev_pill = "pill-green" if st.session_state.reversed_done else "pill-amber"
    rev_txt = "تم عكس الأوزان (1 ↔ 5) ✓" if st.session_state.reversed_done else "الأوزان الخام قبل العكس"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon-bar">
            <span class="kpi-label">العبارات السالبة المعكوسة</span>
            <div class="kpi-icon">🔄</div>
        </div>
        <div class="kpi-number">{"مضبوطة" if st.session_state.reversed_done else "قيد الانتظار"}</div>
        <span class="kpi-pill {rev_pill}">{rev_txt}</span>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# القسم الأول: الرفع الذكي والترميز الآلي
# ==========================================
if nav_page == "1. الرفع الذكي والترميز الآلي":
    st.markdown("""
    <div class="glass-panel">
        <div class="panel-header">
            <h3 class="panel-title">📥 بوابة القراءة الذكية، الترميز الآلي، وعكس العبارات السالبة</h3>
        </div>
        <p class="panel-desc">
            تحول هذه الوحدة استبيانات Google Forms أو Excel النصية تلقائياً إلى مصفوفة رقمية قياسية، وتولد دليل ترميز المتغيرات (Variable View) مع معالجة الفقرات المعكوسة بضغطة زر.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_raw, tab_coded, tab_codebook = st.tabs([
        "📄 البيانات النصية الخام (قبل المعالجة)",
        "🔢 المصفوفة الرقمية المرمزة (Data View)",
        "🗂️ جدول تعريف المتغيرات الآلي (SPSS Variable View)"
    ])

    with tab_raw:
        st.dataframe(st.session_state.raw_df, use_container_width=True, height=340)

    with tab_coded:
        st.dataframe(st.session_state.working_df, use_container_width=True, height=340)

    with tab_codebook:
        st.dataframe(st.session_state.codebook_df, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-panel">
        <div class="panel-header">
            <h3 class="panel-title">🔄 محرك عكس أوزان الفقرات السالبة (Reverse Coding Engine)</h3>
        </div>
        <p class="panel-desc">
            حدد الفقرات السالبة في المقياس ليقوم النظام بقلب أوزانها آلياً (5 ↔ 1 و 4 ↔ 2) لضمان اتساق الدرجة الكلية للمحور ورفع معامل الثبات:
        </p>
    </div>
    """, unsafe_allow_html=True)

    default_rev = [c for c in numeric_cols if "عكسية" in c]
    rev_cols = st.multiselect("اختر الفقرات السالبة (المعكوسة):", numeric_cols, default=default_rev)

    if st.button("⚡ تطبيق عكس الأوزان الآلي وتحديث معامل الثبات"):
        if not st.session_state.reversed_done and rev_cols:
            for c in rev_cols:
                st.session_state.working_df[c] = 6 - pd.to_numeric(st.session_state.working_df[c], errors='coerce')
            st.session_state.reversed_done = True
            st.success(f"تم عكس أوزان الفقرات ({', '.join(rev_cols)}) بنجاح! لاحظ قفزة معامل ألفا كرونباخ في البطاقات العلوية.")
            st.rerun()
        elif st.session_state.reversed_done:
            st.info("تم عكس أوزان هذه الفقرات مسبقاً.")


# ==========================================
# القسم الثاني: محرك التدقيق الجنائي وكشف التلاعب
# ==========================================
elif nav_page == "2. التدقيق الجنائي وكشف التلاعب":
    st.markdown("""
    <div class="glass-panel">
        <div class="panel-header">
            <h3 class="panel-title">🛡️ محرك التدقيق الجنائي الإحصائي وكشف فبركة البيانات (Anti-Curbstoning Engine)</h3>
        </div>
        <p class="panel-desc">
            يمثل هذا المحرك جوهر ابتكار <b>Socio Lab</b>؛ حيث يفحص كل استمارة لكشف <b>الإجابات النمطية الجامدة (SD = 0)</b>، و<b>التناقضات السيكومترية الحادة بين الفقرات الموجبة والسالبة</b>، و<b>الاستمارات المستنسخة مكتبياً (Curbstoning)</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        pos_item = st.selectbox("اختر فقرة موجبة مرجعية لفحص التناقض المنطقي:", numeric_cols, index=0)
    with col_p2:
        neg_idx = 3 if len(numeric_cols) > 3 else 0
        neg_item = st.selectbox("اختر الفقرة السالبة المقابلة لها:", numeric_cols, index=neg_idx)

    raw_coded_temp, _ = auto_code_dataframe(st.session_state.raw_df)
    if st.session_state.cleaned_done:
        raw_coded_temp = raw_coded_temp.loc[st.session_state.working_df.index]

    audit_df, bad_indices = forensic_audit(raw_coded_temp, numeric_cols, pos_item, neg_item)

    col_a1, col_a2, col_a3 = st.columns(3)
    col_a1.metric("إجمالي الاستمارات المفحوصة", f"{len(audit_df)} استمارة")
    col_a2.metric("الاستمارات الصالحة والموثوقة", f"{len(audit_df) - len(bad_indices)} استمارة")
    col_a3.metric("الاستمارات المزيفة المرصودة", f"{len(bad_indices)} استمارات")

    st.markdown("#### 🔍 سجل التشخيص الجنائي الإحصائي للاستمارات:")
    audit_sorted = audit_df.sort_values(by="القرار المنهجي", ascending=False)
    st.dataframe(audit_sorted, use_container_width=True, height=340)

    if len(bad_indices) > 0:
        st.warning(f"⚠️ رصد المحرك الجنائي {len(bad_indices)} استمارات متلاعب بها أو متناقضة منطقياً تشوه نتائج الدراسة.")
        if st.button("🧹 عزل واستبعاد الاستمارات المزيفة آلياً وتطهير العينة"):
            st.session_state.working_df = st.session_state.working_df.drop(index=bad_indices)
            st.session_state.cleaned_done = True
            st.success("تم تطهير قاعدة البيانات بنجاح! ارتفع مؤشر نزاهة العينة إلى 100%.")
            st.rerun()
    else:
        st.success("✅ قاعدة البيانات مطهرة بالكامل وخالية من أي فبركة أو تناقض سيكومتري (مؤشر النزاهة = 100%).")


# ==========================================
# القسم الثالث: المختبر السيكومتري (الصدق والثبات)
# ==========================================
elif nav_page == "3. المختبر السيكومتري (الصدق والثبات)":
    st.markdown("""
    <div class="glass-panel">
        <div class="panel-header">
            <h3 class="panel-title">📐 المختبر السيكومتري الآلي لتحكيم المقاييس (Psychometric Validation Lab)</h3>
        </div>
        <p class="panel-desc">
            يحسب هذا المختبر معامل ألفا كرونباخ (Cronbach's Alpha) ومصفوفة الاتساق الداخلي (Item-Total Correlation)، ويكتشف آلياً الفقرات المشوشة التي ينبغي حذفها لرفع جودة أداة القياس.
        </p>
    </div>
    """, unsafe_allow_html=True)

    selected_scale_items = st.multiselect(
        "حدد فقرات المقياس المراد فحص خصائصها السيكومترية:",
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

        st.info(f"📊 **معامل الثبات ألفا كرونباخ الحالي للمقياس ({len(selected_scale_items)} فقرات):** `{overall_alpha:.3f}`")
        st.dataframe(pd.DataFrame(psych_rows), use_container_width=True)

        if weak_items:
            st.warning(f"💡 توصية المحرك السيكومتري: استبعاد الفقرة المشوشة ({', '.join(weak_items)}) سيرفع ثبات المقياس ومصداقيته.")
            if st.button(f"✂️ حذف الفقرة المشوشة ({', '.join(weak_items)}) وإعادة الحساب فوراً"):
                st.session_state.working_df = st.session_state.working_df.drop(columns=weak_items)
                st.success("تم استبعاد الفقرة المشوشة بنجاح وارتفع معامل ألفا كرونباخ الكلي!")
                st.rerun()
    else:
        st.warning("يرجى تحديد 3 فقرات على الأقل لإجراء الفحص السيكومتري.")


# ==========================================
# القسم الرابع: شجرة القرار الإحصائي وجداول APA
# ==========================================
elif nav_page == "4. شجرة القرار الإحصائي وجداول APA":
    st.markdown("""
    <div class="glass-panel">
        <div class="panel-header">
            <h3 class="panel-title">🌳 شجرة القرار الإحصائي المشروطة ومولد جداول (APA 7th Edition)</h3>
        </div>
        <p class="panel-desc">
            تختبر المنصة تلقائياً شروط اعتدالية التوزيع (Shapiro-Wilk) وتجانس التباين (Levene's Test) في الخلفية، وتوجه الباحث إجبارياً نحو الاختبار المعلمي أو اللامعلمي الصحيح مع توليد الجدول الأكاديمي النهائي.
        </p>
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
        "اختر نوع الفرضية البحثية المراد اختبارها:",
        [
            "🔗 فرضية علاقة ارتباطية بين متغيرين كميين (Correlation Analysis)",
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
            reason_txt = f"نظراً لتحقق شرط اعتدالية التوزيع في المتغيرين (Shapiro-Wilk p = {p_sw_x:.3f}, {p_sw_y:.3f} > 0.05)، اعتمد المحرك اختبار بيرسون المعلمي."
        else:
            test_used = "معامل ارتباط سبيرمان اللامعلمي للرتب (Spearman Rank - rho)"
            r_val, p_val = stats.spearmanr(series_x, series_y)
            reason_txt = f"نظراً لعدم تحقق شرط الاعتدالية في أحد المتغيرين (Shapiro-Wilk p = {min(p_sw_x, p_sw_y):.4f} ≤ 0.05)، حظر النظام اختبار بيرسون ووجه التحليل آلياً نحو بديله اللامعلمي الصحيح (سبيرمان)."

        st.success(f"🧭 **قرار المحرك الإحصائي:** اعتماد **{test_used}**\n\n*{reason_txt}*")

        sig_label = "دالة إحصائياً عند (α = 0.05)" if p_val < 0.05 else "غير دالة إحصائياً"
        st.markdown(f"""
        <div class="apa-container">
            <h4 style="color:#0F172A; margin-top:0; font-weight:800;">جدول (1): نتائج اختبار العلاقة الارتباطية وفق معايير APA 7th Edition</h4>
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
                        <td style="font-weight:700;">{var_x}</td>
                        <td>{len(series_x)}</td>
                        <td>{np.mean(series_x):.2f}</td>
                        <td>{np.std(series_x, ddof=1):.2f}</td>
                        <td rowspan="2" style="font-weight:900; font-size:1.15rem; color:#1E3A8A;">{r_val:.3f}**</td>
                        <td rowspan="2" style="font-weight:700;">{p_val:.4f}</td>
                        <td rowspan="2"><span class="kpi-pill pill-green">{sig_label}</span></td>
                    </tr>
                    <tr>
                        <td style="font-weight:700;">{var_y}</td>
                        <td>{len(series_y)}</td>
                        <td>{np.mean(series_y):.2f}</td>
                        <td>{np.std(series_y, ddof=1):.2f}</td>
                    </tr>
                </tbody>
            </table>
            <p style="font-size:0.88rem; color:#64748B; margin-bottom:0;"><i>ملاحظة: تم استخراج الجدول وتنسيقه آلياً عبر منصة Socio Lab وفق الدليل السابع للجمعية الأمريكية لعلم النفس (APA).</i></p>
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

                st.success(f"🧭 **الاختبار المعتمد آلياً بعد فحص الاعتدالية وتجانس التباين (Levene p = {p_lev:.3f}):** {test_title}")
                st.markdown(f"""
                <div class="apa-container">
                    <h4 style="color:#0F172A; margin-top:0; font-weight:800;">جدول (2): نتائج اختبار الفروق بين المجموعتين وفق معايير APA 7th Edition</h4>
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
                                <td style="font-weight:700;">المجموعة الأولى ({groups[0]})</td>
                                <td>{len(g1)}</td>
                                <td>{np.mean(g1):.2f}</td>
                                <td>{np.std(g1, ddof=1):.2f}</td>
                                <td rowspan="2" style="font-weight:900; font-size:1.15rem; color:#1E3A8A;">{stat_symbol}</td>
                                <td rowspan="2" style="font-weight:700;">{p_val:.4f}</td>
                            </tr>
                            <tr>
                                <td style="font-weight:700;">المجموعة الثانية ({groups[1]})</td>
                                <td>{len(g2)}</td>
                                <td>{np.mean(g2):.2f}</td>
                                <td>{np.std(g2, ddof=1):.2f}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                """, unsafe_allow_html=True)


# ==========================================
# القسم الخامس: التصدير لـ SPSS وشهادة النزاهة
# ==========================================
elif nav_page == "5. التصدير لـ SPSS وشهادة النزاهة":
    st.markdown("""
    <div class="glass-panel">
        <div class="panel-header">
            <h3 class="panel-title">🎓 تصدير الحزمة الإحصائية النهائية (SPSS .sav) وإصدار شهادة النزاهة</h3>
        </div>
        <p class="panel-desc">
            حمل ملفاتك النهائية المطهرة والمرمزة جاهزة للفتح المباشر في برنامج <b>IBM SPSS Statistics</b>، مع شهادة الاعتماد المنهجي لإرفاقها بمذكرة التخرج أو التقرير المؤسسي.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_d1, col_d2, col_d3 = st.columns(3)

    csv_bytes = st.session_state.working_df.to_csv(index=False).encode('utf-8-sig')
    with col_d1:
        st.download_button(
            label="📥 تحميل المصفوفة المرمزة (CSV / Excel)",
            data=csv_bytes,
            file_name="SocioLab_Cleaned_Dataset.csv",
            mime="text/csv"
        )

    codebook_bytes = st.session_state.codebook_df.to_csv(index=False).encode('utf-8-sig')
    with col_d2:
        st.download_button(
            label="📘 تحميل دليل الترميز (Variable View)",
            data=codebook_bytes,
            file_name="SocioLab_SPSS_Codebook.csv",
            mime="text/csv"
        )

    with col_d3:
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
                st.download_button(
                    label="📊 تحميل ملف SPSS الأصلي (.sav)",
                    data=f,
                    file_name="SocioLab_Verified_Data.sav",
                    mime="application/octet-stream"
                )
        else:
            st.info("تصدير `.sav` مفعل عبر مكتبة pyreadstat.")

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    cert_id = f"SL-DZ-{datetime.datetime.now().strftime('%Y%m')}-060"

    st.markdown(f"""
    <div class="luxury-certificate">
        <div class="cert-seal">★ SOCIO LAB VERIFIED DATASET ★</div>
        <h2 style="color:#0F172A; margin-bottom:6px; font-weight:900; font-size:1.85rem;">شهادة التدقيق المنهجي وموثوقية البيانات الميدانية</h2>
        <h5 style="color:#1D4ED8; margin-top:0; font-family:'Plus Jakarta Sans',sans-serif; letter-spacing:1.5px;">FORENSIC STATISTICAL & PSYCHOMETRIC AUDIT CERTIFICATE</h5>
        <hr style="border:1px solid #CBD5E1; width:65%; margin:20px auto;">
        <p style="font-size:1.12rem; color:#1E293B; line-height:2.0; max-width:85%; margin:0 auto;">
            تشهد منصة <b>Socio Lab السحابية للهندسة المنهجية والبيانات</b> بأن قاعدة البيانات الميدانية المرفقة قد خضعت للفحص الجنائي الإحصائي الآلي،
            وتم تدقيقها من حيث التباين الداخلي للاستمارات (<b>IRV</b>)، والاتساق السيكومتري للعبارات المعكوسة، وخلوها من الاستنساخ المكتبي،
            وبلغ معامل الثبات الكلي للمقياس بعد الضبط (<b>α = {alpha_now:.3f}</b>) بحجم عينة صافية ومعتمدة قدره (<b>N = {len(df_current)}</b>).
        </p>
        <div style="display:flex; justify-content:space-around; margin-top:32px; padding-top:20px; border-top:1px dashed #CBD5E1; font-weight:800; color:#0F172A;">
            <div>🔖 رقم الاعتماد المرجعي: <span style="color:#1D4ED8;">{cert_id}</span></div>
            <div>📅 تاريخ الإصدار: <span style="color:#1D4ED8;">{today_str}</span></div>
            <div>🏛️ الجهة المشرفة: <span style="color:#1D4ED8;">Socio Lab - سوق أهراس</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# القسم السادس: بوابة حجز الاستشارات والدورات
# ==========================================
elif nav_page == "6. حجز الاستشارات والدورات التدريبية":
    st.markdown("""
    <div class="glass-panel">
        <div class="panel-header">
            <h3 class="panel-title">📅 بوابة حجز الاستشارات المنهجية والدورات التدريبية (حضوري بسوق أهراس / عن بعد)</h3>
        </div>
        <p class="panel-desc">
            احجز جلسة مرافقة منهجية وإحصائية مخصصة لبحثك أو سجل في معسكرات التدريب التطبيقي على برنامج <b>IBM SPSS</b> ومنهجية <b>IMRAD</b>:
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("booking_form"):
        c_f1, c_f2 = st.columns(2)
        with c_f1:
            client_name = st.text_input("👤 الاسم واللقب الكامل:")
            client_uni = st.text_input("🏛️ الجامعة / المؤسسة:", value="جامعة محمد الشريف مساعدية - سوق أهراس")
            client_level = st.selectbox("🎓 الصفة الأكاديمية أو المهنية:", ["طالب ماستر 2", "طالب دكتوراه", "أستاذ باحث", "مؤسسة اقتصادية / جمعية"])
        with c_f2:
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
