import streamlit as st
import pandas as pd
import numpy as np
import math, datetime, base64, glob

# ==========================================
# 1. إعدادات الصفحة والأيقونة الإحصائية
# ==========================================
st.set_page_config(
    page_title="Socio Lab | Analytics & Methodology",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lobster&family=Readex+Pro:wght@300;400;500;600;700&display=swap');

/* فرض الاتجاه من اليمين إلى اليسار وتوحيد الخطوط */
html, body, [class*="css"], .stApp, .stMarkdown, .stText, .stButton, .stSelectbox, .stMultiSelect, .stRadio, .stCheckbox, input, textarea {
    font-family: 'Readex Pro', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}

#MainMenu, footer { visibility: hidden; }
header { background: transparent !important; }

/* خلفية كحلية متدرجة فاخرة */
.stApp {
    background: radial-gradient(circle at 12% 12%, #0F294A 0%, #061529 52%, #020813 100%) !important;
    color: #E2E8F0 !important;
}

/* مقاسات خطوط احترافية ومدمجة للحاسوب */
h1 { font-size: 1.55rem !important; font-weight: 700 !important; color: #F8FAFC !important; }
h2 { font-size: 1.3rem !important; font-weight: 700 !important; color: #F8FAFC !important; }
h3 { font-size: 1.08rem !important; font-weight: 600 !important; color: #F8FAFC !important; }
h4 { font-size: 0.98rem !important; font-weight: 600 !important; color: #F8FAFC !important; }
p, label, li, .stMarkdown { font-size: 0.88rem !important; line-height: 1.65 !important; color: #CBD5E1 !important; }

/* صناديق التنبيه */
div[data-testid="stAlert"] {
    background: rgba(10, 32, 64, 0.95) !important;
    border: 1px solid rgba(56, 189, 248, 0.4) !important;
    border-right: 4px solid #14B8A6 !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
}
div[data-testid="stAlert"] * { color: #F1F5F9 !important; font-size: 0.86rem !important; }

/* الترويسة العلوية المتناسقة */
.top-navbar {
    background: linear-gradient(135deg, rgba(12, 34, 64, 0.92) 0%, rgba(17, 24, 39, 0.95) 100%);
    border: 1px solid rgba(56, 189, 248, 0.28);
    border-radius: 16px;
    padding: 14px 24px;
    margin-bottom: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.6);
}
.brand-box {
    display: flex;
    align-items: center;
    gap: 14px;
}
.stat-icon-box {
    width: 52px;
    height: 52px;
    border-radius: 14px;
    background: linear-gradient(135deg, #0284C7 0%, #14B8A6 55%, #6366F1 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 18px rgba(20, 184, 166, 0.45);
    flex-shrink: 0;
}
.brand-title {
    font-family: 'Lobster', cursive !important;
    font-size: 2.05rem !important;
    font-weight: 400 !important;
    direction: ltr !important;
    display: inline-block;
    background: linear-gradient(90deg, #FFFFFF 10%, #7DD3FC 55%, #5EEAD4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 !important;
    line-height: 1.15 !important;
}
.brand-sub {
    color: #94A3B8 !important;
    font-size: 0.82rem !important;
    margin: 3px 0 0 0 !important;
}
.loc-badge {
    background: linear-gradient(135deg, rgba(20, 184, 166, 0.16), rgba(99, 102, 241, 0.16));
    border: 1px solid rgba(94, 234, 212, 0.35);
    color: #5EEAD4 !important;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 0.78rem !important;
    font-weight: 600;
}

/* البانر الترحيبي المدمج */
.hero-box {
    background: linear-gradient(135deg, rgba(15, 44, 82, 0.75) 0%, rgba(23, 27, 66, 0.85) 100%);
    border: 1px solid rgba(99, 102, 241, 0.32);
    border-right: 4px solid #14B8A6;
    border-radius: 16px;
    padding: 22px 26px;
    margin-bottom: 20px;
}
.hero-headline {
    font-size: 1.32rem !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    margin: 0 0 8px 0 !important;
}
.hero-text {
    font-size: 0.9rem !important;
    color: #CBD5E1 !important;
    line-height: 1.75 !important;
    margin: 0 !important;
}

/* البطاقات الملونة بتناسق احترافي */
.info-card {
    background: linear-gradient(155deg, rgba(15, 35, 65, 0.82) 0%, rgba(9, 20, 40, 0.94) 100%);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-top: 3px solid #0EA5E9;
    border-radius: 14px;
    padding: 18px;
    height: 100%;
    margin-bottom: 14px;
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.info-card:hover {
    transform: translateY(-3px);
    border-color: #5EEAD4;
}
.card-teal { border-top-color: #14B8A6 !important; }
.card-indigo { border-top-color: #818CF8 !important; }
.card-amber { border-top-color: #F59E0B !important; }

.card-title {
    font-size: 1.02rem !important;
    font-weight: 700 !important;
    color: #F8FAFC !important;
    margin: 0 0 8px 0 !important;
}
.card-text {
    font-size: 0.85rem !important;
    color: #CBD5E1 !important;
    line-height: 1.65 !important;
    margin: 0 0 8px 0 !important;
}
.out-box {
    background: rgba(20, 184, 166, 0.12);
    border-right: 3px solid #14B8A6;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 0.8rem !important;
    color: #5EEAD4 !important;
    margin-top: 8px;
}

/* الشارات الملونة */
.tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.72rem !important;
    font-weight: 600;
    background: rgba(14, 165, 233, 0.16);
    color: #7DD3FC !important;
    border: 1px solid rgba(14, 165, 233, 0.32);
    margin: 4px 0 0 4px;
}
.tag-teal { background: rgba(20, 184, 166, 0.16); color: #5EEAD4 !important; border-color: rgba(20, 184, 166, 0.35); }
.tag-indigo { background: rgba(129, 140, 248, 0.16); color: #C7D2FE !important; border-color: rgba(129, 140, 248, 0.35); }
.tag-amber { background: rgba(245, 158, 11, 0.16); color: #FCD34D !important; border-color: rgba(245, 158, 11, 0.35); }

/* عناوين الأقسام */
.sec-head {
    font-size: 1.14rem !important;
    font-weight: 700 !important;
    color: #5EEAD4 !important;
    margin: 18px 0 12px 0 !important;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(94, 234, 212, 0.22);
}

/* بانر الدعوة لاتخاذ إجراء */
.cta-banner {
    background: linear-gradient(135deg, rgba(20, 184, 166, 0.2), rgba(79, 70, 229, 0.25));
    border: 1px solid rgba(94, 234, 212, 0.4);
    border-right: 4px solid #14B8A6;
    border-radius: 12px;
    padding: 14px 20px;
    margin-top: 16px;
    font-size: 0.88rem !important;
}

/* شريط التبويبات */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: rgba(8, 22, 44, 0.92);
    padding: 6px;
    border-radius: 12px;
    border: 1px solid rgba(56, 189, 248, 0.22);
    flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    padding: 7px 13px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    color: #94A3B8 !important;
    background: transparent !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0284C7 0%, #14B8A6 100%) !important;
    color: #FFFFFF !important;
}

/* الأزرار */
.stButton > button {
    background: linear-gradient(135deg, #0284C7 0%, #14B8A6 100%) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    border-radius: 9px !important;
    padding: 0.45rem 1.2rem !important;
    border: none !important;
}

/* ==========================================
   تجاوب دقيق لشاشات الهواتف (Mobile Responsive)
   ========================================== */
@media only screen and (max-width: 768px) {
    .top-navbar {
        padding: 12px 14px !important;
        flex-direction: column !important;
        align-items: flex-start !important;
    }
    .stat-icon-box {
        width: 42px !important;
        height: 42px !important;
    }
    .brand-title {
        font-size: 1.55rem !important;
    }
    .brand-sub {
        font-size: 0.74rem !important;
        line-height: 1.45 !important;
    }
    .loc-badge {
        font-size: 0.72rem !important;
        padding: 5px 10px !important;
    }
    .hero-box {
        padding: 16px 16px !important;
    }
    .hero-headline {
        font-size: 1.05rem !important;
        line-height: 1.45 !important;
    }
    .hero-text {
        font-size: 0.82rem !important;
        line-height: 1.6 !important;
    }
    .sec-head {
        font-size: 0.98rem !important;
    }
    .info-card {
        padding: 14px !important;
        margin-bottom: 10px !important;
    }
    .card-title {
        font-size: 0.92rem !important;
    }
    .card-text {
        font-size: 0.8rem !important;
        line-height: 1.55 !important;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 6px 10px !important;
        font-size: 0.76rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. تهيئة البيانات وأيقونة التحليل الإحصائي
# ==========================================
if "orders_db" not in st.session_state:
    st.session_state.orders_db = {
        "SL-2026-101": {
            "client": "نموذج استرشادي - مذكرة ماستر (علم الاجتماع)",
            "service": "تحليل إحصائي وتفريغ بيانات SPSS",
            "stage_idx": 2,
            "stages": ["تم استلام الملفات", "قيد المراجعة المنهجية", "مرحلة تنظيف البيانات", "التحليل الإحصائي", "جاهز للتسليم"],
            "notes": "تم الانتهاء من تنظيف 60 استمارة وحساب الصدق والثبات، ويجري استخراج جداول الفرضيات."
        }
    }

# أيقونة SVG احترافية تعبر عن التحليل الإحصائي والبيانات
# ==========================================
# 2. تهيئة البيانات وأيقونة التحليل الإحصائي
# ==========================================
if "orders_db" not in st.session_state:
    st.session_state.orders_db = {
        "SL-2026-101": {
            "client": "نموذج استرشادي - مذكرة ماستر (علم الاجتماع)",
            "service": "تحليل إحصائي وتفريغ بيانات SPSS",
            "stage_idx": 2,
            "stages": ["تم استلام الملفات", "قيد المراجعة المنهجية", "مرحلة تنظيف البيانات", "التحليل الإحصائي", "جاهز للتسليم"],
            "notes": "تم الانتهاء من تنظيف 60 استمارة وحساب الصدق والثبات، ويجري استخراج جداول الفرضيات."
        }
    }

st.markdown("""<div class="top-navbar"><div class="brand-box"><div class="stat-icon-box"><span style="font-size:1.6rem;">📊</span></div><div><div class="brand-title">Socio Lab</div><div class="brand-sub">منصة رقمية للاستشارات المنهجية السوسيولوجية، التحليل الإحصائي، وتجهيز البيانات</div></div></div><div class="loc-badge">📍 حضوريا بسوق أهراس | 🌐 رقميا عبر 58 ولاية</div></div>""", unsafe_allow_html=True)
# ==========================================
# 3. هيكل الصفحات المتكامل (8 تبويبات)
# ==========================================
tabs = st.tabs([
    "🏛️ الرئيسية",
    "🧭 من نحن والنزاهة",
    "💼 الخدمات والمؤسسات B2B",
    "🎓 الدورات التكوينية",
    "📂 نماذج الأعمال",
    "🧰 الأدوات المجانية",
    "📊 تتبع الطلبات",
    "📅 اطلب خدمة والدفع"
])

# --- 1. الرئيسية ---
with tabs[0]:
    st.markdown("""
    <div class="hero-box">
        <div class="hero-headline">من الفكرة البحثية إلى النتائج المحكمة.. شريكك المنهجي والإحصائي الدقيق.</div>
        <p class="hero-text">
            في المنصة الرقمية <span style="font-family:'Lobster',cursive;font-size:1.15rem;color:#5EEAD4;">Socio Lab</span>، نحول البيانات الميدانية الخام إلى رؤى سوسيولوجية وعلمية رصينة. نرافق طلبة الدراسات العليا، الباحثين، والمؤسسات في تصميم أدوات القياس، تنظيف البيانات، والتحليل الإحصائي المتقدم وفق أعلى معايير الجودة والنزاهة العلمية.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">🎯 الفئات المستهدفة (من يستفيد من المنصة الرقمية؟)</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="info-card"><h3 class="card-title">🎓 طلبة الليسانس والماستر</h3><p class="card-text">طلبة جامعة سوق أهراس والجامعات الجزائرية المقبلون على إعداد مذكرات التخرج وتقارير التربص الميداني ويحتاجون مرافقة منهجية وإحصائية دقيقة.</p><span class="tag">مذكرات التخرج</span><span class="tag tag-teal">تقارير التربص</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="info-card card-teal"><h3 class="card-title">🔬 طلبة الدكتوراه والباحثون</h3><p class="card-text">الباحثون، الأساتذة، وفرق ومخابر البحث الراغبون في تحكيم المقاييس السيكومترية، تنظيف قواعد البيانات، وتنسيق الجداول للنشر العلمي المحكم.</p><span class="tag tag-teal">أطروحات الدكتوراه</span><span class="tag tag-indigo">مقالات محكمة</span></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="info-card card-indigo"><h3 class="card-title">🏢 المؤسسات، الإدارات، والجمعيات</h3><p class="card-text">المؤسسات الاقتصادية، الإدارات، والجمعيات التي تحتاج إلى دراسات ميدانية، استطلاعات رأي، وقياس رضا المستفيدين لترشيد قراراتها.</p><span class="tag tag-indigo">استطلاعات الرأي</span><span class="tag tag-amber">حلول B2B</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">✨ لماذا تختار المنصة الرقمية Socio Lab؟</div>', unsafe_allow_html=True)
    r1, r2, r3, r4 = st.columns(4)
    r1.markdown('<div class="info-card"><h4 class="card-title">📖 قراءة سوسيولوجية</h4><p class="card-text">نربط المؤشرات الإحصائية بالسياق النظري والميداني لدراستك بدلا من الأرقام الصماء.</p></div>', unsafe_allow_html=True)
    r2.markdown('<div class="info-card card-teal"><h4 class="card-title">🎯 دقة منهجية صارمة</h4><p class="card-text">نعتمد أحدث الأساليب العلمية في بناء المقاييس واختيار الاختبارات الأنسب لمتغيراتك.</p></div>', unsafe_allow_html=True)
    r3.markdown('<div class="info-card card-indigo"><h4 class="card-title">🔒 سرية وأمان تام</h4><p class="card-text">حماية أفكارك البحثية وبيانات المبحوثين بموجب ميثاق صارم للخصوصية وعدم الإفصاح.</p></div>', unsafe_allow_html=True)
    r4.markdown('<div class="info-card card-amber"><h4 class="card-title">⏱️ التزام بالمواعيد</h4><p class="card-text">تسليم المخرجات في الآجال المحددة مع جلسات شرح ومناقشة للنتائج قبل المناقشة.</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">⚙️ خطوات العمل (How It Works)</div>', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    s1.markdown('<div class="info-card"><h4 class="card-title">1. إرسال الطلب والملفات</h4><p class="card-text">تملأ نموذج الطلب وتحدد الخدمة وترفق مسودة بحثك أو بياناتك.</p></div>', unsafe_allow_html=True)
    s2.markdown('<div class="info-card card-teal"><h4 class="card-title">2. التقييم وتحديد الخطة</h4><p class="card-text">ندرس ملفك ونوافيك بخطة العمل والمدة والتكلفة خلال 24 ساعة.</p></div>', unsafe_allow_html=True)
    s3.markdown('<div class="info-card card-indigo"><h4 class="card-title">3. التنفيذ والمتابعة</h4><p class="card-text">يبدأ العمل المنهجي أو الإحصائي مع تتبع المراحل عبر لوحتك.</p></div>', unsafe_allow_html=True)
    s4.markdown('<div class="info-card card-amber"><h4 class="card-title">4. التسليم والشرح</h4><p class="card-text">تستلم ملفاتك النهائية مع جلسة توضيحية لشرح النتائج قبل المناقشة.</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="cta-banner">🚀 <b>ابدأ الآن:</b> انتقل إلى تبويب <b>«📅 اطلب خدمة والدفع»</b> في أعلى الشاشة لطلب استشارتك أو حجز خدمتك البحثية.</div>', unsafe_allow_html=True)

# --- 2. من نحن وميثاق النزاهة العلمية ---
with tabs[1]:
    st.markdown('<div class="sec-head">🧭 من نحن (About Us)</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-box"><p class="hero-text"><b>Socio Lab</b> هو مختبر استشاري وبحثي ومنصة رقمية متخصصة في المنهجية السوسيولوجية والتحليل الإحصائي للبيانات الاجتماعية والإنسانية. تأسست المنصة لسد الفجوة بين الجانب النظري في الأبحاث الأكاديمية والتطبيق الميداني والإحصائي الدقيق، عبر تقديم حلول بحثية متكاملة تجمع بين الخبرة الميدانية والتمكن التقني.</p></div>', unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    a1.markdown('<div class="info-card card-teal"><h3 class="card-title">🔭 رؤيتنا</h3><p class="card-text">أن نكون المرجع الأول والموثوق للباحثين والمؤسسات في العالم العربي للارتقاء بجودة الإنتاج العلمي والقرارات المبنية على البيانات الدقيقة.</p></div>', unsafe_allow_html=True)
    a2.markdown('<div class="info-card card-indigo"><h3 class="card-title">🎯 رسالتنا</h3><p class="card-text">تمكين الباحثين وطلبة الماستر والدكتوراه والمؤسسات من إنجاز دراسات ميدانية محكمة، عبر توفير استشارات منهجية احترافية، وأدوات قياس موثوقة، وتحليلات إحصائية دقيقة تلتزم بأخلاقيات البحث العلمي وتنبذ التزييف أو الانتحال.</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">⚖️ ميثاق النزاهة العلمية وسياسة العمل (Academic Integrity Charter)</div>', unsafe_allow_html=True)
    ch1, ch2 = st.columns(2)
    with ch1:
        st.markdown("""
        <div class="info-card" style="border-top-color:#F43F5E;">
            <h3 class="card-title">🚫 الخطوط الحمراء للمنصة</h3>
            <p class="card-text">
                تقدم منصة <b>Socio Lab</b> الاستشارة، الضبط المنهجي، والتحليل الإحصائي للبيانات الحقيقية فقط، وترفض تماما:<br>
                • فبركة البيانات الميدانية (Data Fabrication) أو تعديل النتائج لإثبات فرضيات غير محققة.<br>
                • كتابة المذكرات أو الأبحاث الجاهزة نيابة عن الطالب أو أي ممارسة تندرج تحت الانتحال العلمي.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with ch2:
        st.markdown("""
        <div class="info-card card-teal">
            <h3 class="card-title">🛡️ اتفاقية عدم الإفصاح وحماية البيانات (NDA)</h3>
            <p class="card-text">
                تلتزم المنصة بموجب ميثاق السرية وحماية المعطيات الشخصية (القانون 18-07) بأن فكرة الباحث، أدوات قياسه، وبياناته الميدانية محمية قانونيا وأخلاقيا، ولا يتم مشاركتها أو إعادة استخدامها في أي غرض آخر، مع إتلاف الملفات المؤقتة فور انتهاء المعالجة وتسليمها لصاحبها.
            </p>
        </div>
        """, unsafe_allow_html=True)

# --- 3. الخدمات وفضاء المؤسسات B2B ---
with tabs[2]:
    st.markdown('<div class="sec-head">💼 الخدمات الأكاديمية والبحثية (Services)</div>', unsafe_allow_html=True)
    sv1, sv2 = st.columns(2)
    with sv1:
        st.markdown('<div class="info-card"><h3 class="card-title">1. تصميم وبناء أدوات البحث الميداني</h3><p class="card-text">• صياغة وبناء الاستبيانات الورقية والإلكترونية (Google Forms, KoboToolbox) وفق المحاور والفرضيات.<br>• إعداد أدلة المقابلات المعمقة والملاحظة العلمية.<br>• تكييف المقاييس العالمية وترجمتها بما يناسب البيئة الاجتماعية.</p><div class="out-box"><b>المخرجات:</b> نسخة نهائية قابلة للتحكيم والتطبيق مرفقة بدليل الترميز (Codebook).</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="info-card card-indigo"><h3 class="card-title">3. التحكيم والضبط المنهجي</h3><p class="card-text">• تدقيق صياغة الإشكالية، التساؤلات، والفرضيات ومدى قابليتها للاختبار.<br>• تحديد نوع العينة وحجمها المناسب لمجتمع الدراسة.<br>• مواءمة الإطار النظري مع مؤشرات القياس الميداني.</p><div class="out-box"><b>المخرجات:</b> تقرير مفصل بالملاحظات المنهجية والتعديلات المقترحة خطوة بخطوة.</div></div>', unsafe_allow_html=True)
    with sv2:
        st.markdown('<div class="info-card card-teal"><h3 class="card-title">2. التحليل الإحصائي وتفريغ البيانات (SPSS)</h3><p class="card-text">• تفريغ البيانات، ترميزها، وتنظيفها من القيم الشاذة والمفقودة.<br>• حساب الخصائص السيكومترية (الصدق البنائي، الاتساق الداخلي، ألفا كرونباخ).<br>• إجراء الاختبارات الوصفية والاستدلالية وفق طبيعة التوزيع.</p><div class="out-box"><b>المخرجات:</b> ملف SPSS الأصلي + تقرير تحليلي بالجداول والرسوم مع التعليق السوسيولوجي الأولي.</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="info-card card-amber"><h3 class="card-title">4. التوثيق والتدقيق الأكاديمي</h3><p class="card-text">• توثيق المراجع في المتن وفي القائمة النهائية بدقة وفق نظام (APA).<br>• التدقيق اللغوي والأسلوبي للنصوص الأكاديمية لضمان رصانة الأسلوب.<br>• تنسيق الجداول والأشكال البيانية وفق شروط المجلات المحكمة.</p><div class="out-box"><b>المخرجات:</b> ورقة بحثية أو فصل تطبيقي منسق ومضبوط وفق معايير النشر الأكاديمي.</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">🏢 فضاء المؤسسات والجمعيات (B2B / Institutional Solutions)</div>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    b1.markdown('<div class="info-card card-teal"><h3 class="card-title">📊 دراسات قياس الأثر الاجتماعي (Social Impact Assessment)</h3><p class="card-text">تقييم البرامج والمشاريع التنموية والاجتماعية لصالح الجمعيات، الهيئات العمومية، ومراكز الدراسات لقياس مدى تحقق الأهداف الميدانية وتحديد مؤشرات النجاح والفجوات.</p><span class="tag tag-amber">تقارير تنفيذية لصناع القرار</span></div>', unsafe_allow_html=True)
    b2.markdown('<div class="info-card card-indigo"><h3 class="card-title">🗳️ استطلاعات الرأي وقياس رضا المستفيدين والموظفين</h3><p class="card-text">تصميم وتنفيذ مسوح ميدانية أو إلكترونية شاملة للمؤسسات الاقتصادية والخدمية، وتحليل اتجاهات الجمهور الداخلي والخارجي مع تقديم توصيات عملية قابلة للتنفيذ.</p><span class="tag tag-teal">مسوح ميدانية وإلكترونية شاملة</span></div>', unsafe_allow_html=True)

# --- 4. الدورات التكوينية ---
with tabs[3]:
    st.markdown('<div class="sec-head">🎓 البرامج والدورات التكوينية التطبيقية (حضوريا وعن بعد)</div>', unsafe_allow_html=True)
    t1, t2 = st.columns(2)
    t1.markdown('<div class="info-card"><h3 class="card-title">💻 الدورة 1: الأساسيات التطبيقية لتحليل البيانات ببرنامج SPSS</h3><p class="card-text">إعداد قاعدة البيانات، ترميز الاستبيانات، حساب التكرارات والنسب، المتوسطات والانحراف المعياري، وتنسيق الجداول.</p><span class="tag">12 ساعة تطبيقية</span><span class="tag tag-teal">للمبتدئين</span></div>', unsafe_allow_html=True)
    t1.markdown('<div class="info-card card-teal"><h3 class="card-title">📐 الدورة 2: هندسة الاستبيانات الإلكترونية وبناء المقاييس</h3><p class="card-text">تحويل الفرضيات إلى محاور وفقرات قياس، تصميم الاستبيان على Google Forms و KoboToolbox، وتجنب الأخطاء المنهجية.</p><span class="tag tag-teal">8 ساعات تطبيقية</span></div>', unsafe_allow_html=True)
    t2.markdown('<div class="info-card card-indigo"><h3 class="card-title">📈 الدورة 3: الإحصاء الاستدلالي المتقدم واختبار الفرضيات</h3><p class="card-text">فحص الصدق والثبات، شروط الاختبارات المعلمية واللامعلمية، الارتباط والفروق والانحدار، والقراءة السوسيولوجية للنتائج.</p><span class="tag tag-indigo">15 ساعة معمقة</span><span class="tag tag-amber">مستوى متقدم</span></div>', unsafe_allow_html=True)
    t2.markdown('<div class="info-card card-amber"><h3 class="card-title">🏛️ الدورة 4: منهجية إعداد البحوث والمذكرات وفق IMRAD و APA</h3><p class="card-text">الهيكلة المنهجية للدراسة الميدانية، التوثيق العلمي والمراجع بطريقة APA، ومهارات العرض والدفاع أمام لجنة المناقشة.</p><span class="tag tag-amber">10 ساعات</span></div>', unsafe_allow_html=True)

# --- 5. نماذج من أعمالنا (Portfolio & Case Studies) ---
with tabs[4]:
    st.markdown('<div class="sec-head">📂 نماذج من أعمالنا ودراسات الحالة (Portfolio & Case Studies)</div>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    with p1:
        st.markdown("""
        <div class="info-card card-indigo">
            <span class="tag tag-indigo">دراسة حالة (Case Study 01)</span>
            <h3 class="card-title" style="margin-top:8px;">معالجة تشتت البيانات وعدم اعتدالية التوزيع في دراسة سوسيولوجية</h3>
            <p class="card-text">
                <b>المشكلة:</b> واجه باحث في علم الاجتماع رفضا مبدئيا لنتائجه بسبب استخدامه اختبار (T-Test) المعلمي على عينة صغيرة (N=60) ذات توزيع غير طبيعي.<br>
                <b>تدخل Socio Lab:</b> إعادة تنظيف قاعدة البيانات، فحص اعتدالية التوزيع باختبار Shapiro-Wilk، التحول المنهجي إلى اختبار مان-ويتني (Mann-Whitney U) اللامعلمي، وإعادة صياغة الجداول وفق معيار APA 7th مع تعليق سوسيولوجي رصين.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="info-card card-teal">
            <span class="tag tag-teal">دراسة حالة (Case Study 02)</span>
            <h3 class="card-title" style="margin-top:8px;">كشف الاستمارات العشوائية ورفع معامل الثبات من 0.61 إلى 0.86</h3>
            <p class="card-text">
                <b>المشكلة:</b> استلمت جمعية محلية 220 استمارة استطلاع رأي أظهرت نتائج متناقضة وضعفا في ثبات المقياس.<br>
                <b>تدخل Socio Lab:</b> إخضاع الملف للفحص الآلي، اكتشاف واستبعاد 18 استمارة ذات إجابات نمطية متناقضة، وحذف فقرتين مشوشتين في المقياس، مما رفع معامل ألفا كرونباخ إلى 0.86 وقدم تقريرا دقيقا لصناع القرار.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">📋 عينة نموذجية لتنسيق الجداول في تقارير Socio Lab</div>', unsafe_allow_html=True)
    sample_report_df = pd.DataFrame({
        "المحور المدروس": ["تأثير جماعة الرفاق", "الضبط الأسري", "التوافق المدرسي"],
        "حجم العينة (N)": [60, 60, 60],
        "المتوسط الحسابي (M)": [3.84, 2.91, 3.12],
        "الانحراف المعياري (SD)": [0.68, 0.85, 0.74],
        "مستوى التحقق": ["مرتفع", "متوسط", "متوسط"]
    })
    st.dataframe(sample_report_df, use_container_width=True)

# --- 6. الأدوات التفاعلية المجانية الذكية (Lead Magnets) ---
with tabs[5]:
    st.markdown('<div class="sec-head">🧰 الأدوات التفاعلية المجانية للباحثين (Lead Magnets)</div>', unsafe_allow_html=True)
    tool_tabs = st.tabs([
        "🧭 مشخص الاختبار الإحصائي",
        "🧮 حاسبة حجم العينة",
        "✅ قائمة التحقق المنهجية"
    ])

    with tool_tabs[0]:
        st.write("أجب عن الأسئلة الثلاثة الآتية ليقترح عليك النظام الاختبار الإحصائي الأنسب لدراستك فورا:")
        tc1, tc2, tc3 = st.columns(3)
        with tc1:
            goal = st.selectbox("1. ما هو هدف الفرضية؟", ["دراسة العلاقة والارتباط بين متغيرين", "دراسة الفروق بين مجموعات", "دراسة الأثر والتنبؤ (متغير مستقل وتابع)"])
        with tc2:
            var_type = st.selectbox("2. ما هو مستوى قياس المتغيرات؟", ["متغيرات كمية / مقاييس ليكرت (فئوية)", "متغيرات فئوية اسمية (نعم/لا، جنس، تخصص)"])
        with tc3:
            dist_type = st.selectbox("3. طبيعة التوزيع وحجم العينة:", ["توزيع طبيعي وعينة كبيرة (N ≥ 30)", "توزيع غير طبيعي أو عينة صغيرة (N < 30)"])

        if goal == "دراسة العلاقة والارتباط بين متغيرين":
            if var_type == "متغيرات فئوية اسمية (نعم/لا، جنس، تخصص)":
                rec_test = "اختبار كاي تربيع للاستقلالية (Chi-Square Test) ومعامل فاي / كريمر."
            elif "طبيعي" in dist_type:
                rec_test = "معامل ارتباط بيرسون المعلمي (Pearson Correlation - r)."
            else:
                rec_test = "معامل ارتباط سبيرمان اللامعلمي للرتب (Spearman Rank Correlation - rho)."
        elif goal == "دراسة الفروق بين مجموعات":
            grp_num = st.radio("عدد المجموعات المقارنة:", ["مجموعتان مستقلتان (مثل ذكور وإناث)", "ثلاث مجموعات فأكثر (مثل المستوى الدراسي)"], horizontal=True)
            if "مجموعتان" in grp_num:
                rec_test = "اختبار (Independent Samples T-Test) المعلمي." if "طبيعي" in dist_type else "اختبار مان-ويتني (Mann-Whitney U) اللامعلمي."
            else:
                rec_test = "تحليل التباين الأحادي (One-Way ANOVA) المعلمي." if "طبيعي" in dist_type else "اختبار كروسكال-واليس (Kruskal-Wallis) اللامعلمي."
        else:
            rec_test = "تحليل الانحدار الخطي البسيط أو المتعدد (Linear / Multiple Regression) بعد التحقق من شروط البواقي."

        st.success(f"🎯 **الاختبار الإحصائي الموصى به لفرضيتك هو:** {rec_test}")

    with tool_tabs[1]:
        cc1, cc2, cc3 = st.columns(3)
        pop_n = cc1.number_input("حجم مجتمع الدراسة (N):", min_value=10, max_value=1000000, value=1000, step=50)
        conf = cc2.selectbox("مستوى الثقة:", ["95% (Z = 1.96)", "99% (Z = 2.58)"])
        err = cc3.selectbox("هامش الخطأ:", ["5% (0.05)", "3% (0.03)"])
        z = 1.96 if "95%" in conf else 2.58
        e = 0.05 if "5%" in err else 0.03
        n_inf = (z**2 * 0.25) / (e**2)
        s_size = math.ceil(n_inf / (1 + ((n_inf - 1) / pop_n)))
        st.success(f"📐 **حجم العينة العلمي المطلوب:** `{s_size}` مفردة (يستحسن إضافة 10% لتعويض الفاقد الميداني).")

    with tool_tabs[2]:
        st.write("راجع جاهزية مذكرتك أو مقالك العلمي قبل الإيداع أو المناقشة:")
        chk1 = st.checkbox("تطابق عنوان الدراسة مع الإشكالية والفرضيات والأهداف.")
        chk2 = st.checkbox("تحكيم أداة القياس (الاستبيان) وحساب الصدق والثبات (ألفا كرونباخ ≥ 0.70).")
        chk3 = st.checkbox("تنظيف قاعدة البيانات من القيم المفقودة والاستمارات العشوائية قبل التحليل.")
        chk4 = st.checkbox("التحقق من شروط الاختبارات الإحصائية (الاعتدالية وتجانس التباين) قبل تطبيقها.")
        chk5 = st.checkbox("ربط التعليق على الجداول الإحصائية بالإطار النظري والدراسات السابقة (تفسير سوسيولوجي).")
        chk6 = st.checkbox("توثيق جميع المراجع في المتن والقائمة النهائية وفق نظام APA بدقة.")
        score = sum([chk1, chk2, chk3, chk4, chk5, chk6])
        st.progress(score / 6)
        st.write(f"**نسبة جاهزية بحثك الحالية:** `{int((score/6)*100)}%` ({score} من 6 معايير محققة)")

# --- 7. لوحة تحكم العميل ونظام تتبع الطلبات (Client Dashboard) ---
with tabs[6]:
    st.markdown('<div class="sec-head">📊 لوحة تتبع الطلبات وأرشيف الملفات (Client Dashboard)</div>', unsafe_allow_html=True)
    st.write("أدخل رمز المتابعة الخاص بطلبك للاطلاع على مرحلة التنفيذ لحظة بلحظة، تحميل المخرجات، أو إرسال ملاحظات المشرف:")

    track_code = st.text_input("🔑 أدخل رمز متابعة الطلب (جرب الرمز التجريبي: SL-2026-101):", value="SL-2026-101").strip()

    if track_code in st.session_state.orders_db:
        order = st.session_state.orders_db[track_code]
        st.markdown(f"""
        <div class="info-card card-teal">
            <h3 class="card-title">ملف الطلب: {track_code}</h3>
            <p class="card-text"><b>صاحب الطلب:</b> {order['client']} | <b>الخدمة:</b> {order['service']}</p>
            <p class="card-text"><b>تحديث الفريق المنهجي:</b> {order['notes']}</p>
        </div>
        """, unsafe_allow_html=True)

        stages = order["stages"]
        curr = order["stage_idx"]
        st.progress((curr + 1) / len(stages))
        cols_st = st.columns(len(stages))
        for i, st_name in enumerate(stages):
            prefix = "✅" if i <= curr else "⏳"
            cols_st[i].markdown(f"**{prefix} {st_name}**")

        st.markdown('<div class="sec-head">📥 أرشيف الملفات والمخرجات الجاهزة</div>', unsafe_allow_html=True)
        sample_csv = "المتغير,المتوسط,الانحراف_المعياري\nتأثير_الرفاق,3.84,0.68\n".encode("utf-8-sig")
        st.download_button("📥 تحميل ملف النتائج الأولي المعتمد (CSV / Excel)", data=sample_csv, file_name=f"{track_code}_Results.csv")

        st.markdown('<div class="sec-head">✍️ طلب تعديلات (ملاحظات المشرف أو لجنة المناقشة)</div>', unsafe_allow_html=True)
        rev_note = st.text_area("اكتب التعديلات المطلوبة على الجداول أو الاختبارات ليقوم الفريق بتنفيذها:")
        if st.button("إرسال طلب التعديل إلى الفريق"):
            if rev_note:
                st.success("تم إرفاق ملاحظات التعديل بملفك بنجاح، وسيتم تنفيذها وإشعارك خلال 24 ساعة.")
    else:
        st.warning("رمز الطلب غير موجود. تأكد من كتابته بشكل صحيح أو أرسل طلبا جديدا من تبويب «اطلب خدمة والدفع».")

# --- 8. اطلب خدمة، بوابة الدفع المرنة، والأسئلة الشائعة (FAQ & Payment) ---
with tabs[7]:
    st.markdown('<div class="sec-head">📅 نموذج طلب خدمة أو استشارة (Order & Book)</div>', unsafe_allow_html=True)

    with st.form("order_form"):
        fc1, fc2 = st.columns(2)
        with fc1:
            c_name = st.text_input("👤 الاسم الكامل / المؤسسة:")
            c_contact = st.text_input("📱 البريد الإلكتروني / رقم الواتساب:")
            c_role = st.selectbox("🎓 الصفة الأكاديمية أو المهنية:", ["طالب ماستر", "طالب دكتوراه", "أستاذ باحث", "مؤسسة أو جمعية", "طالب ليسانس"])
            c_spec = st.text_input("📚 التخصص العلمي:")
        with fc2:
            c_srv = st.selectbox("💼 نوع الخدمة المطلوبة:", [
                "تصميم استبيان وبناء أداة بحث",
                "تحليل إحصائي وتفريغ بيانات SPSS",
                "ضبط وتحكيم منهجي",
                "توثيق APA وتدقيق أكاديمي",
                "باقة متكاملة (من الأداة إلى التحليل والتقرير)",
                "التسجيل في دورة تكوينية",
                "دراسة ميدانية لمؤسسة أو جمعية (B2B)"
            ])
            c_date = st.date_input("📅 الموعد النهائي المقترح للتسليم:", value=datetime.date.today() + datetime.timedelta(days=7))
            c_files = st.file_uploader("📎 إرفاق ملفات (اختياري: Word, Excel, SPSS, PDF):", type=["doc", "docx", "xlsx", "csv", "sav", "pdf"], accept_multiple_files=True)

        c_desc = st.text_area("📝 وصف مختصر للدراسة أو الطلب:")
        if st.form_submit_button("🚀 إرسال الطلب والحصول على رمز التتبع"):
            if c_name and c_contact:
                new_id = f"SL-2026-{102 + len(st.session_state.orders_db)}"
                st.session_state.orders_db[new_id] = {
                    "client": f"{c_name} ({c_role})",
                    "service": c_srv,
                    "stage_idx": 0,
                    "stages": ["تم استلام الملفات", "قيد المراجعة المنهجية", "مرحلة تنظيف البيانات", "التحليل الإحصائي", "جاهز للتسليم"],
                    "notes": "تم استلام طلبك بنجاح وهو قيد التقييم الأولي من قبل المختص المنهجي."
                }
                st.success(f"تم تسجيل طلبك بنجاح! رمز متابعة طلبك في لوحة التحكم هو: **{new_id}** (احتفظ به لمتابعة تقدم العمل).")
            else:
                st.warning("يرجى إدخال الاسم الكامل ووسيلة التواصل.")

    st.markdown('<div class="sec-head">💳 بوابة الدفع المرنة والأسئلة الشائعة (Payment & FAQ)</div>', unsafe_allow_html=True)
    pay_col, faq_col = st.columns(2)

    with pay_col:
        st.markdown("""
        <div class="info-card card-indigo">
            <h3 class="card-title">💳 خيارات الدفع المرنة المتاحة</h3>
            <p class="card-text">
                نوفر طرق دفع ميسرة تناسب الطلبة والباحثين والمؤسسات:<br>
                • <b>الدفع البريدي والإلكتروني:</b> عبر الحساب البريدي الجاري (CCP) أو تطبيق بريدي موب (BaridiMob).<br>
                • <b>التحويل البنكي والفوترة الرسمية:</b> متاح للمؤسسات، الجمعيات، ومخابر البحث.<br>
                • <b>الدفع المرن على دفعتين:</b> 50% عند اعتماد خطة العمل وبدء التنفيذ، و50% عند جاهزية المخرجات النهائية للمشاريع الكبيرة.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with faq_col:
        with st.expander("❓ كم يستغرق إنجاز التحليل الإحصائي وتجهيز التقرير؟"):
            st.write("تتراوح المدة عادة بين 3 إلى 7 أيام عمل حسب حجم العينة وعدد الفرضيات والمتغيرات، مع إمكانية المعالجة المستعجلة.")
        with st.expander("❓ ماذا لو طلب الأستاذ المشرف تعديلا على الجداول أو الاختبارات؟"):
            st.write("نلتزم بإجراء التعديلات المنهجية والإحصائية التي يطلبها الأستاذ المشرف مجانا ضمن نطاق الدراسة المتفق عليه عبر نظام طلب التعديلات في لوحة التحكم.")
        with st.expander("❓ هل تشرحون لي النتائج الإحصائية قبل موعد المناقشة؟"):
            st.write("نعم، يتضمن كل تحليل إحصائي جلسة شرح توضيحية (حضوريا بسوق أهراس أو عن بعد) لفهم دلالة كل جدول وكيفية الدفاع عنه علميا أمام اللجنة.")
