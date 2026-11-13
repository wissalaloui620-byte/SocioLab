import math
import urllib.parse
import streamlit as st

# ---------------------------------------------------------
# اعدادات رقم الواتساب الخاص بالمنصة (ضعي رقمك هنا بصيغة 213XXXXXXXXX)
# ---------------------------------------------------------
WHATSAPP_NUMBER = "213600000000"

# 1. اعدادات الصفحة
st.set_page_config(
    page_title="Socio Lab | المختبر الاستشاري للبحث السوسيولوجي والتحليل الاحصائي",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. التنسيق العام (CSS) بدون مسافات بادئة
css_styles = """<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Great+Vibes&display=swap');
#MainMenu, header, footer {visibility: hidden;}
.block-container {padding: 0rem !important; max-width: 100% !important;}
.stApp {background-color: #F8FAFC; font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; color: #1E293B;}
h1, h2, h3, h4, p, span, div, label, input, select, textarea, button {font-family: 'Cairo', sans-serif;}
.sl-navbar {background-color: #0A192F; border-bottom: 1px solid #163A5F; padding: 12px 6%; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 999;}
.sl-brand {display: flex; align-items: center; gap: 12px;}
.sl-sigma {width: 38px; height: 38px; background-color: #0F2942; border: 1px solid rgba(20, 184, 166, 0.45); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #2DD4BF; font-weight: 800; font-size: 18px;}
.sl-logo-script {font-family: 'Great Vibes', cursive !important; font-size: 26px; color: #FFFFFF; line-height: 1;}
.sl-logo-sub {font-size: 10px; color: #2DD4BF; display: block; margin-top: 2px;}
.sl-nav-links {display: flex; gap: 24px;}
.sl-nav-links a {color: #E2E8F0; text-decoration: none; font-size: 13.5px; font-weight: 600;}
.sl-nav-links a:hover {color: #2DD4BF;}
.sl-cta-top {background-color: #F59E0B; color: #0A192F !important; font-weight: 700; font-size: 13px; padding: 8px 18px; border-radius: 8px; text-decoration: none;}
.sl-hero {background-color: #0A192F; background-image: radial-gradient(rgba(20, 184, 166, 0.14) 1px, transparent 1px); background-size: 26px 26px; color: #FFFFFF; padding: 50px 6%; border-bottom: 1px solid #163A5F;}
.sl-hero-grid {max-width: 1180px; margin: 0 auto; display: grid; grid-template-columns: 1.25fr 0.95fr; gap: 36px; align-items: center;}
@media (max-width: 900px) {.sl-hero-grid {grid-template-columns: 1fr;} .sl-nav-links {display: none;}}
.sl-badge {display: inline-block; background-color: #0F2942; border: 1px solid rgba(20, 184, 166, 0.35); color: #2DD4BF; font-size: 11.5px; font-weight: 600; padding: 5px 14px; border-radius: 99px; margin-bottom: 14px;}
.sl-hero-title {font-size: 27px; font-weight: 800; line-height: 1.45; color: #FFFFFF; margin-bottom: 14px;}
.sl-hero-title span {color: #2DD4BF;}
.sl-hero-desc {color: #CBD5E1; font-size: 14px; line-height: 1.8; margin-bottom: 24px;}
.sl-hero-btns {display: flex; gap: 12px; flex-wrap: wrap;}
.sl-btn-amber {background-color: #F59E0B; color: #0A192F !important; font-weight: 700; font-size: 13.5px; padding: 10px 22px; border-radius: 10px; text-decoration: none;}
.sl-btn-outline {background-color: #0F2942; border: 1px solid #334155; color: #FFFFFF !important; font-weight: 600; font-size: 13.5px; padding: 10px 22px; border-radius: 10px; text-decoration: none;}
.sl-stat-card {background-color: #0F2942; border: 1px solid #1E3A5F; border-radius: 16px; padding: 20px; box-shadow: 0 15px 30px rgba(0,0,0,0.25);}
.sl-stat-header {display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1E3A5F; padding-bottom: 10px; margin-bottom: 14px;}
.sl-kpi-grid {display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 12px 0; text-align: center;}
.sl-kpi-box {background-color: #0A192F; border: 1px solid #1E3A5F; border-radius: 10px; padding: 8px;}
.sl-kpi-label {font-size: 11px; color: #94A3B8;}
.sl-kpi-val {font-size: 15px; font-weight: 700; margin-top: 2px;}
.sl-reading-box {background-color: #0A192F; border-right: 3px solid #14B8A6; padding: 10px 12px; border-radius: 6px; font-size: 12px; color: #E2E8F0; line-height: 1.65;}
.sl-section {max-width: 1180px; margin: 0 auto; padding: 45px 6%;}
.sl-sec-head {text-align: center; max-width: 620px; margin: 0 auto 32px auto;}
.sl-sec-tag {color: #14B8A6; font-size: 12.5px; font-weight: 700;}
.sl-sec-title {color: #0A192F; font-size: 22px; font-weight: 800; margin: 4px 0 8px 0;}
.sl-sec-sub {color: #64748B; font-size: 13.5px; margin: 0;}
.sl-services-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 18px;}
.sl-srv-card {background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 3.5px solid #14B8A6; border-radius: 14px; padding: 22px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);}
.sl-srv-card.navy-top {border-top-color: #0A192F;}
.sl-srv-card.amber-top {border-top-color: #F59E0B;}
.sl-srv-num {font-size: 16px; font-weight: 800; color: #14B8A6; margin-bottom: 6px;}
.sl-srv-title {font-size: 16px; font-weight: 700; color: #0A192F; margin-bottom: 8px;}
.sl-srv-desc {font-size: 13px; color: #475569; line-height: 1.7; margin: 0;}
.sl-result-banner {background-color: #F0FDFA; border: 1px solid #99F6E4; border-right: 4px solid #14B8A6; padding: 12px 15px; border-radius: 10px; margin-top: 12px; font-size: 13px; color: #0F2942;}
.sl-wa-btn {display: block; text-align: center; background-color: #10B981; color: #FFFFFF !important; font-weight: 700; font-size: 14px; padding: 12px 20px; border-radius: 10px; text-decoration: none; margin-top: 12px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);}
.sl-wa-btn:hover {background-color: #059669;}
.sl-integrity {background-color: #0A192F; color: #FFFFFF; text-align: center; padding: 45px 6%; margin-top: 35px;}
.sl-footer {background-color: #071120; color: #94A3B8; text-align: center; padding: 28px 6%; font-size: 12.5px; border-top: 1px solid #163A5F;}
div[data-baseweb="select"] > div, input, textarea {font-size: 13px !important; border-radius: 8px !important;}
label p {font-size: 13px !important; font-weight: 700 !important; color: #1E293B !important;}
</style>"""

st.markdown(css_styles, unsafe_allow_html=True)

# 3. الشريط العلوي والقسم الترحيبي
hero_html = """<div class="sl-navbar"><div class="sl-brand"><div class="sl-sigma">&Sigma;</div><div><div class="sl-logo-script">Socio Lab</div><span class="sl-logo-sub">للتحليل الاحصائي والمنهجية</span></div></div><div class="sl-nav-links"><a href="#services">خدماتنا</a><a href="#tools">الادوات التفاعلية</a><a href="#integrity">ميثاق النزاهة</a><a href="#order">اطلب خدمة</a></div><a href="#order" class="sl-cta-top">احجز استشارة</a></div><div class="sl-hero"><div class="sl-hero-grid"><div><div class="sl-badge">&mu; دقة منهجية • قراءة سوسيولوجية • توثيق APA</div><div class="sl-hero-title">من الفكرة البحثية الى النتائج المحكمة.. <span>شريكك المنهجي والاحصائي الدقيق</span></div><p class="sl-hero-desc">في <strong>Socio Lab</strong> نحول البيانات الميدانية الخام الى رؤى سوسيولوجية وعلمية رصينة. نرافق الباحثين، طلبة الدراسات العليا، والمؤسسات في تصميم ادوات القياس، تنظيف البيانات، والتحليل الاحصائي المتقدم عبر برنامج SPSS.</p><div class="sl-hero-btns"><a href="#order" class="sl-btn-amber">اطلب خدمتك البحثية الان</a><a href="#tools" class="sl-btn-outline">جرب الادوات الاحصائية المجانية</a></div></div><div class="sl-stat-card"><div class="sl-stat-header"><div><div style="font-size:11px; color:#2DD4BF; font-weight:700;">نموذج مخرجات Socio Lab</div><div style="font-size:14px; font-weight:700; color:#FFFFFF;">تحليل التوزيع الطبيعي ومؤشرات الثبات</div></div><span style="background:rgba(20,184,166,0.18); color:#2DD4BF; font-size:11px; padding:3px 8px; border-radius:6px; font-family:monospace;">SPSS v28</span></div><div style="background:#0A192F; padding:10px; border-radius:10px; border:1px solid #1E3A5F;"><svg viewBox="0 0 300 95" style="width:100%; height:85px; display:block;"><defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#14B8A6" stop-opacity="0.45"/><stop offset="100%" stop-color="#14B8A6" stop-opacity="0.0"/></linearGradient></defs><line x1="10" y1="80" x2="290" y2="80" stroke="#334155" stroke-width="1"/><line x1="150" y1="12" x2="150" y2="80" stroke="#F59E0B" stroke-dasharray="3,3" stroke-width="1.3"/><path d="M 15 80 C 75 80, 105 12, 150 12 C 195 12, 225 80, 285 80 Z" fill="url(#g1)"/><path d="M 15 80 C 75 80, 105 12, 150 12 C 195 12, 225 80, 285 80" fill="none" stroke="#2DD4BF" stroke-width="2.2"/><text x="150" y="92" fill="#F59E0B" font-size="9" text-anchor="middle">&mu; = 3.84</text></svg></div><div class="sl-kpi-grid"><div class="sl-kpi-box"><div class="sl-kpi-label">الفا كرونباخ (&alpha;)</div><div class="sl-kpi-val" style="color:#2DD4BF;">0.892</div></div><div class="sl-kpi-box"><div class="sl-kpi-label">حجم العينة (N)</div><div class="sl-kpi-val" style="color:#FFFFFF;">60</div></div><div class="sl-kpi-box"><div class="sl-kpi-label">الدلالة (Sig)</div><div class="sl-kpi-val" style="color:#F59E0B;">0.001</div></div></div><div class="sl-reading-box"><strong>القراءة السوسيولوجية:</strong> تشير قيمة الفا كرونباخ (0.892) الى اتساق داخلي مرتفع جدا لاداة القياس، مع دلالة احصائية تؤكد اثر المتغير المستقل عند مستوى 0.01.</div></div></div></div>"""

st.markdown(hero_html, unsafe_allow_html=True)

# 4. قسم الخدمات البحثية والاحصائية
services_html = """<div id="services" class="sl-section"><div class="sl-sec-head"><div class="sl-sec-tag">حلول منهجية متكاملة</div><div class="sl-sec-title">خدمات منصة Socio Lab</div><p class="sl-sec-sub">نصمم الادوات ونحلل البيانات وفق الضوابط الاكاديمية المعتمدة في الجامعات والمجلات المحكمة.</p></div><div class="sl-services-grid"><div class="sl-srv-card"><div class="sl-srv-num">01</div><div class="sl-srv-title">تصميم وبناء ادوات البحث</div><p class="sl-srv-desc">صياغة الاستبيانات الورقية والالكترونية وبناء ادلة المقابلات المعمقة والملاحظة العلمية وفق ابعاد وفرضيات الدراسة مع دليل الترميز.</p></div><div class="sl-srv-card navy-top"><div class="sl-srv-num" style="color:#0A192F;">02</div><div class="sl-srv-title">التحليل الاحصائي وتنظيف البيانات (SPSS)</div><p class="sl-srv-desc">تفريغ البيانات وتنظيفها، حساب الصدق والثبات، واجراء الاختبارات الوصفية والاستدلالية مع قراءة سوسيولوجية معمقة للجداول.</p></div><div class="sl-srv-card amber-top"><div class="sl-srv-num" style="color:#F59E0B;">03</div><div class="sl-srv-title">الضبط المنهجي وتحكيم المقاييس</div><p class="sl-srv-desc">مراجعة الاشكالية والفرضيات، ضبط المعاينة، وتقييم الخصائص السيكومترية للمقاييس لضمان سلامة البناء المنهجي للدراسة.</p></div><div class="sl-srv-card navy-top"><div class="sl-srv-num" style="color:#0A192F;">04</div><div class="sl-srv-title">تحليل البيانات الكيفية</div><p class="sl-srv-desc">تفريغ المقابلات المعمقة وتحليل المضمون والتحليل الموضوعاتي للدراسات الميدانية والدراسات المختلطة (الكمية والكيفية).</p></div><div class="sl-srv-card"><div class="sl-srv-num">05</div><div class="sl-srv-title">التوثيق الاكاديمي (APA) والنشر</div><p class="sl-srv-desc">ضبط التوثيق في المتن وقائمة المراجع وفق معايير APA، وتنسيق اوراق المؤتمرات والمقالات العلمية للنشر في المجلات المحكمة.</p></div><div class="sl-srv-card amber-top"><div class="sl-srv-num" style="color:#F59E0B;">06</div><div class="sl-srv-title">مسوح المؤسسات ودراسات الاثر</div><p class="sl-srv-desc">تصميم وتنفيذ استطلاعات الراي ودراسات قياس الاثر الاجتماعي للمؤسسات والجمعيات وتقديم تقارير تنفيذية لصناع القرار.</p></div></div></div>"""

st.markdown(services_html, unsafe_allow_html=True)

# 5. قسم الادوات التفاعلية الذكية
tools_header_html = """<div id="tools" style="max-width:1180px; margin:0 auto; padding:10px 6% 15px 6%;"><div class="sl-sec-head"><div class="sl-sec-tag">مختبر الادوات المجانية</div><div class="sl-sec-title">الادوات التفاعلية لمساعدة الباحث</div><p class="sl-sec-sub">استخدم ادواتنا الذكية لتحديد الاختبار الاحصائي المناسب لفرضيتك او حساب حجم عينتك الممثلة فورا.</p></div></div>"""
st.markdown(tools_header_html, unsafe_allow_html=True)

_, col_t1, col_t2, _ = st.columns([0.06, 0.44, 0.44, 0.06], gap="large")

with col_t1:
    st.markdown('<div style="font-size:15.5px; font-weight:800; color:#0A192F; margin-bottom:10px;">1. مشخص الاختبار الاحصائي (SPSS)</div>', unsafe_allow_html=True)
    goal = st.selectbox(
        "هدف الفرضية البحثية:",
        [
            "قياس العلاقة الارتباطية بين متغيرين",
            "قياس الفروق بين مجموعتين مستقلتين (مثل: ذكور / اناث)",
            "قياس الفروق بين 3 مجموعات فاكثر (مثل: المستويات التعليمية)",
            "قياس اثر متغير مستقل على متغير تابع (التنبؤ)",
        ],
    )
    dist = st.selectbox(
        "طبيعة البيانات والتوزيع:",
        [
            "بيانات كمية تتبع التوزيع الطبيعي (معلمية)",
            "بيانات رتبية او لا تتبع التوزيع الطبيعي (لامعلمية)",
        ],
    )

    is_normal = "معلمية" in dist
    if "العلاقة" in goal:
        t_name = "معامل ارتباط بيرسون (Pearson Correlation)" if is_normal else "معامل ارتباط سبيرمان للرتب (Spearman Rho)"
        t_path = "Analyze > Correlate > Bivariate > Pearson" if is_normal else "Analyze > Correlate > Bivariate > Spearman"
    elif "مجموعتين" in goal:
        t_name = "اختبار ت لعينتين مستقلتين (Independent Samples T-Test)" if is_normal else "اختبار مان-ويتني (Mann-Whitney U Test)"
        t_path = "Analyze > Compare Means > Independent-Samples T Test" if is_normal else "Analyze > Nonparametric Tests > Independent Samples"
    elif "3 مجموعات" in goal:
        t_name = "تحليل التباين الاحادي (One-Way ANOVA)" if is_normal else "اختبار كروسكال-واليس (Kruskal-Wallis Test)"
        t_path = "Analyze > Compare Means > One-Way ANOVA" if is_normal else "Analyze > Nonparametric Tests > K Independent Samples"
    else:
        t_name = "الانحدار الخطي البسيط/المتعدد (Linear Regression)" if is_normal else "الانحدار اللوجستي او الترتيبي (Ordinal Regression)"
        t_path = "Analyze > Regression > Linear" if is_normal else "Analyze > Regression > Ordinal"

    st.markdown(f"""<div class="sl-result-banner"><strong>الاختبار المناسب:</strong> {t_name}<br><span style="font-family:monospace; font-size:11.5px; color:#0D9488;">{t_path}</span></div>""", unsafe_allow_html=True)

with col_t2:
    st.markdown('<div style="font-size:15.5px; font-weight:800; color:#0A192F; margin-bottom:10px;">2. حاسبة حجم العينة الممثلة (معادلة كوكران)</div>', unsafe_allow_html=True)
    pop_size = st.number_input("حجم مجتمع الدراسة الكلي (N):", min_value=10, value=500, step=10)
    margin_label = st.selectbox(
        "هامش الخطا المسموح به:",
        [
            "5% (مستوى ثقة 95% - القياسي في العلوم الاجتماعية)",
            "1% (مستوى ثقة 99% - دقة عالية جدا)",
            "10% (مستوى ثقة 90% - للدراسات الاستطلاعية)",
        ],
    )

    e = 0.05 if "5%" in margin_label else (0.01 if "1%" in margin_label else 0.10)
    z = 1.96 if e == 0.05 else (2.576 if e == 0.01 else 1.645)
    n0 = (z**2 * 0.25) / (e**2)
    sample_n = math.ceil(n0 / (1 + ((n0 - 1) / pop_size)))

    st.markdown(f"""<div class="sl-result-banner" style="display:flex; justify-content:space-between; align-items:center;"><span><strong>الحد الادنى الممثل للعينة (n):</strong></span><span style="font-size:18px; font-weight:800; color:#0A192F;">{sample_n} مفردة</span></div>""", unsafe_allow_html=True)

# 6. ميثاق النزاهة العلمية
integrity_html = """<div id="integrity" class="sl-integrity"><div style="max-width:800px; margin:0 auto;"><span style="background:rgba(245,158,11,0.18); color:#FBBF24; font-size:11.5px; font-weight:700; padding:4px 12px; border-radius:99px;">الالتزام الاخلاقي والعلمي</span><div style="color:#FFFFFF; font-size:20px; font-weight:800; margin:12px 0 8px 0;">ميثاق النزاهة العلمية وسرية البيانات في Socio Lab</div><p style="color:#CBD5E1; font-size:13.5px; line-height:1.8; margin:0;">تلتزم منصة Socio Lab بتقديم الاستشارات المنهجية والتحليل الاحصائي للبيانات الميدانية الحقيقية فقط، وترفض رفضا قاطعا فبركة البيانات او بيع البحوث الجاهزة او اي ممارسة تخل بالامانة العلمية، مع ضمان السرية التامة لافكار الباحثين وبياناتهم.</p></div></div>"""
st.markdown(integrity_html, unsafe_allow_html=True)

# 7. نموذج طلب الخدمة المربوط بالواتساب
order_header_html = """<div id="order" style="max-width:850px; margin:0 auto; padding:45px 6% 15px 6%;"><div class="sl-sec-head" style="margin-bottom:20px;"><div class="sl-sec-title">اطلب خدمتك البحثية او استشارتك</div><p class="sl-sec-sub">املا النموذج التالي وسيتواصل معك فريق Socio Lab خلال 24 ساعة بخطة العمل والتكلفة.</p></div></div>"""
st.markdown(order_header_html, unsafe_allow_html=True)

_, form_col, _ = st.columns([0.12, 0.76, 0.12])
with form_col:
    with st.form("sociolab_order_form"):
        c1, c2 = st.columns(2)
        with c1:
            client_name = st.text_input("الاسم الكامل / المؤسسة *")
            service_type = st.selectbox(
                "نوع الخدمة المطلوبة *",
                [
                    "التحليل الاحصائي وتفريغ البيانات (SPSS)",
                    "تصميم وبناء استبيان او اداة بحث",
                    "الضبط المنهجي وتحكيم الادوات",
                    "تحليل المقابلات والبيانات الكيفية",
                    "التوثيق الاكاديمي (APA) وتنسيق المقالات",
                    "حجز جلسة استشارية فردية",
                ],
            )
        with c2:
            client_role = st.selectbox(
                "الصفة الاكاديمية او المهنية *",
                ["باحث ماستر", "باحث دكتوراه", "استاذ باحث", "مؤسسة / جمعية"],
            )
            client_contact = st.text_input("رقم الواتساب او البريد الالكتروني *")

        study_details = st.text_area("ملخص الدراسة وحجم العينة والتفاصيل المطلوبة *", height=100)
        submitted = st.form_submit_button("تجهيز الطلب وارساله", use_container_width=True)

        if submitted:
            if client_name and client_contact:
                wa_message = (
                    f"السلام عليكم فريق Socio Lab، اود طلب خدمة بحثية:\n"
                    f"- الاسم: {client_name}\n"
                    f"- الصفة: {client_role}\n"
                    f"- الخدمة: {service_type}\n"
                    f"- وسيلة التواصل: {client_contact}\n"
                    f"- تفاصيل الدراسة: {study_details}"
                )
                encoded_msg = urllib.parse.quote(wa_message)
                wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_msg}"

                st.success(f"تم تجهيز طلبك بنجاح يا {client_name}! اضغط على الزر الاخضر ادناه لارساله مباشرة عبر واتساب.")
                st.markdown(
                    f"""<a href="{wa_link}" target="_blank" class="sl-wa-btn">ارسال تفاصيل الطلب الان عبر واتساب Socio Lab</a>""",
                    unsafe_allow_html=True,
                )
            else:
                st.warning("يرجى ملء الاسم ووسيلة التواصل لتأكيد الطلب.")

# 8. التذييل
footer_html = """<div class="sl-footer"><div class="sl-logo-script" style="font-size:24px; margin-bottom:4px;">Socio Lab</div><div>المختبر الاستشاري للبحث السوسيولوجي والتحليل الاحصائي</div><div style="font-size:11px; color:#64748B; margin-top:6px;">جميع الحقوق محفوظة &copy; 2026 Socio Lab</div></div>"""
st.markdown(footer_html, unsafe_allow_html=True)
