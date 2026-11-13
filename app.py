import streamlit as st
import pandas as pd
import numpy as np
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
# 1. إعدادات الصفحة والهوية البصرية الأكاديمية الراقية
# ==========================================
st.set_page_config(
    page_title="Socio Lab | المنصة الوطنية للاستشارات المنهجية والإحصائية والتدريب",
    page_icon="🏛️",
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

    /* خلفية كحلية ملكية عميقة ومريحة للعين */
    .stApp {
        background: radial-gradient(circle at 15% 10%, #172554 0%, #0F172A 50%, #020617 100%) !important;
        color: #F8FAFC !important;
    }

    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #F1F5F9 !important;
    }

    /* الترويسة العلوية للمنصة */
    .top-navbar {
        background: rgba(15, 23, 42, 0.82);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 22px;
        padding: 22px 34px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.65);
    }
    .brand-box {
        display: flex;
        align-items: center;
        gap: 18px;
    }
    .brand-logo {
        width: 66px;
        height: 66px;
        border-radius: 16px;
        background: linear-gradient(135deg, #0284C7 0%, #2563EB 50%, #4F46E5 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.65rem;
        font-weight: 800;
        color: #FFFFFF;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.45);
    }
    .brand-title {
        font-size: 1.75rem;
        font-weight: 700;
        background: linear-gradient(90deg, #FFFFFF 0%, #38BDF8 60%, #93C5FD 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .brand-sub {
        color: #CBD5E1 !important;
        font-size: 0.92rem;
        margin: 5px 0 0 0;
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

    /* البانر التعريفي الرئيسي (Hero Section) */
    .hero-box {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.55) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(96, 165, 250, 0.3);
        border-right: 6px solid #38BDF8;
        border-radius: 22px;
        padding: 32px 36px;
        margin-bottom: 28px;
        box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.5);
    }
    .hero-title {
        font-size: 1.85rem;
        font-weight: 700;
        color: #FFFFFF !important;
        margin-top: 0;
        margin-bottom: 12px;
    }
    .hero-desc {
        font-size: 1.05rem;
        color: #E2E8F0 !important;
        line-height: 1.85;
        margin-bottom: 0;
    }

    /* بطاقات الفئات المستهدفة والخدمات والدورات */
    .info-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.72) 0%, rgba(15, 23, 42, 0.92) 100%);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-top: 3px solid #38BDF8;
        border-radius: 20px;
        padding: 24px;
        height: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.45);
        margin-bottom: 20px;
    }
    .info-card:hover {
        transform: translateY(-6px);
        border-color: #38BDF8;
        box-shadow: 0 20px 40px -12px rgba(56, 189, 248, 0.25);
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
        font-size: 0.92rem;
        color: #CBD5E1 !important;
        line-height: 1.75;
        margin-bottom: 14px;
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

    /* عناوين الأقسام */
    .section-heading {
        font-size: 1.5rem;
        font-weight: 700;
        color: #38BDF8 !important;
        margin: 24px 0 16px 0;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(56, 189, 248, 0.25);
    }

    /* شريط التبويبات الرئيسي */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(15, 23, 42, 0.9);
        padding: 10px;
        border-radius: 18px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px !important;
        padding: 12px 22px !important;
        font-weight: 700 !important;
        font-size: 0.96rem !important;
        color: #94A3B8 !important;
        background: transparent !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0284C7 0%, #2563EB 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
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

    /* شهادة موثوقية البيانات */
    .holo-cert {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 58, 138, 0.85) 100%);
        border: 2px solid #38BDF8;
        border-radius: 22px;
        padding: 36px;
        text-align: center;
        box-shadow: 0 0 40px rgba(56, 189, 248, 0.15);
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. دوال مختبر فحص وتجهيز البيانات (Data Preparation Engine)
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

    # دس 4 استمارات عشوائية/مكررة لاختبار أداة الفحص والتنظيف الآلي
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
    for pattern in ["*.png", "*.jpg", "*.jpeg", "*.webp", "*.PNG", "*.JPG", "*.JPEG"]:
        image_files.extend(glob.glob(pattern))
    if image_files:
        try:
            with open(image_files[0], "rb") as img_f:
                st.session_state.custom_logo_b64 = base64.b64encode(img_f.read()).decode()
        except Exception:
            pass

if st.session_state.custom_logo_b64:
    b64_str = st.session_state.custom_logo_b64
    logo_html = f'<img src="data:image/png;base64,{b64_str}" style="width:70px; height:70px; border-radius:16px; object-fit:contain; background:#0F172A; border:2px solid #38BDF8; padding:4px; box-shadow:0 0 25px rgba(56,189,248,0.5);">'
    cert_logo_html = f'<img src="data:image/png;base64,{b64_str}" style="width:88px; height:88px; border-radius:18px; object-fit:contain; margin-bottom:14px; border:2px solid #38BDF8; padding:5px; background:#0F172A;"><br>'
else:
    logo_html = '<div class="brand-logo">SL</div>'
    cert_logo_html = ''


# ==========================================
# 4. الترويسة العلوية للمنصة (Top Header)
# ==========================================
st.markdown(f"""
<div class="top-navbar">
    <div class="brand-box">
        {logo_html}
        <div>
            <h1 class="brand-title">SOCIO LAB | سوسيو لاب</h1>
            <p class="brand-sub">مؤسسة ناشئة للاستشارات المنهجية والإحصائية، التدريب التطبيقي، والحلول الرقمية للبيانات</p>
        </div>
    </div>
    <div class="location-badge">📍 حضورياً بجامعة سوق أهراس | 🌐 رقمياً عبر 58 ولاية</div>
</div>
""", unsafe_allow_html=True)

with st.expander("🎨 تخصيص شعار المنصة (اضغط هنا لرفع صورة الشعار Logo من جهازك)"):
    uploaded_logo = st.file_uploader("اختر صورة شعار Socio Lab:", type=["png", "jpg", "jpeg", "webp"])
    if uploaded_logo is not None:
        st.session_state.custom_logo_b64 = base64.b64encode(uploaded_logo.getvalue()).decode()
        st.success("تم تحديث شعار المنصة بنجاح!")
        st.rerun()


# ==========================================
# 5. شريط التنقل الرئيسي الواضح للمنصة
# ==========================================
main_tabs = st.tabs([
    "🏛️ الرئيسية والفئات المستهدفة",
    "💼 خدماتنا الاستشارية والميدانية",
    "🎓 الدورات التكوينية والتدريب",
    "🔬 المختبر الرقمي لفحص وتجهيز الاستبيانات",
    "📅 بوابة حجز خدمة أو التسجيل في دورة"
])


# ==========================================
# التبويب 1: الرئيسية والفئات المستهدفة (لمن هذه المنصة؟)
# ==========================================
with main_tabs[0]:
    st.markdown("""
    <div class="hero-box">
        <h2 class="hero-title">مرحباً بك في منصة Socio Lab – شريكك العلمي والمؤسسي الموثوق</h2>
        <p class="hero-desc">
            تجمع مؤسسة <b>Socio Lab</b> بين <b>الفضاء الحضوري</b> للاستشارات المنهجية والإحصائية والتدريب بجامعة محمد الشريف مساعدية بسوق أهراس،
            و<b>المنصة الرقمية السحابية</b> الموجهة للطلبة، الباحثين، والمؤسسات في جميع ولايات الجزائر. نهدف إلى مرافقتك علمياً وتقنياً من مرحلة
            بناء الفكرة وأداة القياس إلى غاية استلام بيانات ميدانية منظفة، موثوقة، ومحللة بدقة وفق ضوابط النزاهة الأكاديمية.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">🎯 من هم المستفيدون من خدمات منصة Socio Lab؟ (الفئات المستهدفة)</div>', unsafe_allow_html=True)

    c_t1, c_t2, c_t3 = st.columns(3)

    with c_t1:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">🎓</div>
            <h3 class="card-title">1. طلبة الليسانس والماستر</h3>
            <p class="card-text">
                طلبة جامعة سوق أهراس ومختلف الجامعات الجزائرية المقبلون على إعداد مذكرات التخرج وتقارير التربص الميداني، والذين يحتاجون إلى مرافقة منهجية سليمة في تصميم الاستبيان، تفريغ البيانات، ومعالجتها دون الوقوع في أخطاء إحصائية.
            </p>
            <span class="badge-tag">مذكرات التخرج</span>
            <span class="badge-tag">تقارير التربص</span>
            <span class="badge-tag badge-green">أسعار تفضيلية للطلبة</span>
        </div>
        """, unsafe_allow_html=True)

    with c_t2:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">🔬</div>
            <h3 class="card-title">2. طلبة الدكتوراه والباحثون</h3>
            <p class="card-text">
                الباحثون الأكاديميون، الأساتذة، وأعضاء فرق ومخابر البحث العلمي (PRFU) الراغبون في تحكيم المقاييس السيكومترية، تدقيق قواعد البيانات الكبرى، وتنسيق الجداول الإحصائية لأطروحات الدكتوراه والمقالات العلمية المحكمة.
            </p>
            <span class="badge-tag">أطروحات الدكتوراه</span>
            <span class="badge-tag">مقالات ASJP / Scopus</span>
            <span class="badge-tag badge-green">تدقيق عالي الدقة</span>
        </div>
        """, unsafe_allow_html=True)

    with c_t3:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">🏢</div>
            <h3 class="card-title">3. المؤسسات، الإدارات، والجمعيات</h3>
            <p class="card-text">
                المؤسسات الاقتصادية العمومية والخاصة، الهيئات الإدارية، ومنظمات المجتمع المدني التي تحتاج إلى إنجاز دراسات ميدانية، استطلاعات رأي، قياس رضا المتعاملين، أو تحليل بيانات اجتماعية وميدانية لترشيد قراراتها.
            </p>
            <span class="badge-tag">استطلاعات الرأي</span>
            <span class="badge-tag">دراسات الأثر الاجتماعي</span>
            <span class="badge-tag badge-amber">عقود ومرافقة B2B</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">✨ لماذا تختار Socio Lab؟ (ركائز القيمة المضافة والنزاهة)</div>', unsafe_allow_html=True)
    c_v1, c_v2, c_v3, c_v4 = st.columns(4)
    with c_v1:
        st.markdown("""
        <div class="info-card">
            <h4 class="card-title">⚖️ النزاهة الأكاديمية</h4>
            <p class="card-text">نرافق الباحث علمياً وتقنياً ونشرح له خطوات التحليل وتفسير النتائج، ونرفض قاطعاً فبركة البيانات أو إنجاز البحوث نيابة عن الطالب.</p>
        </div>
        """, unsafe_allow_html=True)
    with c_v2:
        st.markdown("""
        <div class="info-card">
            <h4 class="card-title">⚡ أتمتة تجهيز البيانات</h4>
            <p class="card-text">منصة رقمية تختصر وقت تنظيف وترميز الاستبيانات وكشف الأخطاء والقيم المفقودة من عدة أيام إلى دقائق معدودة.</p>
        </div>
        """, unsafe_allow_html=True)
    with c_v3:
        st.markdown("""
        <div class="info-card">
            <h4 class="card-title">🔒 سرية وحماية البيانات</h4>
            <p class="card-text">حماية كاملة لسرية قواعد البيانات البحثية والمؤسسية وإخفاء الهوية الشخصية للمبحوثين وفق القانون الجزائري 18-07.</p>
        </div>
        """, unsafe_allow_html=True)
    with c_v4:
        st.markdown("""
        <div class="info-card">
            <h4 class="card-title">🤝 خدمة هجينة (حضوري/رقمي)</h4>
            <p class="card-text">إمكانية الاستفادة من الجلسات الاستشارية والدورات حضورياً بسوق أهراس أو عن بعد عبر المنصة في جميع ولايات الوطن.</p>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# التبويب 2: خدماتنا الاستشارية والميدانية
# ==========================================
with main_tabs[1]:
    st.markdown('<div class="section-heading">💼 قائمة الخدمات الأساسية لمؤسسة Socio Lab</div>', unsafe_allow_html=True)
    st.write("نقدم باقة متكاملة من الخدمات العلمية والتقنية المصممة لتلبية احتياجات الطلبة، الباحثين، والمؤسسات:")

    s_col1, s_col2 = st.columns(2)

    with s_col1:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">🧭</div>
            <h3 class="card-title">1. الاستشارات في منهجية البحث العلمي</h3>
            <p class="card-text">
                جلسات استشارية فردية أو جماعية لضبط إشكالية الدراسة، صياغة الفرضيات، تحديد المتغيرات والمؤشرات الإجرائية، واختيار المنهج العلمي والعينة المناسبة لطبيعة الموضوع.
            </p>
            <span class="badge-tag">حضوري / عن بعد</span>
            <span class="badge-tag badge-green">متاح للطلبة والباحثين</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-card">
            <div class="card-icon">📝</div>
            <h3 class="card-title">2. تصميم الاستبيانات وبناء أدوات جمع البيانات</h3>
            <p class="card-text">
                بناء استبيانات ورقية وإلكترونية محكمة، ضبط صياغة الفقرات والمحاور، اختيار مقاييس التقدير المناسبة، ومراجعة صدق وثبات الأداة قبل توزيعها الميداني النهائي.
            </p>
            <span class="badge-tag">تصميم وتحكيم</span>
            <span class="badge-tag badge-green">استبيانات ومقابلات</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-card">
            <div class="card-icon">🗂️</div>
            <h3 class="card-title">3. تنظيم بيانات الاستبيانات، ترميزها، ومراجعة جودتها</h3>
            <p class="card-text">
                تفريغ الاستمارات الميدانية، تحويل الإجابات النصية إلى رموز رقمية قياسية (Codage)، فحص القيم المفقودة، واستبعاد الاستمارات العشوائية أو المتناقضة لتجهيز ملف بيانات نظيف.
            </p>
            <span class="badge-tag">عبر المنصة الرقمية</span>
            <span class="badge-tag badge-green">تجهيز قبلي للتحليل</span>
        </div>
        """, unsafe_allow_html=True)

    with s_col2:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">📊</div>
            <h3 class="card-title">4. الاستشارات الإحصائية وتحليل البيانات</h3>
            <p class="card-text">
                إجراء المعالجات الإحصائية المناسبة لفرضيات البحث، استخراج الجداول والرسوم البيانية المنسقة أكاديمياً، مع عقد جلسة شرح منهجية للباحث لتوضيح قراءة المؤشرات وتفسيرها.
            </p>
            <span class="badge-tag">تحليل إحصائي دقيق</span>
            <span class="badge-tag badge-green">مرفق بمذكرة شرح</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-card">
            <div class="card-icon">🎓</div>
            <h3 class="card-title">5. المرافقة التقنية والمنهجية في مذكرات التخرج وتقارير التربص</h3>
            <p class="card-text">
                تدقيق الاتساق المنهجي بين الجانب النظري والتطبيقي، مراجعة سلامة عرض وتفسير الجداول الميدانية، وتدريب الطالب على مهارات العرض والمناقشة العلمية أمام اللجنة.
            </p>
            <span class="badge-tag">مرافقة أخلاقية نزيهة</span>
            <span class="badge-tag badge-green">ليسانس وماستر</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-card">
            <div class="card-icon">🏢</div>
            <h3 class="card-title">6. إنجاز الدراسات الميدانية والاستطلاعات للمؤسسات والجمعيات</h3>
            <p class="card-text">
                تنفيذ مسوح اجتماعية واستطلاعات رأي متكاملة لصالح المؤسسات الاقتصادية والهيئات والجمعيات، بدءاً من تصميم الاستمارة وجمع البيانات ميدانياً وصولاً إلى تقديم تقرير تحليلي وتوصيات عملية.
            </p>
            <span class="badge-tag badge-amber">خدمات المؤسسات B2B</span>
            <span class="badge-tag">تقارير استراتيجية</span>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# التبويب 3: الدورات التكوينية والتدريب
# ==========================================
with main_tabs[2]:
    st.markdown('<div class="section-heading">🎓 البرامج والدورات التكوينية التطبيقية (حضورياً وعن بعد)</div>', unsafe_allow_html=True)
    st.write("تنظم مؤسسة **Socio Lab** دورات تدريبية تطبيقية مصغرة ومكثفة موجهة للطلبة، الباحثين، وإطارات المؤسسات لتنمية المهارات المنهجية والإحصائية:")

    tr_col1, tr_col2 = st.columns(2)

    with tr_col1:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">💻</div>
            <h3 class="card-title">الدورة 1: الأساسيات التطبيقية لتحليل البيانات ببرنامج SPSS</h3>
            <p class="card-text">
                <b>الفئة المستهدفة:</b> طلبة الليسانس والماستر المبتدئون في التحليل الإحصائي.<br>
                <b>محاور الدورة:</b> إعداد قاعدة البيانات (Variable View & Data View)، ترميز الاستبيانات وإدخالها، حساب التكرارات والنسب المئوية، المتوسطات والانحراف المعياري، وتنسيق الجداول.
            </p>
            <span class="badge-tag">المدة: 12 ساعة تطبيقية</span>
            <span class="badge-tag">حضوري بسوق أهراس / عن بعد</span>
            <span class="badge-tag badge-green">شهادة مشاركة</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-card">
            <div class="card-icon">📐</div>
            <h3 class="card-title">الدورة 2: هندسة الاستبيانات الإلكترونية والورقية وبناء المقاييس</h3>
            <p class="card-text">
                <b>الفئة المستهدفة:</b> طلبة الدراسات العليا، الباحثون، وإطارات الجمعيات والمؤسسات.<br>
                <b>محاور الدورة:</b> تحويل الإشكالية والفرضيات إلى محاور وفقرات قياس، تصميم الاستبيان على Google Forms بطريقة احترافية، وتجنب الأخطاء المنهجية الشائعة في صياغة الأسئلة.
            </p>
            <span class="badge-tag">المدة: 8 ساعات تطبيقية</span>
            <span class="badge-tag">حضوري / عن بعد</span>
            <span class="badge-tag badge-green">تطبيق عملي</span>
        </div>
        """, unsafe_allow_html=True)

    with tr_col2:
        st.markdown("""
        <div class="info-card">
            <div class="card-icon">📈</div>
            <h3 class="card-title">الدورة 3: الإحصاء الاستدلالي المتقدم واختبار الفرضيات البحثية</h3>
            <p class="card-text">
                <b>الفئة المستهدفة:</b> طلبة الماستر 2، طلبة الدكتوراه، والباحثون الأكاديميون.<br>
                <b>محاور الدورة:</b> فحص الصدق والثبات، شروط اختيار الاختبارات المعلمية واللامعلمية، اختبارات الارتباط، اختبارات الفروق، تحليل الانحدار، وقراءة وتفسير النتائج علمياً.
            </p>
            <span class="badge-tag">المدة: 15 ساعة معمقة</span>
            <span class="badge-tag">حضوري / عن بعد</span>
            <span class="badge-tag badge-amber">مستوى متقدم</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-card">
            <div class="card-icon">🏛️</div>
            <h3 class="card-title">الدورة 4: منهجية إعداد البحوث والمذكرات وفق معيار IMRAD و APA</h3>
            <p class="card-text">
                <b>الفئة المستهدفة:</b> طلبة التخرج والباحثون الراغبون في النشر العلمي.<br>
                <b>محاور الدورة:</b> الهيكلة المنهجية للدراسة الميدانية وفق قالب IMRAD، التوثيق العلمي والمراجع بطريقة APA، عرض ومناقشة النتائج الميدانية، وتقنيات العرض التقديمي يوم المناقشة.
            </p>
            <span class="badge-tag">المدة: 10 ساعات</span>
            <span class="badge-tag">حضوري / عن بعد</span>
            <span class="badge-tag badge-green">تحضير للمناقشة والنشر</span>
        </div>
        """, unsafe_allow_html=True)

    st.info("💡 **للتسجيل في إحدى الدورات التكوينية:** انتقل إلى تبويب **«📅 بوابة حجز خدمة أو التسجيل في دورة»** في أعلى المنصة واختر الدورة المناسبة لك.")


# ==========================================
# التبويب 4: المختبر الرقمي لفحص وتجهيز الاستبيانات (الأداة التقنية المبتكرة)
# ==========================================
with main_tabs[3]:
    st.markdown('<div class="section-heading">🔬 المختبر الرقمي الآلي لفحص جودة الاستبيانات وتجهيزها للتحليل</div>', unsafe_allow_html=True)
    st.write("""
    تتيح لك هذه الأداة الرقمية المبتكرة رفع ملف استبيانك الخام (Excel / CSV) ليقوم النظام آلياً بـ **ترميز الإجابات النصية إلى أرقام**،
    **عكس أوزان العبارات السالبة**، **كشف الاستمارات العشوائية أو المكررة أو الناقصة**، وتصدير ملف بيانات نظيف وجاهز للتحليل الإحصائي.
    """)

    c_src1, c_src2 = st.columns([3, 1])
    with c_src1:
        uploaded_file = st.file_uploader("📂 ارفع ملف استبيانك الخام (Excel أو CSV) أو جرب الأداة على العينة المدمجة:", type=["xlsx", "csv"])
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

    lab_subtabs = st.tabs([
        "1️⃣ الترميز الآلي وعكس العبارات",
        "2️⃣ فحص جودة الاستمارات وتنظيفها",
        "3️⃣ تنزيل الملف الجاهز وتقرير الجودة"
    ])

    with lab_subtabs[0]:
        st.markdown("##### أ. معاينة البيانات النصية الخام مقابل البيانات المرمزة رقمياً:")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.caption("📄 الاستبيان النصي الخام (قبل الترميز):")
            st.dataframe(st.session_state.raw_df, use_container_width=True, height=260)
        with col_v2:
            st.caption("🔢 المصفوفة الرقمية المرمزة آلياً:")
            st.dataframe(st.session_state.working_df, use_container_width=True, height=260)

        st.markdown("##### ب. دليل ترميز المتغيرات المولد آلياً (Codebook):")
        st.dataframe(st.session_state.codebook_df, use_container_width=True)

        st.markdown("##### ج. أداة عكس أوزان العبارات السالبة (Reverse Coding):")
        default_rev = [c for c in numeric_cols if "عكسية" in c]
        rev_cols = st.multiselect("حدد العبارات السالبة في استبيانك لقلب أوزانها (5 ↔ 1):", numeric_cols, default=default_rev)
        if st.button("⚡ تطبيق عكس أوزان العبارات السالبة"):
            if not st.session_state.reversed_done and rev_cols:
                for c in rev_cols:
                    st.session_state.working_df[c] = 6 - pd.to_numeric(st.session_state.working_df[c], errors='coerce')
                st.session_state.reversed_done = True
                st.success("تم عكس أوزان العبارات السالبة بنجاح!")
                st.rerun()
            elif st.session_state.reversed_done:
                st.info("تم عكس أوزان هذه العبارات مسبقاً.")

    with lab_subtabs[1]:
        st.markdown("##### 🛡️ الفحص الآلي لجودة الاستمارات وكشف الإجابات العشوائية أو المكررة:")
        cp1, cp2 = st.columns(2)
        with cp1:
            pos_item = st.selectbox("اختر عبارة موجبة مرجعية لفحص اتساق المبحوث:", numeric_cols, index=0)
        with cp2:
            neg_idx = 3 if len(numeric_cols) > 3 else 0
            neg_item = st.selectbox("اختر العبارة المعكوسة المقابلة لها:", numeric_cols, index=neg_idx)

        raw_coded_temp, _ = auto_code_dataframe(st.session_state.raw_df)
        if st.session_state.cleaned_done:
            raw_coded_temp = raw_coded_temp.loc[st.session_state.working_df.index]

        audit_df, bad_indices = audit_survey_quality(raw_coded_temp, numeric_cols, pos_item, neg_item)

        m1, m2, m3 = st.columns(3)
        m1.metric("إجمالي الاستمارات المفحوصة", f"{len(audit_df)} استمارة")
        m2.metric("الاستمارات السليمة والمقبولة", f"{len(audit_df) - len(bad_indices)} استمارة")
        m3.metric("الاستمارات غير الصالحة المرصودة", f"{len(bad_indices)} استمارات")

        st.dataframe(audit_df.sort_values(by="القرار المنهجي", ascending=False), use_container_width=True, height=300)

        if len(bad_indices) > 0:
            st.warning(f"تم اكتشاف {len(bad_indices)} استمارات تحتوي على إجابات عشوائية مكررة أو متناقضة.")
            if st.button("🧹 استبعاد الاستمارات غير الصالحة وتنظيف قاعدة البيانات"):
                st.session_state.working_df = st.session_state.working_df.drop(index=bad_indices)
                st.session_state.cleaned_done = True
                st.success("تم تنظيف قاعدة البيانات بنجاح وأصبحت جاهزة تماماً للتحليل!")
                st.rerun()
        else:
            st.success("✅ جميع الاستمارات في قاعدة البيانات الحالية سليمة ومتسقة بنسبة 100%.")

    with lab_subtabs[2]:
        st.markdown("##### 📥 تنزيل ملفات البيانات المنظفة والمرمزة:")
        d1, d2, d3 = st.columns(3)

        csv_bytes = st.session_state.working_df.to_csv(index=False).encode('utf-8-sig')
        with d1:
            st.download_button("📥 تنزيل ملف البيانات المرمز (Excel / CSV)", data=csv_bytes, file_name="SocioLab_Cleaned_Data.csv", mime="text/csv")

        codebook_bytes = st.session_state.codebook_df.to_csv(index=False).encode('utf-8-sig')
        with d2:
            st.download_button("📘 تنزيل دليل الترميز (Codebook)", data=codebook_bytes, file_name="SocioLab_Codebook.csv", mime="text/csv")

        with d3:
            if HAS_PYREADSTAT:
                sav_path = "SocioLab_Ready.sav"
                spss_df = st.session_state.working_df.copy()
                for c in spss_df.columns:
                    if c != "رمز_الاستمارة":
                        spss_df[c] = pd.to_numeric(spss_df[c], errors='coerce')
                    else:
                        spss_df[c] = spss_df[c].astype(str)
                clean_cols = {col: f"Q_{i+1}" for i, col in enumerate(spss_df.columns)}
                col_labels = {f"Q_{i+1}": col for i, col in enumerate(spss_df.columns)}
                spss_df = spss_df.rename(columns=clean_cols)
                pyreadstat.write_sav(spss_df, sav_path, column_labels=col_labels)
                with open(sav_path, "rb") as f:
                    st.download_button("📊 تنزيل ملف جاهز لبرنامج التحليل (.sav)", data=f, file_name="SocioLab_Ready_Data.sav", mime="application/octet-stream")

        today_str = datetime.date.today().strftime("%Y-%m-%d")
        cert_id = f"SL-DZ-{datetime.datetime.now().strftime('%Y%m')}-060"

        st.markdown(f"""
        <div class="holo-cert">
            {cert_logo_html}
            <span class="badge-tag badge-green" style="font-size:0.9rem; padding:6px 18px;">★ تقرير فحص وجودة البيانات الميدانية ★</span>
            <h3 style="color:#FFFFFF; margin-top:14px; margin-bottom:8px;">شهادة مراجعة وتجهيز قاعدة البيانات البحثية</h3>
            <p style="font-size:1.02rem; color:#E2E8F0 !important; line-height:1.9; max-width:85%; margin:0 auto;">
                تمت معالجة ومراجعة ملف البيانات عبر المنصة الرقمية لمؤسسة <b>Socio Lab</b>، وشملت المراجعة: توحيد الترميز الرقمي للمتغيرات،
                فحص القيم المفقودة، والتأكد من خلو الاستمارات المعتمدة من التطابق المكرر أو الإجابات النمطية الجامدة.
                إجمالي الاستمارات الصافية الجاهزة للتحليل: (<b>N = {len(df_current)} استمارة</b>).
            </p>
            <div style="display:flex; justify-content:space-around; margin-top:24px; padding-top:16px; border-top:1px dashed rgba(148, 163, 184, 0.3); color:#7DD3FC; font-weight:600;">
                <div>🔖 رقم المرجع: {cert_id}</div>
                <div>📅 التاريخ: {today_str}</div>
                <div>🏛️ مؤسسة Socio Lab - سوق أهراس</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# التبويب 5: بوابة حجز خدمة أو التسجيل في دورة
# ==========================================
with main_tabs[4]:
    st.markdown('<div class="section-heading">📅 بوابة طلب استشارة، دراسة ميدانية، أو التسجيل في دورة تكوينية</div>', unsafe_allow_html=True)
    st.write("يرجى ملء الاستمارة أدناه وتحديد فئتك ونوع الخدمة أو الدورة المطلوبة، وسيتواصل معك فريق **Socio Lab** لتأكيد الموعد (حضورياً بجامعة سوق أهراس أو عن بعد):")

    with st.form("booking_form"):
        cf1, cf2 = st.columns(2)
        with cf1:
            client_name = st.text_input("👤 الاسم واللقب الكامل (أو اسم المؤسسة/الجمعية):")
            client_category = st.selectbox("🎯 الفئة المستفيدة:", [
                "طالب جامعي (ليسانس / ماستر) - جامعة سوق أهراس",
                "طالب جامعي (ليسانس / ماستر) - جامعة جزائرية أخرى",
                "طالب دكتوراه / أستاذ باحث / فرقة بحث",
                "مؤسسة اقتصادية / إدارة عمومية / جمعية"
            ])
            client_uni = st.text_input("🏛️ الكلية / الجامعة / اسم الهيئة:")
        with cf2:
            service_req = st.selectbox("💼 الخدمة أو الدورة المطلوبة:", [
                "استشارة في منهجية البحث العلمي وضبط الإشكالية",
                "تصميم استبيان وبناء أداة جمع البيانات وتحكيمها",
                "تنظيم بيانات الاستبيان، ترميزها، وتحليلها إحصائياً",
                "المرافقة المنهجية والتقنية في مذكرة التخرج أو تقرير التربص",
                "التسجيل في دورة تكوينية: أساسيات التحليل الإحصائي ببرنامج SPSS",
                "التسجيل في دورة تكوينية: هندسة الاستبيانات وبناء المقاييس",
                "التسجيل في دورة تكوينية: الإحصاء المتقدم واختبار الفرضيات",
                "التسجيل في دورة تكوينية: منهجية إعداد البحوث وفق IMRAD و APA",
                "طلب إنجاز دراسة ميدانية أو استطلاع رأي مؤسسي (B2B)"
            ])
            mode_req = st.radio("📍 طريقة الاستفادة المفضلة:", [
                "حضورياً (مقر Socio Lab - جامعة سوق أهراس)",
                "عن بعد (عبر المنصة الرقمية - متاح لجميع الولايات)"
            ])
            client_phone = st.text_input("📱 رقم الهاتف أو البريد الإلكتروني للتواصل:")

        notes = st.text_area("📝 تفاصيل إضافية حول موضوع بحثك أو احتياجك التدريبي / الميداني:")
        submitted = st.form_submit_button("✅ إرسال الطلب وتأكيد الحجز")
        if submitted:
            if client_name and client_phone:
                st.success(f"شكراً لك ({client_name})! تم تسجيل طلبك بخصوص ({service_req}) ضمن فئة ({client_category}) بنجاح. سنتواصل معك خلال 24 ساعة.")
            else:
                st.warning("يرجى إدخال الاسم ورقم الهاتف أو البريد الإلكتروني لتأكيد الطلب.")
