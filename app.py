import math
import urllib.parse
import streamlit as st

# ---------------------------------------------------------
# اعدادات البريد الالكتروني الرسمي للمنصة (ضعي بريدك هنا)
# ---------------------------------------------------------
CONTACT_EMAIL = "contact@sociolab-dz.com"

# 1. اعدادات الصفحة
st.set_page_config(
    page_title="Socio Lab | المختبر الاستشاري للبحث السوسيولوجي والتحليل الاحصائي",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. قاعدة بيانات الخدمات التفصيلية
SERVICES_DATA = {
    "s1": {
        "num": "01",
        "title": "تصميم وبناء ادوات البحث",
        "short_desc": "صياغة الاستبيانات الورقية والالكترونية وبناء ادلة المقابلات المعمقة والملاحظة العلمية وفق ابعاد وفرضيات الدراسة مع دليل الترميز.",
        "full_desc": "نساعدك في ترجمة مفاهيم دراستك النظرية الى مؤشرات قابلة للقياس الميداني الدقيق، سواء كانت دراستك كمية او كيفية، مع مراعاة الخصوصية الثقافية والاجتماعية لعينة البحث.",
        "deliverables": [
            "صياغة محاور وعبارات الاستبيان بدقة علمية خالية من التحيز.",
            "بناء النسخة الالكترونية الاحترافية عبر Google Forms او KoboToolbox.",
            "اعداد دليل المقابلة المعمقة وشبكة الملاحظة للدراسات الكيفية.",
            "تسليم دليل الترميز (Codebook) لتسهيل ادخال البيانات لاحقا."
        ],
        "duration": "من 2 الى 4 ايام عمل",
        "color": "#14B8A6",
        "top_class": ""
    },
    "s2": {
        "num": "02",
        "title": "التحليل الاحصائي وتنظيف البيانات (SPSS)",
        "short_desc": "تفريغ البيانات وتنظيفها، حساب الصدق والثبات، واجراء الاختبارات الوصفية والاستدلالية مع قراءة سوسيولوجية معمقة للجداول.",
        "full_desc": "نحول بياناتك الخام الى جداول احصائية محكمة ومفسرة سوسيولوجيا، مع اختيار الاختبارات المعلمية او اللامعلمية الانسب لطبيعة متغيراتك وتوزيع بياناتك.",
        "deliverables": [
            "ادخال البيانات وتنظيفها (Data Cleaning) ومعالجة القيم المفقودة والشاذة.",
            "حساب الخصائص السيكومترية (الصدق البنائي والاتساق الداخلي الفا كرونباخ).",
            "استخراج الجداول الوصفية والاستدلالية (اختبارات الفروق، الارتباط، والانحدار).",
            "تقديم ملف مخرجات SPSS الاصلي + تقرير Word منسق بالتعليق السوسيولوجي."
        ],
        "duration": "من 3 الى 5 ايام عمل",
        "color": "#0A192F",
        "top_class": "navy-top"
    },
    "s3": {
        "num": "03",
        "title": "الضبط المنهجي وتحكيم المقاييس",
        "short_desc": "مراجعة الاشكالية والفرضيات، ضبط المعاينة، وتقييم الخصائص السيكومترية للمقاييس لضمان سلامة البناء المنهجي للدراسة.",
        "full_desc": "مراجعة شاملة لخطة بحثك قبل الانطلاق في الدراسة الميدانية او قبل ايداع المذكرة، لضمان الترابط المنطقي بين الاشكالية، الفرضيات، الاداة، ونوع العينة.",
        "deliverables": [
            "تدقيق صياغة الاشكالية والتساؤلات والفرضيات ومدى قابليتها للاختبار.",
            "تحديد حجم ونوع العينة الانسب لمجتمع البحث (العشوائية، الطبقية، القصدية).",
            "مواءمة المؤشرات الميدانية مع الاطار النظري للدراسة.",
            "تقرير مفصل بالملاحظات المنهجية والتعديلات المقترحة خطوة بخطوة."
        ],
        "duration": "من 2 الى 3 ايام عمل",
        "color": "#F59E0B",
        "top_class": "amber-top"
    },
    "s4": {
        "num": "04",
        "title": "تحليل البيانات الكيفية",
        "short_desc": "تفريغ المقابلات المعمقة وتحليل المضمون والتحليل الموضوعاتي للدراسات الميدانية والدراسات المختلطة (الكمية والكيفية).",
        "full_desc": "نقدم معالجة علمية دقيقة للنصوص والخطابات والمقابلات الميدانية لاستخراج الفئات الدلالية والانماط السوسيولوجية الكامنة وراء اقوال المبحوثين.",
        "deliverables": [
            "تفريغ التسجيلات الصوتية للمقابلات ومجموعات التركيز بدقة.",
            "الترميز الموضوعاتي (Thematic Coding) وبناء شبكة الفئات التحليلية.",
            "دمج النتائج الكيفية مع المؤشرات الكمية في الدراسات المختلطة.",
            "صياغة تقرير تحليلي مدعم بالشواهد النصية المستخلصة من الميدان."
        ],
        "duration": "من 3 الى 6 ايام عمل",
        "color": "#0A192F",
        "top_class": "navy-top"
    },
    "s5": {
        "num": "05",
        "title": "التوثيق الاكاديمي (APA) والنشر",
        "short_desc": "ضبط التوثيق في المتن وقائمة المراجع وفق معايير APA، وتنسيق اوراق المؤتمرات والمقالات العلمية للنشر في المجلات المحكمة.",
        "full_desc": "نجهز اوراقك البحثية ومقالاتك ومذكراتك وفق احدث اصدارات نظام التوثيق العالمي APA وقوالب المجلات العلمية المحكمة لتفادي الرفض الشكلي.",
        "deliverables": [
            "مطابقة التوثيق في المتن مع قائمة المراجع النهائية بدقة تامة.",
            "تنسيق الجداول والاشكال البيانية وفق معايير النشر الاكاديمي.",
            "تحويل فصول المذكرات الى مقالات علمية مركزة قابلة للنشر.",
            "مراجعة لغوية واسلوبية تضمن رصانة النص العلمي وسلامته."
        ],
        "duration": "من 1 الى 3 ايام عمل",
        "color": "#14B8A6",
        "top_class": ""
    },
    "s6": {
        "num": "06",
        "title": "مسوح المؤسسات ودراسات الاثر",
        "short_desc": "تصميم وتنفيذ استطلاعات الراي ودراسات قياس الاثر الاجتماعي للمؤسسات والجمعيات وتقديم تقارير تنفيذية لصناع القرار.",
        "full_desc": "حلول بحثية موجهة للجمعيات، المؤسسات، ومخابر البحث لتقييم البرامج التنموية، قياس رضا المستفيدين، وتحليل الظواهر الاجتماعية والمؤسساتية.",
        "deliverables": [
            "تصميم خطة المسح الميداني او الالكتروني وتدريب جامعي البيانات.",
            "معالجة قواعد البيانات الضخمة واستخراج لوحات مؤشرات الاداء.",
            "تقييم الاثر الاجتماعي للبرامج والمشاريع قبل وبعد التنفيذ.",
            "تقديم تقرير تنفيذي مدعم بالرسوم البيانية والتوصيات العملية."
        ],
        "duration": "تحدد حسب حجم المشروع",
        "color": "#F59E0B",
        "top_class": "amber-top"
    }
}

# 3. التنقل عبر الروابط في نفس الصفحة
query_params = st.query_params
if "view" in query_params:
    st.session_state.current_view = query_params["view"]
elif "current_view" not in st.session_state:
    st.session_state.current_view = "home"

if "srv" in query_params and query_params["srv"] in SERVICES_DATA:
    st.session_state.selected_srv = query_params["srv"]
elif "selected_srv" not in st.session_state:
    st.session_state.selected_srv = "s2"

# 4. التنسيق العام (CSS)
css_styles = """<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Great+Vibes&display=swap');
#MainMenu, header, footer {visibility: hidden;}
.block-container {padding: 0rem !important; max-width: 100% !important;}
.stApp {background-color: #F8FAFC; font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; color: #1E293B;}
h1, h2, h3, h4, p, span, div, label, input, select, textarea, button {font-family: 'Cairo', sans-serif;}
.sl-navbar {background-color: #0A192F; border-bottom: 1px solid #163A5F; padding: 12px 6%; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 999;}
.sl-brand {display: flex; align-items: center; gap: 12px; text-decoration: none;}
.sl-sigma {width: 38px; height: 38px; background-color: #0F2942; border: 1px solid rgba(20, 184, 166, 0.45); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #2DD4BF; font-weight: 800; font-size: 18px;}
.sl-logo-script {font-family: 'Great Vibes', cursive !important; font-size: 26px; color: #FFFFFF; line-height: 1;}
.sl-logo-sub {font-size: 10px; color: #2DD4BF; display: block; margin-top: 2px;}
.sl-nav-links {display: flex; gap: 20px; flex-wrap: wrap;}
.sl-nav-links a {color: #E2E8F0; text-decoration: none; font-size: 13px; font-weight: 600;}
.sl-nav-links a:hover, .sl-nav-links a.active {color: #2DD4BF;}
.sl-cta-top {background-color: #F59E0B; color: #0A192F !important; font-weight: 700; font-size: 13px; padding: 8px 18px; border-radius: 8px; text-decoration: none;}
.sl-hero {background-color: #0A192F; background-image: radial-gradient(rgba(20, 184, 166, 0.14) 1px, transparent 1px); background-size: 26px 26px; color: #FFFFFF; padding: 48px 6%; border-bottom: 1px solid #163A5F;}
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
.sl-sec-head {text-align: center; max-width: 660px; margin: 0 auto 30px auto;}
.sl-sec-tag {color: #14B8A6; font-size: 12.5px; font-weight: 700;}
.sl-sec-title {color: #0A192F; font-size: 22px; font-weight: 800; margin: 4px 0 8px 0;}
.sl-sec-sub {color: #64748B; font-size: 13.5px; margin: 0;}
.sl-services-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 18px;}
.sl-srv-card {display: block; text-decoration: none !important; background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 3.5px solid #14B8A6; border-radius: 14px; padding: 22px; box-shadow: 0 2px 6px rgba(0,0,0,0.02); transition: all 0.2s ease;}
.sl-srv-card:hover {transform: translateY(-4px); box-shadow: 0 12px 24px rgba(10, 25, 47, 0.08); border-color: #14B8A6;}
.sl-srv-card.navy-top {border-top-color: #0A192F;}
.sl-srv-card.amber-top {border-top-color: #F59E0B;}
.sl-srv-num {font-size: 16px; font-weight: 800; color: #14B8A6; margin-bottom: 6px;}
.sl-srv-title {font-size: 16px; font-weight: 700; color: #0A192F; margin-bottom: 8px;}
.sl-srv-desc {font-size: 13px; color: #475569; line-height: 1.7; margin: 0 0 14px 0;}
.sl-srv-link {font-size: 12.5px; font-weight: 700; color: #0D9488; display: inline-flex; align-items: center; gap: 4px;}
.sl-pkg-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 22px; margin-top: 20px;}
.sl-pkg-card {background: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 16px; padding: 26px; position: relative; box-shadow: 0 4px 15px rgba(10, 25, 47, 0.04);}
.sl-pkg-card.featured {border-color: #0A192F; background: linear-gradient(to bottom, #FFFFFF, #F8FAFC);}
.sl-pkg-badge {display: inline-block; background: #FEF3C7; color: #B45309; font-size: 11.5px; font-weight: 700; padding: 4px 12px; border-radius: 99px; margin-bottom: 10px;}
.sl-pkg-item {font-size: 13px; color: #334155; padding: 6px 0; border-bottom: 1px dashed #E2E8F0;}
.sl-pkg-btn {display: block; text-align: center; background: #0A192F; color: #FFFFFF !important; font-weight: 700; font-size: 13px; padding: 10px; border-radius: 10px; text-decoration: none !important; margin-top: 16px;}
.sl-pkg-btn.amber {background: #F59E0B; color: #0A192F !important;}
.sl-clinic-box {background: #0A192F; border-radius: 18px; padding: 28px; color: #FFFFFF; border: 1px solid #1E3A5F;}
.sl-radar-card {background: #FFFFFF; border: 1px solid #E2E8F0; border-right: 4px solid #14B8A6; border-radius: 12px; padding: 18px; margin-bottom: 14px;}
.sl-probe-result {background: #FFFFFF; border: 1px solid #CBD5E1; border-top: 4px solid #0A192F; border-radius: 12px; padding: 18px; margin-top: 14px; font-size: 13px; line-height: 1.75; color: #1E293B;}
.sl-detail-box {background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 18px; padding: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); margin-bottom: 24px;}
.sl-deliv-item {background: #F8FAFC; border: 1px solid #E2E8F0; border-right: 3.5px solid #14B8A6; padding: 12px 16px; border-radius: 10px; font-size: 13.5px; color: #1E293B; margin-bottom: 10px;}
.sl-pill-tab {display: inline-block; padding: 8px 16px; border-radius: 99px; font-size: 12.5px; font-weight: 700; text-decoration: none !important; margin: 4px; border: 1px solid #CBD5E1; color: #334155 !important; background: #FFFFFF;}
.sl-pill-tab.active {background: #0A192F; color: #2DD4BF !important; border-color: #0A192F;}
.sl-back-link {display: inline-block; color: #0A192F !important; font-weight: 700; font-size: 13.5px; text-decoration: none !important; margin-bottom: 18px; background: #E2E8F0; padding: 7px 16px; border-radius: 8px;}
.sl-result-banner {background-color: #F0FDFA; border: 1px solid #99F6E4; border-right: 4px solid #14B8A6; padding: 12px 15px; border-radius: 10px; margin-top: 12px; font-size: 13px; color: #0F2942;}
.sl-email-btn {display: block; text-align: center; background-color: #0A192F; color: #2DD4BF !important; border: 1.5px solid #14B8A6; font-weight: 700; font-size: 14px; padding: 12px 20px; border-radius: 10px; text-decoration: none !important; margin-top: 12px; box-shadow: 0 4px 12px rgba(10, 25, 47, 0.15);}
.sl-email-btn:hover {background-color: #0F2942;}
.sl-integrity {background-color: #0A192F; color: #FFFFFF; text-align: center; padding: 45px 6%; margin-top: 35px;}
.sl-footer {background-color: #071120; color: #94A3B8; text-align: center; padding: 28px 6%; font-size: 12.5px; border-top: 1px solid #163A5F;}
div[data-baseweb="select"] > div, input, textarea {font-size: 13px !important; border-radius: 8px !important;}
label p {font-size: 13px !important; font-weight: 700 !important; color: #1E293B !important;}
</style>"""

st.markdown(css_styles, unsafe_allow_html=True)

# 5. الشريط العلوي المشترك
active_home = "active" if st.session_state.current_view == "home" else ""
active_srv = "active" if st.session_state.current_view == "services" else ""

navbar_html = f"""<div class="sl-navbar"><a href="?view=home" target="_self" class="sl-brand"><div class="sl-sigma">&Sigma;</div><div><div class="sl-logo-script">Socio Lab</div><span class="sl-logo-sub">للتحليل الاحصائي والمنهجية</span></div></a><div class="sl-nav-links"><a href="?view=home" target="_self" class="{active_home}">الرئيسية</a><a href="?view=services&srv=s1" target="_self" class="{active_srv}">الخدمات والحزم</a><a href="?view=home#tools" target="_self">مختبر الادوات</a><a href="?view=home#clinic-radar" target="_self">العيادة والرادار</a><a href="?view=home#integrity" target="_self">ميثاق النزاهة</a></div><a href="?view=services&srv=s2#order-box" target="_self" class="sl-cta-top">راسلنا لطلب خدمة</a></div>"""
st.markdown(navbar_html, unsafe_allow_html=True)

# =====================================================================
# الصفحة الاولى: الواجهة الرئيسية (HOME)
# =====================================================================
if st.session_state.current_view == "home":
    hero_html = """<div class="sl-hero"><div class="sl-hero-grid"><div><div class="sl-badge">&mu; دقة منهجية • قراءة سوسيولوجية • توثيق APA</div><div class="sl-hero-title">من الفكرة البحثية الى النتائج المحكمة.. <span>شريكك المنهجي والاحصائي الدقيق</span></div><p class="sl-hero-desc">في <strong>Socio Lab</strong> نحول البيانات الميدانية الخام الى رؤى سوسيولوجية وعلمية رصينة. نرافق الباحثين، طلبة الدراسات العليا، والمؤسسات في تصميم ادوات القياس، تنظيف البيانات، والتحليل الاحصائي المتقدم عبر برنامج SPSS.</p><div class="sl-hero-btns"><a href="?view=services&srv=s1" target="_self" class="sl-btn-amber">استكشف الخدمات والحزم الميدانية</a><a href="#tools" target="_self" class="sl-btn-outline">جرب مسبار الفرضيات الذكي</a></div></div><div class="sl-stat-card"><div class="sl-stat-header"><div><div style="font-size:11px; color:#2DD4BF; font-weight:700;">نموذج مخرجات Socio Lab</div><div style="font-size:14px; font-weight:700; color:#FFFFFF;">تحليل التوزيع الطبيعي ومؤشرات الثبات</div></div><span style="background:rgba(20,184,166,0.18); color:#2DD4BF; font-size:11px; padding:3px 8px; border-radius:6px; font-family:monospace;">SPSS v28</span></div><div style="background:#0A192F; padding:10px; border-radius:10px; border:1px solid #1E3A5F;"><svg viewBox="0 0 300 95" style="width:100%; height:85px; display:block;"><defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#14B8A6" stop-opacity="0.45"/><stop offset="100%" stop-color="#14B8A6" stop-opacity="0.0"/></linearGradient></defs><line x1="10" y1="80" x2="290" y2="80" stroke="#334155" stroke-width="1"/><line x1="150" y1="12" x2="150" y2="80" stroke="#F59E0B" stroke-dasharray="3,3" stroke-width="1.3"/><path d="M 15 80 C 75 80, 105 12, 150 12 C 195 12, 225 80, 285 80 Z" fill="url(#g1)"/><path d="M 15 80 C 75 80, 105 12, 150 12 C 195 12, 225 80, 285 80" fill="none" stroke="#2DD4BF" stroke-width="2.2"/><text x="150" y="92" fill="#F59E0B" font-size="9" text-anchor="middle">&mu; = 3.84</text></svg></div><div class="sl-kpi-grid"><div class="sl-kpi-box"><div class="sl-kpi-label">الفا كرونباخ (&alpha;)</div><div class="sl-kpi-val" style="color:#2DD4BF;">0.892</div></div><div class="sl-kpi-box"><div class="sl-kpi-label">حجم العينة (N)</div><div class="sl-kpi-val" style="color:#FFFFFF;">60</div></div><div class="sl-kpi-box"><div class="sl-kpi-label">الدلالة (Sig)</div><div class="sl-kpi-val" style="color:#F59E0B;">0.001</div></div></div><div class="sl-reading-box"><strong>القراءة السوسيولوجية:</strong> تشير قيمة الفا كرونباخ (0.892) الى اتساق داخلي مرتفع جدا لاداة القياس، مع دلالة احصائية تؤكد اثر المتغير المستقل عند مستوى 0.01.</div></div></div></div>"""
    st.markdown(hero_html, unsafe_allow_html=True)

    # القسم الاول: بطاقات الخدمات الفردية
    cards_html = ""
    for key, srv in SERVICES_DATA.items():
        cards_html += f'<a href="?view=services&srv={key}" target="_self" class="sl-srv-card {srv["top_class"]}"><div class="sl-srv-num" style="color:{srv["color"]};">{srv["num"]}</div><div class="sl-srv-title">{srv["title"]}</div><p class="sl-srv-desc">{srv["short_desc"]}</p><span class="sl-srv-link">عرض تفاصيل الخدمة وطلبها &larr;</span></a>'

    services_section = f"""<div id="services" class="sl-section"><div class="sl-sec-head"><div class="sl-sec-tag">حلول منهجية متكاملة</div><div class="sl-sec-title">خدمات منصة Socio Lab</div><p class="sl-sec-sub">اضغط على اي خدمة للانتقال الى صفحتها التفصيلية والاطلاع على المخرجات وطلبها عبر البريد الالكتروني.</p></div><div class="sl-services-grid">{cards_html}</div></div>"""
    st.markdown(services_section, unsafe_allow_html=True)

    # القسم الثاني: حزم الاستشارة المتكاملة للباحث الميداني (Fieldwork Packages)
    packages_html = """<div id="packages" class="sl-section" style="padding-top:10px;"><div class="sl-sec-head"><div class="sl-sec-tag">حلول شاملة لمراحل البحث</div><div class="sl-sec-title">حزم الاستشارة المتكاملة للباحث الميداني</div><p class="sl-sec-sub">باقات عملية مصممة لمرافقتك في اهم محطتين في مسارك البحثي: النزول الى الميدان والاستعداد للمناقشة.</p></div><div class="sl-pkg-grid"><div class="sl-pkg-card"><span class="sl-pkg-badge">المرحلة الاولى: قبل النزول الى الميدان</span><div style="font-size:19px; font-weight:800; color:#0A192F; margin-bottom:8px;">باقة "انطلاق الميدان الامن"</div><p style="font-size:13px; color:#64748B; margin-bottom:14px;">تضمن لك بناء اداة قياس محكمة وعينة ممثلة قبل جمع البيانات لتفادي الاخطاء القاتلة.</p><div class="sl-pkg-item">&#10003; تصميم وبناء اداة البحث (استبيان الكتروني/ورقي او دليل مقابلة).</div><div class="sl-pkg-item">&#10003; الضبط المنهجي للاشكالية والفرضيات وتحكيم المقاييس.</div><div class="sl-pkg-item">&#10003; تحديد نوع وحجم العينة الممثلة بدقة احصائية.</div><a href="?view=services&srv=s1&pkg=p1#order-box" target="_self" class="sl-pkg-btn">اطلب باقة انطلاق الميدان الامن</a></div><div class="sl-pkg-card featured"><span class="sl-pkg-badge" style="background:#0A192F; color:#2DD4BF;">المرحلة الثانية: التحليل والدفاع</span><div style="font-size:19px; font-weight:800; color:#0A192F; margin-bottom:8px;">باقة "المناقشة المحصنة"</div><p style="font-size:13px; color:#64748B; margin-bottom:14px;">تجهزك بنتائج احصائية وكيفية دقيقة وتدربك على الدفاع العلمي امام لجنة المناقشة.</p><div class="sl-pkg-item">&#10003; التحليل الاحصائي الكامل وتنظيف البيانات عبر برنامج SPSS.</div><div class="sl-pkg-item">&#10003; تفريغ وتحليل البيانات الكيفية (المقابلات) ودمجها مع النتائج.</div><div class="sl-pkg-item">&#10003; جلسة تحضيرية افتراضية لشرح الجداول وتوقع اسئلة اللجنة الحرجة.</div><a href="?view=services&srv=s2&pkg=p2#order-box" target="_self" class="sl-pkg-btn amber">اطلب باقة المناقشة المحصنة</a></div></div></div>"""
    st.markdown(packages_html, unsafe_allow_html=True)

    # القسم الثالث: مختبر الادوات التفاعلية الذكية (مسبار الفرضيات + مشخص الاختبار + حاسبة العينة)
    tools_header_html = """<div id="tools" style="max-width:1180px; margin:0 auto; padding:25px 6% 15px 6%;"><div class="sl-sec-head"><div class="sl-sec-tag">مختبر الادوات المجانية</div><div class="sl-sec-title">مسبار الفرضيات والادوات الاحصائية الذكية</div><p class="sl-sec-sub">ادوات تفاعلية فورية لمساعدة الباحث في صياغة الفرضيات، اختيار الاختبار الاحصائي، وحساب حجم العينة.</p></div></div>"""
    st.markdown(tools_header_html, unsafe_allow_html=True)

    # 3.1 مسبار الفرضيات الذكي (AI Hypothesis & Variable Diagnostician)
    _, probe_col, _ = st.columns([0.06, 0.88, 0.06])
    with probe_col:
        st.markdown('<div style="font-size:16.5px; font-weight:800; color:#0A192F; margin-bottom:10px;">1. مسبار الفرضيات الذكي (صياغة الفرضيات والتساؤلات وتحديد التحليل)</div>', unsafe_allow_html=True)
        pc1, pc2, pc3 = st.columns(3)
        with pc1:
            indep_var = st.text_input("المتغير المستقل (X):", placeholder="مثال: جماعة الرفاق / استخدام منصات التواصل")
        with pc2:
            dep_var = st.text_input("المتغير التابع (Y):", placeholder="مثال: السلوك الجانح / التحصيل الدراسي")
        with pc3:
            study_sample = st.text_input("طبيعة عينة الدراسة:", placeholder="مثال: 60 تلميذا في الطور الثانوي")

        if indep_var and dep_var:
            sample_txt = f"لدى عينة من ({study_sample})" if study_sample else "لدى عينة الدراسة"
            probe_output = f"""<div class="sl-probe-result">
<div style="font-weight:800; color:#0D9488; margin-bottom:8px;">التشخيص المنهجي والاحصائي المقترح لدراستك:</div>
<div style="margin-bottom:6px;"><strong>• التساؤل الرئيسي الموازي:</strong> هل توجد علاقة ذات دلالة احصائية (او اثر دال) بين <strong>{indep_var}</strong> و<strong>{dep_var}</strong> {sample_txt}؟</div>
<div style="margin-bottom:6px;"><strong>• الفرضية الصفرية (H0):</strong> لا توجد علاقة ارتباطية (او اثر ذو دلالة احصائية) عند مستوى دلالة (&alpha; &le; 0.05) بين <strong>{indep_var}</strong> و<strong>{dep_var}</strong> {sample_txt}.</div>
<div style="margin-bottom:6px;"><strong>• الفرضية البديلة (H1):</strong> توجد علاقة ارتباطية (او اثر ذو دلالة احصائية) عند مستوى دلالة (&alpha; &le; 0.05) بين <strong>{indep_var}</strong> و<strong>{dep_var}</strong> {sample_txt}.</div>
<div><strong>• مسار التحليل الاحصائي الانسب (SPSS):</strong> ابدأ بحساب معامل الثبات (الفا كرونباخ) لاداة قياس كل متغير، ثم اختبر التوزيع الطبيعي للبيانات؛ فاذا كان التوزيع طبيعيا استخدم <strong>معامل ارتباط بيرسون</strong> لقياس العلاقة و<strong>الانحدار الخطي البسيط</strong> لقياس الاثر، اما اذا كان غير طبيعي فاستخدم <strong>معامل سبيرمان للرتب</strong>.</div>
</div>"""
            st.markdown(probe_output, unsafe_allow_html=True)
        else:
            st.markdown("""<div class="sl-result-banner">اكتب اسم المتغير المستقل والمتغير التابع اعلاه ليقوم المسبار بتوليد التساؤل الرئيسي، الفرضية الصفرية والبديلة، وخطة التحليل الاحصائي فورا.</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # 3.2 مشخص الاختبار وحاسبة العينة
    _, col_t1, col_t2, _ = st.columns([0.06, 0.44, 0.44, 0.06], gap="large")
    with col_t1:
        st.markdown('<div style="font-size:15.5px; font-weight:800; color:#0A192F; margin-bottom:10px;">2. مشخص الاختبار الاحصائي (SPSS)</div>', unsafe_allow_html=True)
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
        st.markdown('<div style="font-size:15.5px; font-weight:800; color:#0A192F; margin-bottom:10px;">3. حاسبة حجم العينة الممثلة (معادلة كوكران)</div>', unsafe_allow_html=True)
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

    # القسم الرابع: عيادة المنهجية والاحصاء المباشرة + رادار الاتجاهات السوسيولوجية
    clinic_radar_html = f"""<div id="clinic-radar" class="sl-section"><div class="sl-hero-grid" style="align-items:start;"><div class="sl-clinic-box"><span style="background:rgba(245,158,11,0.2); color:#FBBF24; font-size:11.5px; font-weight:700; padding:4px 12px; border-radius:99px;">ركن تفاعلي دوري</span><h3 style="color:#FFFFFF; font-size:20px; font-weight:800; margin:12px 0 8px 0;">عيادة المنهجية والاحصاء المباشرة</h3><p style="color:#CBD5E1; font-size:13.5px; line-height:1.75; margin-bottom:16px;">لقاء علمي دوري نفكك فيه ابرز الاخطاء المنهجية والاحصائية الشائعة في رسائل الماستر والدكتوراه (دون ذكر اسماء) مع تقديم التصحيح العلمي المباشر.</p><div style="background:#0F2942; border:1px solid #1E3A5F; border-radius:12px; padding:14px; margin-bottom:16px;"><div style="font-size:12.5px; color:#2DD4BF; font-weight:700; margin-bottom:4px;">ملف الجلسة القادمة:</div><div style="font-size:13.5px; color:#FFFFFF; font-weight:600;">"لماذا يفشل اختبار الفرضيات رغم ارتفاع معامل الثبات؟ اخطاء صياغة مؤشرات الاستبيان"</div></div><a href="mailto:{CONTACT_EMAIL}?subject={urllib.parse.quote('ارسال حالة منهجية لعيادة Socio Lab')}" class="sl-btn-amber" style="display:inline-block;">ارسل اشكاليتك المنهجية عبر البريد لمناقشتها</a></div><div><div style="margin-bottom:14px;"><span class="sl-sec-tag">رؤية استشرافية للظواهر الاجتماعية</span><h3 class="sl-sec-title" style="font-size:20px;">رادار الاتجاهات السوسيولوجية</h3></div><div class="sl-radar-card"><div style="font-size:11.5px; color:#0D9488; font-weight:700;">رصد الظواهر الرقمية</div><div style="font-size:15px; font-weight:800; color:#0A192F; margin:3px 0;">تحولات التنشئة الاجتماعية في ظل المنصات الخوارزمية</div><p style="font-size:12.5px; color:#475569; line-height:1.65; margin:0;">تراجع سلطة الوسائط التقليدية امام صناع المحتوى وتاثير ذلك على القيم الاستهلاكية والسلوكيات المستجدة لدى المراهقين. <strong>فرصة بحثية:</strong> قياس اثر التعرض الانتقائي على التمثل القيمي.</p></div><div class="sl-radar-card" style="border-right-color:#F59E0B;"><div style="font-size:11.5px; color:#D97706; font-weight:700;">رصد السلوكيات المستجدة</div><div style="font-size:15px; font-weight:800; color:#0A192F; margin:3px 0;">التطبيب الذاتي وسوء استخدام المؤثرات العقلية في الوسط الشباني</div><p style="font-size:12.5px; color:#475569; line-height:1.65; margin:0;">انتقال الظاهرة من السياقات الهامشية التقليدية الى الفضاءات شبه الحضرية والرقمية. <strong>فرصة بحثية:</strong> تحليل العوامل السوسيو-مؤسساتية المفسرة للانحراف المستحدث.</p></div></div></div></div>"""
    st.markdown(clinic_radar_html, unsafe_allow_html=True)

    # ميثاق النزاهة العلمية
    integrity_html = """<div id="integrity" class="sl-integrity"><div style="max-width:800px; margin:0 auto;"><span style="background:rgba(245,158,11,0.18); color:#FBBF24; font-size:11.5px; font-weight:700; padding:4px 12px; border-radius:99px;">الالتزام الاخلاقي والعلمي</span><div style="color:#FFFFFF; font-size:20px; font-weight:800; margin:12px 0 8px 0;">ميثاق النزاهة العلمية وسرية البيانات في Socio Lab</div><p style="color:#CBD5E1; font-size:13.5px; line-height:1.8; margin:0;">تلتزم منصة Socio Lab بتقديم الاستشارات المنهجية والتحليل الاحصائي للبيانات الميدانية الحقيقية فقط، وترفض رفضا قاطعا فبركة البيانات او بيع البحوث الجاهزة او اي ممارسة تخل بالامانة العلمية، مع ضمان السرية التامة لافكار الباحثين وبياناتهم.</p></div></div>"""
    st.markdown(integrity_html, unsafe_allow_html=True)

# =====================================================================
# الصفحة الثانية: صفحة الخدمات والحزم المستقلة (SERVICES PAGE)
# =====================================================================
elif st.session_state.current_view == "services":
    current_key = st.session_state.selected_srv
    current_srv = SERVICES_DATA[current_key]
    selected_pkg = query_params.get("pkg", "")

    # شريط التنقل السريع بين الخدمات في نفس الصفحة
    pills_html = ""
    for k, v in SERVICES_DATA.items():
        act = "active" if k == current_key else ""
        pills_html += f'<a href="?view=services&srv={k}" target="_self" class="sl-pill-tab {act}">{v["num"]}. {v["title"]}</a>'

    deliv_html = ""
    for item in current_srv["deliverables"]:
        deliv_html += f'<div class="sl-deliv-item">&#10003; &nbsp; {item}</div>'

    service_page_html = f"""<div class="sl-section" style="padding-top:30px;"><a href="?view=home" target="_self" class="sl-back-link">&rarr; العودة الى الصفحة الرئيسية</a><div style="margin-bottom:24px; text-align:center;">{pills_html}</div><div class="sl-detail-box" style="border-top: 4px solid {current_srv['color']};"><div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;"><span style="background:#0A192F; color:#2DD4BF; font-size:12px; font-weight:700; padding:4px 12px; border-radius:99px;">خدمة رقم {current_srv['num']}</span><span style="background:#FEF3C7; color:#B45309; font-size:12px; font-weight:700; padding:4px 12px; border-radius:99px;">مدة الانجاز التقديرية: {current_srv['duration']}</span></div><h1 style="font-size:24px; font-weight:800; color:#0A192F; margin:8px 0 12px 0;">{current_srv['title']}</h1><p style="font-size:14.5px; color:#475569; line-height:1.8; margin-bottom:22px;">{current_srv['full_desc']}</p><h3 style="font-size:16px; font-weight:800; color:#0A192F; margin-bottom:12px;">ماذا ستستلم في هذه الخدمة (المخرجات):</h3>{deliv_html}</div></div>"""
    st.markdown(service_page_html, unsafe_allow_html=True)

    # نموذج طلب الخدمة او الباقة عبر البريد الالكتروني حصرا
    st.markdown(f"""<div id="order-box" style="max-width:850px; margin:0 auto; padding:10px 6% 15px 6%;"><div class="sl-sec-head" style="margin-bottom:18px;"><div class="sl-sec-title">اطلب الخدمة او الباقة عبر البريد الالكتروني</div><p class="sl-sec-sub">املا البيانات ادناه لتجهيز رسالة رسمية موجهة الى بريد المنصة ({CONTACT_EMAIL}).</p></div></div>""", unsafe_allow_html=True)

    options_list = [v["title"] for v in SERVICES_DATA.values()] + [
        "باقة انطلاق الميدان الامن (تصميم الاداة + الضبط المنهجي + حساب العينة)",
        "باقة المناقشة المحصنة (التحليل الاحصائي SPSS + التحليل الكيفي + جلسة الدفاع)"
    ]

    if selected_pkg == "p1":
        default_index = len(options_list) - 2
    elif selected_pkg == "p2":
        default_index = len(options_list) - 1
    else:
        default_index = options_list.index(current_srv["title"])

    _, form_col, _ = st.columns([0.12, 0.76, 0.12])
    with form_col:
        with st.form("service_email_form"):
            c1, c2 = st.columns(2)
            with c1:
                client_name = st.text_input("الاسم الكامل / المؤسسة *")
                service_type = st.selectbox("الخدمة او الباقة المختارة *", options_list, index=default_index)
            with c2:
                client_role = st.selectbox("الصفة الاكاديمية او المهنية *", ["باحث ماستر", "باحث دكتوراه", "استاذ باحث", "مؤسسة / جمعية"])
                client_email = st.text_input("بريدك الالكتروني للتواصل والرد *")

            study_details = st.text_area("عنوان الدراسة، حجم العينة، والتفاصيل المطلوبة *", height=105)
            submitted = st.form_submit_button("تجهيز رسالة الطلب للبريد الالكتروني", use_container_width=True)

            if submitted:
                if client_name and client_email:
                    subject = f"طلب خدمة بحثية من Socio Lab - {service_type}"
                    body = (
                        f"السلام عليكم فريق Socio Lab،\n\n"
                        f"اود التقدم بطلب الخدمة التالية:\n"
                        f"- الخدمة / الباقة: {service_type}\n"
                        f"- الاسم الكامل: {client_name}\n"
                        f"- الصفة الاكاديمية: {client_role}\n"
                        f"- البريد الالكتروني للرد: {client_email}\n"
                        f"- تفاصيل الدراسة والعينة:\n{study_details}\n\n"
                        f"مع خالص التقدير."
                    )
                    mailto_link = f"mailto:{CONTACT_EMAIL}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"

                    st.success(f"تم تجهيز مسودة طلبك بنجاح يا {client_name}! اضغط على الزر ادناه لفتح تطبيق البريد وارسال الرسالة مباشرة.")
                    st.markdown(
                        f"""<a href="{mailto_link}" class="sl-email-btn">ارسال الطلب الان عبر البريد الالكتروني ({CONTACT_EMAIL})</a>""",
                        unsafe_allow_html=True,
                    )
                else:
                    st.warning("يرجى كتابة الاسم وبريدك الالكتروني لتجهيز الرسالة.")

# 6. التذييل المشترك
footer_html = f"""<div class="sl-footer"><div class="sl-logo-script" style="font-size:24px; margin-bottom:4px;">Socio Lab</div><div>المختبر الاستشاري للبحث السوسيولوجي والتحليل الاحصائي</div><div style="font-size:12px; color:#2DD4BF; margin-top:6px;">البريد الرسمي للتواصل: {CONTACT_EMAIL}</div><div style="font-size:11px; color:#64748B; margin-top:6px;">جميع الحقوق محفوظة &copy; 2026 Socio Lab</div></div>"""
st.markdown(footer_html, unsafe_allow_html=True)
