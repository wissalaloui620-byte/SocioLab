import streamlit as st
import pandas as pd
import numpy as np
import math, datetime, base64, glob

# ==========================================
# 1. إعدادات الصفحة والتنسيق البصري
# ==========================================
st.set_page_config(page_title="Socio Lab", page_icon="🏛️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lobster&family=Readex+Pro:wght@300;400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Readex Pro', sans-serif !important; direction: rtl; text-align: right; }
#MainMenu, footer { visibility: hidden; }
header { background: transparent !important; }
.stApp { background: radial-gradient(circle at 15% 10%, #0A2540 0%, #051324 55%, #020813 100%) !important; color: #F8FAFC !important; }
h1, h2, h3, h4, h5, p, label, .stMarkdown { color: #F1F5F9 !important; }
div[data-testid="stAlert"] { background: rgba(10, 32, 64, 0.95) !important; border: 1px solid #38BDF8 !important; border-right: 5px solid #38BDF8 !important; border-radius: 12px !important; }
div[data-testid="stAlert"] * { color: #F8FAFC !important; }
.top-navbar { background: rgba(8, 25, 48, 0.88); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 20px; padding: 18px 30px; margin-bottom: 22px; display: flex; justify-content: space-between; align-items: center; }
.brand-box { display: flex; align-items: center; gap: 18px; }
.brand-logo { width: 64px; height: 64px; border-radius: 15px; background: linear-gradient(135deg, #0284C7, #1E3A8A); display: flex; align-items: center; justify-content: center; font-family: 'Lobster', cursive !important; font-size: 1.7rem; color: #FFF; }
.brand-title { font-family: 'Lobster', cursive !important; font-size: 2.6rem !important; direction: ltr !important; display: inline-block; background: linear-gradient(180deg, #FFF 15%, #BAE6FD 65%, #7DD3FC 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; line-height: 1.1; }
.brand-sub { color: #CBD5E1 !important; font-size: 0.9rem; margin: 5px 0 0 0; }
.loc-badge { background: rgba(56, 189, 248, 0.14); border: 1px solid rgba(56, 189, 248, 0.4); color: #7DD3FC !important; padding: 8px 16px; border-radius: 999px; font-size: 0.84rem; font-weight: 600; }
.hero-box { background: linear-gradient(135deg, rgba(14, 48, 92, 0.7), rgba(7, 20, 40, 0.95)); border: 1px solid rgba(56, 189, 248, 0.35); border-right: 6px solid #38BDF8; border-radius: 20px; padding: 30px 36px; margin-bottom: 24px; }
.info-card { background: linear-gradient(145deg, rgba(15, 38, 72, 0.75), rgba(8, 22, 44, 0.94)); border: 1px solid rgba(56, 189, 248, 0.22); border-top: 3px solid #38BDF8; border-radius: 18px; padding: 22px; height: 100%; margin-bottom: 18px; }
.card-title { font-size: 1.18rem; font-weight: 700; color: #FFF !important; margin: 0 0 10px 0; }
.card-text { font-size: 0.92rem; color: #CBD5E1 !important; line-height: 1.75; }
.out-box { background: rgba(6, 182, 212, 0.14); border-right: 3px solid #38BDF8; padding: 10px 14px; border-radius: 8px; font-size: 0.86rem; color: #7DD3FC !important; margin-top: 10px; }
.tag { display: inline-block; padding: 4px 11px; border-radius: 999px; font-size: 0.76rem; font-weight: 600; background: rgba(56, 189, 248, 0.16); color: #7DD3FC; border: 1px solid rgba(56, 189, 248, 0.3); margin: 4px 0 0 5px; }
.tag-green { background: rgba(16, 185, 129, 0.16); color: #6EE7B7; border-color: rgba(16, 185, 129, 0.35); }
.tag-amber { background: rgba(245, 158, 11, 0.16); color: #FCD34D; border-color: rgba(245, 158, 11, 0.35); }
.sec-head { font-size: 1.42rem; font-weight: 700; color: #38BDF8 !important; margin: 22px 0 14px 0; padding-bottom: 8px; border-bottom: 1px solid rgba(56, 189, 248, 0.25); }
.cta-banner { background: linear-gradient(135deg, rgba(2, 132, 199, 0.28), rgba(15, 38, 72, 0.92)); border: 1px solid rgba(56, 189, 248, 0.5); border-right: 6px solid #38BDF8; border-radius: 16px; padding: 20px 26px; margin-top: 20px; }
.stTabs [data-baseweb="tab-list"] { gap: 6px; background: rgba(8, 24, 46, 0.95); padding: 8px; border-radius: 16px; border: 1px solid rgba(56, 189, 248, 0.25); flex-wrap: wrap; }
.stTabs [data-baseweb="tab"] { border-radius: 10px !important; padding: 9px 15px !important; font-weight: 700 !important; font-size: 0.9rem !important; color: #94A3B8 !important; background: transparent !important; border: none !important; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #0284C7, #2563EB) !important; color: #FFF !important; }
.stButton > button { background: linear-gradient(135deg, #0284C7, #2563EB) !important; color: #FFF !important; font-weight: 700 !important; border-radius: 10px !important; padding: 0.6rem 1.4rem !important; border: 1px solid rgba(125, 211, 252, 0.4) !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. تهيئة البيانات والشعار
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

if "custom_logo_b64" not in st.session_state:
    st.session_state.custom_logo_b64 = None
    imgs = []
    for p in ["*logo*", "*.png", "*.jpg", "*.jpeg"]:
        imgs.extend(glob.glob(p))
    if imgs:
        try:
            with open(imgs[0], "rb") as f:
                st.session_state.custom_logo_b64 = base64.b64encode(f.read()).decode()
        except Exception:
            pass

logo_html = f'<img src="data:image/png;base64,{st.session_state.custom_logo_b64}" style="width:74px;height:74px;border-radius:16px;object-fit:cover;border:2px solid #38BDF8;">' if st.session_state.custom_logo_b64 else '<div class="brand-logo">SL</div>'

st.markdown(f"""
<div class="top-navbar">
    <div class="brand-box">
        {logo_html}
        <div>
            <h1 class="brand-title">Socio Lab</h1>
            <p class="brand-sub">منصة رقمية للاستشارات المنهجية السوسيولوجية، التحليل الإحصائي، وتجهيز البيانات</p>
        </div>
    </div>
    <div class="loc-badge">📍 حضوريا بسوق أهراس | 🌐 رقميا عبر 58 ولاية</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 3. هيكل الصفحات المتكامل (8 تبويبات)
# ==========================================
tabs = st.tabs([
    "🏛️ الرئيسية",
    "🧭 من نحن والنزاهة",
    "💼 الخدمات والمؤسسات B2B",
    "🎓 الدورات التكوينية",
    "📂 نماذج الأعمال (Portfolio)",
    "🧰 الأدوات الذكية المجانية",
    "📊 لوحة تتبع الطلبات",
    "📅 اطلب خدمة والدفع"
])

# --- 1. الرئيسية ---
with tabs[0]:
    st.markdown("""
    <div class="hero-box">
        <h2 style="font-size:1.9rem;margin-top:0;">من الفكرة البحثية إلى النتائج المحكمة.. شريكك المنهجي والإحصائي الدقيق.</h2>
        <p style="font-size:1.05rem;line-height:1.85;margin-bottom:0;">
            في المنصة الرقمية <span style="font-family:'Lobster',cursive;font-size:1.3rem;color:#7DD3FC;">Socio Lab</span>، نحول البيانات الميدانية الخام إلى رؤى سوسيولوجية وعلمية رصينة. نرافق طلبة الدراسات العليا، الباحثين، والمؤسسات في تصميم أدوات القياس، تنظيف البيانات، والتحليل الإحصائي المتقدم وفق أعلى معايير الجودة والنزاهة العلمية.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">🎯 الفئات المستهدفة (من يستفيد من المنصة الرقمية؟)</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="info-card"><h3 class="card-title">🎓 طلبة الليسانس والماستر</h3><p class="card-text">طلبة جامعة سوق أهراس والجامعات الجزائرية المقبلون على إعداد مذكرات التخرج وتقارير التربص الميداني ويحتاجون مرافقة منهجية وإحصائية دقيقة.</p><span class="tag">مذكرات التخرج</span><span class="tag">تقارير التربص</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="info-card"><h3 class="card-title">🔬 طلبة الدكتوراه والباحثون</h3><p class="card-text">الباحثون، الأساتذة، وفرق ومخابر البحث الراغبون في تحكيم المقاييس السيكومترية، تنظيف قواعد البيانات، وتنسيق الجداول للنشر العلمي المحكم.</p><span class="tag">أطروحات الدكتوراه</span><span class="tag">مقالات محكمة</span></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="info-card"><h3 class="card-title">🏢 المؤسسات، الإدارات، والجمعيات</h3><p class="card-text">المؤسسات الاقتصادية، الإدارات، والجمعيات التي تحتاج إلى دراسات ميدانية، استطلاعات رأي، وقياس رضا المستفيدين لترشيد قراراتها.</p><span class="tag">استطلاعات الرأي</span><span class="tag tag-amber">حلول B2B</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">✨ لماذا تختار المنصة الرقمية Socio Lab؟</div>', unsafe_allow_html=True)
    r1, r2, r3, r4 = st.columns(4)
    r1.markdown('<div class="info-card"><h4 class="card-title">📖 قراءة سوسيولوجية لا أرقام صماء</h4><p class="card-text">نربط المؤشرات الإحصائية بالسياق النظري والميداني لدراستك.</p></div>', unsafe_allow_html=True)
    r2.markdown('<div class="info-card"><h4 class="card-title">🎯 دقة منهجية صارمة</h4><p class="card-text">نعتمد أحدث الأساليب العلمية في بناء المقاييس واختيار الاختبارات الأنسب.</p></div>', unsafe_allow_html=True)
    r3.markdown('<div class="info-card"><h4 class="card-title">🔒 سرية وأمان تام</h4><p class="card-text">حماية أفكارك البحثية وبيانات المبحوثين بموجب ميثاق صارم للخصوصية.</p></div>', unsafe_allow_html=True)
    r4.markdown('<div class="info-card"><h4 class="card-title">⏱️ التزام بالمواعيد</h4><p class="card-text">تسليم المخرجات في الآجال المحددة مع جلسات شرح ومناقشة للنتائج.</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">⚙️ خطوات العمل (How It Works)</div>', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    s1.markdown('<div class="info-card"><h4 class="card-title">1. إرسال الطلب والملفات</h4><p class="card-text">تملأ نموذج الطلب وتحدد الخدمة وترفق مسودة بحثك أو بياناتك.</p></div>', unsafe_allow_html=True)
    s2.markdown('<div class="info-card"><h4 class="card-title">2. التقييم وتحديد الخطة</h4><p class="card-text">ندرس ملفك ونوافيك بخطة العمل والمدة والتكلفة خلال 24 ساعة.</p></div>', unsafe_allow_html=True)
    s3.markdown('<div class="info-card"><h4 class="card-title">3. التنفيذ والمتابعة</h4><p class="card-text">يبدأ العمل المنهجي أو الإحصائي مع تتبع المراحل عبر لوحتك.</p></div>', unsafe_allow_html=True)
    s4.markdown('<div class="info-card"><h4 class="card-title">4. التسليم والشرح</h4><p class="card-text">تستلم ملفاتك النهائية مع جلسة توضيحية لشرح النتائج قبل المناقشة.</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="cta-banner">🚀 <b>ابدأ الآن:</b> انتقل إلى تبويب <b>«📅 اطلب خدمة والدفع»</b> في أعلى الشاشة لطلب استشارتك أو حجز خدمتك البحثية.</div>', unsafe_allow_html=True)

# --- 2. من نحن وميثاق النزاهة العلمية ---
with tabs[1]:
    st.markdown('<div class="sec-head">🧭 من نحن (About Us)</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-box"><p class="card-text" style="font-size:1.05rem;"><b>Socio Lab</b> هو مختبر استشاري وبحثي ومنصة رقمية متخصصة في المنهجية السوسيولوجية والتحليل الإحصائي للبيانات الاجتماعية والإنسانية. تأسست المنصة لسد الفجوة بين الجانب النظري في الأبحاث الأكاديمية والتطبيق الميداني والإحصائي الدقيق، عبر تقديم حلول بحثية متكاملة تجمع بين الخبرة الميدانية والتمكن التقني.</p></div>', unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    a1.markdown('<div class="info-card"><h3 class="card-title">🔭 رؤيتنا</h3><p class="card-text">أن نكون المرجع الأول والموثوق للباحثين والمؤسسات في العالم العربي للارتقاء بجودة الإنتاج العلمي والقرارات المبنية على البيانات الدقيقة.</p></div>', unsafe_allow_html=True)
    a2.markdown('<div class="info-card"><h3 class="card-title">🎯 رسالتنا</h3><p class="card-text">تمكين الباحثين وطلبة الماستر والدكتوراه والمؤسسات من إنجاز دراسات ميدانية محكمة، عبر توفير استشارات منهجية احترافية، وأدوات قياس موثوقة، وتحليلات إحصائية دقيقة تلتزم بأخلاقيات البحث العلمي وتنبذ التزييف أو الانتحال.</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">⚖️ ميثاق النزاهة العلمية وسياسة العمل (Academic Integrity Charter)</div>', unsafe_allow_html=True)
    ch1, ch2 = st.columns(2)
    with ch1:
        st.markdown("""
        <div class="info-card" style="border-top-color:#EF4444;">
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
        <div class="info-card" style="border-top-color:#10B981;">
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
        st.markdown('<div class="info-card"><h3 class="card-title">3. التحكيم والضبط المنهجي</h3><p class="card-text">• تدقيق صياغة الإشكالية، التساؤلات، والفرضيات ومدى قابليتها للاختبار.<br>• تحديد نوع العينة وحجمها المناسب لمجتمع الدراسة.<br>• مواءمة الإطار النظري مع مؤشرات القياس الميداني.</p><div class="out-box"><b>المخرجات:</b> تقرير مفصل بالملاحظات المنهجية والتعديلات المقترحة خطوة بخطوة.</div></div>', unsafe_allow_html=True)
    with sv2:
        st.markdown('<div class="info-card"><h3 class="card-title">2. التحليل الإحصائي وتفريغ البيانات (SPSS)</h3><p class="card-text">• تفريغ البيانات، ترميزها، وتنظيفها من القيم الشاذة والمفقودة.<br>• حساب الخصائص السيكومترية (الصدق البنائي، الاتساق الداخلي، ألفا كرونباخ).<br>• إجراء الاختبارات الوصفية والاستدلالية وفق طبيعة التوزيع.</p><div class="out-box"><b>المخرجات:</b> ملف SPSS الأصلي + تقرير تحليلي بالجداول والرسوم مع التعليق السوسيولوجي الأولي.</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="info-card"><h3 class="card-title">4. التوثيق والتدقيق الأكاديمي</h3><p class="card-text">• توثيق المراجع في المتن وفي القائمة النهائية بدقة وفق نظام (APA).<br>• التدقيق اللغوي والأسلوبي للنصوص الأكاديمية لضمان رصانة الأسلوب.<br>• تنسيق الجداول والأشكال البيانية وفق شروط المجلات المحكمة.</p><div class="out-box"><b>المخرجات:</b> ورقة بحثية أو فصل تطبيقي منسق ومضبوط وفق معايير النشر الأكاديمي.</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">🏢 فضاء المؤسسات والجمعيات (B2B / Institutional Solutions)</div>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    b1.markdown('<div class="info-card"><h3 class="card-title">📊 دراسات قياس الأثر الاجتماعي (Social Impact Assessment)</h3><p class="card-text">تقييم البرامج والمشاريع التنموية والاجتماعية لصالح الجمعيات، الهيئات العمومية، ومراكز الدراسات لقياس مدى تحقق الأهداف الميدانية وتحديد مؤشرات النجاح والفجوات.</p><span class="tag tag-amber">تقارير تنفيذية لصناع القرار</span></div>', unsafe_allow_html=True)
    b2.markdown('<div class="info-card"><h3 class="card-title">🗳️ استطلاعات الرأي وقياس رضا المستفيدين والموظفين</h3><p class="card-text">تصميم وتنفيذ مسوح ميدانية أو إلكترونية شاملة للمؤسسات الاقتصادية والخدمية، وتحليل اتجاهات الجمهور الداخلي والخارجي مع تقديم توصيات عملية قابلة للتنفيذ.</p><span class="tag tag-green">مسوح ميدانية وإلكترونية شاملة</span></div>', unsafe_allow_html=True)

# --- 4. الدورات التكوينية ---
with tabs[3]:
    st.markdown('<div class="sec-head">🎓 البرامج والدورات التكوينية التطبيقية (حضوريا وعن بعد)</div>', unsafe_allow_html=True)
    t1, t2 = st.columns(2)
    t1.markdown('<div class="info-card"><h3 class="card-title">💻 الدورة 1: الأساسيات التطبيقية لتحليل البيانات ببرنامج SPSS</h3><p class="card-text">إعداد قاعدة البيانات، ترميز الاستبيانات، حساب التكرارات والنسب، المتوسطات والانحراف المعياري، وتنسيق الجداول.</p><span class="tag">12 ساعة تطبيقية</span><span class="tag tag-green">للمبتدئين</span></div>', unsafe_allow_html=True)
    t1.markdown('<div class="info-card"><h3 class="card-title">📐 الدورة 2: هندسة الاستبيانات الإلكترونية وبناء المقاييس</h3><p class="card-text">تحويل الفرضيات إلى محاور وفقرات قياس، تصميم الاستبيان على Google Forms و KoboToolbox، وتجنب الأخطاء المنهجية.</p><span class="tag">8 ساعات تطبيقية</span></div>', unsafe_allow_html=True)
    t2.markdown('<div class="info-card"><h3 class="card-title">📈 الدورة 3: الإحصاء الاستدلالي المتقدم واختبار الفرضيات</h3><p class="card-text">فحص الصدق والثبات، شروط الاختبارات المعلمية واللامعلمية، الارتباط والفروق والانحدار، والقراءة السوسيولوجية للنتائج.</p><span class="tag">15 ساعة معمقة</span><span class="tag tag-amber">مستوى متقدم</span></div>', unsafe_allow_html=True)
    t2.markdown('<div class="info-card"><h3 class="card-title">🏛️ الدورة 4: منهجية إعداد البحوث والمذكرات وفق IMRAD و APA</h3><p class="card-text">الهيكلة المنهجية للدراسة الميدانية، التوثيق العلمي والمراجع بطريقة APA، ومهارات العرض والدفاع أمام لجنة المناقشة.</p><span class="tag">10 ساعات</span></div>', unsafe_allow_html=True)

# --- 5. نماذج من أعمالنا (Portfolio & Case Studies) ---
with tabs[4]:
    st.markdown('<div class="sec-head">📂 نماذج من أعمالنا ودراسات الحالة (Portfolio & Case Studies)</div>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    with p1:
        st.markdown("""
        <div class="info-card">
            <span class="tag">دراسة حالة (Case Study 01)</span>
            <h3 class="card-title" style="margin-top:10px;">معالجة تشتت البيانات وعدم اعتدالية التوزيع في دراسة سوسيولوجية</h3>
            <p class="card-text">
                <b>المشكلة:</b> واجه باحث في علم الاجتماع رفضا مبدئيا لنتائجه بسبب استخدامه اختبار (T-Test) المعلمي على عينة صغيرة (N=60) ذات توزيع غير طبيعي.<br>
                <b>تدخل Socio Lab:</b> إعادة تنظيف قاعدة البيانات، فحص اعتدالية التوزيع باختبار Shapiro-Wilk، التحول المنهجي إلى اختبار مان-ويتني (Mann-Whitney U) اللامعلمي، وإعادة صياغة الجداول وفق معيار APA 7th مع تعليق سوسيولوجي رصين.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="info-card">
            <span class="tag tag-green">دراسة حالة (Case Study 02)</span>
            <h3 class="card-title" style="margin-top:10px;">كشف الاستمارات العشوائية ورفع معامل الثبات من 0.61 إلى 0.86</h3>
            <p class="card-text">
                <b>المشكلة:</b> استلمت جمعية محلية 220 استمارة استطلاع رأي أظهرت نتائج متناقضة وضعفا في ثبات المقياس.<br>
                <b>تدخل Socio Lab:</b> إخضاع الملف للفحص الآلي، اكتشاف واستبعاد 18 استمارة ذات إجابات نمطية متناقضة، وحذف فقرتين مشوشتين في المقياس، مما رفع معامل ألفا كرونباخ إلى 0.86 وقدم تقريرا دقيقا لصناع القرار.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 📋 عينة نموذجية لتنسيق الجداول والتعليق السوسيولوجي المعتمد في تقارير Socio Lab:")
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
        "🧭 مشخص الاختبار الإحصائي (Statistical Test Selector)",
        "🧮 حاسبة حجم العينة (Sample Size)",
        "✅ قائمة التحقق المنهجية قبل الإيداع (Research Checklist)"
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
        <div class="info-card">
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

        st.markdown("#### 📥 أرشيف الملفات والمخرجات الجاهزة للتحميل:")
        sample_csv = "المتغير,المتوسط,الانحراف_المعياري\nتأثير_الرفاق,3.84,0.68\n".encode("utf-8-sig")
        st.download_button("📥 تحميل ملف النتائج الأولي المعتمد (CSV / Excel)", data=sample_csv, file_name=f"{track_code}_Results.csv")

        st.markdown("#### ✍️ نظام طلب التعديلات (ملاحظات الأستاذ المشرف أو لجنة المناقشة):")
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
        <div class="info-card">
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
