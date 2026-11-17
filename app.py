import base64
import math
import os
import urllib.parse
import pandas as pd
import streamlit as st

CONTACT_EMAIL = "contact@sociolab-dz.com"
LOGO_FILENAME = "logo.png.jpg"


def get_logo_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def compute_cronbach_alpha(df_num):
    k = df_num.shape[1]
    if k < 2:
        return None
    item_vars = df_num.var(axis=0, ddof=1).sum()
    total_var = df_num.sum(axis=1).var(ddof=1)
    if total_var == 0:
        return None
    return (k / (k - 1)) * (1 - (item_vars / total_var))


logo_b64 = get_logo_base64(LOGO_FILENAME)
icon_val = LOGO_FILENAME if os.path.exists(LOGO_FILENAME) else "📊"

st.set_page_config(
    page_title="Socio Lab | فضاء علمي رقمي لانتاج المعرفة وتطوير البحث",
    page_icon=icon_val,
    layout="wide",
    initial_sidebar_state="collapsed",
)

SERVICES_DATA = {
    "s1": {
        "num": "01",
        "title": "تصميم وبناء ادوات البحث",
        "short_desc": (
            "صياغة الاستبيانات الورقية والالكترونية وبناء ادلة "
            "المقابلات والملاحظة العلمية وفق ابعاد وفرضيات الدراسة."
        ),
        "full_desc": (
            "نساعدك في ترجمة مفاهيم دراستك النظرية الى مؤشرات قابلة "
            "للقياس الميداني الدقيق سواء كانت دراستك كمية او كيفية."
        ),
        "deliverables": [
            "صياغة محاور وعبارات الاستبيان بدقة علمية خالية من التحيز.",
            "بناء النسخة الالكترونية عبر <span class='ltr'>Google Forms</span> او <span class='ltr'>KoboToolbox</span>.",
            "اعداد دليل المقابلة المعمقة وشبكة الملاحظة للدراسات الكيفية.",
            "تسليم دليل الترميز (<span class='ltr'>Codebook</span>) لتسهيل ادخال البيانات لاحقا."
        ],
        "duration": "من 2 الى 4 ايام عمل",
        "color": "#14B8A6",
        "top_class": ""
    },
    "s2": {
        "num": "02",
        "title": "التحليل الاحصائي وتنظيف البيانات (SPSS)",
        "short_desc": (
            "تفريغ البيانات وتنظيفها، حساب الصدق والثبات، واجراء "
            "الاختبارات الوصفية والاستدلالية مع قراءة سوسيولوجية."
        ),
        "full_desc": (
            "نحول بياناتك الخام الى جداول احصائية محكمة ومفسرة "
            "سوسيولوجيا مع اختيار الاختبارات الانسب لطبيعة متغيراتك."
        ),
        "deliverables": [
            "ادخال البيانات وتنظيفها (<span class='ltr'>Data Cleaning</span>) ومعالجة القيم المفقودة والشاذة.",
            "حساب الصدق البنائي والاتساق الداخلي معامل الفا كرونباخ.",
            "استخراج الجداول الوصفية والاستدلالية والفروق والارتباط.",
            "تسليم ملف <span class='ltr'>SPSS</span> الاصلي وتقرير <span class='ltr'>Word</span> بالتعليق السوسيولوجي."
        ],
        "duration": "من 3 الى 5 ايام عمل",
        "color": "#06182C",
        "top_class": "navy-top"
    },
    "s3": {
        "num": "03",
        "title": "الضبط المنهجي وتحكيم المقاييس",
        "short_desc": (
            "مراجعة الاشكالية والفرضيات، ضبط المعاينة، وتقييم "
            "الخصائص السيكومترية للمقاييس لضمان سلامة البناء المنهجي."
        ),
        "full_desc": (
            "مراجعة شاملة لخطة بحثك قبل النزول الى الميدان او قبل "
            "المناقشة لضمان الترابط المنطقي بين عناصر الدراسة."
        ),
        "deliverables": [
            "تدقيق صياغة الاشكالية والتساؤلات والفرضيات وقابليتها للاختبار.",
            "تحديد حجم ونوع العينة الانسب لمجتمع البحث الميداني.",
            "مواءمة المؤشرات الميدانية مع الاطار النظري للدراسة.",
            "تقرير مفصل بالملاحظات المنهجية والتعديلات المقترحة."
        ],
        "duration": "من 2 الى 3 ايام عمل",
        "color": "#F59E0B",
        "top_class": "amber-top"
    },
    "s4": {
        "num": "04",
        "title": "تحليل البيانات الكيفية",
        "short_desc": (
            "تفريغ المقابلات المعمقة وتحليل المضمون والتحليل "
            "الموضوعاتي للدراسات الميدانية والدراسات المختلطة."
        ),
        "full_desc": (
            "معالجة علمية دقيقة للنصوص والمقابلات الميدانية لاستخراج "
            "الفئات الدلالية والانماط السوسيولوجية الكامنة."
        ),
        "deliverables": [
            "تفريغ التسجيلات الصوتية للمقابلات ومجموعات التركيز بدقة.",
            "الترميز الموضوعاتي (<span class='ltr'>Thematic Coding</span>) وبناء شبكة الفئات التحليلية.",
            "دمج النتائج الكيفية مع المؤشرات الكمية في الدراسات المختلطة.",
            "صياغة تقرير تحليلي مدعم بالشواهد النصية من الميدان."
        ],
        "duration": "من 3 الى 6 ايام عمل",
        "color": "#06182C",
        "top_class": "navy-top"
    },
    "s5": {
        "num": "05",
        "title": "التوثيق الاكاديمي (APA 7) والنشر",
        "short_desc": (
            "ضبط التوثيق في المتن وقائمة المراجع وفق الاصدار السابع "
            "APA، وتنسيق اوراق المؤتمرات والمقالات للنشر المحكم."
        ),
        "full_desc": (
            "نجهز اوراقك البحثية ومقالاتك ومذكراتك وفق احدث اصدارات "
            "نظام التوثيق العالمي <span class='ltr'>APA 7th</span> وقوالب المجلات المحكمة."
        ),
        "deliverables": [
            "مطابقة التوثيق في المتن مع قائمة المراجع النهائية بدقة.",
            "تنسيق الجداول والاشكال البيانية وفق معايير النشر الاكاديمي.",
            "تحويل فصول المذكرات الى مقالات علمية مركزة قابلة للنشر.",
            "مراجعة لغوية واسلوبية تضمن رصانة النص العلمي."
        ],
        "duration": "من 1 الى 3 ايام عمل",
        "color": "#14B8A6",
        "top_class": ""
    },
    "s6": {
        "num": "06",
        "title": "مسوح المؤسسات ودراسات الاثر",
        "short_desc": (
            "تصميم وتنفيذ استطلاعات الراي ودراسات قياس الاثر "
            "الاجتماعي للمؤسسات والجمعيات وتقديم تقارير تنفيذية."
        ),
        "full_desc": (
            "حلول بحثية موجهة للجمعيات والمؤسسات ومخابر البحث لتقييم "
            "البرامج التنموية وقياس رضا المستفيدين."
        ),
        "deliverables": [
            "تصميم خطة المسح الميداني او الالكتروني وتدريب الباحثين.",
            "معالجة قواعد البيانات واستخراج لوحات مؤشرات الاداء.",
            "تقييم الاثر الاجتماعي للبرامج والمشاريع قبل وبعد التنفيذ.",
            "تقديم تقرير تنفيذي مدعم بالرسوم البيانية والتوصيات."
        ],
        "duration": "تحدد حسب حجم المشروع",
        "color": "#F59E0B",
        "top_class": "amber-top"
    },
    "s7": {
        "num": "07",
        "title": "مختبر نمذجة المعادلات البنية (SEM)",
        "short_desc": (
            "تحليلات متقدمة للدكتوراه: اختبار الوساطة والاعتدال "
            "والتحليل متعدد المتغيرات عبر SmartPLS و Process Macro."
        ),
        "full_desc": (
            "خدمة متقدمة موجهة لطلبة الدكتوراه والباحثين الاكاديميين "
            "لبناء النماذج السببية واختبار المتغيرات الوسيطة والمعدلة."
        ),
        "deliverables": [
            "تقييم نموذج القياس والصدق التمييزي (<span class='ltr'>HTMT / Fornell</span>).",
            "تقييم النموذج البنيوي ومعاملات المسار (<span class='ltr'>Path Coefficients</span>).",
            "اختبار فرضيات الوساطة والاعتدال عبر <span class='ltr'>Process Macro</span>.",
            "تقرير اكاديمي متكامل بالجداول والرسوم وفق النشر الدولي."
        ],
        "duration": "من 4 الى 7 ايام عمل",
        "color": "#0284C7",
        "top_class": "navy-top"
    }
}

PACKAGES_DATA = {
    "p1": {
        "badge": "المرحلة الاولى: قبل الميدان",
        "title": "باقة انطلاق الميدان الامن",
        "full_label": "باقة انطلاق الميدان الامن (تصميم الاداة + الضبط + العينة)",
        "desc": "تضمن لك بناء اداة قياس محكمة وعينة ممثلة قبل جمع البيانات لتفادي الاخطاء.",
        "items": [
            "تصميم وبناء اداة البحث (استبيان الكتروني/ورقي او دليل مقابلة).",
            "الضبط المنهجي للاشكالية والفرضيات وتحكيم المقاييس.",
            "تحديد نوع وحجم العينة الممثلة بدقة احصائية."
        ],
        "featured": False,
        "btn_class": "",
        "srv_ref": "s1"
    },
    "p2": {
        "badge": "المرحلة الثانية: التحليل والدفاع",
        "title": "باقة المناقشة المحصنة",
        "full_label": "باقة المناقشة المحصنة (التحليل الاحصائي + الكيفي + جلسة الدفاع)",
        "desc": "تجهزك بنتائج احصائية وكيفية دقيقة وتدربك على الدفاع العلمي امام لجنة المناقشة.",
        "items": [
            "التحليل الاحصائي الكامل وتنظيف البيانات عبر برنامج <span class='ltr'>SPSS</span>.",
            "تفريغ وتحليل البيانات الكيفية (المقابلات) ودمجها مع النتائج.",
            "جلسة تحضيرية افتراضية لشرح الجداول وتوقع اسئلة اللجنة الحرجة."
        ],
        "featured": True,
        "btn_class": "amber",
        "srv_ref": "s2"
    },
    "p3": {
        "badge": "الاكثر طلبا لطلبة الماستر",
        "title": "باقة المرافقة الشاملة (من الفكرة الى الايداع)",
        "full_label": "باقة المرافقة الشاملة (تصميم + تحليل + توثيق APA 7 + جلسة دفاع)",
        "desc": "مرافقة متكاملة تغطي كافة الجوانب المنهجية والاحصائية والتوثيقية لمذكرتك.",
        "items": [
            "ضبط الاشكالية والفرضيات وتصميم الاستبيان او دليل المقابلة.",
            "التحليل الاحصائي الكامل (<span class='ltr'>SPSS</span>) او التحليل الكيفي للبيانات.",
            "توثيق المراجع وفق <span class='ltr'>APA 7</span> + جلسة تحضيرية للمناقشة."
        ],
        "featured": True,
        "btn_class": "amber",
        "srv_ref": "s2"
    },
    "p4": {
        "badge": "للدكتوراه والنشر الدولي",
        "title": "باقة الدكتوراه والمجلات المحكمة",
        "full_label": "باقة الدكتوراه والنشر الدولي (نمذجة SEM + مقال محكم + APA 7)",
        "desc": "مصممة لاطروحات الدكتوراه والباحثين المقبلين على النشر في المجلات المصنفة.",
        "items": [
            "التحليل المتقدم ونمذجة المعادلات البنية (<span class='ltr'>SmartPLS / Process</span>).",
            "استخلاص وتنسيق ورقة بحثية للنشر في المجلات المحكمة.",
            "تدقيق وتنظيف قائمة المراجع وفق الاصدار السابع <span class='ltr'>APA 7</span>."
        ],
        "featured": False,
        "btn_class": "",
        "srv_ref": "s7"
    },
    "p5": {
        "badge": "للمؤسسات والجمعيات والمخابر",
        "title": "باقة مسوح المؤسسات وقياس الاثر",
        "full_label": "باقة مسوح المؤسسات وقياس الاثر (تصميم المسح + لوحة مؤشرات + تقرير تنفيذي)",
        "desc": "حلول بحثية متكاملة للجمعيات والمؤسسات لتقييم المشاريع واستطلاعات الراي.",
        "items": [
            "تصميم خطة المسح الميداني او الرقمي وتدريب جامعي البيانات.",
            "معالجة قواعد البيانات الضخمة واستخراج مؤشرات قياس الاثر.",
            "تقرير تنفيذي شامل بالرسوم البيانية والتوصيات لصناع القرار."
        ],
        "featured": False,
        "btn_class": "",
        "srv_ref": "s6"
    }
}

query_params = st.query_params
if "view" in query_params:
    st.session_state.current_view = query_params["view"]
elif "current_view" not in st.session_state:
    st.session_state.current_view = "home"

if "srv" in query_params and query_params["srv"] in SERVICES_DATA:
    st.session_state.selected_srv = query_params["srv"]
elif "selected_srv" not in st.session_state:
    st.session_state.selected_srv = "s2"

css_styles = (
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Great+Vibes&display=swap');"
    "#MainMenu, header, footer {visibility: hidden;}"
    ".block-container {padding: 0rem !important; max-width: 100% !important;}"
    ".stApp {background-color: #F8FAFC; font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; color: #1E293B;}"
    "h1, h2, h3, h4, p, span, div, label, input, select, textarea, button {font-family: 'Cairo', sans-serif;}"
    ".rtl {direction: rtl; text-align: right; unicode-bidi: isolate;}"
    ".ltr {direction: ltr; text-align: left; display: inline-block; unicode-bidi: isolate; font-family: sans-serif;}"
    ".ltr-block {direction: ltr; text-align: left; display: block; unicode-bidi: isolate;}"
    "input, textarea {unicode-bidi: plaintext !important; font-size: 13px !important; border-radius: 8px !important;}"
    "div[data-baseweb='select'] > div {direction: rtl; text-align: right; font-size: 13px !important; border-radius: 8px !important;}"
    "label p {direction: rtl !important; text-align: right !important; font-size: 13px !important; font-weight: 700 !important; color: #1E293B !important;}"
    ".sl-navbar {background-color: #06182C; border-bottom: 1px solid #163A5F; padding: 10px 6%; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 999; direction: rtl;}"
    ".sl-brand {display: flex; align-items: center; gap: 12px; text-decoration: none;}"
    ".sl-logo-img {height: 54px; width: auto; border-radius: 10px; object-fit: cover; border: 1px solid rgba(56, 189, 248, 0.25);}"
    ".sl-sigma {width: 38px; height: 38px; background-color: #0F2942; border: 1px solid rgba(20, 184, 166, 0.45); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #2DD4BF; font-weight: 800; font-size: 18px;}"
    ".sl-logo-script {font-family: 'Great Vibes', cursive !important; font-size: 26px; color: #FFFFFF; line-height: 1; direction: ltr;}"
    ".sl-logo-sub {font-size: 10px; color: #38BDF8; display: block; margin-top: 2px;}"
    ".sl-nav-links {display: flex; gap: 16px; flex-wrap: wrap;}"
    ".sl-nav-links a {color: #E2E8F0; text-decoration: none; font-size: 12.5px; font-weight: 600;}"
    ".sl-nav-links a:hover, .sl-nav-links a.active {color: #38BDF8;}"
    ".sl-cta-top {background-color: #F59E0B; color: #06182C !important; font-weight: 700; font-size: 13px; padding: 8px 18px; border-radius: 8px; text-decoration: none;}"
    ".sl-hero {background-color: #06182C; background-image: radial-gradient(rgba(56, 189, 248, 0.14) 1px, transparent 1px); background-size: 26px 26px; color: #FFFFFF; padding: 48px 6%; border-bottom: 1px solid #163A5F; direction: rtl; text-align: right;}"
    ".sl-hero-grid {max-width: 1180px; margin: 0 auto; display: grid; grid-template-columns: 1.25fr 0.95fr; gap: 36px; align-items: center;}"
    "@media (max-width: 900px) {.sl-hero-grid {grid-template-columns: 1fr;} .sl-nav-links {display: none;}}"
    ".sl-badge {display: inline-block; background-color: #0F2942; border: 1px solid rgba(56, 189, 248, 0.35); color: #38BDF8; font-size: 11.5px; font-weight: 600; padding: 5px 14px; border-radius: 99px; margin-bottom: 14px;}"
    ".sl-hero-title {font-size: 27px; font-weight: 800; line-height: 1.45; color: #FFFFFF; margin-bottom: 14px;}"
    ".sl-hero-title span {color: #38BDF8;}"
    ".sl-hero-desc {color: #CBD5E1; font-size: 14px; line-height: 1.8; margin-bottom: 24px;}"
    ".sl-hero-btns {display: flex; gap: 12px; flex-wrap: wrap;}"
    ".sl-btn-amber {background-color: #F59E0B; color: #06182C !important; font-weight: 700; font-size: 13.5px; padding: 10px 22px; border-radius: 10px; text-decoration: none;}"
    ".sl-btn-outline {background-color: #0F2942; border: 1px solid #334155; color: #FFFFFF !important; font-weight: 600; font-size: 13.5px; padding: 10px 22px; border-radius: 10px; text-decoration: none;}"
    ".sl-stat-card {background-color: #0F2942; border: 1px solid #1E3A5F; border-radius: 16px; padding: 20px; box-shadow: 0 15px 30px rgba(0,0,0,0.25);}"
    ".sl-stat-header {display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1E3A5F; padding-bottom: 10px; margin-bottom: 14px;}"
    ".sl-kpi-grid {display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 12px 0; text-align: center;}"
    ".sl-kpi-box {background-color: #06182C; border: 1px solid #1E3A5F; border-radius: 10px; padding: 8px;}"
    ".sl-kpi-label {font-size: 11px; color: #94A3B8;}"
    ".sl-kpi-val {font-size: 15px; font-weight: 700; margin-top: 2px; direction: ltr;}"
    ".sl-reading-box {background-color: #06182C; border-right: 3px solid #38BDF8; padding: 10px 12px; border-radius: 6px; font-size: 12px; color: #E2E8F0; line-height: 1.65;}"
    ".sl-section {max-width: 1180px; margin: 0 auto; padding: 40px 6%; direction: rtl; text-align: right;}"
    ".sl-sec-head {text-align: center; max-width: 680px; margin: 0 auto 30px auto;}"
    ".sl-sec-tag {color: #0284C7; font-size: 12.5px; font-weight: 700;}"
    ".sl-sec-title {color: #06182C; font-size: 22px; font-weight: 800; margin: 4px 0 8px 0;}"
    ".sl-sec-sub {color: #64748B; font-size: 13.5px; margin: 0;}"
    ".sl-services-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 18px;}"
    ".sl-srv-card {display: block; text-decoration: none !important; background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 3.5px solid #14B8A6; border-radius: 14px; padding: 22px; box-shadow: 0 2px 6px rgba(0,0,0,0.02); transition: all 0.2s ease; text-align: right;}"
    ".sl-srv-card:hover {transform: translateY(-4px); box-shadow: 0 12px 24px rgba(10, 25, 47, 0.08); border-color: #38BDF8;}"
    ".sl-srv-card.active-card {border: 2px solid #0284C7; background: #F0F9FF;}"
    ".sl-srv-card.navy-top {border-top-color: #06182C;}"
    ".sl-srv-card.amber-top {border-top-color: #F59E0B;}"
    ".sl-srv-num {font-size: 16px; font-weight: 800; color: #14B8A6; margin-bottom: 6px; direction: ltr; display: inline-block;}"
    ".sl-srv-title {font-size: 16px; font-weight: 700; color: #06182C; margin-bottom: 8px;}"
    ".sl-srv-desc {font-size: 13px; color: #475569; line-height: 1.7; margin: 0 0 14px 0;}"
    ".sl-srv-link {font-size: 12.5px; font-weight: 700; color: #0284C7; display: inline-flex; align-items: center; gap: 4px;}"
    ".sl-pkg-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px;}"
    ".sl-pkg-card {background: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 16px; padding: 24px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 15px rgba(10, 25, 47, 0.04); transition: 0.2s; text-align: right;}"
    ".sl-pkg-card:hover {transform: translateY(-3px); box-shadow: 0 10px 22px rgba(6, 24, 44, 0.08);}"
    ".sl-pkg-card.featured {border-color: #06182C; background: linear-gradient(to bottom, #FFFFFF, #F0F9FF);}"
    ".sl-pkg-badge {display: inline-block; background: #FEF3C7; color: #B45309; font-size: 11.5px; font-weight: 700; padding: 4px 12px; border-radius: 99px; margin-bottom: 10px;}"
    ".sl-pkg-badge.dark {background: #06182C; color: #38BDF8;}"
    ".sl-pkg-item {font-size: 13px; color: #334155; padding: 6px 0; border-bottom: 1px dashed #E2E8F0;}"
    ".sl-pkg-btn {display: block; text-align: center; background: #06182C; color: #FFFFFF !important; font-weight: 700; font-size: 13px; padding: 10px; border-radius: 10px; text-decoration: none !important; margin-top: 16px;}"
    ".sl-pkg-btn.amber {background: #F59E0B; color: #06182C !important;}"
    ".sl-clinic-box {background: #06182C; border-radius: 18px; padding: 28px; color: #FFFFFF; border: 1px solid #1E3A5F; text-align: right;}"
    ".sl-radar-card {background: #FFFFFF; border: 1px solid #E2E8F0; border-right: 4px solid #0284C7; border-radius: 12px; padding: 18px; margin-bottom: 14px; text-align: right;}"
    ".sl-probe-result {background: #FFFFFF; border: 1px solid #CBD5E1; border-top: 4px solid #06182C; border-radius: 12px; padding: 18px; margin-top: 14px; font-size: 13px; line-height: 1.75; color: #1E293B; text-align: right;}"
    ".sl-track-banner {background: #FFFFFF; border: 1px solid #E2E8F0; border-right: 5px solid #14B8A6; border-radius: 14px; padding: 20px 24px; margin-bottom: 20px; text-align: right;}"
    ".sl-track-banner.adv {border-right-color: #06182C;}"
    ".sl-track-banner.aud {border-right-color: #F59E0B;}"
    ".sl-detail-box {background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 18px; padding: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); margin-bottom: 24px; text-align: right;}"
    ".sl-deliv-item {background: #F8FAFC; border: 1px solid #E2E8F0; border-right: 3.5px solid #0284C7; padding: 12px 16px; border-radius: 10px; font-size: 13.5px; color: #1E293B; margin-bottom: 10px; text-align: right;}"
    ".sl-back-link {display: inline-block; color: #06182C !important; font-weight: 700; font-size: 13.5px; text-decoration: none !important; margin-bottom: 18px; background: #E2E8F0; padding: 7px 16px; border-radius: 8px;}"
    ".sl-result-banner {background-color: #F0F9FF; border: 1px solid #BAE6FD; border-right: 4px solid #0284C7; padding: 12px 15px; border-radius: 10px; margin-top: 12px; font-size: 13px; color: #0F2942; text-align: right;}"
    ".sl-warn-banner {background-color: #FFFBEB; border: 1px solid #FDE68A; border-right: 4px solid #F59E0B; padding: 12px 15px; border-radius: 10px; margin-top: 12px; font-size: 13px; color: #78350F; text-align: right;}"
    ".sl-apa-table {width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 12.5px; text-align: right;}"
    ".sl-apa-table th {border-top: 2px solid #06182C; border-bottom: 1.5px solid #06182C; padding: 8px; color: #06182C; background: #F8FAFC;}"
    ".sl-apa-table td {padding: 8px; border-bottom: 1px solid #E2E8F0;}"
    ".sl-apa-table tr:last-child td {border-bottom: 2px solid #06182C;}"
    ".sl-email-btn {display: block; text-align: center; background-color: #06182C; color: #38BDF8 !important; border: 1.5px solid #38BDF8; font-weight: 700; font-size: 14px; padding: 12px 20px; border-radius: 10px; text-decoration: none !important; margin-top: 12px;}"
    ".sl-integrity {background-color: #06182C; color: #FFFFFF; text-align: center; padding: 45px 6%; margin-top: 35px;}"
    ".sl-footer {background-color: #04101E; color: #94A3B8; text-align: center; padding: 32px 6%; font-size: 12.5px; border-top: 1px solid #163A5F;}"
    "</style>"
)

st.markdown(css_styles, unsafe_allow_html=True)

active_home = "active" if st.session_state.current_view == "home" else ""
active_srv = "active" if st.session_state.current_view == "services" else ""

if logo_b64:
    brand_html = (
        f'<a href="?view=home" target="_self" class="sl-brand">'
        f'<img src="data:image/jpeg;base64,{logo_b64}" alt="Logo" class="sl-logo-img">'
        f'</a>'
    )
else:
    brand_html = (
        '<a href="?view=home" target="_self" class="sl-brand">'
        '<div class="sl-sigma">&Sigma;</div>'
        '<div><div class="sl-logo-script">Socio Lab</div>'
        '<span class="sl-logo-sub">للتحليل الاحصائي والمنهجية</span></div></a>'
    )

navbar_html = (
    f'<div class="sl-navbar">{brand_html}'
    f'<div class="sl-nav-links">'
    f'<a href="?view=home" target="_self" class="{active_home}">الرئيسية</a>'
    f'<a href="?view=services&srv=s1" target="_self" class="{active_srv}">الخدمات والباقات</a>'
    f'<a href="?view=home#data-auditor" target="_self">فحص البيانات</a>'
    f'<a href="?view=home#portfolio" target="_self">نماذج التقارير</a>'
    f'<a href="?view=home#foundation" target="_self">مسار التاسيس</a>'
    f'<a href="?view=home#advanced" target="_self">مسار الدكتوراه</a>'
    f'</div>'
    f'<a href="?view=services&srv=s2#order-box" target="_self" class="sl-cta-top">الخدمات والباقات</a>'
    f'</div>'
)
st.markdown(navbar_html, unsafe_allow_html=True)

# =====================================================================
# الصفحة الاولى: الواجهة الرئيسية (HOME)
# =====================================================================
if st.session_state.current_view == "home":
    hero_html = (
        '<div class="sl-hero"><div class="sl-hero-grid">'
        '<div>'
        '<div class="sl-badge">&mu; دقة منهجية • قراءة سوسيولوجية • توثيق <span class="ltr">APA 7</span></div>'
        '<div class="sl-hero-title">نحن فضاء علمي رقمي لانتاج المعرفة وتطوير البحث.. '
        '<span>شريكك المنهجي والاحصائي الدقيق</span></div>'
        '<p class="sl-hero-desc">في <strong class="ltr">Socio Lab</strong> نحول البيانات الميدانية الخام '
        'الى رؤى سوسيولوجية وعلمية رصينة. نرافق طلبة الماستر في بناء الاساس المنهجي السليم، '
        'وندعم باحثي الدكتوراه والمؤسسات بالتحليلات المتقدمة ونمذجة المعادلات البنية.</p>'
        '<div class="sl-hero-btns">'
        '<a href="?view=services&srv=s1" target="_self" class="sl-btn-amber">تصفح الخدمات والباقات الاستشارية</a>'
        '<a href="#data-auditor" target="_self" class="sl-btn-outline">افحص ملف بياناتك مجانا</a>'
        '</div></div>'
        '<div class="sl-stat-card">'
        '<div class="sl-stat-header"><div>'
        '<div style="font-size:11px; color:#38BDF8; font-weight:700;">نموذج مخرجات <span class="ltr">Socio Lab</span></div>'
        '<div style="font-size:14px; font-weight:700; color:#FFFFFF;">تحليل التوزيع الطبيعي ومؤشرات الثبات</div>'
        '</div>'
        '<span class="ltr" style="background:rgba(56,189,248,0.18); color:#38BDF8; font-size:11px; padding:3px 8px; border-radius:6px;">SPSS &amp; PLS</span>'
        '</div>'
        '<div style="background:#06182C; padding:10px; border-radius:10px; border:1px solid #1E3A5F;">'
        '<svg viewBox="0 0 300 95" style="width:100%; height:85px; display:block;">'
        '<defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0%" stop-color="#38BDF8" stop-opacity="0.45"/>'
        '<stop offset="100%" stop-color="#38BDF8" stop-opacity="0.0"/>'
        '</linearGradient></defs>'
        '<line x1="10" y1="80" x2="290" y2="80" stroke="#334155" stroke-width="1"/>'
        '<line x1="150" y1="12" x2="150" y2="80" stroke="#F59E0B" stroke-dasharray="3,3" stroke-width="1.3"/>'
        '<path d="M 15 80 C 75 80, 105 12, 150 12 C 195 12, 225 80, 285 80 Z" fill="url(#g1)"/>'
        '<path d="M 15 80 C 75 80, 105 12, 150 12 C 195 12, 225 80, 285 80" fill="none" stroke="#38BDF8" stroke-width="2.2"/>'
        '<text x="150" y="92" fill="#F59E0B" font-size="9" text-anchor="middle">&mu; = 3.84</text>'
        '</svg></div>'
        '<div class="sl-kpi-grid">'
        '<div class="sl-kpi-box"><div class="sl-kpi-label">الفا كرونباخ (<span class="ltr">&alpha;</span>)</div>'
        '<div class="sl-kpi-val" style="color:#38BDF8;">0.892</div></div>'
        '<div class="sl-kpi-box"><div class="sl-kpi-label">حجم العينة (<span class="ltr">N</span>)</div>'
        '<div class="sl-kpi-val" style="color:#FFFFFF;">60</div></div>'
        '<div class="sl-kpi-box"><div class="sl-kpi-label">الدلالة (<span class="ltr">Sig</span>)</div>'
        '<div class="sl-kpi-val" style="color:#F59E0B;">0.001</div></div>'
        '</div>'
        '<div class="sl-reading-box"><strong>القراءة السوسيولوجية:</strong> تشير قيمة الفا كرونباخ (0.892) '
        'الى اتساق داخلي مرتفع جدا لاداة القياس، مع دلالة احصائية تؤكد اثر المتغير المستقل عند مستوى 0.01.</div>'
        '</div></div></div>'
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    # =================================================================
    # الميزة 1: اداة الفحص الفوري لملفات البيانات (Live Data Auditor)
    # =================================================================
    auditor_header = (
        '<div id="data-auditor" style="max-width:1180px; margin:0 auto; padding:40px 6% 10px 6%;">'
        '<div class="sl-track-banner aud">'
        '<div style="font-size:12px; color:#D97706; font-weight:800;">مختبر التشخيص الفوري للبيانات</div>'
        '<div style="font-size:20px; font-weight:800; color:#06182C; margin:4px 0;">'
        'افحص قاعدة بياناتك (<span class="ltr">Excel / CSV</span>) واحسب معامل الثبات فورا</div>'
        '<p style="font-size:13px; color:#64748B; margin:0;">ارفع ملف بياناتك الميدانية الاولية ليكشف النظام تلقائيا عن حجم العينة، القيم المفقودة، والاتساق الداخلي (الفا كرونباخ).</p>'
        '</div></div>'
    )
    st.markdown(auditor_header, unsafe_allow_html=True)

    _, aud_col, _ = st.columns([0.06, 0.88, 0.06])
    with aud_col:
        uploaded_file = st.file_uploader(
            "اختر ملف البيانات بصيغة Excel (.xlsx) او CSV (.csv):",
            type=["xlsx", "xls", "csv"],
            help="يتم فحص الملف لحظيا في الذاكرة دون تخزينه حفاظا على سرية بياناتك."
        )

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                n_rows, n_cols = df.shape
                total_cells = n_rows * n_cols
                missing_cells = int(df.isna().sum().sum())
                missing_pct = round((missing_cells / total_cells) * 100, 2) if total_cells > 0 else 0

                num_df = df.select_dtypes(include=["number"])
                alpha_val = compute_cronbach_alpha(num_df)
                alpha_str = f"{alpha_val:.3f}" if alpha_val is not None else "غير متاح"

                k1, k2, k3, k4 = st.columns(4)
                k1.metric("حجم العينة (الحالات N)", f"{n_rows} حالة")
                k2.metric("عدد المتغيرات (الاعمدة)", f"{n_cols} متغير")
                k3.metric("نسبة القيم المفقودة", f"{missing_pct}%")
                k4.metric("معامل الفا كرونباخ (للاعمدة الرقمية)", alpha_str)

                st.markdown(
                    '<div style="font-size:13.5px; font-weight:700; color:#06182C; margin:12px 0 6px 0;">'
                    'معاينة اول 5 صفوف من قاعدة البيانات:</div>',
                    unsafe_allow_html=True,
                )
                st.dataframe(df.head(5), use_container_width=True)

                if missing_cells > 0:
                    st.markdown(
                        f'<div class="sl-warn-banner"><strong>تنبيه منهجي:</strong> تم رصد <strong>{missing_cells}</strong> خلية مفقودة ({missing_pct}%). '
                        f'يوصى بتنظيف البيانات (<span class="ltr">Data Cleaning</span>) قبل اجراء الاختبارات الاستدلالية في <span class="ltr">SPSS</span>.</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        '<div class="sl-result-banner"><strong>سلامة البيانات:</strong> قاعدة بياناتك مكتملة بنسبة 100% وخالية من القيم المفقودة.</div>',
                        unsafe_allow_html=True,
                    )
            except Exception as exc:
                st.error(f"تعذر قراءة الملف. تاكد من ان الملف غير محمي بكلمة مرور وصالح للقراءة. ({exc})")
        else:
            st.markdown(
                '<div class="sl-result-banner"><strong>ملاحظة الخصوصية:</strong> يتم فحص ملفك لحظيا داخل الجلسة ولا يتم حفظ اي نسخة منه، التزاما بميثاق سرية البيانات في <span class="ltr">Socio Lab</span>.</div>',
                unsafe_allow_html=True,
            )

    # =================================================================
    # الميزة 2: معرض نماذج المخرجات والتقارير الحية (Sample Portfolio)
    # =================================================================
    port_header = (
        '<div id="portfolio" style="max-width:1180px; margin:0 auto; padding:35px 6% 10px 6%;">'
        '<div class="sl-sec-head" style="margin-bottom:18px;">'
        '<div class="sl-sec-tag">معايير الجودة الاكاديمية</div>'
        '<div class="sl-sec-title">معرض نماذج المخرجات والتقارير الحية</div>'
        '<p class="sl-sec-sub">اطلع على عينات حقيقية (مجهولة المصدر) توضح دقة صياغة الجداول والقراءة السوسيولوجية التي تستلمها.</p>'
        '</div></div>'
    )
    st.markdown(port_header, unsafe_allow_html=True)

    _, port_col, _ = st.columns([0.06, 0.88, 0.06])
    with port_col:
        tab1, tab2, tab3 = st.tabs([
            "1. نموذج جدول SPSS وقراءة سوسيولوجية (APA 7)",
            "2. نموذج دليل الترميز (Codebook)",
            "3. نموذج التحليل الموضوعاتي للمقابلات الكيفية"
        ])

        with tab1:
            sample_apa_html = (
                '<div class="sl-detail-box" style="margin-bottom:0; padding:22px;">'
                '<div style="font-size:13px; font-weight:800; color:#06182C; margin-bottom:4px;">'
                'جدول رقم (04): نتائج اختبار الانحدار الخطي البسيط لاثر ضغط جماعة الرفاق في السلوك الجانح (N = 60)</div>'
                '<table class="sl-apa-table">'
                '<thead><tr>'
                '<th>المتغير المستقل</th>'
                '<th>معامل الارتباط (<span class="ltr">R</span>)</th>'
                '<th>معامل التحديد (<span class="ltr">R&sup2;</span>)</th>'
                '<th>قيمة (<span class="ltr">F</span>)</th>'
                '<th>معامل الانحدار (<span class="ltr">&Beta;</span>)</th>'
                '<th>مستوى الدلالة (<span class="ltr">Sig</span>)</th>'
                '</tr></thead>'
                '<tbody><tr>'
                '<td>ضغط جماعة الرفاق</td>'
                '<td class="ltr">0.684</td>'
                '<td class="ltr">0.468</td>'
                '<td class="ltr">51.02</td>'
                '<td class="ltr">0.684</td>'
                '<td class="ltr" style="color:#0284C7; font-weight:700;">0.000</td>'
                '</tr></tbody></table>'
                '<div class="sl-reading-box" style="background:#F8FAFC; color:#1E293B; border-right-color:#06182C;">'
                '<strong>نموذج القراءة السوسيولوجية المرفقة:</strong> تكشف المؤشرات الاحصائية في الجدول اعلاه عن وجود اثر دال احصائيا '
                'عند مستوى (0.01) لضغط جماعة الرفاق في تشكل السلوك الجانح لدى المراهقين؛ اذ يفسر هذا المتغير ما نسبته <strong>46.8%</strong> '
                'من التباين الكلي في السلوك الجانح، وهو ما يتسق مع مقاربة التعلم الاجتماعي لسذرلاند حول دور الجماعات الاولية في نقل المعايير المخالفة.'
                '</div></div>'
            )
            st.markdown(sample_apa_html, unsafe_allow_html=True)

        with tab2:
            codebook_html = (
                '<div class="sl-detail-box" style="margin-bottom:0; padding:22px;">'
                '<div style="font-size:13px; font-weight:800; color:#06182C; margin-bottom:8px;">'
                'نموذج من دليل الترميز المرفق بكل استبيان (<span class="ltr">SPSS Variable View</span>)</div>'
                '<table class="sl-apa-table">'
                '<thead><tr>'
                '<th>رمز المتغير (<span class="ltr">Name</span>)</th>'
                '<th>وصف السؤال (<span class="ltr">Label</span>)</th>'
                '<th>قيم الترميز (<span class="ltr">Values</span>)</th>'
                '<th>مستوى القياس (<span class="ltr">Measure</span>)</th>'
                '</tr></thead>'
                '<tbody>'
                '<tr><td class="ltr">Gender</td><td>الجنس</td><td>1 = ذكر ، 2 = انثى</td><td class="ltr">Nominal</td></tr>'
                '<tr><td class="ltr">Peer_Q1</td><td>اتاثر باراء اصدقائي عند اتخاذ القرار</td><td>1 = معارض بشدة ... 5 = موافق بشدة</td><td class="ltr">Ordinal / Scale</td></tr>'
                '<tr><td class="ltr">Total_Peer</td><td>الدرجة الكلية لمحور جماعة الرفاق</td><td>متوسط العبارات (من 1.00 الى 5.00)</td><td class="ltr">Scale</td></tr>'
                '</tbody></table></div>'
            )
            st.markdown(codebook_html, unsafe_allow_html=True)

        with tab3:
            qual_sample_html = (
                '<div class="sl-detail-box" style="margin-bottom:0; padding:22px;">'
                '<div style="font-size:13px; font-weight:800; color:#06182C; margin-bottom:8px;">'
                'نموذج من شبكة التحليل الموضوعاتي للمقابلات المعمقة (<span class="ltr">Thematic Analysis</span>)</div>'
                '<div class="sl-deliv-item"><strong>الفئة الرئيسية الاولى:</strong> التبريرات الذاتية للتداوي الذاتي<br>'
                '<span style="font-size:12px; color:#475569;">• الرموز الفرعية: ضيق الوقت، الثقة في تجارب المحيط، تجنب تكاليف الفحص الطبي.<br>'
                '• الشاهد الميداني (مبحوث رقم 04، 29 سنة): <em>"لما نحس بالاعياء ناخذ نفس الدواء اللي جربو صاحبي بلا ما نروح للطبيب..."</em></span></div>'
                '</div>'
            )
            st.markdown(qual_sample_html, unsafe_allow_html=True)

    # =================================================================
    # المسار الاول: اضافات الباحثين في المستويات التمهيدية
    # =================================================================
    found_header = (
        '<div id="foundation" style="max-width:1180px; margin:0 auto; padding:40px 6% 10px 6%;">'
        '<div class="sl-track-banner">'
        '<div style="font-size:12px; color:#0D9488; font-weight:800;">المسار التمهيدي وبناء الاساس المنهجي</div>'
        '<div style="font-size:20px; font-weight:800; color:#06182C; margin:4px 0;">ادوات كسر رهبة المنهجية للباحثين الجدد وطلبة الماستر</div>'
        '<p style="font-size:13px; color:#64748B; margin:0;">بسطنا لك المفاهيم الغامضة، ووفرنا لك قائمة فحص لاستمارتك قبل الطباعة، وحاسبة لتقدير وقت وتكلفة الميدان.</p>'
        '</div></div>'
    )
    st.markdown(found_header, unsafe_allow_html=True)

    _, f_col1, f_col2, _ = st.columns([0.06, 0.44, 0.44, 0.06], gap="large")

    with f_col1:
        st.markdown(
            '<div style="font-size:15.5px; font-weight:800; color:#06182C; margin-bottom:10px;">'
            '1. دليل "مصطلحات المنهجية ببساطة"</div>',
            unsafe_allow_html=True,
        )
        glossary_dict = {
            "الفرق بين مجتمع البحث والعينة": (
                "مجتمع البحث هو كل الافراد الذين تنطبق عليهم مشكلتك (مثلا: كل تلاميذ الثانوية). "
                "اما العينة فهي جزء مصغر وممثل تختاره لتطبق عليه الاستبيان لانك لا تستطيع استجواب الجميع."
            ),
            "ما هو المتغير المستقل والمتغير التابع؟": (
                "المتغير المستقل هو السبب او المؤثر (مثل: جماعة الرفاق)، اما المتغير التابع فهو النتيجة "
                "او السلوك الذي يتاثر به (مثل: السلوك الجانح). انت تقيس كيف يغير المستقل في التابع."
            ),
            "ما هو المتغير الوسيط (Mediator)؟": (
                "هو الجسر او الحلقة الوسطى التي تفسر كيف ينتقل الاثر من السبب الى النتيجة. "
                "مثال: البطالة (مستقل) تؤدي الى العزلة الاجتماعية (وسيط) التي تقود الى الاكتئاب (تابع)."
            ),
            "متى نستخدم الاستمارة ومتى نستخدم المقابلة؟": (
                "نستخدم الاستمارة عندما نريد ارقاما ونسبا من عدد كبير من الناس (منهج كمي). "
                "ونستخدم المقابلة عندما نريد فهما عميقا لتجارب ودوافع عدد محدود من الحالات (منهج كيفي)."
            ),
            "ما معنى الصدق والثبات في الاستبيان؟": (
                "الصدق يعني ان اسئلتك تقيس فعلا ما وضعت لقياسه ولا تسال عن موضوع اخر. "
                "اما الثبات (الفا كرونباخ) فيعني ان الاستبيان يعطي نتائج مستقرة لو اعدت تطبيقه."
            ),
        }
        selected_term = st.selectbox("اختر المصطلح المنهجي لفهمه ببساطة:", list(glossary_dict.keys()))
        st.markdown(
            f'<div class="sl-result-banner"><strong>الشرح المبسط بالمثال:</strong><br>{glossary_dict[selected_term]}</div>',
            unsafe_allow_html=True,
        )

    with f_col2:
        st.markdown(
            '<div style="font-size:15.5px; font-weight:800; color:#06182C; margin-bottom:10px;">'
            '2. حاسبة وقت وتكلفة النزول الميداني</div>',
            unsafe_allow_html=True,
        )
        fw_sample = st.number_input("حجم العينة المستهدفة (عدد الاستمارات/المقابلات):", min_value=5, value=60, step=5)
        fw_questions = st.number_input("عدد اسئلة الاستمارة او محاور المقابلة:", min_value=5, value=25, step=5)
        region_opts = [
            "مؤسسة واحدة قريبة (ثانوية / جامعة / شركة)",
            "مناطق متفرقة داخل نفس المدينة",
            "مناطق نائية او عدة بلديات متباعدة",
        ]
        fw_region = st.selectbox("طبيعة المنطقة الجغرافية للتوزيع:", region_opts)

        mins_per_form = round(5 + (fw_questions * 0.4))
        total_hours = math.ceil((fw_sample * mins_per_form) / 60)
        factor = 1 if "مؤسسة واحدة" in fw_region else (1.5 if "متفرقة" in fw_region else 2.2)
        est_days = math.ceil((total_hours / 3) * factor)
        print_cost = fw_sample * 25

        st.markdown(
            f'<div class="sl-result-banner">'
            f'<strong>التقدير الميداني لدراستك:</strong><br>'
            f'• زمن ملء الاستمارة الواحدة: <strong>{mins_per_form} دقيقة تقريبا</strong><br>'
            f'• المدة الزمنية المقترحة لانجاز الميدان: <strong>{est_days} ايام عمل ميداني</strong><br>'
            f'• تكلفة الطباعة التقديرية (ورقي): <strong>{print_cost} دج</strong> (او مجاني عبر <span class="ltr">Google Forms</span>)'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)

    _, chk_col, _ = st.columns([0.06, 0.88, 0.06])
    with chk_col:
        st.markdown(
            '<div style="font-size:15.5px; font-weight:800; color:#06182C; margin-bottom:8px;">'
            '3. قالب "تشخيص مشاكل استمارة الاستبيان" قبل النزول للميدان</div>',
            unsafe_allow_html=True,
        )
        cc1, cc2 = st.columns(2)
        with cc1:
            q1 = st.checkbox("كل سؤال يقيس فكرة واحدة فقط (خلو الاستمارة من الاسئلة المزدوجة).", value=True)
            q2 = st.checkbox("صياغة العبارات محايدة ولا توحي للمبحوث باجابة معينة.", value=True)
            q3 = st.checkbox("تضمين ورقة تعريفية تطمئن المبحوث بسرية بياناته لاغراض علمية.",
