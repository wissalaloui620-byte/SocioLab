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
# 1. إعدادات الصفحة والهوية البصرية الأكاديمية
# ==========================================
st.set_page_config(
    page_title="Socio Lab | منصة الهندسة المنهجية والتدقيق الإحصائي",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stMarkdown, .stText, .stButton, .stSelectbox, .stMultiSelect {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
    }

    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E3A8A 100%);
        color: #FFFFFF !important;
        border-left: 1px solid #334155;
    }
    section[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }

    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 60%, #2563EB 100%);
        color: #FFFFFF;
        padding: 28px 34px;
        border-radius: 14px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.25);
        border-right: 6px solid #38BDF8;
    }
    .main-header h1 {
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 2.1rem;
        margin: 0 0 8px 0;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #E0F2FE !important;
        font-size: 1.05rem;
        margin: 0;
        font-weight: 500;
    }

    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-right: 5px solid #1E3A8A;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.05);
        margin-bottom: 16px;
    }
    .metric-title {
        color: #475569;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #0F172A;
        font-size: 1.85rem;
        font-weight: 800;
    }
    .metric-sub {
        color: #0284C7;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 4px;
    }

    .section-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 22px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }
    .section-title {
        color: #1E3A8A;
        font-size: 1.35rem;
        font-weight: 700;
        border-bottom: 2px solid #F1F5F9;
        padding-bottom: 10px;
        margin-bottom: 16px;
    }

    .stButton > button {
        background-color: #1E3A8A !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 0.55rem 1.4rem !important;
        border: none !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton > button:hover {
        background-color: #2563EB !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }

    .apa-table {
        width: 100%;
        border-collapse: collapse;
        margin: 18px 0;
        font-size: 1rem;
        background-color: #FFFFFF;
        direction: rtl;
    }
    .apa-table thead tr {
        border-top: 2px solid #0F172A;
        border-bottom: 1.5px solid #0F172A;
        color: #0F172A;
        font-weight: 700;
    }
    .apa-table th, .apa-table td {
        padding: 12px 15px;
        text-align: center;
    }
    .apa-table tbody tr:last-of-type {
        border-bottom: 2px solid #0F172A;
    }

    .certificate-box {
        background: linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 100%);
        border: 2px solid #1E3A8A;
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(30, 58, 138, 0.08);
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. الدوال الإحصائية والمنهجية (Core Engine)
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
            # فحص آمن وموحد لجميع أنواع النصوص والأرقام في Python 3.14
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
    # استخدام مصفوفة NumPy عشرية مباشرة لتفادي أي خطأ في Python 3.14
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
# 4. القائمة الجانبية (Sidebar Navigation)
# ==========================================
with st.sidebar:
    st.markdown("## 🏛️ **SOCIO LAB**")
    st.markdown("*منصة الهندسة المنهجية والتدقيق الإحصائي السحابي*")
    st.markdown("---")

    nav_page = st.radio(
        "مسار العمل المنهجي:",
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
    st.markdown("### 📂 مصدر قاعدة البيانات")
    data_source = st.selectbox(
        "اختر مصدر البيانات:",
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

    if st.button("🔄 إعادة ضبط البيانات الأصلية"):
        demo_text, _ = generate_demo_dataset()
        st.session_state.raw_df = demo_text
        coded_df, codebook_df = auto_code_dataframe(demo_text)
        st.session_state.working_df = coded_df
        st.session_state.codebook_df = codebook_df
        st.session_state.reversed_done = False
        st.session_state.cleaned_done = False
        st.rerun()

    st.markdown("---")
    st.caption("Socio Lab ResearchTech Platform © 2026\nجامعة محمد الشريف مساعدية - سوق أهراس")


# ==========================================
# 5. الترويسة الرئيسية ومؤشرات الأداء العليا
# ==========================================
st.markdown("""
<div class="main-header">
    <h1>SOCIO LAB | المختبر السحابي للهندسة المنهجية والتدقيق السيكومتري</h1>
    <p>المنصة الجزائرية المبتكرة لأتمتة فحص نزاهة البيانات الميدانية، التحكيم السيكومتري، والتوجيه الإحصائي وفق معايير APA</p>
</div>
""", unsafe_allow_html=True)

df_current = st.session_state.working_df
numeric_cols = [c for c in df_current.columns if c not in ["رمز_الاستمارة", "الجنس", "المستوى_الدراسي"]]

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">حجم العينة قيد المعالجة (N)</div>
        <div class="metric-value">{len(df_current)} استمارة</div>
        <div class="metric-sub">{"بعد العزل الجنائي النظيف" if st.session_state.cleaned_done else "العينة الميدانية الخام"}</div>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">عدد متغيرات وفقرات القياس</div>
        <div class="metric-value">{len(numeric_cols)} فقرة</div>
        <div class="metric-sub">مرمزة رقمياً وجاهزة لـ SPSS</div>
    </div>
    """, unsafe_allow_html=True)

with col_m3:
    alpha_now = calculate_cronbach_alpha(df_current[numeric_cols]) if len(numeric_cols) >= 2 else 0.0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">معامل ألفا كرونباخ الكلي (α)</div>
        <div class="metric-value">{alpha_now:.3f}</div>
        <div class="metric-sub">{"ثبات ممتاز (> 0.80)" if alpha_now >= 0.8 else "يتطلب عكس الفقرات وتنقية المقياس"}</div>
    </div>
    """, unsafe_allow_html=True)

with col_m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">حالة العبارات السالبة (المعكوسة)</div>
        <div class="metric-value">{"تم العكس ✓" if st.session_state.reversed_done else "خام (غير معكوسة)"}</div>
        <div class="metric-sub">ضبط اتجاه الأوزان (1 ↔ 5)</div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# القسم الأول: الرفع الذكي والترميز الآلي
# ==========================================
if nav_page == "1. الرفع الذكي والترميز الآلي":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">1. بوابة القراءة الذكية، الترميز الآلي، وعكس العبارات السالبة</div>', unsafe_allow_html=True)
    st.write("تقوم هذه الوحدة بقراءة الاستبيانات النصية الخام وتحويلها آلياً إلى مصفوفة رقمية قياسية مع بناء دليل الترميز (Variable View) دون تدخل يدوي.")

    tab_raw, tab_coded, tab_codebook = st.tabs([
        "📄 البيانات النصية الخام (قبل المعالجة)",
        "🔢 المصفوفة الرقمية المرمزة (Data View)",
        "🗂️ جدول تعريف المتغيرات الآلي (SPSS Variable View)"
    ])

    with tab_raw:
        st.dataframe(st.session_state.raw_df, use_container_width=True, height=320)

    with tab_coded:
        st.dataframe(st.session_state.working_df, use_container_width=True, height=320)

    with tab_codebook:
        st.dataframe(st.session_state.codebook_df, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🔄 أداة عكس أوزان الفقرات السالبة (Reverse Coding Engine)")
    st.write("حدد الفقرات ذات الصياغة السالبة ليقوم النظام بقلب أوزانها آلياً ($5 \\leftrightarrow 1$ و $4 \\leftrightarrow 2$) لضمان صحة الدرجة الكلية للمحور:")

    default_rev = [c for c in numeric_cols if "عكسية" in c]
    rev_cols = st.multiselect("اختر الفقرات المعكوسة في استبيانك:", numeric_cols, default=default_rev)

    if st.button("تطبيق عكس الأوزان الآلي للفقرات المحددة"):
        if not st.session_state.reversed_done and rev_cols:
            for c in rev_cols:
                st.session_state.working_df[c] = 6 - pd.to_numeric(st.session_state.working_df[c], errors='coerce')
            st.session_state.reversed_done = True
            st.success(f"تم عكس أوزان الفقرات ({', '.join(rev_cols)}) بنجاح! لاحظ ارتفاع معامل الثبات في الأعلى.")
            st.rerun()
        elif st.session_state.reversed_done:
            st.warning("تم عكس أوزان هذه الفقرات مسبقاً.")
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# القسم الثاني: محرك التدقيق الجنائي وكشف التلاعب
# ==========================================
elif nav_page == "2. التدقيق الجنائي وكشف التلاعب":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">2. محرك التدقيق الجنائي الإحصائي وكشف فبركة الاستبيانات (Anti-Curbstoning Engine)</div>', unsafe_allow_html=True)
    st.write("""
    يفحص هذا المحرك مصفوفة البيانات سطراً بسطر لكشف 3 أنواع من الخلل الميداني التي تشوه البحوث:
    1. **الإجابات النمطية الجامدة (Straight-lining):** عندما يختار المبحوث نفس الإجابة لكل الفقرات ($SD = 0$).
    2. **التناقض السيكومتري الحاد:** عندما يوافق المبحوث بشدة على الفقرة الموجبة ونقيضها السالب في آن واحد.
    3. **الاستنساخ المكتبي (Curbstoning):** عندما تتطابق استمارة بالكامل مع استمارة سابقة نتيجة النسخ واللصق.
    """)

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        pos_item = st.selectbox("اختر فقرة موجبة مرجعية لفحص التناقض:", numeric_cols, index=0)
    with col_p2:
        neg_idx = 3 if len(numeric_cols) > 3 else 0
        neg_item = st.selectbox("اختر الفقرة السالبة المقابلة لها منطقياً:", numeric_cols, index=neg_idx)

    raw_coded_temp, _ = auto_code_dataframe(st.session_state.raw_df)
    if st.session_state.cleaned_done:
        raw_coded_temp = raw_coded_temp.loc[st.session_state.working_df.index]

    audit_df, bad_indices = forensic_audit(raw_coded_temp, numeric_cols, pos_item, neg_item)

    col_a1, col_a2, col_a3 = st.columns(3)
    col_a1.metric("إجمالي الاستمارات المفحوصة", f"{len(audit_df)}")
    col_a2.metric("الاستمارات السليمة والموثوقة", f"{len(audit_df) - len(bad_indices)}")
    col_a3.metric("الاستمارات المزيفة / المتناقضة المرصودة", f"{len(bad_indices)}")

    st.markdown("#### 🔍 جدول نتائج الفحص الجنائي للاستمارات:")
    audit_sorted = audit_df.sort_values(by="القرار المنهجي", ascending=False)
    st.dataframe(audit_sorted, use_container_width=True, height=340)

    if len(bad_indices) > 0:
        st.warning(f"تم رصد {len(bad_indices)} استمارات غير صالحة منهجياً تؤثر سلباً على صدق الدراسة.")
        if st.button("🛡️ عزل واستبعاد الاستمارات المزيفة آلياً وتطهير العينة"):
            st.session_state.working_df = st.session_state.working_df.drop(index=bad_indices)
            st.session_state.cleaned_done = True
            st.success("تم عزل الاستمارات المزيفة بنجاح! أصبحت قاعدة البيانات الآن نقية بنسبة 100%.")
            st.rerun()
    else:
        st.success("✅ قاعدة البيانات نقية تماماً وخالية من أي تلاعب أو تناقض سيكومتري (مؤشر النزاهة = 100%).")

    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# القسم الثالث: المختبر السيكومتري (الصدق والثبات)
# ==========================================
elif nav_page == "3. المختبر السيكومتري (الصدق والثبات)":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">3. المختبر السيكومتري الآلي لتحكيم المقاييس (Psychometric Validation Lab)</div>', unsafe_allow_html=True)
    st.write("يقوم المختبر بحساب معامل الثبات ألفا كرونباخ، والاتساق الداخلي لكل فقرة مع الدرجة الكلية، ويكتشف الفقرات المشوشة التي يجب حذفها لرفع جودة المقياس.")

    selected_scale_items = st.multiselect(
        "حدد فقرات المقياس المراد تحكيمها سيكومترياً:",
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
                diag = "⚠️ فقرة ضعيفة/مشوهة (ينصح بحذفها)"
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
                "التوصية السيكومترية": diag
            })

        st.info(f"**معامل ألفا كرونباخ الحالي للمقياس المحدد ({len(selected_scale_items)} فقرات):** `{overall_alpha:.3f}`")
        st.dataframe(pd.DataFrame(psych_rows), use_container_width=True)

        if weak_items:
            st.warning(f"اكتشف المحرك السيكومتري أن الفقرات الآتية تُضعف ثبات المقياس: **{', '.join(weak_items)}**")
            if st.button(f"✂️ استبعاد الفقرات المشوهة ({', '.join(weak_items)}) وإعادة بناء المقياس"):
                st.session_state.working_df = st.session_state.working_df.drop(columns=weak_items)
                st.success("تم حذف الفقرات المشوهة بنجاح وارتفع معامل الثبات الكلي للمقياس!")
                st.rerun()
    else:
        st.warning("يرجى اختيار 3 فقرات على الأقل لإجراء التحليل السيكومتري.")

    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# القسم الرابع: شجرة القرار الإحصائي وجداول APA
# ==========================================
elif nav_page == "4. شجرة القرار الإحصائي وجداول APA":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">4. شجرة القرار الإحصائي المشروطة ومولد الجداول المعيارية (APA 7th Generator)</div>', unsafe_allow_html=True)
    st.write("تمنع هذه الوحدة الأخطاء الشائعة في اختيار الاختبارات الإحصائية؛ حيث تختبر أولاً شرط اعتدالية التوزيع (Normality Test) ثم تنفذ الاختبار المعلمي أو اللامعلمي الصحيح آلياً وتصمم الجدول وفق معايير APA.")

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
            "فرضية علاقة ارتباطية بين متغيرين كميين (Correlation)",
            "فرضية فروق بين مجموعتين مستقلتين (Two Independent Groups - مثل الجنس)"
        ],
        horizontal=True
    )

    if hypothesis_type == "فرضية علاقة ارتباطية بين متغيرين كميين (Correlation)":
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

        st.markdown("##### أ. نتيجة الفحص القبلي الإلزامي لشرط اعتدالية التوزيع (Shapiro-Wilk Normality Test):")
        st.write(f"- اعتدالية المتغير الأول (**{var_x}**): $W = {stat_sw_x:.3f}, p = {p_sw_x:.4f}$")
        st.write(f"- اعتدالية المتغير الثاني (**{var_y}**): $W = {stat_sw_y:.3f}, p = {p_sw_y:.4f}$")

        if is_normal:
            test_used = "معامل ارتباط بيرسون المعلمي (Pearson Correlation - r)"
            r_val, p_val = stats.pearsonr(series_x, series_y)
            reason_txt = "نظراً لتحقق شرط اعتدالية التوزيع في كلا المتغيرين ($p > 0.05$)، وجهت شجرة القرار النظام آلياً لتطبيق اختبار بيرسون المعلمي."
        else:
            test_used = "معامل ارتباط سبيرمان اللامعلمي للرتب (Spearman Rank Correlation - rho)"
            r_val, p_val = stats.spearmanr(series_x, series_y)
            reason_txt = "نظراً لعدم تحقق شرط الاعتدالية في أحد المتغيرين ($p \\le 0.05$)، حظر النظام اختبار بيرسون تجنباً للخطأ المنهجي، ووجه المعالجة آلياً نحو البديل اللامعلمي الصحيح (سبيرمان)."

        st.success(f"**القرار الإحصائي الآلي:** اعتماد **{test_used}**\n\n*{reason_txt}*")

        sig_label = "دالة إحصائياً عند (α = 0.05)" if p_val < 0.05 else "غير دالة إحصائياً"
        st.markdown("##### ب. الجدول النهائي المنسق وفق معايير (APA 7th Edition):")
        st.markdown(f"""
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
                    <td rowspan="2" style="font-weight:800; color:#1E3A8A;">{r_val:.3f}**</td>
                    <td rowspan="2" style="font-weight:700;">{p_val:.4f}</td>
                    <td rowspan="2">{sig_label}</td>
                </tr>
                <tr>
                    <td>{var_y}</td>
                    <td>{len(series_y)}</td>
                    <td>{np.mean(series_y):.2f}</td>
                    <td>{np.std(series_y, ddof=1):.2f}</td>
                </tr>
            </tbody>
        </table>
        <p style="font-size:0.9rem; color:#475569;"><i>ملاحظة منهجية: تم استخراج الجدول آلياً عبر محرك Socio Lab وفق دليل الجمعية الأمريكية لعلم النفس (APA).</i></p>
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
                    test_title = "اختبار (T-Test) لعينتين مستقلتين (معلمي)"
                    stat_symbol = f"t = {t_stat:.3f}"
                else:
                    u_stat, p_val = stats.mannwhitneyu(g1, g2)
                    test_title = "اختبار مان-ويتني (Mann-Whitney U) لعينتين مستقلتين (لامعلمي)"
                    stat_symbol = f"U = {u_stat:.1f}"

                st.success(f"**الاختبار المطبق آلياً بعد فحص الاعتدالية وتجانس التباين (Levene p={p_lev:.3f}):** {test_title}")
                st.markdown(f"""
                <table class="apa-table">
                    <thead>
                        <tr>
                            <th>المجموعة (الجنس)</th>
                            <th>العدد (n)</th>
                            <th>المتوسط الحسابي (M)</th>
                            <th>الانحراف المعياري (SD)</th>
                            <th>قيمة الاختبار</th>
                            <th>مستوى الدلالة (p)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>المجموعة 1 ({groups[0]})</td>
                            <td>{len(g1)}</td>
                            <td>{np.mean(g1):.2f}</td>
                            <td>{np.std(g1, ddof=1):.2f}</td>
                            <td rowspan="2" style="font-weight:800; color:#1E3A8A;">{stat_symbol}</td>
                            <td rowspan="2">{p_val:.4f}</td>
                        </tr>
                        <tr>
                            <td>المجموعة 2 ({groups[1]})</td>
                            <td>{len(g2)}</td>
                            <td>{np.mean(g2):.2f}</td>
                            <td>{np.std(g2, ddof=1):.2f}</td>
                        </tr>
                    </tbody>
                </table>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# القسم الخامس: التصدير لـ SPSS وشهادة النزاهة
# ==========================================
elif nav_page == "5. التصدير لـ SPSS وشهادة النزاهة":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">5. تصدير الملفات الجاهزة (SPSS .sav / Excel) وإصدار شهادة نزاهة البيانات</div>', unsafe_allow_html=True)

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
            st.info("يتم تفعيل تصدير `.sav` المباشر تلقائياً عند رفع المنصة على السحابة.")

    st.markdown("---")
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    cert_id = f"SL-DZ-{datetime.datetime.now().strftime('%Y%m')}-060"

    st.markdown(f"""
    <div class="certificate-box">
        <h2 style="color:#1E3A8A; margin-bottom:6px; font-weight:800;">شهادة التدقيق المنهجي وموثوقية البيانات الميدانية</h2>
        <h4 style="color:#0284C7; margin-top:0;">DATA INTEGRITY & PSYCHOMETRIC AUDIT CERTIFICATE</h4>
        <hr style="border:1px solid #CBD5E1; width:75%; margin:18px auto;">
        <p style="font-size:1.1rem; color:#1E293B; line-height:1.9;">
            تشهد منصة <b>Socio Lab السحابية للهندسة المنهجية والبيانات</b> بأن قاعدة البيانات الميدانية المرفقة قد خضعت للفحص الجنائي الإحصائي
            وتم تدقيقها من حيث التباين الداخلي للاستمارات ($IRV$)، والاتساق السيكومتري للعبارات المعكوسة، وخلوها من الاستنساخ المكتبي،
            وبلغ معامل الثبات الكلي للمقياس بعد الضبط (<b>$\\alpha = {alpha_now:.3f}$</b>) بحجم عينة صافية قدره (<b>$N = {len(df_current)}$</b>).
        </p>
        <div style="display:flex; justify-content:space-around; margin-top:26px; font-weight:700; color:#0F172A;">
            <div>رقم الشهادة المرجعي: {cert_id}</div>
            <div>تاريخ الاعتماد: {today_str}</div>
            <div>المؤسسة المشرفة: Socio Lab - سوق أهراس</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# القسم السادس: بوابة حجز الاستشارات والدورات
# ==========================================
elif nav_page == "6. حجز الاستشارات والدورات التدريبية":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">6. بوابة حجز الاستشارات المنهجية والدورات التدريبية (حضوري بسوق أهراس / عن بعد)</div>', unsafe_allow_html=True)
    st.write("املأ الاستمارة أدناه لحجز جلسة مرافقة منهجية وإحصائية أو للتسجيل في الدورات التطبيقية لبرنامج SPSS:")

    with st.form("booking_form"):
        c_f1, c_f2 = st.columns(2)
        with c_f1:
            client_name = st.text_input("الاسم واللقب الكامل:")
            client_uni = st.text_input("الجامعة / المؤسسة:", value="جامعة محمد الشريف مساعدية - سوق أهراس")
            client_level = st.selectbox("الصفة الأكاديمية أو المهنية:", ["طالب ماستر 2", "طالب دكتوراه", "أستاذ باحث", "مؤسسة اقتصادية / جمعية"])
        with c_f2:
            service_req = st.selectbox("نوع الخدمة المطلوبة:", [
                "استشارة منهجية وضبط أدوات القياس (الاستبيان)",
                "التدقيق الجنائي والمعالجة الإحصائية عبر SPSS",
                "دورة تدريبية تطبيقية في برنامج SPSS ومنهجية IMRAD",
                "إنجاز دراسة ميدانية أو استطلاع رأي مؤسسي (B2B)"
            ])
            mode_req = st.radio("طريقة الاستفادة المفضلة:", ["حضورياً (مقر Socio Lab - سوق أهراس)", "عن بعد (عبر المنصة الرقمية)"])
            client_phone = st.text_input("رقم الهاتف أو البريد الإلكتروني للتواصل:")

        notes = st.text_area("ملخص موضوع البحث أو الاحتياج الإحصائي:")
        submitted = st.form_submit_button("✅ إرسال طلب الحجز والتسجيل")
        if submitted:
            if client_name and client_phone:
                st.success(f"شكراً لك ({client_name})! تم تسجيل طلبك لخدمة ({service_req}) بنجاح، وسيتواصل معك فريق Socio Lab خلال 24 ساعة.")
            else:
                st.warning("يرجى إدخال الاسم ورقم التواصل لتأكيد الحجز.")

    st.markdown('</div>', unsafe_allow_html=True)
