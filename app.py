import streamlit as st
import pandas as pd
import numpy as np
import math
import io
import datetime
import base64
import os
import glob

try:
    import pyreadstat
    HAS_PYREADSTAT = True
except ImportError:
    HAS_PYREADSTAT = False

# ==========================================
# 1. إعدادات الصفحة والهوية البصرية المطابقة للشعار
# ==========================================
st.set_page_config(
    page_title="Socio Lab",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lobster&family=Pacifico&family=Readex+Pro:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

    html, body, [class*="css"], .stMarkdown, .stText, .stButton, .stSelectbox, .stMultiSelect, .stRadio {
        font-family: 'Readex Pro', sans-serif !important;
        direction: rtl;
        text-align: right;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    /* خلفية كحلية مطابقة لألوان الشعار */
    .stApp {
        background: radial-gradient(circle at 15% 10%, #0A2540 0%, #051324 55%, #020813 100%) !important;
        color: #F8FAFC !important;
    }

    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #F1F5F9 !important;
    }

    /* ضبط صناديق التنبيه الافتراضية لكي لا تظهر بيضاء أبداً */
    div[data-testid="stAlert"] {
        background: rgba(10, 32, 64, 0.92) !important;
        border: 1px solid rgba(56, 189, 248, 0.45) !important;
        border-right: 5px solid #38BDF8 !important;
        border-radius: 14px !important;
        color: #F8FAFC !important;
    }
    div[data-testid="stAlert"] * {
        color: #F8FAFC !important;
    }

    /* الترويسة العلوية للمنصة */
    .top-navbar {
        background: rgba(8, 25, 48, 0.85);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 22px;
        padding: 20px 34px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 20px 45px -15px rgba(0, 0, 0, 0.75), 0 0 25px rgba(56, 189, 248, 0.12);
    }
    .brand-box {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .brand-logo {
        width: 68px;
        height: 68px;
        border-radius: 16px;
        background: linear-gradient(135deg, #0284C7 0%, #2563EB 50%, #1E3A8A 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Lobster', 'Pacifico', cursive !important;
        font-size: 1.8rem;
        color: #FFFFFF;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.5);
    }
    .brand-title {
        font-family: 'Lobster', 'Pacifico', cursive !important;
        font-size: 2.65rem !important;
        font-weight: 400 !important;
        letter-spacing: 0.5px;
        direction: ltr !important;
        display: inline-block;
        background: linear-gradient(180deg, #FFFFFF 15%, #BAE6FD 65%, #7DD3FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 14px rgba(56, 189, 248, 0.45));
        margin: 0;
        line-height: 1.15;
    }
    .brand-sub {
        color: #CBD5E1 !important;
        font-size: 0.92rem;
        margin: 6px 0 0 0;
    }
    .location-badge {
        background: rgba(56, 189, 248, 0.14);
        border: 1px solid rgba(56, 189, 248, 0.4);
        color: #7DD3FC !important;
        padding: 9px 18px;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* الواجهة الرئيسية (Hero Section) */
    .hero-box {
        background: linear-gradient(135deg, rgba(14, 48, 92, 0.65) 0%, rgba(7, 20, 40, 0.94) 100%);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-right: 6px solid #38BDF8;
        border-radius: 22px;
        padding: 36px 40px;
        margin-bottom: 28px;
        box-shadow: 0 18px 40px -12px rgba(0, 0, 0, 0.6);
    }
    .hero-title {
        font-size: 1.95rem;
        font-weight: 700;
        color: #FFFFFF !important;
        margin-top: 0;
        margin-bottom: 14px;
        line-height: 1.4;
    }
    .hero-desc {
        font-size: 1.06rem;
        color: #E2E8F0 !important;
        line-height: 1.9;
        margin-bottom: 0;
    }

    /* بانر الدعوة لاتخاذ إجراء في أسفل الصفحة (CTA Banner) */
    .cta-banner {
        background: linear-gradient(135deg, rgba(2, 132, 199, 0.28) 0%, rgba(15, 38, 72, 0.92) 100%);
        border: 1px solid rgba(56, 189, 248, 0.5);
        border-right: 6px solid #38BDF8;
        border-radius: 18px;
        padding: 22px 28px;
        margin-top: 24px;
        box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.5);
        color: #F8FAFC !important;
        font-size: 1.02rem;
        line-height: 1.75;
    }

    /* البطاقات المعلوماتية */
    .info-card {
        background: linear-gradient(145deg, rgba(15, 38, 72, 0.72) 0%, rgba(8, 22, 44, 0.92) 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-top: 3px solid #38BDF8;
        border-radius: 20px;
        padding: 24px;
        height: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }
    .info-card:hover {
        transform: translateY(-5px);
        border-color: #38BDF8;
        box-shadow: 0 20px 40px -12px rgba(56, 189, 248, 0.28);
    }
    .card-icon {
        width: 48px;
        height: 48px;
        border-radius: 14px;
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.35);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.45rem;
        margin-bottom: 14px;
    }
    .card-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #FFFFFF !important;
        margin: 0 0 10px 0;
    }
    .card-text {
        font-size: 0.94rem;
        color: #CBD5E1 !important;
        line-height: 1.8;
        margin-bottom: 12px;
    }
    .output-box {
        background: rgba(6, 182, 212, 0.14);
        border-right: 3px solid #38BDF8;
        padding: 10px 14px;
        border-radius: 8px;
        font-size: 0.88rem;
        color: #7DD3FC !important;
        margin-top: 10px;
    }
    .badge-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        background: rgba(56, 189, 248, 0.16);
        color: #7DD3FC;
        border: 1px solid rgba(56, 189, 248, 0.3);
        margin-left: 6px;
        margin-top: 4px;
    }
    .badge-green {
        background: rgba(16, 185, 129, 0.16);
        color: #6EE7B7;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }
    .badge-amber {
        background: rgba(245, 158, 11, 0.16);
        color: #FCD34D;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }

    /* بطاقات خطوات العمل */
    .step-card {
        background: rgba(10, 28, 56, 0.85);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 18px;
        padding: 22px;
        text-align: center;
        height: 100%;
    }
    .step-num {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        background: linear-gradient(135deg, #0284C7, #2563EB);
        color: #FFFFFF;
        font-weight: 800;
        font-size: 1.2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 12px auto;
        box-shadow: 0 0 18px rgba(56, 189, 248, 0.45);
    }

    /* عناوين الأقسام */
    .section-heading {
        font-size: 1.5rem;
        font-weight: 700;
        color: #38BDF8 !important;
        margin: 26px 0 16px 0;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(56, 189, 248, 0.25);
    }

    /* شريط التبويبات الرئيسي */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(8, 24, 46, 0.92);
        padding: 10px;
        border-radius: 18px;
        border: 1px solid rgba(56, 189, 248, 0.25);
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px !important;
        padding: 10px 18px !important;
        font-weight: 700 !important;
        font-size: 0.94rem !important;
        color: #94A3B8 !important;
        background: transparent !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0284C7 0%, #2563EB 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45) !important;
    }

    /* الأزرار */
    .stButton > button {
        background: linear-gradient(135deg, #0284C7 0%, #2563EB 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 0.65rem 1.6rem !important;
        border: 1px solid rgba(125, 211, 252, 0.4) !important;
        box-shadow: 0 8px 20px -4px rgba(2, 132, 199, 0.45) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 25px -2px rgba(37, 99, 235, 0.65) !important;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. دوال مختبر فحص وتجهيز البيانات
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
        q7 = int(np.clip(base_tendency + np.random.randint(-1, 2), 1, 5))
        q8_rev = int(np.clip(6 - base_tendency + np.random.randint(-1, 2), 1, 5))
        data.append([ids[i], genders[i], levels[i], q1, q2, q3, q4_rev, q5, q6, q7, q8_rev])

    data[13][3:] = [5, 5, 5, 5, 5, 5, 5, 5]
    data[28][3:] = [5, 5, 5, 5, 5, 5, 4, 5]
    data[40][3:] = [1, 1, 1, 1, 1, 1, 2, 1]
    data[51][1:] = data[4][1:]

    columns = [
        "رمز_الاستمارة", "الجنس", "المستوى_الدراسي",
        "العبارة_1_الانضمام_للرفاق", "العبارة_2_التأثر_بالأقران", "العبارة_3_قضاء_الوقت", "العبارة_4_الاستقلالية_عكسية",
        "العبارة_5_مخالفة_النظم", "العبارة_6_التمرد_المدرسي", "العبارة_7_التغيب_المتكرر", "العبارة_8_الانضباط_عكسية"
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
                mapping_str = "ترميز قياسي آلي (مقياس ليكرت 1 إلى 5 / ثنائي)"
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
            "اسم المتغير": col,
            "نوع المتغير": "رقمي (Numeric)" if col != "رمز_الاستمارة" else "نصي (String)",
            "القيم المفقودة": int(df[col].isna().sum()),
            "دليل الترميز الآلي (Codebook)": mapping_str
        })

    return df_coded, pd.DataFrame(codebook)


def audit_survey_quality(df_coded, scale_cols, pos_col=None, neg_col=None):
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
        status = "استمارة سليمة وموثوقة"

        if sd_val < 0.20:
            reasons.append("إجابات نمطية مكررة في كل الأسئلة دون قراءة")
            status = "استمارة غير صالحة (تستبعد)"

        if pos_col and neg_col and pos_col in df_coded.columns and neg_col in df_coded.columns:
            v_pos = pd.to_numeric(row[pos_col], errors='coerce')
            v_neg = pd.to_numeric(row[neg_col], errors='coerce')
            if pd.notna(v_pos) and pd.notna(v_neg):
                if (v_pos >= 4 and v_neg >= 4) or (v_pos <= 2 and v_neg <= 2):
                    reasons.append("تناقض منطقي بين العبارة الموجبة والعبارة المعكوسة")
                    status = "استمارة غير صالحة (تستبعد)"

        if duplicated_mask.loc[idx]:
            reasons.append("استمارة منسوخة ومطابقة كلياً لاستمارة سابقة")
            status = "استمارة غير صالحة (تستبعد)"

        if missing_cnt > len(scale_cols) * 0.3:
            reasons.append(f"نقص كبير في الإجابات ({missing_cnt} أسئلة فارغة)")
            status = "استمارة غير صالحة (تستبعد)"

        if status != "استمارة سليمة وموثوقة":
            flagged_indices.append(idx)

        audit_records.append({
            "رقم الاستمارة": form_id,
            "تباين إجابات المبحوث": round(sd_val, 2),
            "الأسئلة الفارغة": missing_cnt,
            "ملاحظات الفحص الآلي لجودة البيانات": " ، ".join(reasons) if reasons else "إجابات متسقة ومنطقية",
            "القرار المنهجي": status
        })

    return pd.DataFrame(audit_records), flagged_indices


# ==========================================
# 3. تهيئة الجلسة والشعار الذكي
# ==========================================
if "raw_df" not in st.session_state:
    demo_text, _ = generate_demo_dataset()
    st.session_state.raw_df = demo_text
    coded_df, codebook_df = auto_code_dataframe(demo_text)
    st.session_state.working_df = coded_df
    st.session_state.codebook_df = codebook_df
    st.session_state.reversed_done = False
    st.session_state.cleaned_done = False

if "custom_logo_b64" not in st.session_state:
    st.session_state.custom_logo_b64 = None
    image_files = []
    for pattern in ["*logo*", "*.png", "*.jpg", "*.jpeg", "*.webp", "*.PNG", "*.JPG", "*.JPEG"]:
        image_files.extend(glob.glob(pattern))
    if image_files:
        try:
            with open(image_files[0], "rb") as img_f:
                st.session_state.custom_logo_b64 = base64.b64encode(img_f.read()).decode()
        except Exception:
            pass

if st.session_state.custom_logo_b64:
    b64_str = st.session_state.custom_logo_b64
    logo_html = f'<img src="data:image/png;base64,{b64_str}" style="width:76px; height:76px; border-radius:16px; object-fit:cover; background:#051324; border:2px solid #38BDF8; box-shadow:0 0 25px rgba(56,189,248,0.5);">'
else:
    logo_html = '<div class="brand-logo">SL</div>'


# ==========================================
# 4. الترويسة العلوية للمنصة بنفس خط الشعار
# ==========================================
st.markdown(f"""
<div class="top-navbar">
    <div class="brand-box">
        {logo_html}
        <div>
            <h1 class="brand-title">Socio Lab</h1>
            <p class="brand-sub">منصة رقمية للاستشارات المنهجية السوسيولوجية، التحليل الإحصائي، وتجهيز البيانات</p>
        </div>
    </div>
    <div class="location-badge">📍 حضوريا بجامعة سوق أهراس | 🌐 رقميا عبر 58 ولاية</div>
</div>
""", unsafe_allow_html=True)

with st.expander("🎨 تخصيص شعار المنصة (اضغط هنا لرفع صورة الشعار من جهازك)"):
    uploaded_logo = st.file_uploader("اختر صورة شعار Socio Lab:", type=["png", "jpg", "jpeg", "webp"])
    if uploaded_logo is not None:
        st.session_state.custom_logo_b64 = base64.b64encode(uploaded_logo.getvalue()).decode()
        st.success("تم تحديث شعار المنصة بنجاح!")
        st.rerun()


# ==========================================
# 5. الهيكلة التفصيلية للصفحات (7 تبويبات متكاملة)
# ==========================================
main_tabs = st.tabs([
    "🏛️ الرئيسية (Home)",
    "🧭 من نحن (About Us)",
    "💼 خدماتنا (Services)",
    "🎓 الدورات التكوينية",
    "🧰 مكتبة الأدوات (Resources)",
    "📰 المدونة (Blog)",
    "📅 اطلب خدمة / استشارة"
])


# ==========================================
# 1. الصفحة الرئيسية (Home)
# ==========================================
with main_tabs[0]:
    st.markdown("""
    <div class="hero-box">
        <h2 class="hero-title">من الفكرة البحثية إلى النتائج المحكمة.. شريكك المنهجي والإحصائي الدقيق.</h2>
        <p class="hero-desc">
            في المنصة الرقمية <span style="font-family:'Lobster',cursive; font-size:1.35rem; color:#7DD3FC;">Socio Lab</span>، نحول البيانات الميدانية الخام إلى رؤى سوسيولوجية وعلمية رصينة. نرافق طلبة الدراسات العليا، الباحثين، والمؤسسات في تصميم أدوات القياس، تنظيف البيانات، والتحليل الإحصائي المتقدم وفق أعلى معايير الجودة والنزاهة العلمية.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">🎯 الفئات المستهدفة (من يستفيد من المنصة الرقمية؟)</div>', unsafe_allow_html=True)
    ft1, ft2, ft3 = st.columns(3)
    with ft1:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">🎓</div>
            <h3 class="card-title">طلبة الليسانس والماستر</h3>
            <p class="card-text">طلبة جامعة سوق أهراس ومختلف الجامعات الجزائرية المقبلون على إعداد مذكرات التخرج وتقارير التربص الميداني، والذين يبحثون عن مرافقة منهجية وإحصائية دقيقة.</p>
            <span class="badge-tag">مذكرات التخرج</span>
            <span class="badge-tag">تقارير التربص</span>
        </div>
        """, unsafe_allow_html=True)
    with ft2:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">🔬</div>
            <h3 class="card-title">طلبة الدكتوراه والباحثون</h3>
            <p class="card-text">الباحثون الأكاديميون، الأساتذة، وفرق ومخابر البحث الراغبون في تحكيم المقاييس السيكومترية، تنظيف قواعد البيانات، وتنسيق الجداول للنشر في المجلات المصنفة.</p>
            <span class="badge-tag">أطروحات الدكتوراه</span>
            <span class="badge-tag">مقالات محكمة</span>
        </div>
        """, unsafe_allow_html=True)
    with ft3:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">🏢</div>
            <h3 class="card-title">المؤسسات، الإدارات، والجمعيات</h3>
            <p class="card-text">المؤسسات الاقتصادية العمومية والخاصة، الإدارات، والجمعيات التي تحتاج إلى إنجاز دراسات ميدانية، استطلاعات رأي، وتحليل بيانات اجتماعية لترشيد قراراتها.</p>
            <span class="badge-tag">استطلاعات الرأي</span>
            <span class="badge-tag badge-amber">دراسات ميدانية B2B</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">✨ لماذا تختار المنصة الرقمية Socio Lab؟</div>', unsafe_allow_html=True)
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">📖</div>
            <h4 class="card-title">قراءة سوسيولوجية لا أرقام صماء</h4>
            <p class="card-text">لا نكتفي باستخراج جداول SPSS، بل نربط المؤشرات الإحصائية بالسياق النظري والميداني لدراستك.</p>
        </div>
        """, unsafe_allow_html=True)
    with r2:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">🎯</div>
            <h4 class="card-title">دقة منهجية صارمة</h4>
            <p class="card-text">نعتمد أحدث الأساليب العلمية في بناء المقاييس، حساب الصدق والثبات، واختيار الاختبارات الإحصائية الأنسب لطبيعة متغيراتك.</p>
        </div>
        """, unsafe_allow_html=True)
    with r3:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">🔒</div>
            <h4 class="card-title">سرية وأمان تام</h4>
            <p class="card-text">نضمن حماية أفكارك البحثية وبيانات المستجيبين بموجب ميثاق صارم للخصوصية وعدم الإفصاح.</p>
        </div>
        """, unsafe_allow_html=True)
    with r4:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">⏱️</div>
            <h4 class="card-title">التزام بالمواعيد</h4>
            <p class="card-text">تسليم المخرجات في الآجال المحددة مع إتاحة جلسات شرح ومناقشة للنتائج قبل موعد دفاعك أو نشرك العلمي.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">⚙️ خطوات العمل في المنصة (How It Works)</div>', unsafe_allow_html=True)
    st1, st2, st3, st4 = st.columns(4)
    with st1:
        st.markdown("""
        <div class="step-card">
            <div class="step-num">1</div>
            <h4 class="card-title">إرسال الطلب والملفات</h4>
            <p class="card-text">تملأ نموذج الطلب وتحدد الخدمة المطلوبة وترفق مسودة بحثك أو بياناتك.</p>
        </div>
        """, unsafe_allow_html=True)
    with st2:
        st.markdown("""
        <div class="step-card">
            <div class="step-num">2</div>
            <h4 class="card-title">التقييم وتحديد الخطة</h4>
            <p class="card-text">ندرس ملفك ونوافيك بخطة العمل المقترحة، المدة الزمنية، والتكلفة الدقيقة خلال 24 ساعة.</p>
        </div>
        """, unsafe_allow_html=True)
    with st3:
        st.markdown("""
        <div class="step-card">
            <div class="step-num">3</div>
            <h4 class="card-title">التنفيذ والمتابعة</h4>
            <p class="card-text">يبدأ العمل المنهجي أو الإحصائي مع إطلاعك على مراحل التقدم خطوة بخطوة.</p>
        </div>
        """, unsafe_allow_html=True)
    with st4:
        st.markdown("""
        <div class="step-card">
            <div class="step-num">4</div>
            <h4 class="card-title">التسليم والشرح</h4>
            <p class="card-text">تستلم ملفاتك النهائية الجاهزة، مع جلسة توضيحية لشرح النتائج وكيفية الدفاع عنها أمام لجنة المناقشة.</p>
        </div>
        """, unsafe_allow_html=True)

    # بانر الدعوة لاتخاذ إجراء بلون كحلي وخط أبيض واضح تماماً
    st.markdown("""
    <div class="cta-banner">
        🚀 <b style="color:#38BDF8;">دعوتك لطلب استشارة أو خدمة بحثية:</b>
        انتقل إلى تبويب <b style="color:#7DD3FC;">«📅 اطلب خدمة / استشارة»</b> في أعلى الشاشة لملء بياناتك وإرفاق ملفاتك، وسيتواصل معك فريق <b>Socio Lab</b> خلال 24 ساعة.
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 2. صفحة من نحن (About Us)
# ==========================================
with main_tabs[1]:
    st.markdown('<div class="section-heading">🧭 من نحن (About Us)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="hero-box">
        <h3 class="card-title" style="font-size:1.5rem; color:#38BDF8 !important;">المنصة الرقمية والمختبر الاستشاري <span style="font-family:'Lobster',cursive;">Socio Lab</span></h3>
        <p class="hero-desc">
            <b>Socio Lab</b> هو مختبر استشاري وبحثي ومنصة رقمية متخصصة في المنهجية السوسيولوجية والتحليل الإحصائي للبيانات الاجتماعية والإنسانية.
            تأسست المنصة لسد الفجوة بين الجانب النظري في الأبحاث الأكاديمية والتطبيق الميداني والإحصائي الدقيق، عبر تقديم حلول بحثية متكاملة تجمع بين الخبرة الميدانية والتمكن التقني.
        </p>
    </div>
    """, unsafe_allow_html=True)

    ab1, ab2 = st.columns(2)
    with ab1:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">🔭</div>
            <h3 class="card-title">رؤيتنا</h3>
            <p class="card-text">
                أن نكون المرجع الأول والموثوق للباحثين والمؤسسات في العالم العربي للارتقاء بجودة الإنتاج العلمي والقرارات المبنية على البيانات الدقيقة.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with ab2:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">🎯</div>
            <h3 class="card-title">رسالتنا</h3>
            <p class="card-text">
                تمكين الباحثين وطلبة الماستر والدكتوراه والمؤسسات من إنجاز دراسات ميدانية محكمة، عبر توفير استشارات منهجية احترافية، وأدوات قياس موثوقة، وتحليلات إحصائية دقيقة تلتزم بأخلاقيات البحث العلمي وتنبذ التزييف أو الانتحال.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <div class="card-icon">🛡️</div>
        <h3 class="card-title">التزامنا بالنزاهة العلمية وسرية البيانات</h3>
        <p class="card-text">
            تعمل المنصة الرقمية <b>Socio Lab</b> وفق ميثاق صارم لأخلاقيات البحث العلمي؛ حيث نرفض تماما كتابة المذكرات أو البحوث بالنيابة عن الطالب أو اختلاق بيانات غير حقيقية، ونحصر تدخلنا في الاستشارة المنهجية، بناء وتحكيم أدوات القياس، تنظيف البيانات، والمعالجة الإحصائية المشروعة مع الشرح التعليمي الكامل للباحث، مع ضمان السرية التامة لكافة الملفات والبيانات الشخصية للمبحوثين.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 3. صفحة الخدمات (Services)
# ==========================================
with main_tabs[2]:
    st.markdown('<div class="section-heading">💼 خدماتنا البحثية والإحصائية (Services)</div>', unsafe_allow_html=True)

    sv1, sv2 = st.columns(2)

    with sv1:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">📝</div>
            <h3 class="card-title">أولا: تصميم وبناء أدوات البحث الميداني</h3>
            <p class="card-text">
                نصمم لك أداة جمع البيانات الملائمة لإشكالية بحثك ومتغيراته بدقة عالية:<br>
                • صياغة وبناء الاستبيانات الورقية والإلكترونية (Google Forms, KoboToolbox) وفق المحاور والفرضيات.<br>
                • إعداد أدلة المقابلات المعمقة والملاحظة العلمية للدراسات الكيفية.<br>
                • تكييف المقاييس العالمية وترجمتها بما يتناسب مع البيئة الاجتماعية والثقافية لعينة الدراسة.
            </p>
            <div class="output-box">
                <b>المخرجات:</b> نسخة نهائية من الأداة قابلة للتحكيم والتطبيق الميداني مرفقة بدليل الترميز (Codebook).
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-card">
            <div class="card-icon">🧭</div>
            <h3 class="card-title">ثالثا: التحكيم والضبط المنهجي</h3>
            <p class="card-text">
                مراجعة شاملة لخطة البحث لضمان انسجامها المنهجي قبل الشروع في الدراسة الميدانية أو المناقشة:<br>
                • تدقيق صياغة الإشكالية، التساؤلات، والفرضيات ومدى قابليتها للاختبار.<br>
                • تحديد نوع العينة وحجمها المناسب لمجتمع الدراسة.<br>
                • مواءمة الإطار النظري مع مؤشرات القياس الميداني.
            </p>
            <div class="output-box">
                <b>المخرجات:</b> تقرير مفصل بالملاحظات المنهجية والتعديلات المقترحة خطوة بخطوة.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with sv2:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">📊</div>
            <h3 class="card-title">ثانيا: التحليل الإحصائي وتفريغ البيانات (SPSS)</h3>
            <p class="card-text">
                نحول إجابات المبحوثين إلى نتائج إحصائية دقيقة وقابلة للتفسير:<br>
                • تفريغ البيانات، ترميزها، وتنظيفها (Data Cleaning) من القيم الشاذة والمفقودة.<br>
                • حساب الخصائص السيكومترية للأداة (الصدق البنائي، الاتساق الداخلي، ومعامل الثبات ألفا كرونباخ).<br>
                • إجراء الاختبارات الوصفية (التكرارات، النسب، المتوسطات، الانحراف المعياري) والاستدلالية (اختبارات الفروق، الارتباط، الانحدار) وفق طبيعة التوزيع.
            </p>
            <div class="output-box">
                <b>المخرجات:</b> ملف مخرجات SPSS الأصلي + تقرير تحليلي منسق بالجداول والرسوم البيانية مع التعليق السوسيولوجي الأولي على كل جدول.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-card">
            <div class="card-icon">📚</div>
            <h3 class="card-title">رابعا: التوثيق والتدقيق الأكاديمي</h3>
            <p class="card-text">
                نجهز أوراقك البحثية ومقالاتك للنشر في المجلات المحكمة والمؤتمرات الدولية:<br>
                • توثيق المراجع في المتن وفي القائمة النهائية بدقة وفق نظام التوثيق العالمي (APA).<br>
                • التدقيق اللغوي والأسلوبي للنصوص الأكاديمية لضمان سلامة اللغة ورصانة الأسلوب العلمي.<br>
                • تنسيق الجداول والأشكال البيانية وفق شروط المجلات العلمية المستهدفة.
            </p>
            <div class="output-box">
                <b>المخرجات:</b> ورقة بحثية أو فصل تطبيقي منسق ومضبوط وفق معايير النشر الأكاديمي.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# 4. صفحة الدورات التكوينية
# ==========================================
with main_tabs[3]:
    st.markdown('<div class="section-heading">🎓 الدورات التكوينية والتدريب التطبيقي (حضوريا وعن بعد)</div>', unsafe_allow_html=True)
    st.write("تقدم المنصة الرقمية **Socio Lab** دورات تدريبية تطبيقية مصغرة ومكثفة لتطوير مهارات الطلبة، الباحثين، وإطارات المؤسسات:")

    tr1, tr2 = st.columns(2)
    with tr1:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">💻</div>
            <h3 class="card-title">الدورة 1: الأساسيات التطبيقية لتحليل البيانات ببرنامج SPSS</h3>
            <p class="card-text">
                <b>الفئة المستهدفة:</b> طلبة الليسانس والماستر المبتدئون في التحليل الإحصائي.<br>
                <b>المحاور:</b> إعداد قاعدة البيانات، ترميز الاستبيانات وإدخالها، حساب التكرارات والنسب المئوية، المتوسطات والانحراف المعياري، وتنسيق الجداول.
            </p>
            <span class="badge-tag">12 ساعة تطبيقية</span>
            <span class="badge-tag">حضوري بسوق أهراس / عن بعد</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-card">
            <div class="card-icon">📐</div>
            <h3 class="card-title">الدورة 2: هندسة الاستبيانات الإلكترونية وبناء المقاييس</h3>
            <p class="card-text">
                <b>الفئة المستهدفة:</b> طلبة الدراسات العليا، الباحثون، وإطارات الجمعيات والمؤسسات.<br>
                <b>المحاور:</b> تحويل الفرضيات إلى محاور وفقرات قياس، تصميم الاستبيان على Google Forms و KoboToolbox، وتجنب أخطاء صياغة الأسئلة.
            </p>
            <span class="badge-tag">8 ساعات تطبيقية</span>
            <span class="badge-tag badge-green">تطبيق عملي مباشر</span>
        </div>
        """, unsafe_allow_html=True)

    with tr2:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">📈</div>
            <h3 class="card-title">الدورة 3: الإحصاء الاستدلالي المتقدم واختبار الفرضيات</h3>
            <p class="card-text">
                <b>الفئة المستهدفة:</b> طلبة الماستر 2، طلبة الدكتوراه، والباحثون الأكاديميون.<br>
                <b>المحاور:</b> فحص الصدق والثبات، شروط الاختبارات المعلمية واللامعلمية، اختبارات الارتباط والفروق والانحدار، والقراءة السوسيولوجية للنتائج.
            </p>
            <span class="badge-tag">15 ساعة معمقة</span>
            <span class="badge-tag badge-amber">مستوى متقدم</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-card">
            <div class="card-icon">🏛️</div>
            <h3 class="card-title">الدورة 4: منهجية إعداد البحوث والمذكرات وفق IMRAD و APA</h3>
            <p class="card-text">
                <b>الفئة المستهدفة:</b> طلبة التخرج والباحثون الراغبون في النشر العلمي.<br>
                <b>المحاور:</b> الهيكلة المنهجية للدراسة الميدانية، التوثيق العلمي والمراجع بطريقة APA، وعرض ومناقشة النتائج الميدانية أمام اللجان العلمية.
            </p>
            <span class="badge-tag">10 ساعات</span>
            <span class="badge-tag badge-green">تحضير للمناقشة والنشر</span>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# 5. مكتبة الأدوات (Resources)
# ==========================================
with main_tabs[4]:
    st.markdown('<div class="section-heading">🧰 مكتبة الأدوات البحثية التفاعلية (Resources)</div>', unsafe_allow_html=True)

    res_tabs = st.tabs([
        "🧮 حاسبة حجم العينة (Sample Size Calculator)",
        "🔬 أداة تنظيف وترميز الاستبيانات الآلية",
        "📑 نماذج استبيانات وقوالب بحثية جاهزة"
    ])

    with res_tabs[0]:
        st.markdown("""
        <div class="info-card">
            <h3 class="card-title">🧮 حاسبة حجم العينة الإحصائية الدقيقة (معادلة كوكران وستيفن ثامبسون)</h3>
            <p class="card-text">احسب حجم العينة العلمي المناسب لمجتمع دراستك بناء على حجم المجتمع الأصلي، مستوى الثقة، وهامش الخطأ المقبول:</p>
        </div>
        """, unsafe_allow_html=True)

        cc1, cc2, cc3 = st.columns(3)
        with cc1:
            pop_size = st.number_input("حجم مجتمع الدراسة الأصلي (N):", min_value=10, max_value=10000000, value=1000, step=50)
        with cc2:
            conf_level = st.selectbox("مستوى الثقة (Confidence Level):", ["95% (Z = 1.96 - المعيار الشائع)", "99% (Z = 2.58)", "90% (Z = 1.645)"])
        with cc3:
            margin_err = st.selectbox("هامش الخطأ المقبول (Margin of Error):", ["5% (0.05 - المعيار القياسي)", "3% (0.03)", "1% (0.01)"])

        z_val = 1.96 if "95%" in conf_level else (2.58 if "99%" in conf_level else 1.645)
        e_val = 0.05 if "5%" in margin_err else (0.03 if "3%" in margin_err else 0.01)
        p_val = 0.5

        n_inf = (z_val ** 2 * p_val * (1 - p_val)) / (e_val ** 2)
        sample_size = math.ceil(n_inf / (1 + ((n_inf - 1) / pop_size)))

        st.success(f"🎯 **حجم العينة العلمي الموصى به لدراستك هو:** `{sample_size}` مفردة (استمارة صالحة للتحليل).")
        st.caption("ملاحظة منهجية: ينصح بتوزيع 10% إضافية من الاستمارات لتعويض الفاقد أو الاستمارات غير المكتملة ميدانيا.")

    with res_tabs[1]:
        st.write("ارفع ملف استبيانك الخام (Excel / CSV) ليقوم النظام آليا بترميز الإجابات، عكس العبارات السالبة، وكشف الاستمارات العشوائية أو المكررة:")
        c_src1, c_src2 = st.columns([3, 1])
        with c_src1:
            uploaded_file = st.file_uploader("📂 ارفع ملف استبيانك الخام (Excel أو CSV):", type=["xlsx", "csv"])
            if uploaded_file is not None:
                user_df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
                st.session_state.raw_df = user_df
                coded_df, codebook_df = auto_code_dataframe(user_df)
                st.session_state.working_df = coded_df
                st.session_state.codebook_df = codebook_df
                st.session_state.reversed_done = False
                st.session_state.cleaned_done = False
                st.success("تم رفع وترميز ملف الاستبيان بنجاح!")
        with c_src2:
            st.write("")
            st.write("")
            if st.button("🔄 إعادة ضبط العينة التجريبية"):
                demo_text, _ = generate_demo_dataset()
                st.session_state.raw_df = demo_text
                coded_df, codebook_df = auto_code_dataframe(demo_text)
                st.session_state.working_df = coded_df
                st.session_state.codebook_df = codebook_df
                st.session_state.reversed_done = False
                st.session_state.cleaned_done = False
                st.rerun()

        df_current = st.session_state.working_df
        numeric_cols = [c for c in df_current.columns if c not in ["رمز_الاستمارة", "الجنس", "المستوى_الدراسي"]]

        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.caption("📄 البيانات النصية الخام:")
            st.dataframe(st.session_state.raw_df, use_container_width=True, height=230)
        with col_v2:
            st.caption("🔢 المصفوفة الرقمية المرمزة آليا:")
            st.dataframe(st.session_state.working_df, use_container_width=True, height=230)

        default_rev = [c for c in numeric_cols if "عكسية" in c]
        rev_cols = st.multiselect("حدد العبارات السالبة لقلب أوزانها (5 ↔ 1):", numeric_cols, default=default_rev)
        c_act1, c_act2 = st.columns(2)
        with c_act1:
            if st.button("⚡ تطبيق عكس أوزان العبارات السالبة"):
                if not st.session_state.reversed_done and rev_cols:
                    for c in rev_cols:
                        st.session_state.working_df[c] = 6 - pd.to_numeric(st.session_state.working_df[c], errors='coerce')
                    st.session_state.reversed_done = True
                    st.success("تم عكس الأوزان بنجاح!")
                    st.rerun()
        with c_act2:
            raw_coded_temp, _ = auto_code_dataframe(st.session_state.raw_df)
            if st.session_state.cleaned_done:
                raw_coded_temp = raw_coded_temp.loc[st.session_state.working_df.index]
            pos_item = numeric_cols[0] if len(numeric_cols) > 0 else None
            neg_item = numeric_cols[3] if len(numeric_cols) > 3 else pos_item
            audit_df, bad_indices = audit_survey_quality(raw_coded_temp, numeric_cols, pos_item, neg_item)
            if len(bad_indices) > 0:
                if st.button(f"🧹 استبعاد {len(bad_indices)} استمارات غير صالحة وتنظيف الملف"):
                    st.session_state.working_df = st.session_state.working_df.drop(index=bad_indices)
                    st.session_state.cleaned_done = True
                    st.success("تم تنظيف قاعدة البيانات بنجاح!")
                    st.rerun()

        st.dataframe(audit_df.sort_values(by="القرار المنهجي", ascending=False), use_container_width=True, height=240)

        d1, d2 = st.columns(2)
        csv_bytes = st.session_state.working_df.to_csv(index=False).encode('utf-8-sig')
        with d1:
            st.download_button("📥 تنزيل ملف البيانات النظيف (CSV / Excel)", data=csv_bytes, file_name="SocioLab_Cleaned_Data.csv", mime="text/csv")
        codebook_bytes = st.session_state.codebook_df.to_csv(index=False).encode('utf-8-sig')
        with d2:
            st.download_button("📘 تنزيل دليل الترميز (Codebook)", data=codebook_bytes, file_name="SocioLab_Codebook.csv", mime="text/csv")

    with res_tabs[2]:
        q1, q2, q3 = st.columns(3)
        with q1:
            st.markdown("""
            <div class="info-card">
                <div class="card-icon">📋</div>
                <h4 class="card-title">نموذج استبيان سوسيولوجي معياري</h4>
                <p class="card-text">قالب جاهز مقسم إلى البيانات الشخصية ومحاور القياس وفق مقياس ليكرت الثلاثي والخماسي مع تعليمات الصدق الظاهري.</p>
                <span class="badge-tag">صيغة Word / PDF</span>
            </div>
            """, unsafe_allow_html=True)
        with q2:
            st.markdown("""
            <div class="info-card">
                <div class="card-icon">📑</div>
                <h4 class="card-title">قالب ورقة بحثية وفق نظام IMRAD</h4>
                <p class="card-text">نموذج تنسيق أكاديمي للمقالات العلمية ومذكرات التخرج يوضح هيكلة المقدمة، المنهجية، النتائج، والمناقشة.</p>
                <span class="badge-tag">معيار النشر الدولي</span>
            </div>
            """, unsafe_allow_html=True)
        with q3:
            st.markdown("""
            <div class="info-card">
                <div class="card-icon">🔖</div>
                <h4 class="card-title">دليل التوثيق المختصر APA 7th</h4>
                <p class="card-text">ملخص عملي لقواعد توثيق الكتب، المقالات، الرسائل الجامعية، والمواقع الإلكترونية في المتن وقائمة المراجع.</p>
                <span class="badge-tag badge-green">نسخة عربية محدثة</span>
            </div>
            """, unsafe_allow_html=True)


# ==========================================
# 6. المدونة (Blog)
# ==========================================
with main_tabs[5]:
    st.markdown('<div class="section-heading">📰 المدونة المنهجية والإحصائية (Blog)</div>', unsafe_allow_html=True)
    st.write("مقالات وشروحات تطبيقية مبسطة لمساعدة الباحثين والطلبة على تجنب الأخطاء المنهجية وإتقان أدوات البحث:")

    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown("""
        <div class="info-card">
            <span class="badge-tag">شروحات SPSS</span>
            <h3 class="card-title" style="margin-top:10px;">كيف تختار الاختبار الإحصائي المناسب لفرضيتك؟</h3>
            <p class="card-text">
                دليل عملي يوضح الفرق بين الاختبارات المعلمية واللامعلمية، ومتى نستخدم معامل ارتباط بيرسون أو سبيرمان، ومتى نلجأ لاختبار T-Test أو مان-ويتني بناء على شروط التوزيع الطبيعي وحجم العينة.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with b2:
        st.markdown("""
        <div class="info-card">
            <span class="badge-tag badge-amber">أخطاء منهجية شائعة</span>
            <h3 class="card-title" style="margin-top:10px;">7 أخطاء قاتلة عند تصميم الاستبيان الميداني</h3>
            <p class="card-text">
                تعرف على أبرز الأخطاء التي تفقد الاستبيان صدقه العلمي: الأسئلة المزدوجة، الأسئلة الموجهة لإجابة معينة، إهمال العبارات المعكوسة، وعدم تطابق بدائل الإجابة مع طبيعة المتغير المدروس.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with b3:
        st.markdown("""
        <div class="info-card">
            <span class="badge-tag badge-green">أخلاقيات البحث العلمي</span>
            <h3 class="card-title" style="margin-top:10px;">النزاهة الأكاديمية وحماية بيانات المبحوثين</h3>
            <p class="card-text">
                لماذا يعد الحفاظ على سرية هوية المبحوثين وأمانة تفريغ البيانات الميدانية حجر الأساس في البحث السوسيولوجي الرصين؟ وكيف تحمي بحثك من شبهات الانتحال أو تزييف النتائج.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# 7. اطلب خدمة / استشارة (Order & Book)
# ==========================================
with main_tabs[6]:
    st.markdown('<div class="section-heading">📅 اطلب خدمة بحثية أو احجز جلسة استشارية (Order & Book)</div>', unsafe_allow_html=True)
    st.write("املأ النموذج أدناه وأرفق ملفاتك (اختياري)، وسيقوم فريق المنصة الرقمية **Socio Lab** بدراسة طلبك وموافاتك بخطة العمل والتكلفة خلال 24 ساعة:")

    with st.form("order_service_form"):
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            client_name = st.text_input("👤 الاسم الكامل / المؤسسة:")
            client_contact = st.text_input("📱 البريد الإلكتروني / رقم الواتساب:")
            client_role = st.selectbox("🎓 الصفة الأكاديمية أو المهنية:", [
                "طالب ماستر",
                "طالب دكتوراه",
                "أستاذ باحث",
                "مؤسسة أو جمعية",
                "طالب ليسانس"
            ])
            client_specialty = st.text_input("📚 التخصص العلمي:")

        with f_col2:
            service_type = st.selectbox("💼 نوع الخدمة المطلوبة:", [
                "تصميم استبيان وبناء أداة بحث",
                "تحليل إحصائي وتفريغ بيانات SPSS",
                "ضبط وتحكيم منهجي",
                "توثيق APA وتدقيق أكاديمي",
                "باقة متكاملة (من تصميم الأداة إلى التحليل والتقرير)",
                "التسجيل في دورة تكوينية",
                "حجز جلسة توجيه فردي"
            ])
            deadline_date = st.date_input("📅 الموعد النهائي المقترح للتسليم:", value=datetime.date.today() + datetime.timedelta(days=7))
            attached_files = st.file_uploader(
                "📎 إرفاق ملفات (اختياري: Word, Excel, SPSS, PDF):",
                type=["doc", "docx", "xlsx", "xls", "csv", "sav", "pdf"],
                accept_multiple_files=True
            )

        order_desc = st.text_area("📝 وصف مختصر للدراسة أو الطلب:")

        submitted = st.form_submit_button("🚀 إرسال الطلب وحجز الخدمة الآن")
        if submitted:
            if client_name and client_contact:
                files_count = len(attached_files) if attached_files else 0
                st.success(
                    f"تم استلام طلبك بنجاح يا ({client_name})! "
                    f"الخدمة المطلوبة: ({service_type}) | الموعد المقترح: ({deadline_date}) | عدد الملفات المرفقة: ({files_count}). "
                    f"سيتواصل معك فريق Socio Lab عبر ({client_contact}) خلال 24 ساعة."
                )
            else:
                st.warning("يرجى إدخال الاسم الكامل ووسيلة التواصل (البريد الإلكتروني أو رقم الواتساب) لإرسال الطلب.")
