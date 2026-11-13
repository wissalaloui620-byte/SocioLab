import streamlit as st
import pandas as pd
import numpy as np
import math, datetime

# ==========================================
# 1. إعدادات الصفحة والهوية البصرية المتكاملة
# ==========================================
st.set_page_config(
    page_title="Socio Lab | Research & Analytics Ecosystem",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lobster&family=Readex+Pro:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stApp, .stMarkdown, .stText, .stButton, .stSelectbox, .stMultiSelect, .stRadio, .stCheckbox, input, textarea {
    font-family: 'Readex Pro', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}

#MainMenu, footer { visibility: hidden; }
header { background: transparent !important; }

.stApp {
    background: radial-gradient(circle at 12% 12%, #0F294A 0%, #061529 52%, #020813 100%) !important;
    color: #E2E8F0 !important;
}

h1 { font-size: 1.5rem !important; font-weight: 700 !important; color: #F8FAFC !important; }
h2 { font-size: 1.25rem !important; font-weight: 700 !important; color: #F8FAFC !important; }
h3 { font-size: 1.05rem !important; font-weight: 600 !important; color: #F8FAFC !important; }
h4 { font-size: 0.96rem !important; font-weight: 600 !important; color: #F8FAFC !important; }
p, label, li, .stMarkdown { font-size: 0.87rem !important; line-height: 1.65 !important; color: #CBD5E1 !important; }

div[data-testid="stAlert"] {
    background: rgba(10, 32, 64, 0.95) !important;
    border: 1px solid rgba(56, 189, 248, 0.4) !important;
    border-right: 4px solid #14B8A6 !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
}
div[data-testid="stAlert"] * { color: #F1F5F9 !important; font-size: 0.85rem !important; }

/* الترويسة العلوية */
.top-navbar {
    background: linear-gradient(135deg, rgba(12, 34, 64, 0.94) 0%, rgba(17, 24, 39, 0.96) 100%);
    border: 1px solid rgba(56, 189, 248, 0.3);
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
.brand-box { display: flex; align-items: center; gap: 14px; }
.stat-icon-box {
    width: 50px; height: 50px; border-radius: 14px;
    background: linear-gradient(135deg, #0284C7 0%, #14B8A6 55%, #6366F1 100%);
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 0 18px rgba(20, 184, 166, 0.45);
    flex-shrink: 0;
}
.brand-title {
    font-family: 'Lobster', cursive !important;
    font-size: 2.0rem !important;
    font-weight: 400 !important;
    direction: ltr !important;
    display: inline-block;
    background: linear-gradient(90deg, #FFFFFF 10%, #7DD3FC 55%, #5EEAD4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 !important;
    line-height: 1.15 !important;
}
.brand-sub { color: #94A3B8 !important; font-size: 0.81rem !important; margin: 3px 0 0 0 !important; }
.loc-badge {
    background: linear-gradient(135deg, rgba(20, 184, 166, 0.16), rgba(99, 102, 241, 0.16));
    border: 1px solid rgba(94, 234, 212, 0.35);
    color: #5EEAD4 !important;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 0.77rem !important;
    font-weight: 600;
}

/* البانر الترحيبي */
.hero-box {
    background: linear-gradient(135deg, rgba(15, 44, 82, 0.78) 0%, rgba(23, 27, 66, 0.88) 100%);
    border: 1px solid rgba(99, 102, 241, 0.32);
    border-right: 4px solid #14B8A6;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 18px;
}
.hero-headline { font-size: 1.28rem !important; font-weight: 700 !important; color: #FFFFFF !important; margin: 0 0 8px 0 !important; }
.hero-text { font-size: 0.88rem !important; color: #CBD5E1 !important; line-height: 1.7 !important; margin: 0 !important; }

/* البطاقات الملونة */
.info-card {
    background: linear-gradient(155deg, rgba(15, 35, 65, 0.84) 0%, rgba(9, 20, 40, 0.95) 100%);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-top: 3px solid #0EA5E9;
    border-radius: 14px;
    padding: 16px 18px;
    height: 100%;
    margin-bottom: 14px;
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.info-card:hover { transform: translateY(-3px); border-color: #5EEAD4; }
.card-teal { border-top-color: #14B8A6 !important; }
.card-indigo { border-top-color: #818CF8 !important; }
.card-amber { border-top-color: #F59E0B !important; }
.card-rose { border-top-color: #F43F5E !important; }

.card-title { font-size: 1.0rem !important; font-weight: 700 !important; color: #F8FAFC !important; margin: 0 0 7px 0 !important; }
.card-text { font-size: 0.84rem !important; color: #CBD5E1 !important; line-height: 1.62 !important; margin: 0 0 8px 0 !important; }
.out-box {
    background: rgba(20, 184, 166, 0.12);
    border-right: 3px solid #14B8A6;
    padding: 7px 11px;
    border-radius: 6px;
    font-size: 0.79rem !important;
    color: #5EEAD4 !important;
    margin-top: 8px;
}

/* الشارات */
.tag {
    display: inline-block;
    padding: 3px 9px;
    border-radius: 999px;
    font-size: 0.71rem !important;
    font-weight: 600;
    background: rgba(14, 165, 233, 0.16);
    color: #7DD3FC !important;
    border: 1px solid rgba(14, 165, 233, 0.32);
    margin: 4px 0 0 4px;
}
.tag-teal { background: rgba(20, 184, 166, 0.16); color: #5EEAD4 !important; border-color: rgba(20, 184, 166, 0.35); }
.tag-indigo { background: rgba(129, 140, 248, 0.16); color: #C7D2FE !important; border-color: rgba(129, 140, 248, 0.35); }
.tag-amber { background: rgba(245, 158, 11, 0.16); color: #FCD34D !important; border-color: rgba(245, 158, 11, 0.35); }

.sec-head {
    font-size: 1.12rem !important;
    font-weight: 700 !important;
    color: #5EEAD4 !important;
    margin: 18px 0 12px 0 !important;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(94, 234, 212, 0.22);
}

.cta-banner {
    background: linear-gradient(135deg, rgba(20, 184, 166, 0.2), rgba(79, 70, 229, 0.25));
    border: 1px solid rgba(94, 234, 212, 0.4);
    border-right: 4px solid #14B8A6;
    border-radius: 12px;
    padding: 14px 18px;
    margin-top: 14px;
    font-size: 0.86rem !important;
}

.devis-box {
    background: rgba(8, 22, 44, 0.96);
    border: 1.5px solid #38BDF8;
    border-radius: 14px;
    padding: 20px 24px;
    margin-top: 14px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 5px;
    background: rgba(8, 22, 44, 0.94);
    padding: 6px;
    border-radius: 12px;
    border: 1px solid rgba(56, 189, 248, 0.22);
    flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    padding: 6px 11px !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    color: #94A3B8 !important;
    background: transparent !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0284C7 0%, #14B8A6 100%) !important;
    color: #FFFFFF !important;
}

.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #0284C7 0%, #14B8A6 100%) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.83rem !important;
    border-radius: 9px !important;
    padding: 0.45rem 1.1rem !important;
    border: none !important;
}

@media only screen and (max-width: 768px) {
    .top-navbar { padding: 12px 14px !important; flex-direction: column !important; align-items: flex-start !important; }
    .stat-icon-box { width: 40px !important; height: 40px !important; }
    .brand-title { font-size: 1.5rem !important; }
    .brand-sub { font-size: 0.73rem !important; }
    .loc-badge { font-size: 0.7rem !important; padding: 4px 10px !important; }
    .hero-box { padding: 14px !important; }
    .hero-headline { font-size: 1.02rem !important; }
    .hero-text { font-size: 0.8rem !important; }
    .sec-head { font-size: 0.96rem !important; }
    .info-card { padding: 13px !important; margin-bottom: 10px !important; }
    .card-title { font-size: 0.9rem !important; }
    .card-text { font-size: 0.79rem !important; }
    .stTabs [data-baseweb="tab"] { padding: 5px 8px !important; font-size: 0.74rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. تهيئة البيانات والترويسة النظيفة
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

st.markdown("""<div class="top-navbar"><div class="brand-box"><div class="stat-icon-box"><span style="font-size:1.55rem;">📊</span></div><div><div class="brand-title">Socio Lab</div><div class="brand-sub">حاضنة منهجية ومنصة رقمية للاستشارات السوسيولوجية، التحليل الإحصائي والكيفي، وتجهيز البيانات</div></div></div><div class="loc-badge">📍 حضوريا بسوق أهراس | 🌐 رقميا عبر 58 ولاية</div></div>""", unsafe_allow_html=True)

# ==========================================
# 3. هيكل المنصة المتكاملة (10 تبويبات شاملة)
# ==========================================
tabs = st.tabs([
    "🏛️ الرئيسية",
    "🧭 من نحن والنزاهة",
    "💼 الخدمات (كمي وكيفي ونشر)",
    "🛒 متجر المنتجات الرقمية",
    "🎓 Socio Lab Academy",
    "🤝 الشبكة العلمية والشراكات",
    "🧰 الأنظمة والأدوات الذكية",
    "📂 نماذج الأعمال",
    "📊 تتبع الطلبات",
    "📅 اطلب خدمة والدفع"
])

# --- 1. الرئيسية ---
with tabs[0]:
    st.markdown("""
    <div class="hero-box">
        <div class="hero-headline">من الفكرة البحثية إلى النتائج المحكمة.. شريكك المنهجي والإحصائي الدقيق.</div>
        <p class="hero-text">
            في المنصة الرقمية <span style="font-family:'Lobster',cursive;font-size:1.1rem;color:#5EEAD4;">Socio Lab</span>، نحول البيانات الميدانية الخام إلى رؤى سوسيولوجية وعلمية رصينة. نرافق طلبة الدراسات العليا، الباحثين، والمؤسسات في تصميم أدوات القياس، تنظيف البيانات، والتحليل الكمي والكيفي المتقدم وفق أعلى معايير الجودة والنزاهة العلمية.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">🎯 الفئات المستهدفة (من يستفيد من المنصة الرقمية؟)</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="info-card"><h3 class="card-title">🎓 طلبة الليسانس والماستر</h3><p class="card-text">طلبة جامعة سوق أهراس والجامعات الجزائرية المقبلون على إعداد مذكرات التخرج وتقارير التربص الميداني ويحتاجون مرافقة منهجية وإحصائية دقيقة.</p><span class="tag">مذكرات التخرج</span><span class="tag tag-teal">تقارير التربص</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="info-card card-teal"><h3 class="card-title">🔬 طلبة الدكتوراه والباحثون</h3><p class="card-text">الباحثون، الأساتذة، وفرق ومخابر البحث الراغبون في تحكيم المقاييس السيكومترية، التحليل الكيفي، وتنسيق المقالات للنشر العلمي المحكم (ASJP / Scopus).</p><span class="tag tag-teal">أطروحات الدكتوراه</span><span class="tag tag-indigo">نشر علمي</span></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="info-card card-indigo"><h3 class="card-title">🏢 المؤسسات، الإدارات، والجمعيات</h3><p class="card-text">المؤسسات الاقتصادية، الإدارات، والجمعيات التي تحتاج إلى دراسات قياس الأثر الاجتماعي، استطلاعات الرأي، وتدريب فرق البحث الميداني.</p><span class="tag tag-indigo">دراسات الأثر</span><span class="tag tag-amber">حلول B2B</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">✨ لماذا تختار المنصة الرقمية Socio Lab؟</div>', unsafe_allow_html=True)
    r1, r2, r3, r4 = st.columns(4)
    r1.markdown('<div class="info-card"><h4 class="card-title">📖 قراءة سوسيولوجية</h4><p class="card-text">نربط المؤشرات الإحصائية والكيفية بالسياق النظري والميداني لدراستك بدلا من الأرقام الصماء.</p></div>', unsafe_allow_html=True)
    r2.markdown('<div class="info-card card-teal"><h4 class="card-title">🎯 دقة منهجية صارمة</h4><p class="card-text">نعتمد أحدث الأساليب العلمية في بناء المقاييس واختيار الاختبارات الأنسب لمتغيراتك.</p></div>', unsafe_allow_html=True)
    r3.markdown('<div class="info-card card-indigo"><h4 class="card-title">🔒 سرية وأمان تام</h4><p class="card-text">حماية أفكارك البحثية وبيانات المبحوثين بموجب اتفاقية عدم إفصاح صارمة (NDA).</p></div>', unsafe_allow_html=True)
    r4.markdown('<div class="info-card card-amber"><h4 class="card-title">⏱️ التزام بالمواعيد</h4><p class="card-text">تسليم المخرجات في الآجال المحددة مع جلسات شرح ومناقشة للنتائج قبل المناقشة.</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">⚙️ خطوات العمل (How It Works)</div>', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    s1.markdown('<div class="info-card"><h4 class="card-title">1. إرسال الطلب والملفات</h4><p class="card-text">تملأ نموذج الطلب وتحدد الخدمة وترفق مسودة بحثك أو بياناتك.</p></div>', unsafe_allow_html=True)
    s2.markdown('<div class="info-card card-teal"><h4 class="card-title">2. التقييم وتحديد الخطة</h4><p class="card-text">ندرس ملفك ونوافيك بخطة العمل والمدة والتكلفة خلال 24 ساعة.</p></div>', unsafe_allow_html=True)
    s3.markdown('<div class="info-card card-indigo"><h4 class="card-title">3. التنفيذ والمتابعة</h4><p class="card-text">يبدأ العمل المنهجي أو الإحصائي مع تتبع المراحل عبر لوحتك.</p></div>', unsafe_allow_html=True)
    s4.markdown('<div class="info-card card-amber"><h4 class="card-title">4. التسليم والشرح</h4><p class="card-text">تستلم ملفاتك النهائية مع جلسة توضيحية لشرح النتائج قبل المناقشة.</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="cta-banner">🚀 <b>ابدأ الآن:</b> استخدم <b>حاسبة التسعير الفوري</b> في تبويب الأنظمة الذكية أو انتقل مباشرة إلى <b>«📅 اطلب خدمة والدفع»</b> لحجز استشارتك.</div>', unsafe_allow_html=True)

# --- 2. من نحن وميثاق النزاهة ---
with tabs[1]:
    st.markdown('<div class="sec-head">🧭 من نحن (About Us)</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-box"><p class="hero-text"><b>Socio Lab</b> هو مختبر استشاري وبحثي وحاضنة منهجية ورقمية متخصصة في المنهجية السوسيولوجية والتحليل الإحصائي والكيفي للبيانات الاجتماعية والإنسانية. تأسست المنصة لسد الفجوة بين الجانب النظري في الأبحاث الأكاديمية والتطبيق الميداني الدقيق، عبر حلول بحثية متكاملة تجمع بين الخبرة الميدانية والتمكن التقني.</p></div>', unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    a1.markdown('<div class="info-card card-teal"><h3 class="card-title">🔭 رؤيتنا</h3><p class="card-text">أن نكون المرجع الأول والموثوق للباحثين والمؤسسات في العالم العربي للارتقاء بجودة الإنتاج العلمي والقرارات المبنية على البيانات الدقيقة.</p></div>', unsafe_allow_html=True)
    a2.markdown('<div class="info-card card-indigo"><h3 class="card-title">🎯 رسالتنا</h3><p class="card-text">تمكين الباحثين وطلبة الماستر والدكتوراه والمؤسسات من إنجاز دراسات ميدانية محكمة، عبر توفير استشارات منهجية احترافية، وأدوات قياس موثوقة، وتحليلات دقيقة تلتزم بأخلاقيات البحث العلمي وتنبذ التزييف أو الانتحال.</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">⚖️ ميثاق النزاهة العلمية وسياسة العمل (Academic Integrity Charter)</div>', unsafe_allow_html=True)
    ch1, ch2 = st.columns(2)
    with ch1:
        st.markdown('<div class="info-card card-rose"><h3 class="card-title">🚫 الخطوط الحمراء للمنصة</h3><p class="card-text">تقدم منصة <b>Socio Lab</b> الاستشارة، الضبط المنهجي، والتحليل الإحصائي والكيفي للبيانات الحقيقية فقط، وترفض تماما:<br>• فبركة البيانات الميدانية (Data Fabrication) أو تعديل النتائج لإثبات فرضيات غير محققة.<br>• بيع البحوث الجاهزة أو كتابة المذكرات نيابة عن الطالب أو أي ممارسة تندرج تحت الانتحال العلمي.</p></div>', unsafe_allow_html=True)
    with ch2:
        st.markdown('<div class="info-card card-teal"><h3 class="card-title">🛡️ اتفاقية عدم الإفصاح وحماية البيانات (NDA)</h3><p class="card-text">وثيقة إلكترونية تضمن للباحث أن فكرته البحثية وأدواته وبياناته الميدانية محمية قانونيا وأخلاقيا وفق القانون الجزائري 18-07، ولن تستخدم في أي غرض آخر، مع إتلاف الملفات المؤقتة فور تسليم العمل.</p></div>', unsafe_allow_html=True)

# --- 3. الخدمات الشاملة (كمي + كيفي + ما بعد البحث + B2B) ---
with tabs[2]:
    st.markdown('<div class="sec-head">📊 أولا: الخدمات المنهجية والكمية (Quantitative & SPSS)</div>', unsafe_allow_html=True)
    sv1, sv2 = st.columns(2)
    with sv1:
        st.markdown('<div class="info-card"><h3 class="card-title">1. تصميم وبناء أدوات البحث الميداني</h3><p class="card-text">• صياغة الاستبيانات الورقية والإلكترونية (Google Forms, KoboToolbox) وفق المحاور والفرضيات.<br>• تكييف المقاييس العالمية وترجمتها بما يناسب البيئة الاجتماعية.<br>• الضبط والتحكيم المنهجي للإشكالية والفرضيات وتحديد حجم العينة.</p><div class="out-box"><b>المخرجات:</b> أداة قياس محكمة + دليل الترميز (Codebook).</div></div>', unsafe_allow_html=True)
    with sv2:
        st.markdown('<div class="info-card card-teal"><h3 class="card-title">2. التحليل الإحصائي وتفريغ البيانات (SPSS)</h3><p class="card-text">• تفريغ البيانات، ترميزها، وتنظيفها من القيم الشاذة والمفقودة.<br>• حساب الخصائص السيكومترية (الصدق البنائي، الاتساق الداخلي، ألفا كرونباخ).<br>• إجراء الاختبارات الوصفية والاستدلالية (الفروق، الارتباط، الانحدار).</p><div class="out-box"><b>المخرجات:</b> ملف SPSS الأصلي + تقرير تحليلي بالجداول والتعليق السوسيولوجي.</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">🎙️ ثانيا: خدمات الدراسات الكيفية والمنهجيات المختلطة (Qualitative & Mixed Methods)</div>', unsafe_allow_html=True)
    ql1, ql2, ql3 = st.columns(3)
    with ql1:
        st.markdown('<div class="info-card card-indigo"><h3 class="card-title">تفريغ وتحليل المقابلات المعمقة</h3><p class="card-text">تحويل التسجيلات الصوتية للمقابلات ومجموعات التركيز (Focus Groups) إلى نصوص مكتوبة بدقة، وتحليلها موضوعاتيا (Thematic Analysis) أو عبر تحليل المضمون المنهجي.</p><span class="tag tag-indigo">تحليل موضوعاتي</span></div>', unsafe_allow_html=True)
    with ql2:
        st.markdown('<div class="info-card card-teal"><h3 class="card-title">برمجيات التحليل الكيفي المتخصصة</h3><p class="card-text">تقديم خدمات الترميز الشبكي وبناء الفئات المفاهيمية باستخدام برمجيات التحليل الكيفي المعتمدة عالميا مثل <b>NVivo</b> و <b>ATLAS.ti</b> و <b>MAXQDA</b>.</p><span class="tag tag-teal">NVivo / MAXQDA</span></div>', unsafe_allow_html=True)
    with ql3:
        st.markdown('<div class="info-card"><h3 class="card-title">تصميم الدراسات المختلطة (Mixed)</h3><p class="card-text">مساعدة الباحثين في دمج النتائج الكمية والكيفية في تقرير بحثي واحد متناسق (مثل دراسة مسحية لعينة واسعة مدعمة بمقابلات مع حالات خاصة أو خبراء).</p><span class="tag">دمج كمي-كيفي</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">📑 ثالثا: خدمات ما بعد البحث والنشر العلمي (Post-Research & Publishing)</div>', unsafe_allow_html=True)
    pb1, pb2, pb3 = st.columns(3)
    with pb1:
        st.markdown('<div class="info-card card-amber"><h3 class="card-title">تحويل المذكرات إلى مقالات علمية</h3><p class="card-text">استخلاص أوراق بحثية مركزة من رسائل الماستر والدكتوراه وتنسيقها وتوثيقها وفق نظام (APA) وقوالب المجلات الوطنية (منصة ASJP) والدولية المحكمة.</p><span class="tag tag-amber">نشر ASJP / Scopus</span></div>', unsafe_allow_html=True)
    with pb2:
        st.markdown('<div class="info-card"><h3 class="card-title">العروض التقديمية للمناقشات والمؤتمرات</h3><p class="card-text">إعداد عروض احترافية ومختصرة تركز على الإشكالية، المنهجية، وأهم النتائج باستخدام الرسوم البيانية التفاعلية (Infographics) بهوية بصرية رصينة.</p><span class="tag">عروض دفاع رصينة</span></div>', unsafe_allow_html=True)
    with pb3:
        st.markdown('<div class="info-card card-indigo"><h3 class="card-title">إعداد الملصقات العلمية (Posters)</h3><p class="card-text">تصميم ملصقات المشاركة في الملتقيات العلمية الوطنية والدولية (Academic Posters) وفق المعايير الأكاديمية القياسية والوضوح البصري.</p><span class="tag tag-indigo">ملتقيات دولية</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">🏢 رابعا: فضاء المؤسسات والجمعيات (B2B / Institutional Solutions)</div>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    b1.markdown('<div class="info-card card-teal"><h3 class="card-title">📊 دراسات قياس الأثر الاجتماعي (Social Impact Assessment)</h3><p class="card-text">تقييم البرامج والمشاريع التنموية والاجتماعية لصالح الجمعيات، الهيئات العمومية، ومراكز الدراسات مع تقديم تقارير تنفيذية لصناع القرار.</p></div>', unsafe_allow_html=True)
    b2.markdown('<div class="info-card card-indigo"><h3 class="card-title">🗳️ استطلاعات الرأي وقياس رضا المستفيدين والموظفين</h3><p class="card-text">تصميم وتنفيذ مسوح ميدانية أو إلكترونية شاملة للمؤسسات الاقتصادية والخدمية لقياس اتجاهات الجمهور الداخلي والخارجي.</p></div>', unsafe_allow_html=True)

# --- 4. متجر المنتجات الرقمية الجاهزة (Digital Products Store) ---
with tabs[3]:
    st.markdown('<div class="sec-head">🛒 متجر المنتجات الرقمية الجاهزة (Digital Products Store)</div>', unsafe_allow_html=True)
    st.write("أدوات وقوالب ومقاييس علمية جاهزة للتحميل الفوري لمساعدة الباحثين على إنجاز أعمالهم بدقة وسرعة:")

    st1, st2, st3 = st.columns(3)
    with st1:
        st.markdown("""
        <div class="info-card">
            <span class="tag">كتيبات تطبيقية (E-Books)</span>
            <h3 class="card-title" style="margin-top:8px;">دليل الباحث الميداني وقراءة جداول SPSS</h3>
            <p class="card-text">
                • <b>الكتيب 1:</b> دليل الباحث الميداني لتجنب أخطاء المعاينة وبناء الاستبيان.<br>
                • <b>الكتيب 2:</b> خطوات قراءة والتعليق على جداول SPSS سوسيولوجيا (مع أمثلة تطبيقية).
            </p>
            <div class="out-box">السعر الرمزي: <b>800 دج</b> للكتيب (تحميل PDF فوري)</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📥 طلب الكتيبات التطبيقية", key="btn_ebook"):
            st.info("للحصول على الكتيبات، حدد «منتج رقمي: كتيب تطبيقي» في تبويب اطلب خدمة.")

    with st2:
        st.markdown("""
        <div class="info-card card-teal">
            <span class="tag tag-teal">حزم القوالب الجاهزة</span>
            <h3 class="card-title" style="margin-top:8px;">حزمة قوالب Word (APA) و Excel الإحصائية</h3>
            <p class="card-text">
                • قوالب <b>Word</b> مبرمجة مسبقا بضوابط التوثيق الأكاديمي (APA 7th) وتنسيق المذكرات والمقالات.<br>
                • قوالب <b>Excel</b> مجهزة لحساب المعادلات الإحصائية الأولية وتفريغ البيانات وتنظيفها آليا.
            </p>
            <div class="out-box">السعر الرمزي: <b>1,200 دج</b> للحزمة الكاملة</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📥 طلب حزمة القوالب الجاهزة", key="btn_tpl"):
            st.info("للحصول على الحزمة، حدد «منتج رقمي: حزمة قوالب» في تبويب اطلب خدمة.")

    with st3:
        st.markdown("""
        <div class="info-card card-indigo">
            <span class="tag tag-indigo">بنك المقاييس المحكمة</span>
            <h3 class="card-title" style="margin-top:8px;">مقاييس نفسية واجتماعية وأمنية مقننة محليا</h3>
            <p class="card-text">
                توفير مقاييس جاهزة ومقننة في البيئة الجزائرية والمحلية، مرفقة بـ <b>بطاقة تقنية لكل مقياس</b> تشمل: أبعاده، طريقة تصحيحه، معاملات صدقه وثباته، ومراجعه الأصلية.
            </p>
            <div class="out-box">السعر الرمزي: <b>1,500 دج</b> للمقياس مع بطاقته التقنية</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📥 تصفح وطلب مقياس محكم", key="btn_scale"):
            st.info("اذكر موضوع متغيرك في تبويب اطلب خدمة لتزويدك بالمقياس المقنن المناسب.")

# --- 5. جناح التدريب وبناء القدرات (Socio Lab Academy) ---
with tabs[4]:
    st.markdown('<div class="sec-head">🎓 جناح التدريب وبناء القدرات (Socio Lab Academy)</div>', unsafe_allow_html=True)
    st.write("نحول الخبرة الاستشارية إلى برامج تدريبية تطبيقية قصيرة ومكثفة للطلبة، الباحثين، وفرق الجمعيات:")

    ac1, ac2, ac3 = st.columns(3)
    with ac1:
        st.markdown("""
        <div class="info-card">
            <span class="tag">ورشات عمل مباشرة (Bootcamps)</span>
            <h3 class="card-title" style="margin-top:8px;">معسكرات نهاية الأسبوع التطبيقية</h3>
            <p class="card-text">
                دورات مركزة عبر الإنترنت أو حضوريا نهاية الأسبوع (مثلا: ورشة من 3 أيام حول بناء الاستبيان الإلكتروني، تنظيف البيانات، وتطبيق اختبارات SPSS خطوة بخطوة).
            </p>
            <span class="badge-tag tag-teal">تدريب تفاعلي مباشر</span>
        </div>
        """, unsafe_allow_html=True)
    with ac2:
        st.markdown("""
        <div class="info-card card-teal">
            <span class="tag tag-teal">دورات مسجلة حسب الطلب</span>
            <h3 class="card-title" style="margin-top:8px;">كبسولات مهارية قصيرة (On-Demand)</h3>
            <p class="card-text">
                فيديوهات تعليمية قصيرة ومقسمة حسب المهارة، يقتنيها الطالب ليتعلم بنفسه كيفية إدخال بياناته، حساب الصدق والثبات، واستخراج معاملات الارتباط أو الفروق في وقت قياسي.
            </p>
            <span class="badge-tag tag-indigo">متاحة 24/7</span>
        </div>
        """, unsafe_allow_html=True)
    with ac3:
        st.markdown("""
        <div class="info-card card-amber">
            <span class="tag tag-amber">تدريب فرق البحث الميداني</span>
            <h3 class="card-title" style="margin-top:8px;">تأهيل الباحثين الميدانيين والجمعيات</h3>
            <p class="card-text">
                تدريب الجامعيين أو أعضاء الجمعيات على تقنيات إجراء المقابلة الميدانية، أخلاقيات التعامل مع المبحوثين، واستخدام الأجهزة اللوحية (KoboToolbox) في المسح الميداني.
            </p>
            <span class="badge-tag tag-amber">تأهيل ميداني</span>
        </div>
        """, unsafe_allow_html=True)

# --- 6. الشبكة العلمية والشراكات والمرصد الاجتماعي ---
with tabs[5]:
    st.markdown('<div class="sec-head">🤝 الشبكة العلمية وبوابة المحكمين (Expert & Peer Network)</div>', unsafe_allow_html=True)
    nt1, nt2 = st.columns(2)
    with nt1:
        st.markdown("""
        <div class="info-card card-indigo">
            <h3 class="card-title">👨‍🏫 قاعدة بيانات الأساتذة المحكمين</h3>
            <p class="card-text">
                فضاء يربط بين الباحثين الذين يحتاجون إلى «تحكيم أداة الدراسة» وأساتذة جامعيين متخصصين في مختلف فروع علم الاجتماع، علم النفس، والإحصاء لتقييم الاستبيانات إلكترونيا وإصدار شهادات تحكيم موثقة.
            </p>
            <span class="tag tag-indigo">تحكيم إلكتروني موثق</span>
        </div>
        """, unsafe_allow_html=True)
    with nt2:
        st.markdown("""
        <div class="info-card card-teal">
            <h3 class="card-title">🗺️ شبكة جامعي البيانات الميدانيين (Enumerators)</h3>
            <p class="card-text">
                قائمة بباحثين ميدانيين موثوقين ومدربين في مختلف ولايات الوطن لتسهيل توزيع الاستبيانات أو إجراء المقابلات الميدانية لصالح المؤسسات أو الباحثين المقيمين في مناطق بعيدة.
            </p>
            <span class="tag tag-teal">تغطية وطنية ميدانية</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">🏛️ قسم الشراكات والمسؤولية العلمية والمرصد الاجتماعي</div>', unsafe_allow_html=True)
    pr1, pr2 = st.columns(2)
    with pr1:
        st.markdown("""
        <div class="info-card">
            <h3 class="card-title">🎤 رعاية الملتقيات والأيام الدراسية</h3>
            <p class="card-text">
                ركن مخصص لطلبات الشراكة العلمية مع النوادي الطلابية، حاضنات الأعمال، ومخابر البحث لتقديم ورشات منهجية وإحصائية مجانية أو مدعمة على هامش المؤتمرات والملتقيات الجامعية.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with pr2:
        st.markdown("""
        <div class="info-card card-amber">
            <h3 class="card-title">📡 التقارير الدورية والمرصد الاجتماعي</h3>
            <p class="card-text">
                نشر نتائج استطلاعات رأي قصيرة تجريها منصة <b>Socio Lab</b> دوريا حول ظواهر اجتماعية أو أكاديمية راهنة (مثل تحديات النشر العلمي لدى الباحثين، أو توجهات الشباب المهنية) في تقارير مختصرة.
            </p>
        </div>
        """, unsafe_allow_html=True)

# --- 7. الأنظمة والأدوات الذكية (Tech & Automation + Lead Magnets) ---
with tabs[6]:
    st.markdown('<div class="sec-head">🧰 الأنظمة الذكية والأدوات التفاعلية المجانية (Tech & Automation)</div>', unsafe_allow_html=True)
    smart_tabs = st.tabs([
        "💰 حاسبة التسعير الفوري وعرض السعر (Devis)",
        "🧭 مشخص الاختبار الإحصائي",
        "🧮 حاسبة حجم العينة",
        "📖 قاموس المصطلحات (Glossary)",
        "✅ قائمة التحقق المنهجية"
    ])

    # أ. حاسبة التسعير الفوري + توليد عرض سعر (Devis)
    with smart_tabs[0]:
        st.write("احسب التكلفة التقديرية لخدمتك فورا، وقم بتوليد عرض سعر رسمي (Devis) قابل للتحميل:")
        q_c1, q_c2, q_c3, q_c4 = st.columns(4)
        with q_c1:
            q_srv = st.selectbox("نوع الخدمة:", [
                "تحليل إحصائي وتفريغ SPSS",
                "تصميم وتحكيم استبيان",
                "تحليل كيفي (مقابلات / NVivo)",
                "تحويل مذكرة إلى مقال علمي",
                "باقة متكاملة (أداة + تحليل + تقرير)"
            ])
        with q_c2:
            q_sample = st.number_input("حجم العينة المتوقع:", min_value=10, max_value=5000, value=60, step=10)
        with q_c3:
            q_items = st.number_input("عدد أسئلة / فقرات الأداة:", min_value=5, max_value=200, value=25, step=5)
        with q_c4:
            q_urgency = st.selectbox("مدة التسليم:", ["عادي (5 - 7 أيام)", "مستعجل (48 - 72 ساعة)"])

        base_prices = {
            "تحليل إحصائي وتفريغ SPSS": 4000,
            "تصميم وتحكيم استبيان": 3000,
            "تحليل كيفي (مقابلات / NVivo)": 5000,
            "تحويل مذكرة إلى مقال علمي": 4500,
            "باقة متكاملة (أداة + تحليل + تقرير)": 8500
        }
        est_price = base_prices[q_srv] + (max(0, q_sample - 50) * 15) + (max(0, q_items - 20) * 40)
        if "مستعجل" in q_urgency:
            est_price = int(est_price * 1.25)

        st.success(f"💵 **التسعيرة التقديرية الفورية لطلبك:** `{est_price:,} دج`")

        client_devis_name = st.text_input("أدخل اسمك أو اسم المؤسسة / المخبر لإصدار عرض سعر رسمي (Devis):", value="باحث / مؤسسة")
        devis_date = datetime.date.today().strftime("%Y-%m-%d")
        devis_num = f"DEV-SL-{datetime.datetime.now().strftime('%Y%m%d')}"

        st.markdown(f"""
        <div class="devis-box">
            <h4 style="color:#38BDF8 !important;margin-top:0;">📄 عرض سعر أولي رسمي (DEVIS PROFORMA) - منصة Socio Lab</h4>
            <p><b>رقم العرض:</b> {devis_num} | <b>التاريخ:</b> {devis_date} | <b>المستفيد:</b> {client_devis_name}</p>
            <p><b>البيان:</b> {q_srv} (حجم العينة: {q_sample} مفردة، عدد الفقرات: {q_items}، نظام التسليم: {q_urgency})</p>
            <p style="font-size:1.05rem;color:#5EEAD4 !important;"><b>المبلغ الإجمالي التقديري: {est_price:,} دينار جزائري (DZD)</b></p>
        </div>
        """, unsafe_allow_html=True)

        devis_txt = f"SOCIO LAB - DEVIS PROFORMA\nرقم العرض: {devis_num}\nالتاريخ: {devis_date}\nالمستفيد: {client_devis_name}\nالخدمة: {q_srv}\nحجم العينة: {q_sample}\nعدد الفقرات: {q_items}\nمدة التسليم: {q_urgency}\nالمبلغ التقديري: {est_price} DZD\n".encode("utf-8-sig")
        st.download_button("📥 تحميل نسخة عرض السعر (Devis)", data=devis_txt, file_name=f"{devis_num}.txt")

    # ب. مشخص الاختبار الإحصائي
    with smart_tabs[1]:
        tc1, tc2, tc3 = st.columns(3)
        goal = tc1.selectbox("1. هدف الفرضية:", ["دراسة العلاقة والارتباط", "دراسة الفروق بين مجموعات", "دراسة الأثر والتنبؤ"])
        var_type = tc2.selectbox("2. نوع المتغيرات:", ["كمية / مقاييس ليكرت", "اسمية فئوية (نعم/لا، جنس)"])
        dist_type = tc3.selectbox("3. التوزيع وحجم العينة:", ["توزيع طبيعي (N ≥ 30)", "توزيع غير طبيعي أو عينة صغيرة"])

        if goal == "دراسة العلاقة والارتباط":
            rec = "اختبار كاي تربيع (Chi-Square)" if "اسمية" in var_type else ("معامل ارتباط بيرسون (Pearson r)" if "طبيعي" in dist_type else "معامل ارتباط سبيرمان (Spearman rho)")
        elif goal == "دراسة الفروق بين مجموعات":
            grp = st.radio("عدد المجموعات:", ["مجموعتان مستقلتان", "3 مجموعات فأكثر"], horizontal=True)
            if "مجموعتان" in grp:
                rec = "اختبار (Independent T-Test)" if "طبيعي" in dist_type else "اختبار مان-ويتني (Mann-Whitney U)"
            else:
                rec = "تحليل التباين الأحادي (ANOVA)" if "طبيعي" in dist_type else "اختبار كروسكال-واليس (Kruskal-Wallis)"
        else:
            rec = "تحليل الانحدار الخطي البسيط أو المتعدد (Linear / Multiple Regression)"
        st.success(f"🎯 **الاختبار الإحصائي الأنسب:** {rec}")

    # ج. حاسبة حجم العينة
    with smart_tabs[2]:
        cc1, cc2, cc3 = st.columns(3)
        pop_n = cc1.number_input("حجم مجتمع الدراسة (N):", min_value=10, max_value=1000000, value=1000, step=50)
        conf = cc2.selectbox("مستوى الثقة:", ["95% (Z = 1.96)", "99% (Z = 2.58)"])
        err = cc3.selectbox("هامش الخطأ:", ["5% (0.05)", "3% (0.03)"])
        z = 1.96 if "95%" in conf else 2.58
        e = 0.05 if "5%" in err else 0.03
        n_inf = (z**2 * 0.25) / (e**2)
        s_size = math.ceil(n_inf / (1 + ((n_inf - 1) / pop_n)))
        st.success(f"📐 **حجم العينة العلمي المطلوب:** `{s_size}` مفردة.")

    # د. قاموس المصطلحات المنهجية والإحصائية (Methodology Glossary)
    with smart_tabs[3]:
        st.write("مرجع مبسط لأهم المصطلحات المنهجية والإحصائية باللغتين العربية والإنجليزية:")
        glossary_data = pd.DataFrame([
            {"المصطلح بالعربية": "الصدق البنائي (Construct Validity)", "الشرح المبسط": "مدى قياس فقرات الاستبيان للمفهوم النظري الذي صممت لقياسه فعليا، ويقاس غالبا بالاتساق الداخلي أو التحليل العاملي."},
            {"المصطلح بالعربية": "معامل ألفا كرونباخ (Cronbach's Alpha)", "الشرح المبسط": "مؤشر يقيس ثبات أداة القياس واتساق إجابات المبحوثين، وتعد القيمة 0.70 فأكثر مقبولة علميا."},
            {"المصطلح بالعربية": "الدلالة الإحصائية (Statistical Significance - p-value)", "الشرح المبسط": "احتمال أن تكون النتيجة ناتجة عن الصدفة؛ إذا كانت أقل من 0.05 فالعلاقة أو الفروق دالة إحصائيا."},
            {"المصطلح بالعربية": "المتغير الوسيط (Mediating Variable)", "الشرح المبسط": "متغير يفسر الآلية التي يؤثر بها المتغير المستقل في المتغير التابع (حلقة وصل بينهما)."},
            {"المصطلح بالعربية": "العينة القصدية (Purposive Sample)", "الشرح المبسط": "عينة غير احتمالية يختار فيها الباحث مفردات محددة لامتلاكها خصائص أو خبرة دقيقة تخدم موضوع الدراسة."},
            {"المصطلح بالعربية": "التحليل الموضوعاتي (Thematic Analysis)", "الشرح المبسط": "منهجية كيفية لتحليل نصوص المقابلات واستخراج الأنماط والمواضيع المتكررة ذات المعنى."}
        ])
        search_term = st.text_input("🔍 ابحث عن مصطلح منهجي أو إحصائي:")
        if search_term:
            filtered_g = glossary_data[glossary_data["المصطلح بالعربية"].str.contains(search_term, case=False) | glossary_data["الشرح المبسط"].str.contains(search_term, case=False)]
            st.dataframe(filtered_g, use_container_width=True)
        else:
            st.dataframe(glossary_data, use_container_width=True)

    # هـ. قائمة التحقق المنهجية
    with smart_tabs[4]:
        chk1 = st.checkbox("تطابق عنوان الدراسة مع الإشكالية والفرضيات والأهداف.")
        chk2 = st.checkbox("تحكيم أداة القياس وحساب الصدق والثبات (ألفا كرونباخ ≥ 0.70).")
        chk3 = st.checkbox("تنظيف قاعدة البيانات من القيم المفقودة والاستمارات العشوائية.")
        chk4 = st.checkbox("التحقق من شروط الاختبارات الإحصائية (الاعتدالية وتجانس التباين).")
        chk5 = st.checkbox("ربط التعليق على الجداول بالإطار النظري (تفسير سوسيولوجي).")
        chk6 = st.checkbox("توثيق جميع المراجع وفق نظام APA بدقة.")
        score = sum([chk1, chk2, chk3, chk4, chk5, chk6])
        st.progress(score / 6)
        st.write(f"**نسبة جاهزية بحثك:** `{int((score/6)*100)}%`")

# --- 8. نماذج من أعمالنا (Portfolio) ---
with tabs[7]:
    st.markdown('<div class="sec-head">📂 نماذج من أعمالنا ودراسات الحالة (Portfolio & Case Studies)</div>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    with p1:
        st.markdown('<div class="info-card card-indigo"><span class="tag tag-indigo">دراسة حالة 01</span><h3 class="card-title" style="margin-top:8px;">معالجة عدم اعتدالية التوزيع في دراسة سوسيولوجية</h3><p class="card-text"><b>المشكلة:</b> رفض مبدئي لنتائج باحث بسبب استخدام T-Test المعلمي على عينة صغيرة (N=60) غير طبيعية التوزيع.<br><b>الحل:</b> فحص Shapiro-Wilk، التحول المنهجي لاختبار مان-ويتني اللامعلمي، وتنسيق الجداول وفق معيار APA 7th.</p></div>', unsafe_allow_html=True)
    with p2:
        st.markdown('<div class="info-card card-teal"><span class="tag tag-teal">دراسة حالة 02</span><h3 class="card-title" style="margin-top:8px;">رفع معامل الثبات من 0.61 إلى 0.86 وتنقية العينة</h3><p class="card-text"><b>المشكلة:</b> استطلاع رأي لجمعية محلية (220 استمارة) أظهر تشتتا وضعفا في ثبات المقياس.<br><b>الحل:</b> استبعاد 18 استمارة عشوائية متناقضة وحذف فقرتين مشوشتين، مما رفع الثبات إلى 0.86.</p></div>', unsafe_allow_html=True)

# --- 9. لوحة تحكم العميل ونظام تتبع الطلبات ---
with tabs[8]:
    st.markdown('<div class="sec-head">📊 لوحة تتبع الطلبات وأرشيف الملفات (Client Dashboard)</div>', unsafe_allow_html=True)
    track_code = st.text_input("🔑 أدخل رمز متابعة الطلب (جرب الرمز التجريبي: SL-2026-101):", value="SL-2026-101").strip()

    if track_code in st.session_state.orders_db:
        order = st.session_state.orders_db[track_code]
        st.markdown(f'<div class="info-card card-teal"><h3 class="card-title">ملف الطلب: {track_code}</h3><p class="card-text"><b>صاحب الطلب:</b> {order["client"]} | <b>الخدمة:</b> {order["service"]}</p><p class="card-text"><b>تحديث الفريق:</b> {order["notes"]}</p></div>', unsafe_allow_html=True)

        stages = order["stages"]
        curr = order["stage_idx"]
        st.progress((curr + 1) / len(stages))
        cols_st = st.columns(len(stages))
        for i, st_name in enumerate(stages):
            prefix = "✅" if i <= curr else "⏳"
            cols_st[i].markdown(f"**{prefix} {st_name}**")

        sample_csv = "المتغير,المتوسط,الانحراف_المعياري\nتأثير_الرفاق,3.84,0.68\n".encode("utf-8-sig")
        st.download_button("📥 تحميل ملف المخرجات الأولي من الأرشيف", data=sample_csv, file_name=f"{track_code}_Results.csv")

        rev_note = st.text_area("✍️ إرسال ملاحظات الأستاذ المشرف أو طلب تعديل:")
        if st.button("إرسال طلب التعديل"):
            if rev_note:
                st.success("تم إرفاق ملاحظات التعديل بملفك بنجاح.")
    else:
        st.warning("رمز الطلب غير موجود.")

# --- 10. اطلب خدمة وبوابة الدفع المرنة ---
with tabs[9]:
    st.markdown('<div class="sec-head">📅 نموذج طلب خدمة أو منتج رقمي أو شراكة</div>', unsafe_allow_html=True)
    with st.form("order_form"):
        fc1, fc2 = st.columns(2)
        with fc1:
            c_name = st.text_input("👤 الاسم الكامل / المؤسسة / النادي العلمي:")
            c_contact = st.text_input("📱 البريد الإلكتروني / رقم الواتساب:")
            c_role = st.selectbox("🎓 الصفة:", ["طالب ماستر", "طالب دكتوراه", "أستاذ باحث", "مؤسسة أو جمعية", "نادي طلابي / مخبر بحث"])
        with fc2:
            c_srv = st.selectbox("💼 نوع الطلب:", [
                "تصميم استبيان وبناء أداة بحث",
                "تحليل إحصائي وتفريغ بيانات SPSS",
                "دراسة كيفية (تحليل مقابلات / NVivo / مختلط)",
                "تحويل مذكرة إلى مقال علمي / عرض مناقشة / بوستر",
                "منتج رقمي (كتيب تطبيقي / حزمة قوالب / مقياس محكم)",
                "تحكيم أداة دراسة عبر شبكة الأساتذة المحكمين",
                "طلب شراكة علمية أو رعاية ملتقى دراسي"
            ])
            c_date = st.date_input("📅 الموعد النهائي المقترح:", value=datetime.date.today() + datetime.timedelta(days=7))
            c_files = st.file_uploader("📎 إرفاق ملفات (Word, Excel, SPSS, PDF):", type=["doc", "docx", "xlsx", "csv", "sav", "pdf"], accept_multiple_files=True)

        c_desc = st.text_area("📝 تفاصيل الطلب أو الدراسة:")
        if st.form_submit_button("🚀 إرسال الطلب والحصول على رمز التتبع"):
            if c_name and c_contact:
                new_id = f"SL-2026-{102 + len(st.session_state.orders_db)}"
                st.session_state.orders_db[new_id] = {
                    "client": f"{c_name} ({c_role})",
                    "service": c_srv,
                    "stage_idx": 0,
                    "stages": ["تم استلام الملفات", "قيد المراجعة المنهجية", "مرحلة تنظيف البيانات", "التحليل الإحصائي", "جاهز للتسليم"],
                    "notes": "تم استلام طلبك بنجاح وهو قيد التقييم الأولي."
                }
                st.success(f"تم تسجيل طلبك بنجاح! رمز متابعة طلبك في لوحة التحكم هو: **{new_id}**")
            else:
                st.warning("يرجى إدخال الاسم الكامل ووسيلة التواصل.")

    st.markdown('<div class="sec-head">💳 بوابة الدفع المرنة والأسئلة الشائعة (FAQ & Payment)</div>', unsafe_allow_html=True)
    pay_col, faq_col = st.columns(2)
    with pay_col:
        st.markdown('<div class="info-card card-indigo"><h3 class="card-title">💳 خيارات الدفع المرنة المتاحة</h3><p class="card-text">• <b>الدفع البريدي والإلكتروني:</b> الحساب البريدي الجاري (CCP) أو تطبيق بريدي موب (BaridiMob).<br>• <b>التحويل البنكي والفوترة الرسمية:</b> متاح للمؤسسات، الجمعيات، ومخابر البحث.<br>• <b>الدفع المرن على دفعتين:</b> 50% عند اعتماد خطة العمل و50% عند جاهزية المخرجات النهائية للمشاريع الكبيرة.</p></div>', unsafe_allow_html=True)
    with faq_col:
        with st.expander("❓ كم يستغرق إنجاز التحليل الإحصائي أو الكيفي؟"):
            st.write("تتراوح المدة بين 3 إلى 7 أيام عمل حسب حجم العينة أو عدد المقابلات، مع توفر خيار المعالجة المستعجلة.")
        with st.expander("❓ ماذا لو طلب المشرف تعديلا على الجداول أو الاختبارات؟"):
            st.write("نلتزم بإجراء التعديلات التي يطلبها المشرف مجانا ضمن نطاق الدراسة المتفق عليه عبر لوحة التتبع.")
        with st.expander("❓ هل تشرحون لي النتائج قبل موعد المناقشة؟"):
            st.write("نعم، يتضمن كل عمل جلسة شرح توضيحية (حضوريا بسوق أهراس أو عن بعد) لفهم النتائج والدفاع عنها علميا.")
