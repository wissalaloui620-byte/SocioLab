import base64
import datetime
import math
import os
import random
import re
import urllib.parse
from collections import Counter
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

CONTACT_EMAIL = "sociolab.dz2026@gmail.com"
LOGO_FILENAME = "En-tête élégant Socio Lab et analytics.png"
APP_URL = "https://sociolab-dz.streamlit.app"


def get_logo_base64(file_path):
    candidates = [
        file_path,
        "En-tête élégant Socio Lab et analytics.png",
        "En-tete elegant Socio Lab et analytics.png",
        "logo.png",
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            with open(candidate, "rb") as f:
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

# =====================================================================
# قاعدة بيانات المحاور الـ 14 لمنظومة Socio Lab المتكاملة
# =====================================================================
PILLARS_DATA = {
    "p01": {
        "num": "01",
        "cat": "التحليل والبيانات",
        "title": "المختبر الاحصائي (Statistical Lab - SPSS)",
        "short": "التحليل الاحصائي الشامل عبر SPSS: الوصفي، الاستدلالي، المعلمي واللامعلمي، العاملي EFA/CFA، والنمذجة المتقدمة.",
        "desc": "القلب النابض للمنصة؛ نغطي كافة مستويات التحليل الاحصائي الاساسي والمتقدم مع اختبار الافتراضات واعداد الجداول وفق APA 7.",
        "items": [
            "الاحصاء الوصفي والاستدلالي (T-test, ANOVA, Pearson, Mann-Whitney, Kruskal-Wallis, Chi-square).",
            "تحليل الانحدار (الخطي، المتعدد، اللوجستي) وتحليل التباين متعدد المتغيرات (MANOVA, MANCOVA).",
            "تحليل الثبات والصدق (Cronbach Alpha, Split-Half, التحليل العاملي الاستكشافي EFA والتوكيدي CFA).",
            "التحليل المتقدم: تحليل المسار، النمذجة الهيكلية SEM، الوساطة والتعديل، السلاسل الزمنية، والبيانات الطولية.",
            "اختبار التوزيع الطبيعي وتجانس التباين، كشف القيم المتطرفة، معالجة القيم المفقودة، وتفسير مخرجات SPSS."
        ]
    },
    "p02": {
        "num": "02",
        "cat": "المنهجية والاستشارات",
        "title": "مركز الاستشارات الاحصائية والمنهجية",
        "short": "مرافقة علمية منذ بناء الاشكالية وتحديد العينة الى غاية اعداد خطة التحليل الاحصائي قبل جمع البيانات.",
        "desc": "جودة التحليل تبدا من تصميم الدراسة قبل فتح برنامج SPSS. نرافق الباحث في ضبط البناء المنهجي بالكامل.",
        "items": [
            "تحديد المنهج المناسب، التصميم البحثي، مجتمع الدراسة، ووحدة التحليل.",
            "حساب حجم العينة واختيار طريقة المعاينة الانسب (عشوائية، طبقية، قصدية، كرة الثلج).",
            "صياغة الاشكالية والتساؤلات وبناء الفرضيات والتعريف الاجرائي للمفاهيم والمتغيرات.",
            "بناء النموذج المفاهيمي واختيار المقاييس العلمية ومراجعة التوافق بين الفرضيات والاختبارات."
        ]
    },
    "p03": {
        "num": "03",
        "cat": "المنهجية والاستشارات",
        "title": "مركز تصميم الاستبيانات وادوات جمع البيانات",
        "short": "بناء الاستبيانات والمقاييس النفسية والاجتماعية، التحكيم، الاختبار القبلي، وبرمجة Google Forms و LimeSurvey.",
        "desc": "مختبر متخصص يحول المفاهيم النظرية المجردة الى مؤشرات ميدانية قابلة للقياس الدقيق.",
        "items": [
            "تصميم الاستبيانات الاكاديمية وبناء المقاييس النفسية والاجتماعية وصياغة الاسئلة المغلقة والمفتوحة.",
            "التحكيم العلمي للاستبيانات وتنفيذ الاختبار القبلي (Pilot Study) لضبط الصدق والثبات.",
            "اعداد دليل المقابلة المعمقة وشبكة الملاحظة الميدانية واستمارات جمع البيانات.",
            "برمجة الاستمارات الرقمية (Google Forms, Microsoft Forms, LimeSurvey) وانشاء قاعدة الترميز Codebook."
        ]
    },
    "p04": {
        "num": "04",
        "cat": "التحليل والبيانات",
        "title": "مركز تحليل البيانات (Data Analysis Center)",
        "short": "بيئات تحليل متعددة تشمل SPSS، R، Python، Stata، Jamovi، JASP، SmartPLS، AMOS، و Excel.",
        "desc": "ندعم بيئات احصائية وبرمجية متنوعة لتلبية متطلبات العلوم الاجتماعية، الاقتصادية، والطبية.",
        "items": [
            "تنظيف قواعد البيانات، دمج الملفات، معالجة القيم المفقودة، واكتشاف الاخطاء.",
            "التحليل المتقدم عبر بيئات R و Python و Stata والاختبارات البايزية عبر JASP و Jamovi.",
            "نمذجة المعادلات الهيكلية عبر SmartPLS و AMOS وبناء لوحات البيانات التفاعلية Dashboards.",
            "تصور البيانات (Data Visualization)، استخراج المؤشرات، وبناء النماذج التنبؤية."
        ]
    },
    "p05": {
        "num": "05",
        "cat": "التحليل والبيانات",
        "title": "مختبر البحث النوعي والمختلط (NVivo & MAXQDA)",
        "short": "تحليل المقابلات المعمقة، مجموعات التركيز، تحليل المضمون والخطاب، وتصميم الدراسات المختلطة.",
        "desc": "مختبر مستقل للبحوث الكيفية والمختلطة لدمج عمق الفهم النوعي مع دقة المؤشرات الكمية.",
        "items": [
            "تحليل المقابلات المعمقة ومجموعات التركيز (Focus Groups) وتحليل الوثائق والخطاب الرقمي.",
            "التحليل الموضوعاتي (Thematic Analysis) والترميز المفتوح والمحوري والانتقائي عبر NVivo و MAXQDA.",
            "تصميم الدراسات المختلطة (Mixed Methods) وبناء جداول التكامل بين النتائج الكمية والنوعية.",
            "تفسير التناقضات بين النتائج الميدانية واعداد تقارير متكاملة للعلوم الاجتماعية والاعلام."
        ]
    },
    "p06": {
        "num": "06",
        "cat": "التكوين والمعرفة",
        "title": "الاكاديمية الرقمية (Socio Lab Academy)",
        "short": "مسارات تكوينية متدرجة في SPSS، الاحصاء التطبيقي، منهجية البحث، وبرامج R و Python و SmartPLS.",
        "desc": "تكوين تطبيقي عملي يربط الجانب النظري بالتدريب على قواعد بيانات حقيقية مع شهادات انجاز.",
        "items": [
            "مسار SPSS من الصفر الى الاحتراف (ادخال البيانات، الاختبارات، التحليل العاملي، وتفسير المخرجات).",
            "مسار الاحصاء التطبيقي ومنهجية البحث العلمي (بناء الاشكالية، المعاينة، تصميم الادوات).",
            "مسار البرامج المتقدمة: Excel المتقدم، Jamovi، JASP، R، Python، SmartPLS، و NVivo.",
            "دورات مباشرة ومسجلة، ورشات تطبيقية، ومخيمات تدريبية احصائية مع مشاريع تطبيقية."
        ]
    },
    "p07": {
        "num": "07",
        "cat": "التكوين والمعرفة",
        "title": "المكتبة العلمية الرقمية (Socio Library)",
        "short": "مراجع الاحصاء والمنهجية، قوالب الجداول، نماذج التقارير، وقاموس المصطلحات عربي-فرنسي-انجليزي.",
        "desc": "مرجع معرفي مفتوح يضم الادلة التطبيقية وقوالب الجداول والقاموس الثلاثي للمصطلحات الاحصائية.",
        "items": [
            "ادلة تطبيقية مبسطة لبرامج التحليل الاحصائي ومناهج البحث في العلوم الاجتماعية والانسانية.",
            "قوالب جاهزة للجداول الاحصائية وفق APA 7 ونماذج تقارير التحليل وتصميم الاستبيانات.",
            "قاموس المصطلحات الاحصائية والمنهجية (عربي - فرنسي - انجليزي) مع الشرح والامثلة."
        ]
    },
    "p08": {
        "num": "08",
        "cat": "الابتكار والذكاء",
        "title": "المساعد الاحصائي الذكي (Socio AI)",
        "short": "مساعد بحثي ذكي لشرح الاختبارات، تفسير مخرجات SPSS، واكتشاف اخطاء البيانات بالعربية والفرنسية.",
        "desc": "محرك ذكي يجمع بين القواعد الاحصائية الموثقة والمراجعة البشرية لمساعدة الباحث في فهم نتائجه.",
        "items": [
            "شرح الاختبارات الاحصائية واقتراح الاختبار الانسب لطبيعة المتغيرات والفرضيات.",
            "تفسير مخرجات SPSS (Alpha, Pearson, Spearman, ANOVA, الانحدار، والتحليل العاملي).",
            "تحويل النتائج الاحصائية الى صياغة اكاديمية رصينة وتقديم تنبيهات عند وجود اخطاء منهجية."
        ]
    },
    "p09": {
        "num": "09",
        "cat": "المنهجية والاستشارات",
        "title": "مركز النشر والدعم الاكاديمي",
        "short": "التوجيه لاختيار المجلات المحكمة، تنسيق المقالات، التدقيق اللغوي، Zotero/Mendeley، والملصقات العلمية.",
        "desc": "نرافق الباحث في تجويد اوراقه العلمية وتنسيقها وفق معايير النشر الدولي دون المساس بالامانة العلمية.",
        "items": [
            "التوجيه في اختيار المجلات العلمية المناسبة والتحقق من فهرستها وتنسيق المقالات.",
            "مراجعة الجداول والاشكال، التدقيق اللغوي الاكاديمي، والترجمة العلمية للملخصات.",
            "ضبط المراجع باستخدام APA و Chicago والتكوين على Zotero و Mendeley و ORCID.",
            "تصميم الملصقات العلمية (Posters) والعروض التقديمية للمؤتمرات والملتقيات."
        ]
    },
    "p10": {
        "num": "10",
        "cat": "الابتكار والذكاء",
        "title": "مرصد الدراسات الاجتماعية (Socio Observatory)",
        "short": "رصد وتحليل الظواهر الاجتماعية، استطلاعات الراي، خرائط الظواهر، واوراق السياسات (Policy Briefs).",
        "desc": "مرصد علمي يتابع التحولات الاجتماعية والرقمية (الجريمة، الشباب، التعليم، السلوك الرقمي) بالبيانات الميدانية.",
        "items": [
            "دراسة وتحليل مؤشرات الظواهر الاجتماعية: الانحراف، السلوك الرقمي، التعليم، الشباب، والاسرة.",
            "اعداد تقارير دورية، استطلاعات راي، وبناء قواعد بيانات وخرائط للظواهر الاجتماعية.",
            "نشر اوراق سياسات (Policy Briefs) وتقديم دراسات استشرافية للهيئات ومراكز البحث."
        ]
    },
    "p11": {
        "num": "11",
        "cat": "المؤسسات والشبكة",
        "title": "مركز الاستشارات والدراسات المؤسساتية",
        "short": "استطلاعات الراي، قياس الرضا الوظيفي، المناخ التنظيمي، تقييم البرامج، ولوحات القيادة للمؤسسات.",
        "desc": "حلول بحثية واحصائية موجهة للجامعات، البلديات، المؤسسات الاقتصادية، ومراكز التكوين والجمعيات.",
        "items": [
            "تنفيذ الدراسات الميدانية واستطلاعات الراي وقياس رضا العملاء والمستفيدين.",
            "دراسات الموارد البشرية: قياس الرضا الوظيفي، المناخ التنظيمي، والالتزام والثقة التنظيمية.",
            "تقييم جودة الخدمات والاثر الاجتماعي للبرامج والمشاريع وبناء مؤشرات الاداء ولوحات القيادة."
        ]
    },
    "p12": {
        "num": "12",
        "cat": "المؤسسات والشبكة",
        "title": "فضاء الباحثين (Socio Research Network)",
        "short": "مجتمع علمي عربي للتشبيك البحثي، الاعلان عن الملتقيات، والبحث عن شركاء ومستشارين في البحث.",
        "desc": "شبكة علمية تربط الباحثين العرب لتبادل الخبرات، الاعلان عن المؤتمرات، وتكوين فرق بحثية مشتركة.",
        "items": [
            "فضاء للتشبيك البحثي والبحث عن شركاء في مشاريع البحث والمقالات المشتركة.",
            "الاعلان عن الملتقيات والمؤتمرات العلمية وفرص النشر والورشات الافتراضية.",
            "تنظيم لقاءات علمية مع اساتذة وخبراء وعرض مشاريع التخرج المتميزة بموافقة اصحابها."
        ]
    },
    "p13": {
        "num": "13",
        "cat": "الابتكار والذكاء",
        "title": "مختبر الادوات الاحصائية المجانية التفاعلية",
        "short": "ادوات حسابية تفاعلية مجانية داخل المنصة لحساب حجم العينة، الفا كرونباخ، الاختبارات، وتوليد الجداول.",
        "desc": "ادوات مجانية متاحة يوميا للباحثين داخل المنصة لاجراء الحسابات السريعة واختيار الاختبار المناسب.",
        "items": [
            "حاسبات العينة (Sample Size)، الثبات (Cronbach Alpha)، والاحصاء الوصفي.",
            "حاسبات الارتباط والفروق (Pearson, Spearman, T-Test, ANOVA, Chi-Square).",
            "ادوات متقدمة: حجم الاثر (Effect Size)، القوة الاحصائية (Power)، فترات الثقة، ومولد جداول APA."
        ]
    },
    "p14": {
        "num": "14",
        "cat": "التكوين والمعرفة",
        "title": "مركز الترجمة والمصطلحات الاحصائية",
        "short": "ترجمة التقارير ومخرجات SPSS، وتوحيد المصطلحات الاحصائية والمنهجية بين العربية والفرنسية والانجليزية.",
        "desc": "نعالج الفجوة اللغوية لدى الباحثين العرب عبر ترجمة علمية دقيقة للمصطلحات والتقارير الاحصائية.",
        "items": [
            "ترجمة المصطلحات الاحصائية والمنهجية وشرح دلالتها التقنية باللغات الثلاث.",
            "ترجمة تقارير التحليل الاحصائي ومخرجات برنامج SPSS من الانجليزية او الفرنسية الى العربية.",
            "توحيد المصطلحات الاكاديمية في الرسائل الجامعية والاوراق الموجهة للنشر الدولي."
        ]
    }
}

PACKAGES_DATA = {
    "pk1": {
        "badge": "المرحلة الاولى: قبل الميدان",
        "title": "باقة التصميم والضبط المنهجي",
        "full_label": "باقة التصميم والضبط المنهجي (بناء الاستمارة + التحكيم + تحديد العينة)",
        "desc": "مخصصة لبناء اساس منهجي سليم واداة قياس محكمة قبل النزول الى الميدان.",
        "items": [
            "صياغة الاشكالية والفرضيات وتحديد المتغيرات والمؤشرات.",
            "بناء الاستبيان او دليل المقابلة مع قاعدة الترميز Codebook.",
            "حساب حجم العينة وتحديد استراتيجية المعاينة المناسبة."
        ],
        "featured": False,
        "btn_class": "",
        "ref": "p03"
    },
    "pk2": {
        "badge": "الاكثر طلبا لطلبة الماستر",
        "title": "باقة التحليل الاحصائي الشامل (SPSS)",
        "full_label": "باقة التحليل الاحصائي الشامل (تنظيف البيانات + الاختبارات + APA 7)",
        "desc": "تغطي كافة مراحل المعالجة الاحصائية في SPSS مع القراءة السوسيولوجية.",
        "items": [
            "تنظيف البيانات، فحص التوزيع الطبيعي، وحساب الصدق والثبات.",
            "اجراء كافة الاختبارات الوصفية والاستدلالية والفروق والارتباط.",
            "اعداد الجداول وفق APA 7 + تقرير بالتفسير السوسيولوجي."
        ],
        "featured": True,
        "btn_class": "rose",
        "ref": "p01"
    },
    "pk3": {
        "badge": "للدكتوراه والنشر الدولي",
        "title": "باقة النمذجة المتقدمة والنشر المحكم",
        "full_label": "باقة النمذجة المتقدمة والنشر المحكم (SEM / SmartPLS + مقال علمي)",
        "desc": "موجهة لاطروحات الدكتوراه والباحثين المقبلين على النشر في المجلات المصنفة.",
        "items": [
            "التحليل المتقدم: SEM، تحليل المسار، الوساطة والتعديل عبر SmartPLS/AMOS.",
            "هيكلة الورقة البحثية وفق IMRAD وضبط المراجع عبر Zotero/APA 7.",
            "مراجعة منهجية شاملة للجداول والاشكال البيانية."
        ],
        "featured": True,
        "btn_class": "rose",
        "ref": "p04"
    },
    "pk4": {
        "badge": "للمؤسسات ومخابر البحث",
        "title": "باقة الدراسات المؤسساتية والمرصد",
        "full_label": "باقة الدراسات المؤسساتية والمرصد (مسح ميداني + Dashboard + تقرير)",
        "desc": "حلول متكاملة للجامعات والبلديات والمؤسسات الاقتصادية والجمعيات.",
        "items": [
            "تصميم المسوح الميدانية والرقمية وقياس الرضا الوظيفي والمناخ التنظيمي.",
            "بناء لوحات القيادة التفاعلية Dashboards واستخراج مؤشرات الاداء.",
            "اعداد التقرير التنفيذي واوراق السياسات Policy Briefs."
        ],
        "featured": False,
        "btn_class": "",
        "ref": "p11"
    }
}

query_params = st.query_params
if "view" in query_params:
    st.session_state.current_view = query_params["view"]
elif "current_view" not in st.session_state:
    st.session_state.current_view = "home"

if "pil" in query_params and query_params["pil"] in PILLARS_DATA:
    st.session_state.selected_pil = query_params["pil"]
elif "selected_pil" not in st.session_state:
    st.session_state.selected_pil = "p01"

# =====================================================================
# SOCIO LAB — DESIGN SYSTEM (Light & Dark Modes + CSS Variables)
# =====================================================================
css_styles = (
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Great+Vibes&display=swap');"
    ":root {"
    "  --plum: #3E0B4F;"
    "  --purple: #6F2DBD;"
    "  --rose: #D58A9B;"
    "  --lavender: #E8D7F1;"
    "  --navy: #0F2D5B;"
    "  --cyan: #00B4D8;"
    "  --bg: #F4F6FA;"
    "  --surface: #FFFFFF;"
    "  --surface-soft: #FAF8FC;"
    "  --text: #3E0B4F;"
    "  --text-muted: #667085;"
    "  --border: #E8D7F1;"
    "  --primary: #6F2DBD;"
    "  --radius-card: 16px;"
    "  --radius-button: 10px;"
    "  --shadow-card: 0 4px 20px rgba(62, 11, 79, 0.06);"
    "}"
    "@media (prefers-color-scheme: dark) {"
    "  :root {"
    "    --bg: #130D1C;"
    "    --surface: #20172B;"
    "    --surface-soft: #291D36;"
    "    --text: #F4EAF8;"
    "    --text-muted: #B9AFC4;"
    "    --border: #493453;"
    "    --primary: #8A45CE;"
    "    --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.22);"
    "  }"
    "}"
    "[data-theme='dark'] {"
    "  --bg: #130D1C;"
    "  --surface: #20172B;"
    "  --surface-soft: #291D36;"
    "  --text: #F4EAF8;"
    "  --text-muted: #B9AFC4;"
    "  --border: #493453;"
    "  --primary: #8A45CE;"
    "  --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.22);"
    "}"
    "#MainMenu, header, footer {visibility: hidden;}"
    ".block-container {padding: 0rem !important; max-width: 100% !important;}"
    ".stApp, body {background-color: var(--bg) !important; font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; color: var(--text);}"
    "h1, h2, h3, h4, p, span, div, label, input, select, textarea, button {font-family: 'Cairo', sans-serif;}"
    ".rtl {direction: rtl; text-align: right; unicode-bidi: isolate;}"
    ".ltr {direction: ltr; text-align: left; display: inline-block; unicode-bidi: isolate; font-family: sans-serif;}"
    ".ltr-block {direction: ltr; text-align: left; display: block; unicode-bidi: isolate;}"
    "input, textarea {unicode-bidi: plaintext !important; font-size: 13px !important; border-radius: var(--radius-button) !important; border: 1px solid var(--border) !important; background-color: var(--surface) !important; color: var(--text) !important;}"
    "div[data-baseweb='select'] > div {direction: rtl; text-align: right; font-size: 13px !important; border-radius: var(--radius-button) !important; border-color: var(--border) !important; background-color: var(--surface) !important;}"
    "label p {direction: rtl !important; text-align: right !important; font-size: 13px !important; font-weight: 700 !important; color: var(--text) !important;}"

    "/* Navbar */"
    ".sl-navbar {background: var(--plum); border-bottom: 2px solid var(--rose); padding: 10px 6%; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 999; direction: rtl; box-shadow: var(--shadow-card);}"
    ".sl-brand {display: flex; align-items: center; gap: 12px; text-decoration: none;}"
    ".sl-logo-img {height: 54px; width: auto; border-radius: 10px; object-fit: cover; border: 1.5px solid var(--rose); background: var(--surface); padding: 2px;}"
    ".sl-sigma {width: 38px; height: 38px; background: var(--primary); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #FFFFFF; font-weight: 800; font-size: 18px;}"
    ".sl-logo-script {font-family: 'Great Vibes', cursive !important; font-size: 26px; color: #FFFFFF; line-height: 1; direction: ltr;}"
    ".sl-logo-sub {font-size: 10px; color: var(--lavender); display: block; margin-top: 2px;}"
    ".sl-nav-links {display: flex; gap: 14px; flex-wrap: wrap;}"
    ".sl-nav-links a {color: var(--lavender); text-decoration: none; font-size: 13px; font-weight: 700; padding: 6px 12px; border-radius: var(--radius-button); transition: all 0.2s ease;}"
    ".sl-nav-links a:hover, .sl-nav-links a.active {color: #FFFFFF; background: var(--primary);}"
    ".sl-cta-top {background: var(--primary); color: #FFFFFF !important; font-weight: 700; font-size: 13px; padding: 9px 20px; border-radius: var(--radius-button); text-decoration: none; border: 1px solid var(--rose);}"

    "/* Hero */"
    ".sl-hero {background: linear-gradient(135deg, var(--plum) 0%, var(--navy) 100%); color: #FFFFFF; padding: 50px 6%; border-bottom: 3px solid var(--rose); direction: rtl; text-align: right;}"
    ".sl-hero-grid {max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 1.2fr 1fr; gap: 38px; align-items: center;}"
    "@media (max-width: 900px) {.sl-hero-grid {grid-template-columns: 1fr;} .sl-nav-links {display: none;}}"
    ".sl-badge {display: inline-flex; align-items: center; gap: 6px; background: rgba(213, 138, 155, 0.18); border: 1px solid var(--rose); color: var(--lavender); font-size: 12px; font-weight: 700; padding: 5px 15px; border-radius: 99px; margin-bottom: 15px;}"
    ".sl-hero-title {font-size: 29px; font-weight: 800; line-height: 1.45; color: #FFFFFF; margin-bottom: 15px;}"
    ".sl-hero-title span {color: var(--rose);}"
    ".sl-hero-desc {color: var(--lavender); font-size: 14.2px; line-height: 1.85; margin-bottom: 24px;}"
    ".sl-hero-btns {display: flex; gap: 14px; flex-wrap: wrap;}"
    ".sl-btn-amber {background: var(--primary); color: #FFFFFF !important; font-weight: 800; font-size: 13.5px; padding: 11px 24px; border-radius: var(--radius-button); text-decoration: none; border: 1px solid var(--rose);}"
    ".sl-btn-outline {background: rgba(255, 255, 255, 0.1); border: 1.5px solid var(--cyan); color: #FFFFFF !important; font-weight: 700; font-size: 13.5px; padding: 11px 24px; border-radius: var(--radius-button); text-decoration: none;}"

    "/* Hero Preview Card */"
    ".sl-stat-card {background: rgba(15, 45, 91, 0.72); backdrop-filter: blur(14px); border: 1px solid rgba(213, 138, 155, 0.4); border-radius: var(--radius-card); padding: 20px; box-shadow: var(--shadow-card);}"
    ".sl-stat-header {display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(232, 215, 241, 0.25); padding-bottom: 10px; margin-bottom: 12px;}"
    ".sl-kpi-grid {display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 12px 0; text-align: center;}"
    ".sl-kpi-box {background: rgba(62, 11, 79, 0.75); border: 1px solid rgba(213, 138, 155, 0.35); border-radius: 10px; padding: 9px;}"
    ".sl-kpi-label {font-size: 11px; color: var(--lavender);}"
    ".sl-kpi-val {font-size: 15.5px; font-weight: 800; margin-top: 2px; direction: ltr;}"
    ".sl-reading-box {background: rgba(62, 11, 79, 0.8); border-right: 3.5px solid var(--cyan); padding: 11px 14px; border-radius: 8px; font-size: 12.2px; color: #FFFFFF; line-height: 1.65;}"

    "/* Trust Bar & Bento Cards */"
    ".sl-trust-bar {background: var(--surface); border-bottom: 1px solid var(--border); padding: 18px 6%; box-shadow: var(--shadow-card);}"
    ".sl-trust-grid {max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; text-align: center;}"
    ".sl-trust-num {font-size: 20px; font-weight: 800; color: var(--primary);}"
    ".sl-trust-txt {font-size: 12.2px; color: var(--text-muted); font-weight: 700;}"
    ".sl-persona-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); gap: 18px; margin-top: 12px;}"
    ".sl-persona-card {background: var(--surface); border: 1px solid var(--border); border-top: 4px solid var(--primary); border-radius: var(--radius-card); padding: 22px; box-shadow: var(--shadow-card); text-align: right;}"
    ".sl-persona-card.adv {border-top-color: var(--navy);}"
    ".sl-persona-card.inst {border-top-color: var(--rose);}"

    "/* Sections & Cards */"
    ".sl-section {max-width: 1200px; margin: 0 auto; padding: 38px 6%; direction: rtl; text-align: right;}"
    ".sl-sec-head {text-align: center; max-width: 740px; margin: 0 auto 26px auto;}"
    ".sl-sec-tag {color: var(--primary); font-size: 12.5px; font-weight: 800; background: var(--surface-soft); border: 1px solid var(--border); display: inline-block; padding: 4px 14px; border-radius: 99px; margin-bottom: 6px;}"
    ".sl-sec-title {color: var(--text); font-size: 23px; font-weight: 800; margin: 4px 0 8px 0;}"
    ".sl-sec-sub {color: var(--text-muted); font-size: 13.8px; margin: 0;}"
    ".sl-services-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(295px, 1fr)); gap: 18px;}"
    ".sl-srv-card {display: block; text-decoration: none !important; background: var(--surface); border: 1px solid var(--border); border-top: 4px solid var(--primary); border-radius: var(--radius-card); padding: 20px; box-shadow: var(--shadow-card); transition: all 0.2s ease; text-align: right;}"
    ".sl-srv-card:hover {transform: translateY(-3px); border-color: var(--rose);}"
    ".sl-srv-card.active-card {border: 2px solid var(--primary); background: var(--surface-soft);}"
    ".sl-srv-num {font-size: 14px; font-weight: 800; color: var(--rose); margin-bottom: 4px; direction: ltr; display: inline-block;}"
    ".sl-srv-cat {font-size: 11px; font-weight: 700; color: var(--primary); background: var(--surface-soft); border: 1px solid var(--border); padding: 2px 10px; border-radius: 99px; float: left;}"
    ".sl-srv-title {font-size: 15.5px; font-weight: 800; color: var(--text); margin: 8px 0; clear: both;}"
    ".sl-srv-desc {font-size: 12.8px; color: var(--text-muted); line-height: 1.7; margin: 0 0 12px 0;}"
    ".sl-srv-link {font-size: 12.5px; font-weight: 800; color: var(--primary); display: inline-flex; align-items: center; gap: 4px;}"

    "/* Packages */"
    ".sl-pkg-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 16px;}"
    ".sl-pkg-card {background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-card); padding: 22px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: var(--shadow-card); text-align: right;}"
    ".sl-pkg-card.featured {border: 2px solid var(--primary); background: var(--surface-soft);}"
    ".sl-pkg-badge {display: inline-block; background: var(--surface-soft); border: 1px solid var(--border); color: var(--text); font-size: 11.5px; font-weight: 700; padding: 4px 12px; border-radius: 99px; margin-bottom: 10px;}"
    ".sl-pkg-badge.dark {background: var(--plum); color: #FFFFFF; border-color: var(--rose);}"
    ".sl-pkg-item {font-size: 13px; color: var(--text); padding: 6px 0; border-bottom: 1px dashed var(--border);}"
    ".sl-pkg-btn {display: block; text-align: center; background: var(--navy); color: #FFFFFF !important; font-weight: 700; font-size: 13px; padding: 10px; border-radius: var(--radius-button); text-decoration: none !important; margin-top: 16px;}"
    ".sl-pkg-btn.rose {background: var(--primary); color: #FFFFFF !important; font-weight: 800;}"

    "/* Containers & Banners */"
    ".sl-about-box, .sl-detail-box {background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-card); padding: 24px; margin-bottom: 18px; box-shadow: var(--shadow-card); text-align: right;}"
    ".sl-clinic-box {background: linear-gradient(135deg, var(--plum) 0%, var(--navy) 100%); border-radius: var(--radius-card); padding: 24px; color: #FFFFFF; border-right: 4px solid var(--cyan); box-shadow: var(--shadow-card); text-align: right;}"
    ".sl-radar-card {background: var(--surface); border: 1px solid var(--border); border-right: 4px solid var(--primary); border-radius: var(--radius-card); padding: 16px; margin-top: 10px; box-shadow: var(--shadow-card); text-align: right;}"
    ".sl-probe-result {background: var(--surface); border: 1px solid var(--border); border-right: 4px solid var(--primary); border-radius: var(--radius-card); padding: 16px; margin-top: 12px; font-size: 13px; line-height: 1.75; color: var(--text); box-shadow: var(--shadow-card); text-align: right;}"
    ".sl-deliv-item {background: var(--surface-soft); border: 1px solid var(--border); border-right: 3.5px solid var(--primary); padding: 10px 14px; border-radius: var(--radius-button); font-size: 13px; color: var(--text); margin-bottom: 8px; text-align: right;}"
    ".sl-back-link {display: inline-block; color: var(--text) !important; font-weight: 800; font-size: 13px; text-decoration: none !important; margin-bottom: 16px; background: var(--surface); border: 1px solid var(--border); padding: 7px 16px; border-radius: var(--radius-button);}"
    ".sl-back-link:hover {border-color: var(--primary); color: var(--primary) !important;}"
    ".sl-result-banner {background-color: var(--surface-soft); border: 1px solid var(--border); border-right: 4px solid var(--primary); padding: 12px 15px; border-radius: var(--radius-button); margin-top: 10px; font-size: 13px; color: var(--text); text-align: right;}"
    ".sl-warn-banner {background-color: var(--surface-soft); border: 1px solid var(--rose); border-right: 4px solid var(--rose); padding: 12px 15px; border-radius: var(--radius-button); margin-top: 10px; font-size: 13px; color: var(--text); text-align: right;}"
    ".sl-cert-box {background: linear-gradient(135deg, var(--plum) 0%, var(--navy) 100%); border: 2px solid var(--rose); border-radius: var(--radius-card); padding: 20px; color: #FFFFFF; text-align: center; margin-top: 12px;}"

    "/* APA 7 Tables */"
    ".sl-apa-table {width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 12.8px; direction: rtl; background: var(--surface);}"
    ".sl-apa-table th {border-top: 2px solid var(--plum); border-bottom: 1.5px solid var(--plum); padding: 9px; color: var(--text); background: var(--surface-soft); text-align: right; font-weight: 800;}"
    ".sl-apa-table td {padding: 9px; border-bottom: 1px solid var(--border); text-align: right; vertical-align: middle; color: var(--text);}"
    ".sl-apa-table td.num-cell {direction: ltr; text-align: right; font-family: sans-serif; display: table-cell;}"
    ".sl-apa-table tr:last-child td {border-bottom: 2px solid var(--plum);}"

    ".sl-email-btn {display: block; text-align: center; background: var(--primary); color: #FFFFFF !important; font-weight: 800; font-size: 14px; padding: 12px 20px; border-radius: var(--radius-button); text-decoration: none !important; margin-top: 12px;}"
    ".sl-integrity {background: linear-gradient(125deg, var(--plum) 0%, var(--navy) 100%); color: #FFFFFF; text-align: center; padding: 42px 6%; margin-top: 25px; border-top: 2px solid var(--rose);}"
    ".sl-footer {background-color: var(--plum); color: var(--lavender); text-align: center; padding: 30px 6%; font-size: 12.5px; border-top: 2px solid var(--rose);}"
    "</style>"
)

st.markdown(css_styles, unsafe_allow_html=True)

active_home = "active" if st.session_state.current_view == "home" else ""
active_srv = "active" if st.session_state.current_view == "services" else ""
active_app = "active" if st.session_state.current_view == "applied_lab" else ""

if logo_b64:
    brand_html = (
        f'<a href="?view=home" target="_self" class="sl-brand">'
        f'<img src="data:image/png;base64,{logo_b64}" alt="Socio Lab Logo" class="sl-logo-img">'
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
    f'<a href="?view=services&pil=p01" target="_self" class="{active_srv}">الخدمات والباقات (14)</a>'
    f'<a href="?view=applied_lab" target="_self" class="{active_app}">استوديو البحث الميداني</a>'
    f'<a href="?view=home#interactive-lab" target="_self">المختبر الذكي</a>'
    f'<a href="?view=home#about-us" target="_self">من نحن</a>'
    f'</div>'
    f'<a href="?view=services&pil=p01#order-box" target="_self" class="sl-cta-top">اطلب خدمة الان</a>'
    f'</div>'
)
st.markdown(navbar_html, unsafe_allow_html=True)

# =====================================================================
# الصفحة الاولى: الواجهة الرئيسية
# =====================================================================
if st.session_state.current_view == "home":
    if logo_b64:
        hero_right_card = (
            f'<div class="sl-stat-card">'
            f'<div class="sl-stat-header"><div>'
            f'<div style="font-size:11px; color:var(--rose); font-weight:700;">الهوية البصرية الرسمية</div>'
            f'<div style="font-size:14.5px; font-weight:800; color:#FFFFFF;">معا .. نحو معرفة اعمق لمجتمع افضل</div>'
            f'</div>'
            f'<span class="ltr" style="background:rgba(0,180,216,0.2); color:var(--cyan); font-size:11px; padding:4px 10px; border-radius:8px; font-weight:700;">SPSS &amp; PLS</span>'
            f'</div>'
            f'<div style="background:var(--surface); padding:8px; border-radius:14px; border:1.5px solid var(--rose); margin-bottom:12px;">'
            f'<img src="data:image/png;base64,{logo_b64}" alt="Socio Lab Banner" style="width:100%; height:auto; border-radius:10px; display:block;">'
            f'</div>'
            f'<div class="sl-kpi-grid">'
            f'<div class="sl-kpi-box"><div class="sl-kpi-label">الفا كرونباخ (<span class="ltr">&alpha;</span>)</div>'
            f'<div class="sl-kpi-val" style="color:var(--cyan);">0.892</div></div>'
            f'<div class="sl-kpi-box"><div class="sl-kpi-label">حجم العينة (<span class="ltr">N</span>)</div>'
            f'<div class="sl-kpi-val" style="color:#FFFFFF;">60</div></div>'
            f'<div class="sl-kpi-box"><div class="sl-kpi-label">الدلالة (<span class="ltr">Sig</span>)</div>'
            f'<div class="sl-kpi-val" style="color:var(--rose);">0.001</div></div>'
            f'</div>'
            f'<div class="sl-reading-box"><strong>القراءة السوسيولوجية:</strong> تشير قيمة الفا كرونباخ (0.892) '
            f'الى اتساق داخلي مرتفع جدا لاداة القياس، مع دلالة احصائية تؤكد اثر المتغير المستقل عند مستوى 0.01.</div>'
            f'</div>'
        )
    else:
        hero_right_card = (
            '<div class="sl-stat-card">'
            '<div class="sl-stat-header"><div>'
            '<div style="font-size:11px; color:var(--rose); font-weight:700;">محاكاة حية لمخرجات <span class="ltr">Socio Lab</span></div>'
            '<div style="font-size:14.5px; font-weight:800; color:#FFFFFF;">تحليل التوزيع الطبيعي ومؤشرات الثبات</div>'
            '</div>'
            '<span class="ltr" style="background:rgba(0,180,216,0.2); color:var(--cyan); font-size:11px; padding:4px 10px; border-radius:8px; font-weight:700;">SPSS &amp; PLS</span>'
            '</div>'
            '<div style="background:rgba(62,11,79,0.75); padding:12px; border-radius:12px; border:1px solid rgba(213,138,155,0.3);">'
            '<svg viewBox="0 0 300 95" style="width:100%; height:88px; display:block;">'
            '<defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0%" stop-color="#00B4D8" stop-opacity="0.55"/>'
            '<stop offset="100%" stop-color="#3E0B4F" stop-opacity="0.0"/>'
            '</linearGradient></defs>'
            '<line x1="10" y1="80" x2="290" y2="80" stroke="rgba(232,215,241,0.35)" stroke-width="1"/>'
            '<line x1="150" y1="12" x2="150" y2="80" stroke="#D58A9B" stroke-dasharray="3,3" stroke-width="1.6"/>'
            '<path d="M 15 80 C 75 80, 105 12, 150 12 C 195 12, 225 80, 285 80 Z" fill="url(#g1)"/>'
            '<path d="M 15 80 C 75 80, 105 12, 150 12 C 195 12, 225 80, 285 80" fill="none" stroke="#00B4D8" stroke-width="2.6"/>'
            '<text x="150" y="92" fill="#D58A9B" font-size="9.5" font-weight="bold" text-anchor="middle">&mu; = 3.84</text>'
            '</svg></div>'
            '<div class="sl-kpi-grid">'
            '<div class="sl-kpi-box"><div class="sl-kpi-label">الفا كرونباخ (<span class="ltr">&alpha;</span>)</div>'
            '<div class="sl-kpi-val" style="color:var(--cyan);">0.892</div></div>'
            '<div class="sl-kpi-box"><div class="sl-kpi-label">حجم العينة (<span class="ltr">N</span>)</div>'
            '<div class="sl-kpi-val" style="color:#FFFFFF;">60</div></div>'
            '<div class="sl-kpi-box"><div class="sl-kpi-label">الدلالة (<span class="ltr">Sig</span>)</div>'
            '<div class="sl-kpi-val" style="color:var(--rose);">0.001</div></div>'
            '</div>'
            '<div class="sl-reading-box"><strong>القراءة السوسيولوجية:</strong> تشير قيمة الفا كرونباخ (0.892) '
            'الى اتساق داخلي مرتفع جدا لاداة القياس، مع دلالة احصائية تؤكد اثر المتغير المستقل عند مستوى 0.01.</div>'
            '</div>'
        )

    hero_html = (
        f'<div class="sl-hero"><div class="sl-hero-grid">'
        f'<div>'
        f'<div class="sl-badge">&mu; دقة منهجية • قراءة سوسيولوجية • توثيق <span class="ltr">APA 7</span></div>'
        f'<div class="sl-hero-title">نحن فضاء علمي رقمي لانتاج المعرفة وتطوير البحث.. '
        f'<span>شريكك المنهجي والاحصائي الدقيق</span></div>'
        f'<p class="sl-hero-desc">في <strong class="ltr">Socio Lab</strong> نحول البيانات الميدانية الخام '
        f'الى رؤى سوسيولوجية وعلمية رصينة. نرافق طلبة الليسانس والماستر والدكتوراه، والاساتذة، '
        f'ومخابر البحث، والمؤسسات في التحليل الاحصائي، التصميم المنهجي، والبحث النوعي والمختلط.</p>'
        f'<div class="sl-hero-btns">'
        f'<a href="?view=services&pil=p01" target="_self" class="sl-btn-amber">تصفح اقسام المنصة (14) والباقات</a>'
        f'<a href="?view=applied_lab" target="_self" class="sl-btn-outline">استوديو البحث الميداني التطبيقي</a>'
        f'</div></div>'
        f'{hero_right_card}'
        f'</div></div>'
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    trust_bar_html = (
        '<div class="sl-trust-bar"><div class="sl-trust-grid">'
        '<div><div class="sl-trust-num">14 محورا</div><div class="sl-trust-txt">منظومة علمية واحصائية وتكوينية شاملة</div></div>'
        '<div><div class="sl-trust-num">11 بيئة تحليل</div><div class="sl-trust-txt ltr">SPSS, R, Python, SmartPLS, NVivo...</div></div>'
        '<div><div class="sl-trust-num ltr">APA 7th</div><div class="sl-trust-txt">التزام صارم بمعايير التوثيق العالمي</div></div>'
        '<div><div class="sl-trust-num">100%</div><div class="sl-trust-txt">بيانات ميدانية حقيقية وسرية تامة</div></div>'
        '</div></div>'
    )
    st.markdown(trust_bar_html, unsafe_allow_html=True)

    persona_html = (
        '<div class="sl-section" style="padding-bottom:10px;">'
        '<div class="sl-sec-head" style="margin-bottom:20px;">'
        '<div class="sl-sec-tag">الفئات المستهدفة والمسارات البحثية</div>'
        '<div class="sl-sec-title">من تخدم منصة <span class="ltr">Socio Lab</span>؟</div>'
        '</div>'
        '<div class="sl-persona-grid">'
        '<div class="sl-persona-card">'
        '<div style="font-size:12px; color:var(--primary); font-weight:800;">01 • طلبة الليسانس والماستر</div>'
        '<div style="font-size:16.5px; font-weight:800; color:var(--text); margin:6px 0 8px 0;">بناء الاساس المنهجي ومذكرات التخرج</div>'
        '<p style="font-size:13px; color:var(--text-muted); line-height:1.75; margin-bottom:12px;">'
        'صياغة الاشكالية والفرضيات، تصميم الاستبيانات، التحليل الوصفي والاستدلالي عبر SPSS، وتنسيق الجداول وفق APA 7.</p>'
        '<a href="#interactive-lab" class="sl-srv-link">استخدم الادوات التفاعلية المجانية ادناه &darr;</a>'
        '</div>'
        '<div class="sl-persona-card adv">'
        '<div style="font-size:12px; color:var(--navy); font-weight:800;">02 • طلبة الدكتوراه والاساتذة الباحثون</div>'
        '<div style="font-size:16.5px; font-weight:800; color:var(--text); margin:6px 0 8px 0;">النمذجة المتقدمة والنشر الدولي المحكم</div>'
        '<p style="font-size:13px; color:var(--text-muted); line-height:1.75; margin-bottom:12px;">'
        'تحليل المسار، النمذجة الهيكلية SEM (SmartPLS / AMOS)، التحليل العاملي EFA/CFA، والبحث النوعي والمختلط.</p>'
        '<a href="?view=applied_lab" target="_self" class="sl-srv-link">انتقل الى استوديو البحث الميداني التطبيقي &larr;</a>'
        '</div>'
        '<div class="sl-persona-card inst">'
        '<div style="font-size:12px; color:var(--rose); font-weight:800;">03 • مخابر البحث، الجامعات، والمؤسسات</div>'
        '<div style="font-size:16.5px; font-weight:800; color:var(--text); margin:6px 0 8px 0;">استطلاعات الراي، المرصد، ولوحات القيادة</div>'
        '<p style="font-size:13px; color:var(--text-muted); line-height:1.75; margin-bottom:12px;">'
        'الدراسات الميدانية، قياس الرضا الوظيفي والمناخ التنظيمي، تقييم البرامج، واعداد اوراق السياسات Policy Briefs.</p>'
        '<a href="?view=services&pil=p11" target="_self" class="sl-srv-link">تصفح حلول المؤسسات ومخابر البحث &larr;</a>'
        '</div>'
        '</div></div>'
    )
    st.markdown(persona_html, unsafe_allow_html=True)

    # =================================================================
    # المختبر التفاعلي المبوب (5 تبويبات)
    # =================================================================
    lab_header = (
        '<div id="interactive-lab" style="max-width:1200px; margin:0 auto; padding:25px 6% 10px 6%;">'
        '<div class="sl-sec-head" style="margin-bottom:16px;">'
        '<div class="sl-sec-tag">مختبر الادوات الاحصائية والمنهجية المجانية</div>'
        '<div class="sl-sec-title">المختبر التفاعلي الذكي (<span class="ltr">Statistical &amp; Methodological Tools</span>)</div>'
        '<p class="sl-sec-sub">تنقل بين التبويبات الخمسة ادناه لاستخدام فاحص البيانات، اختيار الاختبار الاحصائي، الهندسة البصرية، والتوثيق.</p>'
        '</div></div>'
    )
    st.markdown(lab_header, unsafe_allow_html=True)

    _, lab_col, _ = st.columns([0.04, 0.92, 0.04])
    with lab_col:
        tab_data, tab_selector, tab_visual, tab_socio, tab_defense = st.tabs([
            "1. فحص البيانات وجداول APA 7",
            "2. مختبر اختيار الاختبار (Test Selector)",
            "3. الهندسة البصرية والمخططات",
            "4. الذكاء السوسيولوجي والقياس",
            "5. التوثيق، القاموس الثلاثي، والشهادة"
        ])

        with tab_data:
            st.markdown(
                '<div style="font-size:16px; font-weight:800; color:var(--text); margin:10px 0;">'
                'أ. فاحص البيانات الفوري (<span class="ltr">Excel / CSV Data Auditor</span>)</div>',
                unsafe_allow_html=True,
            )
            uploaded_file = st.file_uploader(
                "ارفع ملف بياناتك الميدانية بصيغة Excel (.xlsx) او CSV (.csv) لفحصه لحظيا:",
                type=["xlsx", "xls", "csv"],
                key="home_uploader"
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
                    k1.metric("حجم العينة (N)", f"{n_rows} حالة")
                    k2.metric("عدد المتغيرات", f"{n_cols} متغير")
                    k3.metric("القيم المفقودة", f"{missing_pct}%")
                    k4.metric("الفا كرونباخ", alpha_str)

                    missing_by_col = df.isna().sum()
                    if missing_cells > 0:
                        st.bar_chart(missing_by_col[missing_by_col > 0])

                    st.dataframe(df.head(5), use_container_width=True)

                    audit_report_txt = (
                        f"تقرير الفحص الاولي لقاعدة البيانات - مختبر Socio Lab\n"
                        f"====================================================\n"
                        f"اسم الملف: {uploaded_file.name}\n"
                        f"- حجم العينة (N): {n_rows} حالة\n"
                        f"- عدد المتغيرات: {n_cols} متغير\n"
                        f"- الخلايا المفقودة: {missing_cells} ({missing_pct}%)\n"
                        f"- معامل الفا كرونباخ: {alpha_str}\n"
                        f"للطلب الكامل للتحليل: {CONTACT_EMAIL}\n"
                    )
                    st.download_button(
                        label="تحميل تقرير الفحص الاولي ممهورا باسم Socio Lab (.txt)",
                        data=audit_report_txt,
                        file_name="SocioLab_Data_Audit_Report.txt",
                        mime="text/plain",
                        use_container_width=True,
                    )
                except Exception as exc:
                    st.error(f"تعذر قراءة الملف: {exc}")
            else:
                st.markdown(
                    '<div class="sl-result-banner"><strong>ملاحظة الخصوصية:</strong> يتم فحص ملفك لحظيا داخل الجلسة ولا يتم حفظ اي نسخة منه.</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<hr style='margin:22px 0; border-color:var(--border);'>", unsafe_allow_html=True)

            st.markdown(
                '<div style="font-size:16px; font-weight:800; color:var(--text); margin-bottom:8px;">'
                'ب. مولد الجداول الاحصائية المطابقة لمعايير <span class="ltr">APA 7</span></div>',
                unsafe_allow_html=True,
            )
            at1, at2, at3, at4, at5 = st.columns(5)
            with at1:
                apa_tbl_num = st.text_input("رقم الجدول:", value="01")
            with at2:
                apa_var_name = st.text_input("اسم البعد / المتغير:", value="الوعي الرقمي")
            with at3:
                apa_mean = st.text_input("المتوسط (M):", value="3.84")
            with at4:
                apa_sd = st.text_input("الانحراف المعياري (SD):", value="0.62")
            with at5:
                apa_sig = st.text_input("الدلالة (Sig):", value="0.001")

            apa_tbl_title = st.text_input("عنوان الجدول العلمي:", value="المتوسطات الحسابية والانحرافات المعيارية لاستجابات افراد العينة")

            generated_apa_table = (
                f'<div class="sl-detail-box" style="margin-top:10px; padding:18px;">'
                f'<div style="font-weight:800; color:var(--text); font-size:13.5px;">جدول رقم ({apa_tbl_num})</div>'
                f'<div style="font-style:italic; color:var(--text-muted); font-size:13px; margin-bottom:8px;">{apa_tbl_title}</div>'
                f'<table class="sl-apa-table">'
                f'<thead><tr>'
                f'<th>المتغير / البعد</th>'
                f'<th>المتوسط الحسابي (<span class="ltr">M</span>)</th>'
                f'<th>الانحراف المعياري (<span class="ltr">SD</span>)</th>'
                f'<th>مستوى الدلالة (<span class="ltr">Sig</span>)</th>'
                f'</tr></thead>'
                f'<tbody><tr>'
                f'<td>{apa_var_name}</td>'
                f'<td class="num-cell">{apa_mean}</td>'
                f'<td class="num-cell">{apa_sd}</td>'
                f'<td class="num-cell">{apa_sig}</td>'
                f'</tr></tbody></table>'
                f'<div style="font-size:11.5px; color:var(--text-muted); font-style:italic;">ملاحظة. النتائج مستخرجة وفق معايير النشر الاكاديمي APA 7th.</div>'
                f'</div>'
            )
            st.markdown(generated_apa_table, unsafe_allow_html=True)

            st.markdown("<hr style='margin:22px 0; border-color:var(--border);'>", unsafe_allow_html=True)
            st.markdown(
                '<div style="font-size:16px; font-weight:800; color:var(--text); margin-bottom:10px;">'
                'ج. معرض نماذج المخرجات الحية (جدول الانحدار + دليل الترميز)</div>',
                unsafe_allow_html=True,
            )
            sub_t1, sub_t2 = st.tabs(["نموذج جدول SPSS وقراءة سوسيولوجية (APA 7)", "نموذج دليل الترميز (Codebook)"])
            with sub_t1:
                sample_apa_html = (
                    '<div class="sl-detail-box" style="margin-bottom:0; padding:18px;">'
                    '<div style="font-size:13px; font-weight:800; color:var(--text); margin-bottom:4px;">'
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
                    '<td class="num-cell">0.684</td>'
                    '<td class="num-cell">0.468</td>'
                    '<td class="num-cell">51.02</td>'
                    '<td class="num-cell">0.684</td>'
                    '<td class="num-cell" style="color:var(--primary); font-weight:700;">0.000</td>'
                    '</tr></tbody></table>'
                    '<div class="sl-reading-box" style="background:var(--surface-soft); color:var(--text); border-right-color:var(--primary);">'
                    '<strong>نموذج القراءة السوسيولوجية المرفقة:</strong> تكشف المؤشرات الاحصائية في الجدول اعلاه عن وجود اثر دال احصائيا '
                    'عند مستوى (0.01) لضغط جماعة الرفاق في تشكل السلوك الجانح لدى المراهقين؛ اذ يفسر هذا المتغير ما نسبته <strong>46.8%</strong> '
                    'من التباين الكلي في السلوك الجانح، وهو ما يتسق مع مقاربة التعلم الاجتماعي لسذرلاند.'
                    '</div></div>'
                )
                st.markdown(sample_apa_html, unsafe_allow_html=True)
            with sub_t2:
                st.markdown(
                    '<div class="sl-detail-box" style="margin-bottom:0; padding:18px;">'
                    '<table class="sl-apa-table">'
                    '<thead><tr><th>رمز المتغير</th><th>وصف السؤال</th><th>قيم الترميز</th><th>مستوى القياس</th></tr></thead>'
                    '<tbody>'
                    '<tr><td class="num-cell">Gender</td><td>الجنس</td><td>1 = ذكر ، 2 = انثى</td><td class="num-cell">Nominal</td></tr>'
                    '<tr><td class="num-cell">Peer_Q1</td><td>اتاثر باراء اصدقائي عند اتخاذ القرار</td><td>1 = معارض بشدة ... 5 = موافق بشدة</td><td class="num-cell">Ordinal</td></tr>'
                    '</tbody></table></div>',
                    unsafe_allow_html=True,
                )

        with tab_selector:
            st.markdown(
                '<div style="font-size:16px; font-weight:800; color:var(--text); margin:10px 0;">'
                'مختبر اختيار الاختبار الاحصائي (<span class="ltr">Statistical Test Selector</span>)</div>',
                unsafe_allow_html=True,
            )
            ts1, ts2, ts3 = st.columns(3)
            with ts1:
                ts_goal = st.selectbox(
                    "1. طبيعة العلاقة او الهدف:",
                    [
                        "قياس العلاقة الارتباطية بين متغيرين",
                        "قياس الفروق بين مجموعتين مستقلتين",
                        "قياس الفروق بين 3 مجموعات فاكثر",
                        "قياس الفروق القبلية والبعدية لنفس العينة",
                        "قياس اثر متغير مستقل على متغير تابع",
                        "اختبار العلاقة بين متغيرين اسميين (فئات)",
                    ],
                )
            with ts2:
                ts_scale = st.selectbox(
                    "2. مستوى قياس البيانات:",
                    [
                        "كمي متصل (فئوي / نسبي)",
                        "رتبي (مثل مقياس ليكرت)",
                        "اسمي (تصنيفي مثل الجنس والتخصص)",
                    ],
                )
            with ts3:
                ts_norm = st.selectbox(
                    "3. شرط التوزيع الطبيعي:",
                    [
                        "يتبع التوزيع الطبيعي (Sig > 0.05)",
                        "لا يتبع التوزيع الطبيعي (Sig < 0.05)",
                    ],
                )

            is_param = ("كمي" in ts_scale) and ("يتبع التوزيع الطبيعي" in ts_norm)

            if "الارتباطية" in ts_goal:
                if is_param:
                    t_title = "معامل ارتباط بيرسون (Pearson Correlation)"
                    t_why = "لقياس قوة واتجاه العلاقة الخطية بين متغيرين كميين متصلين."
                    t_cond = "التوزيع الطبيعي للمتغيرين، العلاقة الخطية، وعدم وجود قيم متطرفة حادة."
                    t_spss = "Analyze > Correlate > Bivariate > Pearson"
                    t_interp = "اذا كانت قيمة Sig اقل من 0.05 توجد علاقة دالة؛ تقترب r من 1 كلما زادت القوة."
                else:
                    t_title = "معامل ارتباط سبيرمان (Spearman's Rho)"
                    t_why = "لقياس العلاقة الرتبية بين متغيرين لا يتبعان التوزيع الطبيعي او مقاسين بمقياس ليكرت."
                    t_cond = "بيانات رتبية او كمية ملتوية، وعلاقة رتيبة (Monotonic) بين المتغيرين."
                    t_spss = "Analyze > Correlate > Bivariate > Spearman"
                    t_interp = "نفس قراءة بيرسون؛ قيمة Sig اقل من 0.05 تعني وجود ارتباط دال احصائيا."
            elif "مجموعتين مستقلتين" in ts_goal:
                if is_param:
                    t_title = "اختبار ت لعينتين مستقلتين (Independent-Samples T-Test)"
                    t_why = "لمقارنة متوسطات درجات مجموعتين مستقلتين تماما (مثل: ذكور واناث)."
                    t_cond = "استقلال العينتين، التوزيع الطبيعي، وتجانس التباين (اختبار Levene)."
                    t_spss = "Analyze > Compare Means > Independent-Samples T Test"
                    t_interp = "اذا كانت Sig اقل من 0.05 توجد فروق ذات دلالة احصائية لصالح المجموعة ذات المتوسط الاعلى."
                else:
                    t_title = "اختبار مان-ويتني (Mann-Whitney U Test)"
                    t_why = "البديل اللامعلمي لاختبار T لمقارنة رتب مجموعتين مستقلتين عند اختلال التوزيع الطبيعي."
                    t_cond = "استقلال العينتين وقياس المتغير التابع بمستوى رتبي او كمي غير طبيعي."
                    t_spss = "Analyze > Nonparametric Tests > Legacy Dialogs > 2 Independent Samples"
                    t_interp = "نعتمد على متوسط الرتب (Mean Rank) وقيمة Sig لتحديد دلالة الفروق."
            elif "3 مجموعات" in ts_goal:
                if is_param:
                    t_title = "تحليل التباين الاحادي (One-Way ANOVA)"
                    t_why = "لمقارنة متوسطات 3 مجموعات مستقلة فاكثر (مثل: المستويات التعليمية او الفئات العمرية)."
                    t_cond = "التوزيع الطبيعي داخل كل مجموعة وتجانس التباين بين المجموعات."
                    t_spss = "Analyze > Compare Means > One-Way ANOVA"
                    t_interp = "قيمة F بدلالة Sig اقل من 0.05 تعني وجود فروق؛ نستخدم اختبارات Post-Hoc لمعرفة مصدرها."
                else:
                    t_title = "اختبار كروسكال-واليس (Kruskal-Wallis H Test)"
                    t_why = "البديل اللامعلمي لتحليل التباين الاحادي عند مقارنة 3 مجموعات فاكثر."
                    t_cond = "عينات مستقلة وبيانات رتبية او غير طبيعية التوزيع."
                    t_spss = "Analyze > Nonparametric Tests > Legacy Dialogs > K Independent Samples"
                    t_interp = "تدل قيمة مربع كاي ودلالتها Sig اقل من 0.05 على وجود فروق دالة بين المجموعات."
            elif "القبلية والبعدية" in ts_goal:
                if is_param:
                    t_title = "اختبار ت للعينات المرتبطة (Paired-Samples T-Test)"
                    t_why = "لقياس اثر برنامج تدريبي او تدخل عبر مقارنة القياس القبلي والبعدي لنفس الافراد."
                    t_cond = "التوزيع الطبيعي للفروق بين القياسين القبلي والبعدي."
                    t_spss = "Analyze > Compare Means > Paired-Samples T Test"
                    t_interp = "مقارنة متوسط القياس البعدي بالقبلي مع فحص قيمة t ومستوى الدلالة Sig."
                else:
                    t_title = "اختبار ويلكوكسون (Wilcoxon Signed-Rank Test)"
                    t_why = "البديل اللامعلمي لاختبار العينات المرتبطة عند عدم تحقق التوزيع الطبيعي."
                    t_cond = "بيانات مرتبطة (قبل/بعد) بمستوى قياس رتبي او كمي ملتوٍ."
                    t_spss = "Analyze > Nonparametric Tests > Legacy Dialogs > 2 Related Samples"
                    t_interp = "يعتمد على الرتب السالبة والموجبة وقيمة Z ومستوى الدلالة Sig."
            elif "اثر متغير مستقل" in ts_goal:
                t_title = "تحليل الانحدار الخطي (Linear Regression)"
                t_why = "للتنبؤ بقيمة المتغير التابع ومعرفة نسبة التباين التي يفسرها المتغير المستقل (R Square)."
                t_cond = "الخطية، التوزيع الطبيعي للبواقي، واستقلال الاخطاء (Durbin-Watson)."
                t_spss = "Analyze > Regression > Linear"
                t_interp = "قيمة R2 تحدد نسبة التفسير، ومعامل Beta يحدد قوة واتجاه التاثير."
            else:
                t_title = "اختبار كاي تربيع للاستقلالية (Chi-Square Test)"
                t_why = "لفحص العلاقة بين متغيرين اسميين تصنيفيين عبر الجداول المتقاطعة (Crosstabs)."
                t_cond = "الا يقل التكرار المتوقع في اكثر من 20% من الخلايا عن 5."
                t_spss = "Analyze > Descriptive Statistics > Crosstabs > Statistics > Chi-square"
                t_interp = "قيمة Pearson Chi-Square بدلالة Sig اقل من 0.05 تعني وجود ارتباط بين الفئتين."

            selector_card = (
                f'<div class="sl-probe-result">'
                f'<div style="font-size:16px; font-weight:800; color:var(--primary); margin-bottom:10px;">الاختبار المقترح: {t_title}</div>'
                f'<div style="margin-bottom:6px;"><strong>• لماذا ومتى نستخدمه؟</strong> {t_why}</div>'
                f'<div style="margin-bottom:6px;"><strong>• شروط الاستخدام:</strong> {t_cond}</div>'
                f'<div style="margin-bottom:6px;"><strong>• مسار التطبيق في SPSS:</strong> <span class="ltr" style="font-family:monospace; color:var(--text); font-weight:700;">{t_spss}</span></div>'
                f'<div><strong>• كيفية تفسير النتائج:</strong> {t_interp}</div>'
                f'</div>'
            )
            st.markdown(selector_card, unsafe_allow_html=True)

            st.markdown("<hr style='margin:20px 0; border-color:var(--border);'>", unsafe_allow_html=True)
            sc_c1, sc_c2 = st.columns(2, gap="large")
            with sc_c1:
                st.markdown('<div style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:6px;">حاسبة حجم العينة (معادلة ستيفن ثامبسون)</div>', unsafe_allow_html=True)
                pop_size = st.number_input("حجم مجتمع الدراسة الكلي (N):", min_value=10, value=500, step=10)
                margin_label = st.selectbox("هامش الخطا المسموح به:", ["5% (مستوى ثقة 95%)", "1% (مستوى ثقة 99%)", "10% (مستوى ثقة 90%)"])
                e = 0.05 if "5%" in margin_label else (0.01 if "1%" in margin_label else 0.10)
                z = 1.96 if e == 0.05 else (2.576 if e == 0.01 else 1.645)
                n0 = (z**2 * 0.25) / (e**2)
                sample_n = math.ceil(n0 / (1 + ((n0 - 1) / pop_size)))
                st.markdown(f'<div class="sl-result-banner"><strong>الحد الادنى للعينة (n):</strong> <span style="font-size:17px; font-weight:800;">{sample_n} مفردة</span></div>', unsafe_allow_html=True)

            with sc_c2:
                st.markdown('<div style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:6px;">حاسبة حجم الاثر (<span class="ltr">Cohen\'s d</span>)</div>', unsafe_allow_html=True)
                ef1, ef2, ef3 = st.columns(3)
                with ef1:
                    m1_val = st.number_input("متوسط 1:", value=3.90, step=0.1)
                with ef2:
                    m2_val = st.number_input("متوسط 2:", value=3.20, step=0.1)
                with ef3:
                    sd_pool = st.number_input("الانحراف:", min_value=0.1, value=0.85, step=0.05)
                cohen_d = round(abs(m1_val - m2_val) / sd_pool, 2)
                d_interp = "اثر ضعيف" if cohen_d < 0.5 else ("اثر متوسط" if cohen_d < 0.8 else "اثر قوي")
                st.markdown(f'<div class="sl-result-banner"><strong>قيمة Cohen\'s d:</strong> {cohen_d} ({d_interp})</div>', unsafe_allow_html=True)

        with tab_visual:
            st.markdown(
                '<div style="font-size:16px; font-weight:800; color:var(--text); margin:10px 0;">'
                '1. مصور النماذج السببية والمسارات (<span class="ltr">Causal Path Diagram Builder</span>)</div>',
                unsafe_allow_html=True,
            )
            vp1, vp2, vp3 = st.columns(3)
            with vp1:
                v_indep = st.text_input("المتغير المستقل (X):", value="ضغط جماعة الرفاق", key="v_ind")
            with vp2:
                v_med = st.text_input("المتغير الوسيط / المعدل (M):", value="ضعف الرقابة الاسرية", key="v_med")
            with vp3:
                v_dep = st.text_input("المتغير التابع (Y):", value="السلوك الجانح", key="v_dep")

            svg_diagram = (
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 220" style="width:100%; max-height:220px; background:var(--surface); border:1px solid var(--border); border-radius:16px;">'
                f'<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
                f'<path d="M 0 1 L 10 5 L 0 9 z" fill="#6F2DBD"/></marker></defs>'
                f'<rect x="460" y="110" width="200" height="55" rx="10" fill="#3E0B4F" stroke="#D58A9B" stroke-width="2"/>'
                f'<text x="560" y="133" fill="#E8D7F1" font-size="11" text-anchor="middle" font-family="Cairo, sans-serif">المتغير المستقل (X)</text>'
                f'<text x="560" y="152" fill="#FFFFFF" font-size="13" font-weight="bold" text-anchor="middle" font-family="Cairo, sans-serif">{v_indep}</text>'
                f'<rect x="250" y="25" width="200" height="55" rx="10" fill="#E8D7F1" stroke="#6F2DBD" stroke-width="2"/>'
                f'<text x="350" y="48" fill="#6F2DBD" font-size="11" text-anchor="middle" font-family="Cairo, sans-serif">المتغير الوسيط (M)</text>'
                f'<text x="350" y="67" fill="#3E0B4F" font-size="13" font-weight="bold" text-anchor="middle" font-family="Cairo, sans-serif">{v_med}</text>'
                f'<rect x="40" y="110" width="200" height="55" rx="10" fill="#0F2D5B" stroke="#00B4D8" stroke-width="2"/>'
                f'<text x="140" y="133" fill="#00B4D8" font-size="11" text-anchor="middle" font-family="Cairo, sans-serif">المتغير التابع (Y)</text>'
                f'<text x="140" y="152" fill="#FFFFFF" font-size="13" font-weight="bold" text-anchor="middle" font-family="Cairo, sans-serif">{v_dep}</text>'
                f'<line x1="460" y1="138" x2="246" y2="138" stroke="#6F2DBD" stroke-width="2.2" marker-end="url(#arrow)"/>'
                f'<text x="350" y="155" fill="#6F2DBD" font-size="11" font-weight="bold" text-anchor="middle">الاثر المباشر (H1)</text>'
                f'<line x1="520" y1="110" x2="410" y2="82" stroke="#D58A9B" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrow)"/>'
                f'<line x1="290" y1="80" x2="180" y2="108" stroke="#D58A9B" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrow)"/>'
                f'</svg>'
            )
            st.markdown(svg_diagram, unsafe_allow_html=True)
            st.download_button(
                label="تحميل مخطط النموذج السببي بصيغة صورة متجهة (.svg)",
                data=svg_diagram,
                file_name="SocioLab_Causal_Model.svg",
                mime="image/svg+xml",
                use_container_width=True,
            )

            st.markdown("<hr style='margin:20px 0; border-color:var(--border);'>", unsafe_allow_html=True)
            st.markdown(
                '<div style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:6px;">'
                '2. محاكي التوزيع الطبيعي والالتواء (<span class="ltr">Skewness Visualizer</span>)</div>',
                unsafe_allow_html=True,
            )
            skew_val = st.slider("حرك مؤشر الالتواء (Skewness) لمعاينة شكل التوزيع:", -2.0, 2.0, 0.0, 0.2)
            x_vals = np.linspace(-3, 3, 100)
            y_vals = np.exp(-0.5 * ((x_vals - skew_val) ** 2))
            chart_df = pd.DataFrame({"الكثافة الاحتمالية": y_vals}, index=np.round(x_vals, 2))
            st.line_chart(chart_df, height=150)

        with tab_socio:
            st.markdown(
                '<div style="font-size:16px; font-weight:800; color:var(--text); margin:10px 0;">'
                '1. مترجم الاحصاء الى خطاب سوسيولوجي (<span class="ltr">Stats-to-Sociology Translator</span>)</div>',
                unsafe_allow_html=True,
            )
            st_c1, st_c2 = st.columns([0.45, 0.55])
            with st_c1:
                res_pattern = st.selectbox(
                    "اختر طبيعة النتيجة الاحصائية:",
                    [
                        "علاقة ارتباطية طردية قوية ودالة احصائيا",
                        "علاقة ارتباطية عكسية دالة احصائيا",
                        "عدم وجود فروق ذات دلالة احصائية بين الجنسين",
                        "رفض الفرضية البديلة وقبول الفرضية الصفرية",
                    ],
                )
                res_vars = st.text_input("متغيرا النتيجة:", value="التعرض للمنصات الرقمية والاغتراب القيمي")

            with st_c2:
                socio_templates = {
                    "علاقة ارتباطية طردية قوية ودالة احصائيا": (
                        f"تكشف الدلالة الاحصائية عن وجود تلازم بنائي طردي بين ({res_vars})؛ وهو ما يعكس ديناميكية "
                        f"التفاعل الاجتماعي حيث يؤدي تنامي المتغير المستقل الى اعادة تشكيل تمثلات الفاعلين وسلوكهم داخل النسق."
                    ),
                    "علاقة ارتباطية عكسية دالة احصائيا": (
                        f"تبرز المؤشرات الاحصائية علاقة عكسية دالة بين ({res_vars})، مما يدل على ان ارتفاع مستويات المتغير الاول "
                        f"يعمل كآلية ضبط وقائية تحد من تفاقم الظاهرة المدروسة، وهو ما ينسجم مع مقاربات الضبط الاجتماعي."
                    ),
                    "عدم وجود فروق ذات دلالة احصائية بين الجنسين": (
                        f"يشير غياب الفروق الدالة احصائيا بين الذكور والاناث في ({res_vars}) الى تجانس التنشئة الاجتماعية "
                        f"وتماثل التعرض لنفس المؤثرات الثقافية والمؤسساتية، مما يقلص الفجوة التقليدية بين الجنسين."
                    ),
                    "رفض الفرضية البديلة وقبول الفرضية الصفرية": (
                        f"ان عدم تحقق الفرضية البحثية حول ({res_vars}) لا يعد فشلا للبحث، بل يمثل كشفا سوسيولوجيا مهما "
                        f"يؤكد حياد هذا العامل ويدفع نحو البحث عن محددات بنيوية وثقافية اخرى اكثر تفسيرا للظاهرة."
                    ),
                }
                st.markdown(
                    f'<div class="sl-probe-result" style="margin-top:0;">'
                    f'<strong style="color:var(--primary);">الصياغة السوسيولوجية المقترحة للتقرير:</strong><br>'
                    f'"{socio_templates[res_pattern]}"</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<hr style='margin:20px 0; border-color:var(--border);'>", unsafe_allow_html=True)
            sc_l1, sc_l2 = st.columns(2, gap="large")
            with sc_l1:
                st.markdown('<div style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:8px;">2. مفسر مستويات مقياس ليكرت وطول الفئة</div>', unsafe_allow_html=True)
                likert_type = st.selectbox("نوع المقياس:", ["مقياس ليكرت الخماسي (1 الى 5)", "مقياس ليكرت الثلاثي (1 الى 3)", "مقياس ليكرت الرباعي (1 الى 4)"])
                mean_input = st.number_input("قيمة المتوسط الحسابي:", min_value=1.0, max_value=5.0, value=3.68, step=0.05)

                max_scale = 5 if "الخماسي" in likert_type else (3 if "الثلاثي" in likert_type else 4)
                cat_len = round((max_scale - 1) / 3, 2)
                low_lim = round(1 + cat_len, 2)
                mid_lim = round(low_lim + cat_len, 2)
                lvl_label = "مستوى منخفض" if mean_input <= low_lim else ("مستوى متوسط" if mean_input <= mid_lim else "مستوى مرتفع")

                st.markdown(
                    f'<div class="sl-result-banner">'
                    f'<strong>النتيجة:</strong> المتوسط (<strong>{mean_input}</strong>) يقع ضمن <strong>[{lvl_label}]</strong>.<br>'
                    f'<span style="font-size:12px;">طول الفئة = {cat_len} | منخفض (1-{low_lim})، متوسط ({low_lim+0.01:.2f}-{mid_lim})، مرتفع ({mid_lim+0.01:.2f}-{max_scale}).</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            with sc_l2:
                st.markdown('<div style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:8px;">3. كاشف التحيز في صياغة اسئلة الاستبيان</div>', unsafe_allow_html=True)
                q_draft = st.text_input("اكتب عبارة من استبيانك لفحصها:", placeholder="مثال: هل توافق على ان الادارة سيئة ومقصرة؟")
                if q_draft:
                    issues = []
                    if " و" in q_draft and ("هل " in q_draft or "ان " in q_draft):
                        issues.append("احتمال وجود سؤال مزدوج يقيس فكرتين في عبارة واحدة.")
                    if any(w in q_draft for w in ["سيئة", "ممتازة", "خطير", "بالطبع", "لا شك"]):
                        issues.append("صياغة ايحائية غير محايدة قد توجه اجابة المبحوث.")
                    if issues:
                        st.markdown('<div class="sl-warn-banner"><strong>تنبيه:</strong><br>• ' + "<br>• ".join(issues) + '</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="sl-result-banner"><strong>صياغة سليمة:</strong> العبارة واضحة ومحايدة.</div>', unsafe_allow_html=True)

        with tab_defense:
            st.markdown(
                '<div style="font-size:16px; font-weight:800; color:var(--text); margin:10px 0;">'
                '1. قاموس المصطلحات الاحصائية (<span class="ltr">عربي - Français - English</span>)</div>',
                unsafe_allow_html=True,
            )
            dict_terms = {
                "معامل الثبات الفا كرونباخ | Alpha de Cronbach | Cronbach's Alpha": "مؤشر يقيس الاتساق الداخلي لعبارات المقياس؛ تعد القيمة اكبر من 0.70 مقبولة احصائيا.",
                "مستوى الدلالة الاحصائية | Seuil de signification | P-Value (Sig)": "احتمال وقوع النتيجة عن طريق الصدفة؛ اذا كان اقل من 0.05 نرفض الفرضية الصفرية.",
                "التوزيع الطبيعي | Distribution normale | Normal Distribution": "توزيع اعتدالي للبيانات على شكل جرس يحدد ما اذا كنا سنستخدم اختبارات معلمية او لامعلمية.",
                "المتغير الوسيط | Variable médiatrice | Mediating Variable": "متغير يفسر الية وكيفية انتقال الاثر من المتغير المستقل الى المتغير التابع.",
                "نمذجة المعادلات الهيكلية | Modélisation par équations structurelles | SEM": "تقنية احصائية متقدمة تختبر نماذج سببية متعددة المسارات والمتغيرات الكامنة."
            }
            sel_dterm = st.selectbox("ابحث في القاموس الثلاثي:", list(dict_terms.keys()))
            st.markdown(f'<div class="sl-result-banner"><strong>التعريف والاستخدام:</strong> {dict_terms[sel_dterm]}</div>', unsafe_allow_html=True)

            st.markdown("<hr style='margin:20px 0; border-color:var(--border);'>", unsafe_allow_html=True)
            dc1, dc2 = st.columns(2, gap="large")
            with dc1:
                st.markdown('<div style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:8px;">2. مولد المراجع (<span class="ltr">APA 7th</span>)</div>', unsafe_allow_html=True)
                ref_author = st.text_input("المؤلف:", placeholder="مثال: العلوي، وصال / Bourdieu, P.")
                ref_year = st.text_input("السنة:", placeholder="2026")
                ref_title = st.text_input("العنوان:", placeholder="اثر جماعة الرفاق في السلوك الجانح")
                ref_source = st.text_input("المصدر:", placeholder="مجلة العلوم الاجتماعية، 14(2)")
                if ref_author and ref_year and ref_title:
                    is_latin = ref_author.strip()[0].isascii()
                    ref_dir_class = "ltr-block" if is_latin else "rtl"
                    st.markdown(f'<div class="sl-result-banner"><div class="{ref_dir_class}">{ref_author} ({ref_year}). <em>{ref_title}</em>. {ref_source}.</div></div>', unsafe_allow_html=True)

            with dc2:
                st.markdown('<div style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:8px;">3. شهادة الجاهزية المنهجية الاولية</div>', unsafe_allow_html=True)
                cert_name = st.text_input("اسم الباحث(ة):", placeholder="مثال: علوي وصال")
                cert_study = st.text_input("عنوان البحث:", placeholder="مثال: اثر جماعة الرفاق في السلوك الجانح")
                if cert_name and cert_study:
                    today_str = datetime.date.today().strftime("%Y-%m-%d")
                    cert_code = f"SL-CERT-{random.randint(1000, 9999)}"
                    st.markdown(
                        f'<div class="sl-cert-box" style="padding:16px;">'
                        f'<div style="font-size:11px; color:var(--rose); font-weight:700;">مختبر Socio Lab</div>'
                        f'<div style="font-size:16px; font-weight:800; margin:4px 0;">شهادة اجتياز الفحص المنهجي الاولي</div>'
                        f'<div style="font-size:12.5px;">الباحث(ة): <strong>{cert_name}</strong> | رمز: <span class="ltr">{cert_code}</span> ({today_str})</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

    # =================================================================
    # الارشيف التفاعلي لعيادة المنهجية ومرصد الدراسات الاجتماعية
    # =================================================================
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    _, cr_col1, cr_col2, _ = st.columns([0.05, 0.44, 0.44, 0.05], gap="large")

    with cr_col1:
        st.markdown(
            '<div class="sl-clinic-box">'
            '<span style="background:rgba(0, 180, 216, 0.2); color:var(--cyan); font-size:11.5px; font-weight:700; padding:4px 12px; border-radius:99px;">عيادة المنهجية</span>'
            '<h3 style="color:#FFFFFF; font-size:19px; font-weight:800; margin:10px 0 6px 0;">عيادة المنهجية والاحصاء المباشرة</h3>'
            '<p style="color:var(--lavender); font-size:13px; line-height:1.7; margin-bottom:0;">تشخيص وتصحيح ابرز الاخطاء المنهجية والاحصائية الشائعة في الرسائل الجامعية:</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        clinic_cases = {
            "حالة 01: ارتفاع معامل الثبات مع فشل اختبار الفرضيات": "السبب المنهجي: صياغة عبارات الاستبيان بشكل عام لا يقيس المتغير التابع بدقة. التصحيح: ربط كل عبارة بمؤشر اجرائي محدد.",
            "حالة 02: استخدام اختبار T-Test لعينة صغيرة غير طبيعية": "السبب المنهجي: تطبيق اختبارات معلمية دون فحص التوزيع الطبيعي. التصحيح: التحول الى اختبار مان-ويتني (Mann-Whitney).",
            "حالة 03: تداخل المتغير الوسيط مع المتغير المعدل": "السبب المنهجي: الخلط بين تفسير الية الانتقال (الوساطة) وشروط القوة (الاعتدال). التصحيح: ضبط النموذج عبر Process Macro."
        }
        sel_case = st.selectbox("اختر الحالة المنهجية لقراءة التشخيص:", list(clinic_cases.keys()))
        st.markdown(f'<div class="sl-result-banner">{clinic_cases[sel_case]}</div>', unsafe_allow_html=True)

    with cr_col2:
        st.markdown(
            '<div><span class="sl-sec-tag">مرصد الدراسات الاجتماعية (Socio Observatory)</span>'
            '<h3 class="sl-sec-title" style="font-size:19px; margin-bottom:8px;">رادار الظواهر والاتجاهات السوسيولوجية</h3></div>',
            unsafe_allow_html=True,
        )
        radar_topics = {
            "1. السلوك الرقمي والتنمر الالكتروني لدى المراهقين": "رصد تحولات التنشئة الاجتماعية في ظل المنصات الخوارزمية وتاثيرها على القيم. فرصة بحثية: قياس اثر التعرض الانتقائي.",
            "2. الجريمة، الانحراف، وتعاطي المؤثرات العقلية": "تحليل العوامل السوسيو-مؤسساتية المفسرة للتداوي الذاتي وسوء استخدام المؤثرات العقلية في الوسط الشباني.",
            "3. التعليم العالي والفجوة الرقمية": "دراسة اخلاقيات البحث العلمي وتوظيف الذكاء الاصطناعي في البيئة الجامعية بين التمكين والاتكالية."
        }
        sel_radar = st.selectbox("تصفح ملفات الرصد الاجتماعي:", list(radar_topics.keys()))
        st.markdown(f'<div class="sl-radar-card"><p style="font-size:13px; color:var(--text-muted); line-height:1.7; margin:0;">{radar_topics[sel_radar]}</p></div>', unsafe_allow_html=True)

    qr_img_url = f"https://api.qrserver.com/v1/create-qr-code/?size=130x130&data={urllib.parse.quote(APP_URL)}"
    about_qr_html = (
        f'<div id="about-us" class="sl-section" style="padding-top:20px;">'
        f'<div class="sl-about-box" style="display:grid; grid-template-columns: 1fr auto; gap:24px; align-items:center;">'
        f'<div>'
        f'<div class="sl-sec-tag">الهوية العلمية والمرجعية الاكاديمية</div>'
        f'<h3 style="font-size:21px; font-weight:800; color:var(--text); margin:4px 0 10px 0;">من نحن؟ رؤية <span class="ltr">Socio Lab</span></h3>'
        f'<p style="font-size:13.5px; color:var(--text); line-height:1.8; margin-bottom:10px;">'
        f'<strong class="ltr">Socio Lab</strong> منصة علمية رقمية متخصصة في الاحصاء وتحليل البيانات والبحث العلمي، تجمع بين التكنولوجيا، '
        f'المنهجية العلمية، والابتكار البحثي. نهدف الى ان نكون المرجع العربي الرائد والموثوق في الاحصاء التطبيقي باستخدام SPSS والبيئات المتقدمة.</p>'
        f'<p style="font-size:13px; color:var(--text-muted); line-height:1.75; margin:0;">'
        f'نخدم طلبة الليسانس والماستر والدكتوراه، الاساتذة، مخابر البحث، الجامعات، والمؤسسات العمومية والخاصة ومراكز الدراسات.</p>'
        f'</div>'
        f'<div style="text-align:center; background:var(--surface-soft); padding:14px; border-radius:14px; border:1px solid var(--border);">'
        f'<img src="{qr_img_url}" alt="QR Code" style="width:120px; height:120px; display:block; margin:0 auto 6px auto;">'
        f'<div style="font-size:11px; font-weight:700; color:var(--text);">امسح الرمز لمشاركة المنصة</div>'
        f'</div>'
        f'</div></div>'
    )
    st.markdown(about_qr_html, unsafe_allow_html=True)

    integrity_html = (
        '<div id="integrity" class="sl-integrity">'
        '<div style="max-width:800px; margin:0 auto;">'
        '<span style="background:rgba(213, 138, 155, 0.22); color:var(--lavender); font-size:11.5px; font-weight:700; padding:4px 12px; border-radius:99px;">الالتزام الاخلاقي والعلمي</span>'
        '<div style="color:#FFFFFF; font-size:20px; font-weight:800; margin:12px 0 8px 0;">ميثاق النزاهة العلمية وسرية البيانات في <span class="ltr">Socio Lab</span></div>'
        '<p style="color:var(--lavender); font-size:13.5px; line-height:1.8; margin:0;">تلتزم منصة <span class="ltr">Socio Lab</span> بتقديم الاستشارات المنهجية والتحليل الاحصائي للبيانات الميدانية الحقيقية فقط، وترفض رفضا قاطعا فبركة البيانات او بيع البحوث الجاهزة او شراء النشر او اي ممارسة تخل بالامانة العلمية، مع ضمان السرية التامة لافكار الباحثين وبياناتهم.</p>'
        '</div></div>'
    )
    st.markdown(integrity_html, unsafe_allow_html=True)

# =====================================================================
# الصفحة الثانية: المنظومة المتكاملة للخدمات والباقات (14 محورا)
# =====================================================================
elif st.session_state.current_view == "services":
    current_key = st.session_state.selected_pil
    current_pil = PILLARS_DATA[current_key]
    selected_pkg = query_params.get("pkg", "")

    st.markdown(
        '<div class="sl-section" style="padding-top:28px; padding-bottom:10px;">'
        '<a href="?view=home" target="_self" class="sl-back-link">&rarr; العودة الى الواجهة الرئيسية</a>'
        '<div class="sl-sec-head" style="margin-bottom:18px;">'
        '<div class="sl-sec-tag">الهيكلة الشاملة لمنصة Socio Lab</div>'
        '<div class="sl-sec-title">الاقسام والخدمات العلمية والاحصائية (14 محورا)</div>'
        '<p class="sl-sec-sub">تصفح الاقسام حسب التخصص، واضغط على اي قسم لعرض خدماته التفصيلية او اطلب خدماتك مباشرة في الاسفل.</p>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    _, srv_wrap, _ = st.columns([0.05, 0.90, 0.05])
    with srv_wrap:
        cat_tabs = st.tabs([
            "جميع الاقسام (14)",
            "التحليل الاحصائي والبيانات (SPSS & المتقدم)",
            "المنهجية، الاستبيانات، والنشر",
            "الاكاديمية، المكتبة، والترجمة",
            "المرصد، المؤسسات، والذكاء الاصطناعي"
        ])

        def render_pillar_cards(filter_cat=None):
            html_out = '<div class="sl-services-grid">'
            for k, p in PILLARS_DATA.items():
                if filter_cat and p["cat"] not in filter_cat:
                    continue
                act_cls = "active-card" if k == current_key else ""
                html_out += (
                    f'<a href="?view=services&pil={k}#pillar-details" target="_self" class="sl-srv-card {act_cls}">'
                    f'<span class="sl-srv-num">{p["num"]}</span>'
                    f'<span class="sl-srv-cat">{p["cat"]}</span>'
                    f'<div class="sl-srv-title">{p["title"]}</div>'
                    f'<p class="sl-srv-desc">{p["short"]}</p>'
                    f'<span class="sl-srv-link">عرض قائمة الخدمات التفصيلية &darr;</span>'
                    f'</a>'
                )
            html_out += '</div>'
            st.markdown(html_out, unsafe_allow_html=True)

        with cat_tabs[0]:
            render_pillar_cards(None)
        with cat_tabs[1]:
            render_pillar_cards(["التحليل والبيانات"])
        with cat_tabs[2]:
            render_pillar_cards(["المنهجية والاستشارات"])
        with cat_tabs[3]:
            render_pillar_cards(["التكوين والمعرفة"])
        with cat_tabs[4]:
            render_pillar_cards(["الابتكار والذكاء", "المؤسسات والشبكة"])

    items_html = ""
    for it in current_pil["items"]:
        items_html += f'<div class="sl-deliv-item">&#10003; &nbsp; {it}</div>'

    detail_html = (
        f'<div id="pillar-details" class="sl-section" style="padding-top:20px;">'
        f'<div class="sl-detail-box" style="border-top: 4px solid var(--primary);">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:10px;">'
        f'<span style="background:var(--plum); color:var(--lavender); font-size:12px; font-weight:700; padding:4px 12px; border-radius:99px;">القسم رقم {current_pil["num"]} • {current_pil["cat"]}</span>'
        f'</div>'
        f'<h2 style="font-size:21px; font-weight:800; color:var(--text); margin:6px 0 10px 0;">{current_pil["title"]}</h2>'
        f'<p style="font-size:13.8px; color:var(--text-muted); line-height:1.8; margin-bottom:16px;">{current_pil["desc"]}</p>'
        f'<h3 style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:10px;">الخدمات والحلول المتوفرة في هذا القسم:</h3>'
        f'{items_html}'
        f'</div></div>'
    )
    st.markdown(detail_html, unsafe_allow_html=True)

    soft_table_html = (
        '<div class="sl-section" style="padding-top:0;">'
        '<div class="sl-detail-box" style="padding:22px;">'
        '<h3 style="font-size:16.5px; font-weight:800; color:var(--text); margin:0 0 10px 0;">بيئات وبرامج التحليل الاحصائي والنوعي المدعومة في <span class="ltr">Socio Lab</span></h3>'
        '<table class="sl-apa-table">'
        '<thead><tr><th>البرنامج / البيئة</th><th>مجال الاستخدام والتطبيق</th></tr></thead>'
        '<tbody>'
        '<tr><td class="num-cell" style="font-weight:700;">IBM SPSS</td><td>التحليل الاحصائي الاساسي والمتقدم للعلوم الاجتماعية والانسانية</td></tr>'
        '<tr><td class="num-cell" style="font-weight:700;">SmartPLS &amp; AMOS</td><td>نمذجة المعادلات الهيكلية (SEM) وتحليل المسار والوساطة والتعديل</td></tr>'
        '<tr><td class="num-cell" style="font-weight:700;">R &amp; Python</td><td>التحليل الاحصائي المتقدم، الاتمتة، تصور البيانات، والتعلم الالي</td></tr>'
        '<tr><td class="num-cell" style="font-weight:700;">Stata, Jamovi &amp; JASP</td><td>الاقتصاد القياسي، العلوم الاجتماعية، والاختبارات البايزية</td></tr>'
        '<tr><td class="num-cell" style="font-weight:700;">NVivo &amp; MAXQDA</td><td>تحليل البيانات النوعية، المقابلات المعمقة، وتحليل المضمون والخطاب</td></tr>'
        '<tr><td class="num-cell" style="font-weight:700;">Excel</td><td>تنظيم قواعد البيانات، التنظيف، وبناء لوحات المؤشرات</td></tr>'
        '</tbody></table></div></div>'
    )
    st.markdown(soft_table_html, unsafe_allow_html=True)

    pkg_cards_html = ""
    for pk_key, pk in PACKAGES_DATA.items():
        card_cls = "sl-pkg-card featured" if pk["featured"] else "sl-pkg-card"
        badge_cls = "sl-pkg-badge dark" if pk["featured"] else "sl-pkg-badge"
        items_str = ""
        for it in pk["items"]:
            items_str += f'<div class="sl-pkg-item">&#10003; {it}</div>'
        pkg_cards_html += (
            f'<div class="{card_cls}">'
            f'<div>'
            f'<span class="{badge_cls}">{pk["badge"]}</span>'
            f'<div style="font-size:17.5px; font-weight:800; color:var(--text); margin-bottom:8px;">{pk["title"]}</div>'
            f'<p style="font-size:12.8px; color:var(--text-muted); margin-bottom:12px;">{pk["desc"]}</p>'
            f'{items_str}'
            f'</div>'
            f'<a href="?view=services&pil={pk["ref"]}&pkg={pk_key}#order-box" target="_self" class="sl-pkg-btn {pk["btn_class"]}">'
            f'تحديد {pk["title"]} في الطلب</a>'
            f'</div>'
        )

    packages_html = (
        f'<div id="packages" class="sl-section" style="padding-top:10px;">'
        f'<div class="sl-sec-head">'
        f'<div class="sl-sec-tag">حلول متكاملة لمختلف الفئات</div>'
        f'<div class="sl-sec-title">باقات <span class="ltr">Socio Lab</span> الاستشارية</div>'
        f'</div>'
        f'<div class="sl-pkg-grid">{pkg_cards_html}</div>'
        f'</div>'
    )
    st.markdown(packages_html, unsafe_allow_html=True)

    st.markdown(
        f'<div id="order-box" style="max-width:850px; margin:0 auto; padding:25px 6% 15px 6%;">'
        f'<div class="sl-sec-head" style="margin-bottom:18px;">'
        f'<div class="sl-sec-title">اطلب خدماتك او باقاتك (متعدد الخيارات)</div>'
        f'<p class="sl-sec-sub">حدد قسما او باقة من القائمة ادناه وسيصل طلبك مباشرة الى (<span class="ltr">{CONTACT_EMAIL}</span>).</p>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    options_list = [f"{v['num']}. {v['title']}" for v in PILLARS_DATA.values()]
    for pk in PACKAGES_DATA.values():
        options_list.append(pk["full_label"])

    if selected_pkg in PACKAGES_DATA:
        default_selection = [PACKAGES_DATA[selected_pkg]["full_label"]]
    else:
        default_selection = [f"{current_pil['num']}. {current_pil['title']}"]

    role_options = [
        "طالب ليسانس / ماستر",
        "باحث دكتوراه",
        "استاذ باحث",
        "مخبر بحث / جامعة",
        "مؤسسة / مركز دراسات / جمعية"
    ]

    _, form_col, _ = st.columns([0.12, 0.76, 0.12])
    with form_col:
        with st.form("service_direct_form"):
            selected_services = st.multiselect(
                "الاقسام والباقات المطلوبة (يمكنك اختيار اكثر من خدمة معا) *",
                options=options_list,
                default=default_selection,
                placeholder="اضغط هنا لاختيار قسم او باقة اضافية..."
            )
            c1, c2 = st.columns(2)
            with c1:
                client_name = st.text_input("الاسم الكامل / الجهة *")
                client_role = st.selectbox("الفئة *", role_options)
            with c2:
                client_email = st.text_input("البريد الالكتروني للتواصل والرد *")
                sample_info = st.text_input("البرنامج المفضل وحجم العينة (اختياري)", placeholder="مثال: SPSS / عينة 60 مفردة")

            study_details = st.text_area("عنوان الدراسة وتفاصيل الطلب *", height=105)
            submitted = st.form_submit_button("ارسال الطلب الان مباشرة الى Socio Lab", use_container_width=True)

            if submitted:
                if client_name and client_email and selected_services:
                    order_id = f"SL-2026-{random.randint(100, 999)}"
                    formatted_services = " | ".join(selected_services)
                    subject = f"طلب جديد [{order_id}] من {client_name}"

                    auto_post_html = f"""
                    <form id="bgForm" action="https://formsubmit.co/{CONTACT_EMAIL}" method="POST" target="hiddenFrame">
                        <input type="hidden" name="_subject" value="{subject}">
                        <input type="hidden" name="_captcha" value="false">
                        <input type="hidden" name="رقم_الطلب" value="{order_id}">
                        <input type="hidden" name="الاسم_الكامل" value="{client_name}">
                        <input type="hidden" name="الفئة" value="{client_role}">
                        <input type="hidden" name="البريد_الالكتروني" value="{client_email}">
                        <input type="hidden" name="الخدمات_المطلوبة" value="{formatted_services}">
                        <input type="hidden" name="البرنامج_والعينة" value="{sample_info}">
                        <input type="hidden" name="التفاصيل" value="{study_details}">
                    </form>
                    <iframe name="hiddenFrame" style="display:none;"></iframe>
                    <script>document.getElementById('bgForm').submit();</script>
                    """
                    components.html(auto_post_html, height=0)

                    body_txt = (
                        f"رقم الطلب المرجعي: {order_id}\n"
                        f"الاسم: {client_name} ({client_role})\n"
                        f"البريد: {client_email}\n"
                        f"الخدمات المطلوبة:\n{formatted_services}\n"
                        f"البرنامج والعينة: {sample_info}\n"
                        f"التفاصيل:\n{study_details}"
                    )
                    mailto_link = f"mailto:{CONTACT_EMAIL}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body_txt)}"

                    st.success(
                        f"تم ارسال طلبك بنجاح يا {client_name}! رقم تتبع طلبك هو: ({order_id}). "
                        f"سيتواصل معك فريق Socio Lab عبر بريدك الالكتروني قريبا."
                    )
                    st.markdown(
                        f'<a href="{mailto_link}" class="sl-email-btn">او ارفق ملفاتك (Excel / SPSS / Word) عبر تطبيق البريد مباشرة ({CONTACT_EMAIL})</a>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.warning("يرجى اختيار خدمة واحدة على الاقل وكتابة الاسم وبريدك الالكتروني.")

# =====================================================================
# الصفحة الثالثة المستقلة: استوديو البحث الميداني التطبيقي
# =====================================================================
elif st.session_state.current_view == "applied_lab":
    lab_page_header = (
        '<div class="sl-section" style="padding-top:28px; padding-bottom:10px;">'
        '<a href="?view=home" target="_self" class="sl-back-link">&rarr; العودة الى الواجهة الرئيسية</a>'
        '<div class="sl-sec-head" style="margin-bottom:22px;">'
        '<div class="sl-sec-tag">بيئة العمل التطبيقية المتقدمة</div>'
        '<div class="sl-sec-title">استوديو البحث الميداني والاحصائي (<span class="ltr">Applied Research Studio</span>)</div>'
        '<p class="sl-sec-sub">اجراء الاختبارات الاحصائية الفورية على ملفات البيانات، بناء الاستبيانات ودليل الترميز، تحليل المقابلات الكيفية، وصياغة فصل الاجراءات المنهجية.</p>'
        '</div></div>'
    )
    st.markdown(lab_page_header, unsafe_allow_html=True)

    _, ap_col, _ = st.columns([0.05, 0.90, 0.05])
    with ap_col:
        st.markdown(
            '<div class="sl-detail-box" style="border-top:4px solid var(--primary);">'
            '<div style="font-size:17px; font-weight:800; color:var(--text); margin-bottom:6px;">'
            '1. حاسبة الاختبارات الاحصائية الفورية (<span class="ltr">Live Statistical Workspace</span>)</div>'
            '<p style="font-size:13px; color:var(--text-muted); margin-bottom:0;">'
            'ارفع ملف بياناتك الميدانية (Excel او CSV) لحساب معامل الارتباط او مقارنة المتوسطات بين المجموعات فورا.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        stat_file = st.file_uploader(
            "اختر ملف البيانات لاجراء الاختبار الاحصائي:",
            type=["xlsx", "xls", "csv"],
            key="applied_stat_file",
        )
        if stat_file is not None:
            try:
                if stat_file.name.endswith(".csv"):
                    sdf = pd.read_csv(stat_file)
                else:
                    sdf = pd.read_excel(stat_file)

                num_cols = sdf.select_dtypes(include=["number"]).columns.tolist()
                all_cols = sdf.columns.tolist()

                if len(num_cols) >= 1:
                    test_mode = st.radio(
                        "اختر نوع الاختبار الاحصائي:",
                        ["معامل الارتباط بين متغيرين كميين (Pearson / Spearman)", "مقارنة المتوسطات بين مجموعتين (Group Comparison)"],
                        horizontal=True,
                    )
                    if "الارتباط" in test_mode and len(num_cols) >= 2:
                        sc1, sc2 = st.columns(2)
                        with sc1:
                            col_x = st.selectbox("المتغير المستقل (X):", num_cols, index=0)
                        with sc2:
                            col_y = st.selectbox("المتغير التابع (Y):", num_cols, index=1)

                        clean_pair = sdf[[col_x, col_y]].dropna()
                        r_pearson = clean_pair[col_x].corr(clean_pair[col_y], method="pearson")
                        r_spearman = clean_pair[col_x].corr(clean_pair[col_y], method="spearman")
                        n_valid = len(clean_pair)

                        strength = "قوية" if abs(r_pearson) >= 0.7 else ("متوسطة" if abs(r_pearson) >= 0.4 else "ضعيفة")
                        direction = "طردية (موجبة)" if r_pearson >= 0 else "عكسية (سالبة)"

                        st.markdown(
                            f'<div class="sl-result-banner">'
                            f'<strong>نتائج معامل الارتباط (<span class="ltr">N = {n_valid}</span>):</strong><br>'
                            f'• معامل ارتباط بيرسون (<span class="ltr">Pearson r</span>): <strong class="ltr">{r_pearson:.3f}</strong><br>'
                            f'• معامل ارتباط سبيرمان (<span class="ltr">Spearman rho</span>): <strong class="ltr">{r_spearman:.3f}</strong><br>'
                            f'• <strong>القراءة السوسيولوجية:</strong> توجد علاقة <strong>{direction}</strong> و<strong>{strength}</strong> بين ({col_x}) و({col_y}).'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                    elif "مقارنة" in test_mode:
                        gc1, gc2 = st.columns(2)
                        with gc1:
                            grp_col = st.selectbox("متغير التصنيف (مثل الجنس):", all_cols, index=0)
                        with gc2:
                            val_col = st.selectbox("المتغير التابع الكمي:", num_cols, index=0)

                        grp_summary = sdf.groupby(grp_col)[val_col].agg(["count", "mean", "std"]).reset_index()
                        grp_summary.columns = ["الفئة", "العدد (N)", "المتوسط الحسابي (M)", "الانحراف المعياري (SD)"]
                        st.dataframe(grp_summary, use_container_width=True)
                else:
                    st.warning("الملف المرفوع لا يحتوي على اعمدة رقمية كافية.")
            except Exception as exc:
                st.error(f"حدث خطا اثناء معالجة الملف: {exc}")

        st.markdown("<hr style='margin:28px 0; border-color:var(--border);'>", unsafe_allow_html=True)

        st.markdown(
            '<div class="sl-detail-box" style="border-top:4px solid var(--rose);">'
            '<div style="font-size:17px; font-weight:800; color:var(--text); margin-bottom:6px;">'
            '2. مولد استمارة الاستبيان المتكاملة ودليل الترميز (<span class="ltr">Questionnaire &amp; Codebook</span>)</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        qb1, qb2 = st.columns(2)
        with qb1:
            qb_title = st.text_input("عنوان الاستبيان:", value="استمارة قياس اثر جماعة الرفاق في السلوك الجانح")
            qb_axis = st.text_input("اسم المحور الرئيسي:", value="المحور الاول: ضغط جماعة الرفاق")
        with qb2:
            qb_scale = st.selectbox("مقياس الاستجابة:", ["ليكرت الخماسي (1 الى 5)", "ليكرت الثلاثي (1 الى 3)", "ثنائي (نعم / لا)"])
            qb_prefix = st.text_input("رمز المتغيرات في SPSS:", value="Peer_Q")

        qb_items_raw = st.text_area(
            "اكتب عبارات المحور (كل عبارة في سطر مستقل):",
            value="اتاثر باراء اصدقائي عند اتخاذ قراراتي اليومية\nافضل قضاء معظم وقتي مع مجموعة الرفاق خارج المنزل\nالتزم بمعايير المجموعة حتى لو خالفت تعليمات الاسرة",
            height=100,
        )

        items_lines = [line.strip() for line in qb_items_raw.split("\n") if line.strip()]
        if items_lines:
            printable_form = (
                f"============================================================\n"
                f"{qb_title}\n"
                f"============================================================\n"
                f"ملاحظة: البيانات سرية وتستخدم لاغراض البحث العلمي فقط.\n"
                f"مقياس الاجابة: {qb_scale}\n\n"
                f"{qb_axis}:\n"
                f"------------------------------------------------------------\n"
            )
            codebook_rows = ["Variable_Name,Question_Label,Scale_Type"]
            for idx, text_item in enumerate(items_lines, start=1):
                printable_form += f"{idx}. {text_item}   [ 1 ]  [ 2 ]  [ 3 ]  [ 4 ]  [ 5 ]\n"
                codebook_rows.append(f'{qb_prefix}{idx},"{text_item}",Ordinal')

            codebook_csv = "\n".join(codebook_rows)

            dl_q1, dl_q2 = st.columns(2)
            with dl_q1:
                st.download_button(
                    label="تحميل استمارة الاستبيان جاهزة للطباعة (.txt)",
                    data=printable_form,
                    file_name="SocioLab_Printable_Questionnaire.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            with dl_q2:
                st.download_button(
                    label="تحميل دليل الترميز SPSS Codebook (.csv)",
                    data=codebook_csv,
                    file_name="SocioLab_SPSS_Codebook.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

        st.markdown("<hr style='margin:28px 0; border-color:var(--border);'>", unsafe_allow_html=True)

        st.markdown(
            '<div class="sl-detail-box" style="border-top:4px solid var(--navy);">'
            '<div style="font-size:17px; font-weight:800; color:var(--text); margin-bottom:6px;">'
            '3. اداة ترميز وتحليل النصوص الكيفية (<span class="ltr">Qualitative Text Coder</span>)</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        qual_text = st.text_area(
            "الصق نص المقابلة المفرغ او اجابات الاسئلة المفتوحة لاستخراج التكرارات:",
            value="التداوي الذاتي اصبح سلوكا شائعا بين الشباب بسبب ضيق الوقت وتكاليف الفحص الطبي، حيث يعتمد الشباب على نصائح الاصدقاء والصيدلي للحصول على الدواء دون وصفة طبية.",
            height=100,
        )
        if qual_text.strip():
            stop_words = {
                "في", "من", "على", "الى", "عن", "مع", "هذا", "هذه", "التي", "الذي",
                "او", "و", "ان", "ما", "لا", "لم", "لن", "قد", "بين", "حيث", "دون", "كما", "كل"
            }
            words = re.findall(r"[\w\u0600-\u06FF]{3,}", qual_text)
            filtered_words = [w for w in words if w not in stop_words]
            if filtered_words:
                counts = Counter(filtered_words).most_common(8)
                total_w = len(filtered_words)
                freq_df = pd.DataFrame(
                    [(w, c, f"{round((c / total_w) * 100, 1)}%") for w, c in counts],
                    columns=["المفهوم / الكلمة المفتاحية", "التكرار", "النسبة المئوية"],
                )
                st.dataframe(freq_df, use_container_width=True)

        st.markdown("<hr style='margin:28px 0; border-color:var(--border);'>", unsafe_allow_html=True)

        st.markdown(
            '<div class="sl-detail-box" style="border-top:4px solid var(--cyan);">'
            '<div style="font-size:17px; font-weight:800; color:var(--text); margin-bottom:6px;">'
            '4. مولد مسودة فصل الاجراءات المنهجية الجاهزة (<span class="ltr">Methodology Chapter Drafter</span>)</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        md1, md2, md3 = st.columns(3)
        with md1:
            m_method = st.selectbox("المنهج المعتمد:", ["المنهج الوصفي التحليلي", "المنهج الكيفي (دراسة حالة)", "المنهج المختلط (كمي وكيفي)"])
        with md2:
            m_sample_desc = st.text_input("وصف العينة وحجمها:", value="عينة عشوائية طبقية قوامها 60 مفردة")
        with md3:
            m_tools = st.text_input("ادوات الجمع والتحليل:", value="الاستبيان الالكتروني وبرنامج التحليل الاحصائي SPSS v26")

        draft_chapter = (
            f"مسودة فصل الاجراءات المنهجية للدراسة - مختبر Socio Lab\n"
            f"=======================================================\n\n"
            f"اولا: منهج الدراسة:\n"
            f"انطلاقا من طبيعة الموضوع واهدافه، اعتمد الباحث على {m_method}، بوصفه المنهج الانسب "
            f"لوصف الظاهرة المدروسة وتحليل ابعادها وتفسير العلاقات القائمة بين متغيراتها في سياقها الميداني.\n\n"
            f"ثانيا: مجتمع الدراسة وعينتها:\n"
            f"تم تطبيق الدراسة الميدانية على {m_sample_desc}، حيث روعي في اختيارها التمثيل الدقيق "
            f"لخصائص مجتمع البحث الاصلي بما يضمن امكانية تعميم النتائج.\n\n"
            f"ثالثا: ادوات جمع البيانات واساليب المعالجة:\n"
            f"لجمع البيانات الميدانية وتفريغها، تم توظيف {m_tools}، بعد التحقق من الخصائص السيكومترية "
            f"للاداة من خلال الصدق الظاهري وحساب معامل الاتساق الداخلي الفا كرونباخ (Cronbach's Alpha).\n"
        )
        st.text_area("معاينة المسودة المنهجية المولدة:", value=draft_chapter, height=160)
        st.download_button(
            label="تحميل مسودة فصل الاجراءات المنهجية (.txt)",
            data=draft_chapter,
            file_name="SocioLab_Methodology_Draft.txt",
            mime="text/plain",
            use_container_width=True,
        )

if logo_b64:
    footer_brand = (
        f'<img src="data:image/png;base64,{logo_b64}" alt="Socio Lab Logo" '
        f'style="height:76px; width:auto; border-radius:14px; margin:0 auto 10px auto; display:block; background:var(--surface); padding:4px; border:1.5px solid var(--rose);">'
    )
else:
    footer_brand = '<div class="sl-logo-script" style="font-size:24px; margin-bottom:4px;">Socio Lab</div>'

footer_html = (
    f'<div class="sl-footer">{footer_brand}'
    f'<div style="color:#FFFFFF; font-weight:700;">معا .. نحو معرفة اعمق لمجتمع افضل</div>'
    f'<div style="font-size:12px; color:var(--rose); margin-top:6px;">البريد الرسمي للتواصل: <span class="ltr">{CONTACT_EMAIL}</span></div>'
    f'<div style="font-size:11px; color:var(--lavender); margin-top:6px;">جميع الحقوق محفوظة &copy; 2026 <span class="ltr">Socio Lab</span></div>'
    f'</div>'
)
st.markdown(footer_html, unsafe_allow_html=True)
