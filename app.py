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
            "بناء النسخة الالكترونية عبر <span class='ltr'>Google Forms</span>.",
            "اعداد دليل المقابلة المعمقة وشبكة الملاحظة للدراسات الكيفية.",
            "تسليم دليل الترميز (<span class='ltr'>Codebook</span>) لتسهيل الادخال."
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
            "ادخال البيانات وتنظيفها ومعالجة القيم المفقودة والشاذة.",
            "حساب الصدق البنائي والاتساق الداخلي معامل الفا كرونباخ.",
            "استخراج الجداول الوصفية والاستدلالية والفروق والارتباط.",
            "تسليم ملف <span class='ltr'>SPSS</span> وتقرير <span class='ltr'>Word</span>."
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
            "الترميز الموضوعاتي (<span class='ltr'>Thematic Coding</span>).",
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
            "نظام التوثيق العالمي <span class='ltr'>APA 7th</span> وقوالب المجلات."
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
            "تقييم نموذج القياس والصدق التمييزي (<span class='ltr'>HTMT</span>).",
            "تقييم النموذج البنيوي ومعاملات المسار (<span class='ltr'>Path</span>).",
            "اختبار فرضيات الوساطة والاعتدال عبر <span class='ltr'>Process Macro</span>.",
            "تقرير اكاديمي متكامل بالجداول والرسوم وفق النشر الدولي."
        ],
        "duration": "من 4 الى 7 ايام عمل",
        "color": "#0284C7",
        "top_class": "navy-top"
    },
    "s8": {
        "num": "08",
        "title": "استوديو السوسيولوجيا البصرية والانفوغرافيك",
        "short_desc": (
            "تحويل مخرجات التحليل الاحصائي والكيفي الى لوحات بيانات "
            "تفاعلية وملصقات علمية احترافية للمؤتمرات والمناقشات."
        ),
        "full_desc": (
            "نترجم الارقام والجداول الصماء الى سرد بصري علمي جذاب "
            "(<span class='ltr'>Data Storytelling</span>) يعزز حضورك في المؤتمرات والتقارير."
        ),
        "deliverables": [
            "تصميم ملصق علمي (<span class='ltr'>Scientific Poster</span>) للمؤتمرات والملتقيات.",
            "انشاء لوحات مؤشرات بصرية (<span class='ltr'>Dashboards</span>) لتقارير الجمعيات.",
            "رسوم بيانية متقدمة عالية الدقة جاهزة للطباعة والعرض.",
            "ملخص بصري لاهم نتائج الدراسة بلغة سوسيولوجية واضحة."
        ],
        "duration": "من 2 الى 4 ايام عمل",
        "color": "#14B8A6",
        "top_class": ""
    },
    "s9": {
        "num": "09",
        "title": "توطين وتكييف المقاييس العالمية",
        "short_desc": (
            "الترجمة العكسية للمقاييس الاجنبية وتكييفها ثقافيا مع البيئة "
            "المحلية واختبار خصائصها السيكومترية على عينة استطلاعية."
        ),
        "full_desc": (
            "نمكنك من استخدام احدث المقاييس العالمية المنشورة بالانجليزية "
            "او الفرنسية في دراستك بعد تكييفها وتقنينها منهجيا."
        ),
        "deliverables": [
            "الترجمة العلمية والترجمة العكسية (<span class='ltr'>Back-Translation</span>).",
            "تكييف المفردات ثقافيا واجتماعيا لتلائم مجتمع البحث المحلي.",
            "حساب الصدق العاملي والثبات على العينة الاستطلاعية.",
            "تسليم النسخة المقننة مرفقة بدليل التصحيح وتفسير الدرجات."
        ],
        "duration": "من 3 الى 5 ايام عمل",
        "color": "#06182C",
        "top_class": "navy-top"
    },
    "s10": {
        "num": "10",
        "title": "مختبر محاكاة لجنة المناقشة",
        "short_desc": (
            "جلسة تدريبية افتراضية لفحص ثغرات المذكرة وتدريب الباحث "
            "على الدفاع العلمي والرد على اسئلة المنهجية والاحصاء."
        ),
        "full_desc": (
            "نضعك في اجواء المناقشة الحقيقية قبل الموعد الرسمي لتعزيز "
            "ثقتك وتحصين دفاعك العلمي امام اسئلة الاساتذة المناقشين."
        ),
        "deliverables": [
            "مراجعة نقدية شاملة للفصل المنهجي وجداول التحليل.",
            "قائمة باهم الاسئلة الحرجة المتوقعة مع اجاباتها النموذجية.",
            "جلسة محاكاة مباشرة لتدريبك على تبرير العينة والاختبارات.",
            "توجيهات حول بناء عرض تقديمي (<span class='ltr'>PowerPoint</span>) محكم."
        ],
        "duration": "جلسة مكثفة + تقرير",
        "color": "#F59E0B",
        "top_class": "amber-top"
    },
    "s11": {
        "num": "11",
        "title": "الخرائط السوسيولوجية المكانية (Social GIS)",
        "short_desc": (
            "ربط الظواهر الاجتماعية بالفضاء الجغرافي وانتاج خرائط "
            "حرارية توضح التوزيع المجالي للظواهر عبر الاحياء والبلديات."
        ),
        "full_desc": (
            "دمج التحليل الاحصائي مع نظم المعلومات الجغرافية لدراسة "
            "التفاوتات المجالية، الهشاشة الحضرية، والتوزيع الجغرافي للظواهر."
        ),
        "deliverables": [
            "توطين البيانات الميدانية جغرافيا حسب البلديات او الاحياء.",
            "انتاج خرائط حرارية (<span class='ltr'>Heatmaps</span>) وخرائط توزيع موضوعاتية.",
            "تحليل الارتباط المكاني للظواهر الاجتماعية والحضرية.",
            "تسليم خرائط عالية الدقة مرفقة بقراءة سوسيو-مجالية."
        ],
        "duration": "من 4 الى 6 ايام عمل",
        "color": "#0284C7",
        "top_class": "navy-top"
    },
    "s12": {
        "num": "12",
        "title": "هندسة الاستبيانات الرقمية الذكية",
        "short_desc": (
            "تصميم استمارات رقمية متقدمة عبر KoboToolbox للعمل بدون "
            "انترنت مع برمجة المنطق الشرطي وتحديد الموقع الجغرافي."
        ),
        "full_desc": (
            "حلول جمع البيانات الرقمية الاحترافية للمسوح الميدانية الكبرى "
            "التي تمنع اخطاء الادخال وتختصر وقت التفريغ."
        ),
        "deliverables": [
            "برمجة الاستمارة على <span class='ltr'>KoboToolbox</span> للعمل بدون انترنت.",
            "اضافة قواعد التخطي الذكي (<span class='ltr'>Skip Logic</span>) والتحقق.",
            "تفعيل التتبع الجغرافي (<span class='ltr'>GPS</span>) لضمان مصداقية النزول الميداني.",
            "تصدير قاعدة البيانات جاهزة ومشفرة مباشرة الى <span class='ltr'>SPSS</span>."
        ],
        "duration": "من 2 الى 3 ايام عمل",
        "color": "#14B8A6",
        "top_class": ""
    },
    "s13": {
        "num": "13",
        "title": "حاضنة تحويل الاطروحات الى مقالات دولية",
        "short_desc": (
            "اعادة هيكلة فصول الماستر والدكتوراه الى اوراق علمية "
            "مكثفة وفق البنية العالمية IMRAD للنشر في المجلات المحكمة."
        ),
        "full_desc": (
            "نرافقك في استخلاص مقال علمي رصين من رسالتك يتوافق مع شروط "
            "المجلات المصنفة (<span class='ltr'>ASJP / Scopus</span>)."
        ),
        "deliverables": [
            "تفكيك الفصل التطبيقي واعادة صياغته وفق منهجية <span class='ltr'>IMRAD</span>.",
            "تكثيف العرض الاحصائي والنتائج بما يتناسب مع حجم المقال.",
            "ضبط الملخص والكلمات المفتاحية والتوثيق وفق قالب المجلة.",
            "مراجعة لغوية ومنهجية لتفادي الرفض الشكلي الاولي."
        ],
        "duration": "من 4 الى 6 ايام عمل",
        "color": "#F59E0B",
        "top_class": "amber-top"
    },
    "s14": {
        "num": "14",
        "title": "مختبر التحليل المختلط والتثليث المنهجي",
        "short_desc": (
            "الجمع المنهجي بين التحليل الاحصائي الكمي وتحليل المضمون "
            "الكيفي لتفسير الظواهر الاجتماعية بعمق وشمولية."
        ),
        "full_desc": (
            "تصميم استراتيجيات التثليث (<span class='ltr'>Triangulation</span>) لدمج دلالة الارقام "
            "مع عمق الشواهد والمقابلات في فصل تحليلي متجانس."
        ),
        "deliverables": [
            "بناء مصفوفة الدمج بين المؤشرات الكمية والفئات الكيفية.",
            "تفسير التناقضات او التطابقات بين نتائج الاستبيان والمقابلة.",
            "صياغة فصل النتائج والمناقشة باسلوب سوسيولوجي متكامل.",
            "تقديم توصيات عملية مبنية على الادلة المزدوجة."
        ],
        "duration": "من 4 الى 7 ايام عمل",
        "color": "#06182C",
        "top_class": "navy-top"
    }
}

PACKAGES_DATA = {
    "p1": {
        "badge": "المرحلة الاولى: قبل الميدان",
        "title": "باقة انطلاق الميدان الامن",
        "full_label": "باقة انطلاق الميدان الامن (تصميم الاداة + الضبط + العينة)",
        "desc": "تضمن لك بناء اداة قياس محكمة وعينة ممثلة قبل جمع البيانات.",
        "items": [
            "تصميم وبناء اداة البحث (استبيان او دليل مقابلة).",
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
        "full_label": "باقة المناقشة المحصنة (التحليل الاحصائي + الكيفي + الدفاع)",
        "desc": "تجهزك بنتائج احصائية وكيفية دقيقة وتدربك على الدفاع امام اللجنة.",
        "items": [
            "التحليل الاحصائي الكامل وتنظيف البيانات عبر <span class='ltr'>SPSS</span>.",
            "تفريغ وتحليل البيانات الكيفية ودمجها مع النتائج.",
            "جلسة محاكاة لشرح الجداول وتوقع اسئلة اللجنة."
        ],
        "featured": True,
        "btn_class": "amber",
        "srv_ref": "s2"
    },
    "p3": {
        "badge": "الاكثر طلبا لطلبة الماستر",
        "title": "باقة المرافقة الشاملة (من الفكرة الى الايداع)",
        "full_label": "باقة المرافقة الشاملة (تصميم + تحليل + APA 7 + دفاع)",
        "desc": "مرافقة متكاملة تغطي كافة الجوانب المنهجية والاحصائية لمذكرتك.",
        "items": [
            "ضبط الاشكالية والفرضيات وتصميم الاستبيان او المقابلة.",
            "التحليل الاحصائي الكامل (<span class='ltr'>SPSS</span>) او الكيفي.",
            "توثيق المراجع وفق <span class='ltr'>APA 7</span> + جلسة للمناقشة."
        ],
        "featured": True,
        "btn_class": "amber",
        "srv_ref": "s2"
    },
    "p4": {
        "badge": "للدكتوراه والنشر الدولي",
        "title": "باقة الدكتوراه والمجلات المحكمة",
        "full_label": "باقة الدكتوراه والنشر الدولي (SEM + مقال محكم + APA 7)",
        "desc": "مصممة لاطروحات الدكتوراه والباحثين المقبلين على النشر الدولي.",
        "items": [
            "التحليل المتقدم ونمذجة المعادلات (<span class='ltr'>SmartPLS</span>).",
            "استخلاص وتنسيق ورقة بحثية للنشر في المجلات المحكمة.",
            "تدقيق قائمة المراجع وفق <span class='ltr'>APA 7</span>."
        ],
        "featured": False,
        "btn_class": "",
        "srv_ref": "s7"
    },
    "p5": {
        "badge": "للمؤسسات والجمعيات والمخابر",
        "title": "باقة مسوح المؤسسات وقياس الاثر",
        "full_label": "باقة مسوح المؤسسات وقياس الاثر (مسح + مؤشرات + تقرير)",
        "desc": "حلول بحثية متكاملة للجمعيات والمؤسسات لتقييم المشاريع.",
        "items": [
            "هندسة المسح الرقمي (<span class='ltr'>Kobo</span>) وتدريب جامعي البيانات.",
            "معالجة قواعد البيانات الضخمة واستخراج الخرائط والمؤشرات.",
            "تقرير تنفيذي شامل بالرسوم البصرية والتوصيات."
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
    ".sl-trust-bar {background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0; padding: 18px 6%;}"
    ".sl-trust-grid {max-width: 1180px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; text-align: center;}"
    ".sl-trust-item {padding: 6px;}"
    ".sl-trust-num {font-size: 20px; font-weight: 800; color: #06182C;}"
    ".sl-trust-txt {font-size: 12px; color: #64748B; font-weight: 600;}"
    ".sl-persona-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; margin-top: 10px;}"
    ".sl-persona-card {background: #FFFFFF; border: 1px solid #E2E8F0; border-right: 5px solid #14B8A6; border-radius: 14px; padding: 22px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); text-align: right;}"
    ".sl-persona-card.adv {border-right-color: #06182C;}"
    ".sl-section {max-width: 1180px; margin: 0 auto; padding: 36px 6%; direction: rtl; text-align: right;}"
    ".sl-sec-head {text-align: center; max-width: 680px; margin: 0 auto 26px auto;}"
    ".sl-sec-tag {color: #0284C7; font-size: 12.5px; font-weight: 700;}"
    ".sl-sec-title {color: #06182C; font-size: 22px; font-weight: 800; margin: 4px 0 8px 0;}"
    ".sl-sec-sub {color: #64748B; font-size: 13.5px; margin: 0;}"
    ".sl-services-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px;}"
    ".sl-srv-card {display: block; text-decoration: none !important; background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 3.5px solid #14B8A6; border-radius: 14px; padding: 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.02); transition: all 0.2s ease; text-align: right;}"
    ".sl-srv-card:hover {transform: translateY(-4px); box-shadow: 0 12px 24px rgba(10, 25, 47, 0.08); border-color: #38BDF8;}"
    ".sl-srv-card.active-card {border: 2px solid #0284C7; background: #F0F9FF;}"
    ".sl-srv-card.navy-top {border-top-color: #06182C;}"
    ".sl-srv-card.amber-top {border-top-color: #F59E0B;}"
    ".sl-srv-num {font-size: 15px; font-weight: 800; color: #14B8A6; margin-bottom: 6px; direction: ltr; display: inline-block;}"
    ".sl-srv-title {font-size: 15.5px; font-weight: 700; color: #06182C; margin-bottom: 8px;}"
    ".sl-srv-desc {font-size: 12.8px; color: #475569; line-height: 1.7; margin: 0 0 14px 0;}"
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
    ".sl-scale-card {background: #FFFFFF; border: 1px solid #E2E8F0; border-right: 4px solid #06182C; border-radius: 12px; padding: 18px; text-align: right;}"
    ".sl-about-box {background: #FFFFFF; border: 1px solid #CBD5E1; border-top: 4px solid #0284C7; border-radius: 16px; padding: 28px; text-align: right;}"
    ".sl-clinic-box {background: #06182C; border-radius: 18px; padding: 28px; color: #FFFFFF; border: 1px solid #1E3A5F; text-align: right;}"
    ".sl-radar-card {background: #FFFFFF; border: 1px solid #E2E8F0; border-right: 4px solid #0284C7; border-radius: 12px; padding: 18px; margin-bottom: 14px; text-align: right;}"
    ".sl-probe-result {background: #FFFFFF; border: 1px solid #CBD5E1; border-top: 4px solid #06182C; border-radius: 12px; padding: 18px; margin-top: 14px; font-size: 13px; line-height: 1.75; color: #1E293B; text-align: right;}"
    ".sl-detail-box {background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 18px; padding: 26px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); margin-bottom: 20px; text-align: right;}"
    ".sl-deliv-item {background: #F8FAFC; border: 1px solid #E2E8F0; border-right: 3.5px solid #0284C7; padding: 12px 16px; border-radius: 10px; font-size: 13.5px; color: #1E293B; margin-bottom: 10px; text-align: right;}"
    ".sl-guar-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px; margin-bottom: 20px;}"
    ".sl-guar-card {background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 3px solid #14B8A6; border-radius: 12px; padding: 16px; text-align: right;}"
    ".sl-back-link {display: inline-block; color: #06182C !important; font-weight: 700; font-size: 13.5px; text-decoration: none !important; margin-bottom: 18px; background: #E2E8F0; padding: 7px 16px; border-radius: 8px;}"
    ".sl-result-banner {background-color: #F0F9FF; border: 1px solid #BAE6FD; border-right: 4px solid #0284C7; padding: 12px 15px; border-radius: 10px; margin-top: 12px; font-size: 13px; color: #0F2942; text-align: right;}"
    ".sl-warn-banner {background-color: #FFFBEB; border: 1px solid #FDE68A; border-right: 4px solid #F59E0B; padding: 12px 15px; border-radius: 10px; margin-top: 12px; font-size: 13px; color: #78350F; text-align: right;}"
    ".sl-apa-table {width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 12.5px; text-align: right;}"
    ".sl-apa-table th {border-top: 2px solid #06182C; border-bottom: 1.5px solid #06182C; padding: 8px; color: #06182C; background: #F8FAFC;}"
    ".sl-apa-table td {padding: 8px; border-bottom: 1px solid #E2E8F0;}"
    ".sl-apa-table tr:last-child td {border-bottom: 2px solid #06182C;}"
    ".sl-email-btn {display: block; text-align: center; background-color: #06182C; color: #38BDF8 !important; border: 1.5px solid #38BDF8; font-weight: 700; font-size: 14px; padding: 12px 20px; border-radius: 10px; text-decoration: none !important; margin-top: 12px;}"
    ".sl-integrity {background-color: #06182C; color: #FFFFFF; text-align: center; padding: 45px 6%; margin-top: 25px;}"
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
    f'<a href="?view=services&srv=s1" target="_self" class="{active_srv}">الخدمات والباقات (14)</a>'
    f'<a href="?view=home#interactive-lab" target="_self">المختبر التفاعلي</a>'
    f'<a href="?view=home#clinic-radar" target="_self">العيادة والرادار</a>'
    f'<a href="?view=home#about-us" target="_self">من نحن</a>'
    f'</div>'
    f'<a href="?view=services&srv=s2#order-box" target="_self" class="sl-cta-top">اطلب خدمة الان</a>'
    f'</div>'
)
st.markdown(navbar_html, unsafe_allow_html=True)

# =====================================================================
# الصفحة الاولى: الواجهة الرئيسية المنظمة في 4 محطات بصرية
# =====================================================================
if st.session_state.current_view == "home":
    # المحطة 1: القسم الترحيبي المزدوج + شريط الثقة
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
        '<a href="?view=services&srv=s1" target="_self" class="sl-btn-amber">تصفح الخدمات (14) والباقات الاستشارية</a>'
        '<a href="#interactive-lab" target="_self" class="sl-btn-outline">دخول المختبر التفاعلي المجاني</a>'
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

    trust_bar_html = (
        '<div class="sl-trust-bar"><div class="sl-trust-grid">'
        '<div class="sl-trust-item"><div class="sl-trust-num">14 خدمة</div><div class="sl-trust-txt">منهجية واحصائية وابداعية متخصصة</div></div>'
        '<div class="sl-trust-item"><div class="sl-trust-num ltr">APA 7th</div><div class="sl-trust-txt">التزام صارم بمعايير التوثيق العالمي</div></div>'
        '<div class="sl-trust-item"><div class="sl-trust-num">100%</div><div class="sl-trust-txt">بيانات ميدانية حقيقية وسرية تامة</div></div>'
        '<div class="sl-trust-item"><div class="sl-trust-num">24 ساعة</div><div class="sl-trust-txt">استجابة سريعة وتقدير فوري للتكلفة</div></div>'
        '</div></div>'
    )
    st.markdown(trust_bar_html, unsafe_allow_html=True)

    # المحطة 2: بوابة التوجيه الذكي حسب مستوى الباحث
    persona_html = (
        '<div class="sl-section" style="padding-bottom:10px;">'
        '<div class="sl-sec-head" style="margin-bottom:18px;">'
        '<div class="sl-sec-tag">مسارات مصممة لاحتياجك</div>'
        '<div class="sl-sec-title">اختر مسارك البحثي داخل <span class="ltr">Socio Lab</span></div>'
        '</div>'
        '<div class="sl-persona-grid">'
        '<div class="sl-persona-card">'
        '<div style="font-size:12px; color:#0D9488; font-weight:800;">المسار الاول: التأسيس وبناء المذكرة</div>'
        '<div style="font-size:17px; font-weight:800; color:#06182C; margin:4px 0 8px 0;">للباحثين الجدد وطلبة الماستر</div>'
        '<p style="font-size:13px; color:#475569; line-height:1.7; margin-bottom:10px;">'
        'اكسر رهبة المنهجية عبر دليل المصطلحات المبسطة، قائمة فحص الاستبيان، مسبار الفرضيات، وحاسبة العينة.</p>'
        '<a href="#interactive-lab" class="sl-srv-link">انتقل الى تبويب التأسيس المنهجي ادناه &darr;</a>'
        '</div>'
        '<div class="sl-persona-card adv">'
        '<div style="font-size:12px; color:#0284C7; font-weight:800;">المسار الثاني: الدقة القياسية والنشر الدولي</div>'
        '<div style="font-size:17px; font-weight:800; color:#06182C; margin:4px 0 8px 0;">لطلبة الدكتوراه، الاساتذة، والمؤسسات</div>'
        '<p style="font-size:13px; color:#475569; line-height:1.7; margin-bottom:10px;">'
        'افحص ملفات بياناتك فورا، حمل قوالب التحكيم، استكشف بنك المقاييس المقننة، واضبط مراجعك وفق <span class="ltr">APA 7</span>.</p>'
        '<a href="#interactive-lab" class="sl-srv-link">انتقل الى تبويبات الفحص والتوثيق ادناه &darr;</a>'
        '</div>'
        '</div></div>'
    )
    st.markdown(persona_html, unsafe_allow_html=True)

    # المحطة 3: المختبر التفاعلي المبوب (4 تبويبات أفقية تجمع كل الأدوات بذكاء)
    lab_header = (
        '<div id="interactive-lab" style="max-width:1180px; margin:0 auto; padding:25px 6% 10px 6%;">'
        '<div class="sl-sec-head" style="margin-bottom:16px;">'
        '<div class="sl-sec-tag">مختبر الادوات المجانية الذكية</div>'
        '<div class="sl-sec-title">المختبر التفاعلي المتكامل للباحث</div>'
        '<p class="sl-sec-sub">تنقل بين التبويبات الاربعة ادناه لاستخدام كافة الادوات الاحصائية والمنهجية فورا.</p>'
        '</div></div>'
    )
    st.markdown(lab_header, unsafe_allow_html=True)

    _, lab_col, _ = st.columns([0.05, 0.90, 0.05])
    with lab_col:
        t_audit, t_found, t_scales, t_quote = st.tabs([
            "1. فحص البيانات ومعرض المخرجات",
            "2. ادوات التأسيس المنهجي و SPSS",
            "3. القوالب الجاهزة وبنك المقاييس",
            "4. التوثيق APA 7 وحاسبة التكلفة"
        ])

        # -------------------------------------------------------------
        # التبويب 1: فحص البيانات + معرض المخرجات الحية
        # -------------------------------------------------------------
        with t_audit:
            st.markdown(
                '<div style="font-size:16px; font-weight:800; color:#06182C; margin:10px 0;">'
                'أ. فاحص البيانات الفوري (<span class="ltr">Excel / CSV Data Auditor</span>)</div>',
                unsafe_allow_html=True,
            )
            uploaded_file = st.file_uploader(
                "ارفع ملف بياناتك الميدانية بصيغة Excel (.xlsx) او CSV (.csv) لفحصه لحظيا:",
                type=["xlsx", "xls", "csv"],
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

                    st.dataframe(df.head(5), use_container_width=True)

                    if missing_cells > 0:
                        st.markdown(
                            f'<div class="sl-warn-banner"><strong>تنبيه منهجي:</strong> تم رصد <strong>{missing_cells}</strong> خلية مفقودة ({missing_pct}%). '
                            f'يوصى بتنظيف البيانات (<span class="ltr">Data Cleaning</span>) قبل التحليل في <span class="ltr">SPSS</span>.</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            '<div class="sl-result-banner"><strong>سلامة البيانات:</strong> قاعدة بياناتك مكتملة بنسبة 100% وخالية من القيم المفقودة.</div>',
                            unsafe_allow_html=True,
                        )
                except Exception as exc:
                    st.error(f"تعذر قراءة الملف: {exc}")
            else:
                st.markdown(
                    '<div class="sl-result-banner"><strong>ملاحظة الخصوصية:</strong> يتم فحص ملفك لحظيا داخل الجلسة ولا يتم حفظ اي نسخة منه.</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<hr style='margin:24px 0; border-color:#E2E8F0;'>", unsafe_allow_html=True)
            st.markdown(
                '<div style="font-size:16px; font-weight:800; color:#06182C; margin-bottom:10px;">'
                'ب. معرض نماذج المخرجات والتقارير الحية (مجهولة المصدر)</div>',
                unsafe_allow_html=True,
            )

            sub_t1, sub_t2, sub_t3 = st.tabs([
                "نموذج جدول SPSS وقراءة سوسيولوجية (APA 7)",
                "نموذج دليل الترميز (Codebook)",
                "نموذج التحليل الموضوعاتي للمقابلات"
            ])

            with sub_t1:
                sample_apa_html = (
                    '<div class="sl-detail-box" style="margin-bottom:0; padding:18px;">'
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
                    'من التباين الكلي في السلوك الجانح، وهو ما يتسق مع مقاربة التعلم الاجتماعي لسذرلاند.'
                    '</div></div>'
                )
                st.markdown(sample_apa_html, unsafe_allow_html=True)

            with sub_t2:
                codebook_html = (
                    '<div class="sl-detail-box" style="margin-bottom:0; padding:18px;">'
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

            with sub_t3:
                qual_sample_html = (
                    '<div class="sl-detail-box" style="margin-bottom:0; padding:18px;">'
                    '<div style="font-size:13px; font-weight:800; color:#06182C; margin-bottom:8px;">'
                    'نموذج من شبكة التحليل الموضوعاتي للمقابلات المعمقة (<span class="ltr">Thematic Analysis</span>)</div>'
                    '<div class="sl-deliv-item"><strong>الفئة الرئيسية الاولى:</strong> التبريرات الذاتية للتداوي الذاتي<br>'
                    '<span style="font-size:12px; color:#475569;">• الرموز الفرعية: ضيق الوقت، الثقة في تجارب المحيط، تجنب تكاليف الفحص الطبي.<br>'
                    '• الشاهد الميداني (مبحوث رقم 04، 29 سنة): <em>"لما نحس بالاعياء ناخذ نفس الدواء اللي جربو صاحبي بلا ما نروح للطبيب..."</em></span></div>'
                    '</div>'
                )
                st.markdown(qual_sample_html, unsafe_allow_html=True)

        # -------------------------------------------------------------
        # التبويب 2: ادوات التأسيس المنهجي و SPSS
        # -------------------------------------------------------------
        with t_found:
            st.markdown(
                '<div style="font-size:16px; font-weight:800; color:#06182C; margin:10px 0;">'
                'أ. مسبار الفرضيات الذكي (توليد التساؤلات والفرضيات وخطة التحليل)</div>',
                unsafe_allow_html=True,
            )
            pc1, pc2, pc3 = st.columns(3)
            with pc1:
                indep_var = st.text_input("المتغير المستقل (X):", placeholder="مثال: جماعة الرفاق")
            with pc2:
                dep_var = st.text_input("المتغير التابع (Y):", placeholder="مثال: السلوك الجانح")
            with pc3:
                study_sample = st.text_input("طبيعة عينة الدراسة:", placeholder="مثال: 60 تلميذا")

            if indep_var and dep_var:
                s_txt = f"لدى عينة من ({study_sample})" if study_sample else "لدى عينة الدراسة"
                probe_output = (
                    f'<div class="sl-probe-result">'
                    f'<div style="font-weight:800; color:#0284C7; margin-bottom:8px;">التشخيص المنهجي المقترح لدراستك:</div>'
                    f'<div style="margin-bottom:6px;"><strong>• التساؤل الرئيسي:</strong> هل توجد علاقة ذات دلالة احصائية بين <strong>{indep_var}</strong> و<strong>{dep_var}</strong> {s_txt}؟</div>'
                    f'<div style="margin-bottom:6px;"><strong>• الفرضية الصفرية (<span class="ltr">H0</span>):</strong> لا توجد علاقة ارتباطية او اثر دال احصائيا عند مستوى (0.05) بين <strong>{indep_var}</strong> و<strong>{dep_var}</strong> {s_txt}.</div>'
                    f'<div style="margin-bottom:6px;"><strong>• الفرضية البديلة (<span class="ltr">H1</span>):</strong> توجد علاقة ارتباطية او اثر دال احصائيا عند مستوى (0.05) بين <strong>{indep_var}</strong> و<strong>{dep_var}</strong> {s_txt}.</div>'
                    f'<div><strong>• مسار التحليل (<span class="ltr">SPSS</span>):</strong> احسب الثبات (الفا كرونباخ) اولا، ثم اختبر التوزيع الطبيعي؛ استخدم <strong>بيرسون والانحدار الخطي</strong> للبيانات الطبيعية، او <strong>سبيرمان</strong> للرتبية.</div>'
                    f'</div>'
                )
                st.markdown(probe_output, unsafe_allow_html=True)

            st.markdown("<hr style='margin:20px 0; border-color:#E2E8F0;'>", unsafe_allow_html=True)

            fc1, fc2 = st.columns(2, gap="large")
            with fc1:
                st.markdown(
                    '<div style="font-size:15px; font-weight:800; color:#06182C; margin-bottom:8px;">'
                    'ب. دليل "مصطلحات المنهجية ببساطة"</div>',
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

                st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
                st.markdown(
                    '<div style="font-size:15px; font-weight:800; color:#06182C; margin-bottom:8px;">'
                    'ج. مشخص الاختبار الاحصائي (<span class="ltr">SPSS</span>)</div>',
                    unsafe_allow_html=True,
                )
                goal_options = [
                    "قياس العلاقة الارتباطية بين متغيرين",
                    "قياس الفروق بين مجموعتين مستقلتين",
                    "قياس الفروق بين 3 مجموعات فاكثر",
                    "قياس اثر متغير مستقل على متغير تابع",
                ]
                dist_options = [
                    "بيانات كمية تتبع التوزيع الطبيعي (معلمية)",
                    "بيانات رتبية او غير طبيعية (لامعلمية)",
                ]
                goal = st.selectbox("هدف الفرضية البحثية:", goal_options)
                dist = st.selectbox("طبيعة البيانات والتوزيع:", dist_options)

                is_normal = "معلمية" in dist
                if "العلاقة" in goal:
                    t_name = "معامل ارتباط بيرسون (Pearson)" if is_normal else "معامل ارتباط سبيرمان (Spearman)"
                    t_path = "Analyze > Correlate > Bivariate > Pearson" if is_normal else "Analyze > Correlate > Bivariate > Spearman"
                elif "مجموعتين" in goal:
                    t_name = "اختبار ت لعينتين مستقلتين (T-Test)" if is_normal else "اختبار مان-ويتني (Mann-Whitney)"
                    t_path = "Analyze > Compare Means > Independent-Samples T Test" if is_normal else "Analyze > Nonparametric Tests > Independent Samples"
                elif "3 مجموعات" in goal:
                    t_name = "تحليل التباين الاحادي (One-Way ANOVA)" if is_normal else "اختبار كروسكال-واليس (Kruskal-Wallis)"
                    t_path = "Analyze > Compare Means > One-Way ANOVA" if is_normal else "Analyze > Nonparametric Tests > K Independent Samples"
                else:
                    t_name = "الانحدار الخطي (Linear Regression)" if is_normal else "الانحدار اللوجستي او الترتيبي"
                    t_path = "Analyze > Regression > Linear" if is_normal else "Analyze > Regression > Ordinal"

                st.markdown(
                    f'<div class="sl-result-banner"><strong>الاختبار المناسب:</strong> {t_name}<br>'
                    f'<span class="ltr-block" style="font-family:monospace; font-size:12px; color:#0284C7; margin-top:4px;">{t_path}</span></div>',
                    unsafe_allow_html=True,
                )

            with fc2:
                st.markdown(
                    '<div style="font-size:15px; font-weight:800; color:#06182C; margin-bottom:8px;">'
                    'د. مرشد استراتيجية المعاينة وحاسبة الحجم</div>',
                    unsafe_allow_html=True,
                )
                pop_nature = st.selectbox(
                    "طبيعة مجتمع دراستك:",
                    [
                        "مجتمع متجانس وتتوفر قائمة اسمية كاملة بافراده",
                        "مجتمع مقسم الى فئات او طبقات (ذكور/اناث، مستويات)",
                        "فئات حساسة او يصعب الوصول اليها (احداث، متعاطين)",
                        "مجتمع كبير ولا تتوفر قائمة اسمية مسبقة",
                    ],
                )
                if "متجانس" in pop_nature:
                    s_type = "العينة العشوائية البسيطة (Simple Random)"
                    s_text = "اعتمد الباحث على العينة العشوائية البسيطة نظرا لتجانس مفردات مجتمع البحث وتوفر اطار معاينة محدد."
                elif "طبقات" in pop_nature:
                    s_type = "العينة العشوائية الطبقية التناسبية (Stratified)"
                    s_text = "تم اختيار العينة العشوائية الطبقية لضمان التمثيل العادل لمختلف الفئات الفرعية داخل مجتمع الدراسة."
                elif "حساسة" in pop_nature:
                    s_type = "عينة كرة الثلج او العينة القصدية (Snowball / Purposive)"
                    s_text = "نظرا لخصوصية مجتمع البحث وصعوبة حصر مفرداته في قوائم رسمية، تم الاعتماد على العينة القصدية وكرة الثلج."
                else:
                    s_type = "العينة الحصصية او المنتظمة (Quota / Systematic)"
                    s_text = "في ظل اتساع مجتمع الدراسة وعدم توفر قائمة حصرية شاملة، تم اللجوء الى العينة الحصصية لتمثيل الخصائص الاساسية."

                st.markdown(
                    f'<div class="sl-result-banner"><strong>النوع الانسب:</strong> {s_type}<br>'
                    f'<span style="font-size:12px; color:#334155;">"{s_text}"</span></div>',
                    unsafe_allow_html=True,
                )

                st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
                pop_size = st.number_input("حجم مجتمع الدراسة الكلي (N):", min_value=10, value=500, step=10)
                margin_options = [
                    "5% (مستوى ثقة 95% - القياسي)",
                    "1% (مستوى ثقة 99% - دقة عالية)",
                    "10% (مستوى ثقة 90% - استطلاعية)",
                ]
                margin_label = st.selectbox("هامش الخطا المسموح به:", margin_options)
                e = 0.05 if "5%" in margin_label else (0.01 if "1%" in margin_label else 0.10)
                z = 1.96 if e == 0.05 else (2.576 if e == 0.01 else 1.645)
                n0 = (z**2 * 0.25) / (e**2)
                sample_n = math.ceil(n0 / (1 + ((n0 - 1) / pop_size)))

                st.markdown(
                    f'<div class="sl-result-banner" style="display:flex; justify-content:space-between; align-items:center;">'
                    f'<span><strong>الحد الادنى للعينة (<span class="ltr">n</span>):</strong></span>'
                    f'<span style="font-size:18px; font-weight:800; color:#06182C;">{sample_n} مفردة</span></div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<hr style='margin:20px 0; border-color:#E2E8F0;'>", unsafe_allow_html=True)
            st.markdown(
                '<div style="font-size:15px; font-weight:800; color:#06182C; margin-bottom:8px;">'
                'هـ. قالب "تشخيص مشاكل استمارة الاستبيان" قبل النزول للميدان</div>',
                unsafe_allow_html=True,
            )
            cc1, cc2 = st.columns(2)
            with cc1:
                q1 = st.checkbox("كل سؤال يقيس فكرة واحدة فقط (بدون اسئلة مزدوجة).", value=True)
                q2 = st.checkbox("صياغة العبارات محايدة ولا توحي باجابة معينة.", value=True)
                q3 = st.checkbox("تضمين ورقة تعريفية تطمئن المبحوث بسرية بياناته.", value=True)
            with cc2:
                q4 = st.checkbox("توافق بدائل الاجابة (ليكرت) مع طبيعة العبارات.", value=True)
                q5 = st.checkbox("تغطية جميع فرضيات وابعاد الدراسة باسئلة واضحة.", value=False)
                q6 = st.checkbox("عرض الاستمارة على محكمين او تجريبها استطلاعيا.", value=False)

            score = sum([q1, q2, q3, q4, q5, q6])
            if score == 6:
                st.markdown(
                    '<div class="sl-result-banner"><strong>جاهزية الاستمارة (6/6):</strong> ممتاز! استمارتك مستوفية للشروط المنهجية وجاهزة للميدان.</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="sl-warn-banner"><strong>درجة جاهزية الاستمارة ({score}/6):</strong> لديك {6 - score} نقاط منهجية غير مكتملة قد تضعف الصدق في <span class="ltr">SPSS</span>.</div>',
                    unsafe_allow_html=True,
                )

        # -------------------------------------------------------------
        # التبويب 3: القوالب القابلة للتحميل وبنك المقاييس المقننة
        # -------------------------------------------------------------
        with t_scales:
            sc_c1, sc_c2 = st.columns(2, gap="large")
            with sc_c1:
                st.markdown(
                    '<div style="font-size:15.5px; font-weight:800; color:#06182C; margin:10px 0;">'
                    'أ. مولد القوالب الاكاديمية للتحميل الفوري</div>',
                    unsafe_allow_html=True,
                )
                tpl_researcher = st.text_input("اسم الباحث / الطالبة:", placeholder="مثال: علوي وصال")
                tpl_uni = st.text_input("الجامعة والكلية:", placeholder="مثال: جامعة سوق اهراس")
                tpl_title = st.text_input("عنوان الدراسة:", placeholder="مثال: اثر جماعة الرفاق في السلوك الجانح")
                tpl_hypo = st.text_input("الفرضية الرئيسية:", placeholder="مثال: توجد علاقة دالة احصائيا...")

                r_name = tpl_researcher if tpl_researcher else "[اسم الباحث]"
                r_uni = tpl_uni if tpl_uni else "[اسم الجامعة والكلية]"
                r_title = tpl_title if tpl_title else "[عنوان الدراسة]"
                r_hypo = tpl_hypo if tpl_hypo else "[الفرضية الرئيسية]"

                arbitration_doc = (
                    f"{r_uni}\n----------------------------------------\n"
                    f"استمارة تحكيم اداة الدراسة (الصدق الظاهري)\n----------------------------------------\n"
                    f"الاستاذ(ة) الدكتور(ة): ....................\n"
                    f"عنوان الدراسة: « {r_title} »\n"
                    f"اعداد الباحث(ة): {r_name}\n"
                    f"الفرضية المرجعية: {r_hypo}\n\n"
                    f"يرجى تقييم عبارات الاداة من حيث الوضوح والانتماء للبعد.\n"
                    f"توقيع الاستاذ المحكم:\n"
                )
                consent_doc = (
                    f"{r_uni}\n----------------------------------------\n"
                    f"ميثاق سرية البيانات للمبحوثين\n----------------------------------------\n"
                    f"يجري الباحث(ة) {r_name} دراسة حول: « {r_title} ».\n"
                    f"نحيطكم علما بان اجاباتكم سرية للغاية وتستخدم لاغراض البحث العلمي فقط.\n"
                )

                st.download_button(
                    label="تحميل استمارة تحكيم الاداة للاساتذة (.txt)",
                    data=arbitration_doc,
                    file_name="SocioLab_Arbitration_Form.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
                st.download_button(
                    label="تحميل ورقة ميثاق سرية البيانات (.txt)",
                    data=consent_doc,
                    file_name="SocioLab_Confidentiality_Cover.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

            with sc_c2:
                st.markdown(
                    '<div style="font-size:15.5px; font-weight:800; color:#06182C; margin:10px 0;">'
                    'ب. بنك المقاييس السوسيولوجية والنفسية المقننة</div>',
                    unsafe_allow_html=True,
                )
                scales_db = {
                    "مقياس ضغط جماعة الرفاق للمراهقين": {
                        "dims": "الانصياع المعياري، المحاكاة السلوكية، الحاجة للقبول الاجتماعي.",
                        "items": "24 عبارة موزعة على 3 ابعاد.",
                        "key": "مقياس ليكرت الخماسي (من 1 الى 5).",
                        "alpha": "0.88 (ثبات مرتفع في البيئة المحلية)."
                    },
                    "مقياس الوعي الامني والرقمي لدى الشباب": {
                        "dims": "حماية الخصوصية، التحقق من المعلومات، الوعي بالمخاطر السيبرانية.",
                        "items": "30 عبارة موزعة على 3 ابعاد.",
                        "key": "مقياس ليكرت الثلاثي (دائما = 3 ، احيانا = 2 ، نادرا = 1).",
                        "alpha": "0.85 (مقنن على طلبة الجامعة)."
                    },
                    "مقياس التوافق النفسي والاجتماعي": {
                        "dims": "التوافق الشخصي، التوافق الاسري، التوافق الدراسي والاجتماعي.",
                        "items": "36 عبارة بصياغة موجبة وسالبة.",
                        "key": "بدائل ثنائية (نعم / لا).",
                        "alpha": "0.84 (ثبات اعادة التطبيق والاتساق الداخلي)."
                    },
                    "مقياس الرضا الوظيفي والالتزام التنظيمي": {
                        "dims": "بيئة العمل، نظام الحوافز، العلاقة مع القيادة، الانتماء المؤسساتي.",
                        "items": "28 عبارة موزعة على 4 ابعاد.",
                        "key": "مقياس ليكرت الخماسي (من 1 الى 5).",
                        "alpha": "0.91 (مقنن على موظفي المؤسسات)."
                    }
                }
                sel_scale = st.selectbox("اختر المقياس لعرض بطاقته التقنية:", list(scales_db.keys()))
                sc_info = scales_db[sel_scale]
                st.markdown(
                    f'<div class="sl-scale-card">'
                    f'<div style="font-size:14.5px; font-weight:800; color:#06182C; margin-bottom:6px;">{sel_scale}</div>'
                    f'<div style="font-size:12.5px; color:#334155; margin-bottom:4px;"><strong>• الابعاد:</strong> {sc_info["dims"]}</div>'
                    f'<div style="font-size:12.5px; color:#334155; margin-bottom:4px;"><strong>• البناء:</strong> {sc_info["items"]}</div>'
                    f'<div style="font-size:12.5px; color:#334155; margin-bottom:4px;"><strong>• مفتاح التصحيح:</strong> {sc_info["key"]}</div>'
                    f'<div style="font-size:12.5px; color:#0284C7; margin-bottom:10px;"><strong>• معامل الثبات:</strong> {sc_info["alpha"]}</div>'
                    f'<a href="?view=services&srv=s9#order-box" target="_self" class="sl-srv-link">اطلب تكييف او تحكيم هذا المقياس لدراستك &larr;</a>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        # -------------------------------------------------------------
        # التبويب 4: التوثيق APA 7 وحاسبة التكلفة التقديرية
        # -------------------------------------------------------------
        with t_quote:
            st.markdown(
                '<div style="font-size:16px; font-weight:800; color:#06182C; margin:10px 0;">'
                'أ. حاسبة التكلفة والمدة التقديرية الفورية</div>',
                unsafe_allow_html=True,
            )
            qc1, qc2, qc3, qc4 = st.columns(4)
            with qc1:
                q_srv = st.selectbox(
                    "نوع الخدمة المطلوبة:",
                    [
                        "تصميم وبناء اداة البحث",
                        "التحليل الاحصائي (SPSS)",
                        "تحليل البيانات الكيفية",
                        "نمذجة المعادلات (SEM)",
                        "باقة المرافقة الشاملة",
                    ],
                )
            with qc2:
                q_n = st.number_input("حجم العينة (N):", min_value=10, value=60, step=10, key="q_n_tab")
            with qc3:
                q_axes = st.number_input("عدد المحاور او الفرضيات:", min_value=1, value=4, step=1)
            with qc4:
                q_speed = st.selectbox("سرعة التسليم:", ["عادي (3 الى 5 ايام)", "مستعجل (48 ساعة)"])

            base_prices = {
                "تصميم وبناء اداة البحث": 2500,
                "التحليل الاحصائي (SPSS)": 4500,
                "تحليل البيانات الكيفية": 4000,
                "نمذجة المعادلات (SEM)": 7500,
                "باقة المرافقة الشاملة": 8500,
            }
            est_min = base_prices[q_srv] + (q_axes * 300) + (math.floor(q_n / 50) * 500)
            if "مستعجل" in q_speed:
                est_min = round(est_min * 1.25)
            est_max = est_min + 1500
            est_time = "48 ساعة عمل" if "مستعجل" in q_speed else "من 3 الى 5 ايام عمل"

            st.markdown(
                f'<div class="sl-result-banner" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">'
                f'<div><strong>التكلفة التقديرية:</strong> <span style="font-size:17px; font-weight:800; color:#06182C;">{est_min} - {est_max} دج</span> &nbsp;|&nbsp; '
                f'<strong>مدة الانجاز:</strong> {est_time}</div>'
                f'<a href="?view=services&srv=s2#order-box" target="_self" class="sl-btn-amber" style="padding:7px 16px; font-size:12.5px;">اطلب هذا العرض الان &larr;</a>'
                f'</div>',
                unsafe_allow_html=True,
            )

            st.markdown("<hr style='margin:22px 0; border-color:#E2E8F0;'>", unsafe_allow_html=True)
            ac1, ac2 = st.columns(2, gap="large")
            with ac1:
                st.markdown(
                    '<div style="font-size:15px; font-weight:800; color:#06182C; margin-bottom:8px;">'
                    'ب. مولد وضابط المراجع (<span class="ltr">APA 7th Edition</span>)</div>',
                    unsafe_allow_html=True,
                )
                ref_opts = ["كتاب اكاديمي", "مقال في مجلة علمية محكمة", "رسالة ماجستير / اطروحة دكتوراه"]
                ref_type = st.selectbox("نوع المرجع العلمي:", ref_opts)
                ref_author = st.text_input("لقب واسم المؤلف:", placeholder="مثال: العلوي، وصال / Bourdieu, P.")
                ref_year = st.text_input("سنة النشر:", placeholder="مثال: 2026")
                ref_title = st.text_input("عنوان الكتاب او المقال:", placeholder="مثال: اثر جماعة الرفاق / La Distinction")
                ref_source = st.text_input("دار النشر / المجلة / الجامعة:", placeholder="مثال: مجلة العلوم الاجتماعية، 14(2)")

                if ref_author and ref_year and ref_title:
                    is_latin = ref_author.strip()[0].isascii()
                    ref_dir_class = "ltr-block" if is_latin else "rtl"
                    sep_comma = ", " if is_latin else "، "
                    thesis_label = "[Unpublished doctoral dissertation]" if is_latin else "[اطروحة غير منشورة]"

                    if ref_type == "كتاب اكاديمي":
                        formatted_ref = f"{ref_author} ({ref_year}). <em>{ref_title}</em>. {ref_source}."
                    elif ref_type == "مقال في مجلة علمية محكمة":
                        formatted_ref = f"{ref_author} ({ref_year}). {ref_title}. <em>{ref_source}</em>."
                    else:
                        formatted_ref = f"{ref_author} ({ref_year}). <em>{ref_title}</em> {thesis_label}. {ref_source}."

                    author_last = ref_author.split(",")[0].split("،")[0]
                    in_text = f"({author_last}{sep_comma}{ref_year})"
                    st.markdown(
                        f'<div class="sl-result-banner">'
                        f'<strong>في المتن:</strong> <span class="{"ltr" if is_latin else "rtl"}">{in_text}</span><br>'
                        f'<strong>في القائمة (<span class="ltr">APA 7</span>):</strong>'
                        f'<div class="{ref_dir_class}" style="margin-top:4px; font-weight:600;">{formatted_ref}</div></div>',
                        unsafe_allow_html=True,
                    )

            with ac2:
                st.markdown(
                    '<div style="font-size:15px; font-weight:800; color:#06182C; margin-bottom:8px;">'
                    'ج. محك ضبط الامانة الاكاديمية وتفادي الاستلال</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<div class="sl-detail-box" style="padding:18px; margin-bottom:0; border-top:3.5px solid #F59E0B;">'
                    '<div style="font-size:14px; font-weight:800; color:#06182C; margin-bottom:8px;">قواعد ذهبية لحماية اطروحتك من الانتحال العلمي</div>'
                    '<p style="font-size:13px; color:#475569; line-height:1.75; margin:0;">'
                    '<strong>1. الاقتباس الحرفي:</strong> لا تنقل فقرة حرفيا لاكثر من 40 كلمة دون وضعها بين مزدوجين وذكر رقم الصفحة.<br>'
                    '<strong>2. اعادة الصياغة (<span class="ltr">Paraphrasing</span>):</strong> استوعب الفكرة السوسيولوجية وصغها باسلوبك مع الحفاظ على توثيق المصدر.<br>'
                    '<strong>3. توثيق البيانات الخام:</strong> احتفظ بملفات الاستبيان الاصلية وملفات <span class="ltr">SPSS</span> لاثبات مصداقية النتائج امام لجان الخبرة.</p>'
                    '</div>',
                    unsafe_allow_html=True,
                )

    # المحطة 4: عيادة المنهجية + رادار الاتجاهات + من نحن + ميثاق النزاهة
    clinic_subj = urllib.parse.quote("ارسال حالة منهجية لعيادة Socio Lab")
    clinic_radar_html = (
        f'<div id="clinic-radar" class="sl-section">'
        f'<div class="sl-hero-grid" style="align-items:start;">'
        f'<div class="sl-clinic-box">'
        f'<span style="background:rgba(245,158,11,0.2); color:#FBBF24; font-size:11.5px; font-weight:700; padding:4px 12px; border-radius:99px;">ركن تفاعلي دوري</span>'
        f'<h3 style="color:#FFFFFF; font-size:20px; font-weight:800; margin:12px 0 8px 0;">عيادة المنهجية والاحصاء المباشرة</h3>'
        f'<p style="color:#CBD5E1; font-size:13.5px; line-height:1.75; margin-bottom:16px;">لقاء علمي دوري نفكك فيه ابرز الاخطاء المنهجية والاحصائية الشائعة في رسائل الماستر والدكتوراه (دون ذكر اسماء) مع التصحيح المباشر.</p>'
        f'<div style="background:#0F2942; border:1px solid #1E3A5F; border-radius:12px; padding:14px; margin-bottom:16px;">'
        f'<div style="font-size:12.5px; color:#38BDF8; font-weight:700; margin-bottom:4px;">ملف الجلسة القادمة:</div>'
        f'<div style="font-size:13.5px; color:#FFFFFF; font-weight:600;">"لماذا يفشل اختبار الفرضيات رغم ارتفاع معامل الثبات؟ اخطاء صياغة مؤشرات الاستبيان"</div>'
        f'</div>'
        f'<a href="mailto:{CONTACT_EMAIL}?subject={clinic_subj}" class="sl-btn-amber" style="display:inline-block;">ارسل اشكاليتك المنهجية عبر البريد لمناقشتها</a>'
        f'</div>'
        f'<div>'
        f'<div style="margin-bottom:14px;"><span class="sl-sec-tag">رؤية استشرافية للظواهر الاجتماعية</span>'
        f'<h3 class="sl-sec-title" style="font-size:20px;">رادار الاتجاهات السوسيولوجية</h3></div>'
        f'<div class="sl-radar-card">'
        f'<div style="font-size:11.5px; color:#0284C7; font-weight:700;">رصد الظواهر الرقمية</div>'
        f'<div style="font-size:15px; font-weight:800; color:#06182C; margin:3px 0;">تحولات التنشئة الاجتماعية في ظل المنصات الخوارزمية</div>'
        f'<p style="font-size:12.5px; color:#475569; line-height:1.65; margin:0;">تراجع سلطة الوسائط التقليدية امام صناع المحتوى وتاثير ذلك على القيم الاستهلاكية لدى المراهقين. <strong>فرصة بحثية:</strong> قياس اثر التعرض الانتقائي على التمثل القيمي.</p>'
        f'</div>'
        f'<div class="sl-radar-card" style="border-right-color:#F59E0B;">'
        f'<div style="font-size:11.5px; color:#D97706; font-weight:700;">رصد السلوكيات المستجدة</div>'
        f'<div style="font-size:15px; font-weight:800; color:#06182C; margin:3px 0;">التطبيب الذاتي وسوء استخدام المؤثرات العقلية في الوسط الشباني</div>'
        f'<p style="font-size:12.5px; color:#475569; line-height:1.65; margin:0;">انتقال الظاهرة من السياقات الهامشية التقليدية الى الفضاءات شبه الحضرية والرقمية. <strong>فرصة بحثية:</strong> تحليل العوامل السوسيو-مؤسساتية المفسرة للانحراف المستحدث.</p>'
        f'</div></div></div></div>'
    )
    st.markdown(clinic_radar_html, unsafe_allow_html=True)

    about_html = (
        '<div id="about-us" class="sl-section" style="padding-top:10px;">'
        '<div class="sl-about-box">'
        '<div style="font-size:12px; color:#0284C7; font-weight:800; margin-bottom:4px;">الهوية العلمية والمرجعية الاكاديمية</div>'
        '<h3 style="font-size:21px; font-weight:800; color:#06182C; margin:0 0 12px 0;">من نحن؟ رؤية مختبر <span class="ltr">Socio Lab</span></h3>'
        '<p style="font-size:14px; color:#334155; line-height:1.85; margin-bottom:14px;">'
        'تاسس <strong class="ltr">Socio Lab</strong> ليكون فضاء علميا رقميا متخصصا في المرافقة المنهجية والتحليل الاحصائي للبحوث السوسيولوجية '
        'والانسانية. ينطلق المختبر من خبرة اكاديمية وميدانية متعمقة في سوسيولوجيا الانحراف والجريمة، التنظيم والعمل، وديناميكيات التعليم العالي، '
        'بهدف ردم الفجوة بين التنظير السوسيولوجي والتطبيق الاحصائي الدقيق.</p>'
        '<p style="font-size:13.5px; color:#475569; line-height:1.75; margin:0;">'
        'نؤمن في <strong class="ltr">Socio Lab</strong> بان الارقام الاحصائية لا تكتسب قيمتها العلمية الا بقراءة سوسيولوجية واعية تربط المؤشرات '
        'بالسياق الاجتماعي والثقافي، ولذلك ندمج بين الصرامة التقنية في برامج التحليل (<span class="ltr">SPSS, SmartPLS</span>) والعمق المنهجي الرصين.</p>'
        '</div></div>'
    )
    st.markdown(about_html, unsafe_allow_html=True)

    integrity_html = (
        '<div id="integrity" class="sl-integrity">'
        '<div style="max-width:800px; margin:0 auto;">'
        '<span style="background:rgba(245,158,11,0.18); color:#FBBF24; font-size:11.5px; font-weight:700; padding:4px 12px; border-radius:99px;">الالتزام الاخلاقي والعلمي</span>'
        '<div style="color:#FFFFFF; font-size:20px; font-weight:800; margin:12px 0 8px 0;">ميثاق النزاهة العلمية وسرية البيانات في <span class="ltr">Socio Lab</span></div>'
        '<p style="color:#CBD5E1; font-size:13.5px; line-height:1.8; margin:0;">تلتزم منصة <span class="ltr">Socio Lab</span> بتقديم الاستشارات المنهجية والتحليل الاحصائي للبيانات الميدانية الحقيقية فقط، وترفض رفضا قاطعا فبركة البيانات او بيع البحوث الجاهزة او اي ممارسة تخل بالامانة العلمية، مع ضمان السرية التامة لافكار الباحثين وبياناتهم.</p>'
        '</div></div>'
    )
    st.markdown(integrity_html, unsafe_allow_html=True)

# =====================================================================
# الصفحة الثانية: صفحة الخدمات الـ 14 والباقات المستقلة
# =====================================================================
elif st.session_state.current_view == "services":
    current_key = st.session_state.selected_srv
    current_srv = SERVICES_DATA[current_key]
    selected_pkg = query_params.get("pkg", "")

    cards_html = ""
    for key, srv in SERVICES_DATA.items():
        act_card = "active-card" if key == current_key else ""
        cards_html += (
            f'<a href="?view=services&srv={key}#service-details" target="_self" class="sl-srv-card {srv["top_class"]} {act_card}">'
            f'<div class="sl-srv-num" style="color:{srv["color"]};">{srv["num"]}</div>'
            f'<div class="sl-srv-title">{srv["title"]}</div>'
            f'<p class="sl-srv-desc">{srv["short_desc"]}</p>'
            f'<span class="sl-srv-link">عرض تفاصيل المخرجات &darr;</span>'
            f'</a>'
        )

    all_services_html = (
        f'<div class="sl-section" style="padding-top:28px;">'
        f'<a href="?view=home" target="_self" class="sl-back-link">&rarr; العودة الى الواجهة الرئيسية</a>'
        f'<div class="sl-sec-head">'
        f'<div class="sl-sec-tag">14 خدمة بحثية واحصائية وابداعية متخصصة</div>'
        f'<div class="sl-sec-title">خدمات منصة <span class="ltr">Socio Lab</span></div>'
        f'<p class="sl-sec-sub">اختر اي خدمة للاطلاع على مخرجاتها التفصيلية، او انتقل للاسفل لاختيار باقات متكاملة.</p>'
        f'</div>'
        f'<div class="sl-services-grid">{cards_html}</div>'
        f'</div>'
    )
    st.markdown(all_services_html, unsafe_allow_html=True)

    deliv_html = ""
    for item in current_srv["deliverables"]:
        deliv_html += f'<div class="sl-deliv-item">&#10003; &nbsp; {item}</div>'

    service_detail_html = (
        f'<div id="service-details" class="sl-section" style="padding-top:0;">'
        f'<div class="sl-detail-box" style="border-top: 4px solid {current_srv["color"]};">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">'
        f'<span style="background:#06182C; color:#38BDF8; font-size:12px; font-weight:700; padding:4px 12px; border-radius:99px;">تفاصيل الخدمة رقم {current_srv["num"]}</span>'
        f'<span style="background:#FEF3C7; color:#B45309; font-size:12px; font-weight:700; padding:4px 12px; border-radius:99px;">مدة الانجاز التقديرية: {current_srv["duration"]}</span>'
        f'</div>'
        f'<h2 style="font-size:22px; font-weight:800; color:#06182C; margin:8px 0 12px 0;">{current_srv["title"]}</h2>'
        f'<p style="font-size:14px; color:#475569; line-height:1.8; margin-bottom:20px;">{current_srv["full_desc"]}</p>'
        f'<h3 style="font-size:15.5px; font-weight:800; color:#06182C; margin-bottom:12px;">ماذا ستستلم في هذه الخدمة (المخرجات):</h3>'
        f'{deliv_html}'
        f'</div></div>'
    )
    st.markdown(service_detail_html, unsafe_allow_html=True)

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
            f'<div style="font-size:18px; font-weight:800; color:#06182C; margin-bottom:8px;">{pk["title"]}</div>'
            f'<p style="font-size:13px; color:#64748B; margin-bottom:14px;">{pk["desc"]}</p>'
            f'{items_str}'
            f'</div>'
            f'<a href="?view=services&srv={pk["srv_ref"]}&pkg={pk_key}#order-box" target="_self" class="sl-pkg-btn {pk["btn_class"]}">'
            f'تحديد {pk["title"]} في الطلب</a>'
            f'</div>'
        )

    packages_html = (
        f'<div id="packages" class="sl-section" style="padding-top:10px;">'
        f'<div class="sl-sec-head">'
        f'<div class="sl-sec-tag">حلول شاملة لمختلف المستويات البحثية</div>'
        f'<div class="sl-sec-title">باقات <span class="ltr">Socio Lab</span> الاستشارية</div>'
        f'<p class="sl-sec-sub">اختر الباقة المناسبة لمرحلتك البحثية، ويمكنك دمج اكثر من باقة او خدمة في طلب واحد ادناه.</p>'
        f'</div>'
        f'<div class="sl-pkg-grid">{pkg_cards_html}</div>'
        f'</div>'
    )
    st.markdown(packages_html, unsafe_allow_html=True)

    faq_header_html = (
        '<div id="faq-guarantees" class="sl-section" style="padding-top:15px; padding-bottom:15px;">'
        '<div class="sl-sec-head" style="margin-bottom:22px;">'
        '<div class="sl-sec-tag">الشفافية والمرافقة المستمرة</div>'
        '<div class="sl-sec-title">الاسئلة الشائعة وضمانات العمل في <span class="ltr">Socio Lab</span></div>'
        '<p class="sl-sec-sub">نضمن لك مرافقة علمية موثوقة ومرونة كاملة حتى اجازة بحثك ومناقشته بنجاح.</p>'
        '</div>'
        '<div class="sl-guar-grid">'
        '<div class="sl-guar-card">'
        '<div style="font-size:14.5px; font-weight:800; color:#06182C; margin-bottom:6px;">1. ضمان تعديلات المشرف</div>'
        '<p style="font-size:12.5px; color:#475569; line-height:1.65; margin:0;">'
        'نتكفل مجانا بتنفيذ اي تعديلات احصائية او منهجية يطلبها الاستاذ المشرف على الجداول او الاختبارات المستخرجة.</p>'
        '</div>'
        '<div class="sl-guar-card" style="border-top-color:#06182C;">'
        '<div style="font-size:14.5px; font-weight:800; color:#06182C; margin-bottom:6px;">2. تسليم كافة الملفات الاصلية</div>'
        '<p style="font-size:12.5px; color:#475569; line-height:1.65; margin:0;">'
        'تستلم قاعدة البيانات (<span class="ltr">.sav</span>)، ملف المخرجات (<span class="ltr">.spv</span>)، وتقرير <span class="ltr">Word</span> منسق وفق <span class="ltr">APA 7</span>.</p>'
        '</div>'
        '<div class="sl-guar-card" style="border-top-color:#F59E0B;">'
        '<div style="font-size:14.5px; font-weight:800; color:#06182C; margin-bottom:6px;">3. جلسة شرح قبل المناقشة</div>'
        '<p style="font-size:12.5px; color:#475569; line-height:1.65; margin:0;">'
        'نوفر شرحا مبسطا لنتائجك وكيفية قراءة المؤشرات الاحصائية لتتمكن من الدفاع عن دراستك بثقة امام اللجنة.</p>'
        '</div>'
        '<div class="sl-guar-card" style="border-top-color:#0284C7;">'
        '<div style="font-size:14.5px; font-weight:800; color:#06182C; margin-bottom:6px;">4. سرية تامة للبيانات</div>'
        '<p style="font-size:12.5px; color:#475569; line-height:1.65; margin:0;">'
        'تخضع جميع الاستبيانات وقواعد البيانات المرسلة لبروتوكول سرية صارم ويتم حذفها فور انتهاء المهمة.</p>'
        '</div>'
        '</div></div>'
    )
    st.markdown(faq_header_html, unsafe_allow_html=True)

    _, faq_col, _ = st.columns([0.08, 0.84, 0.08])
    with faq_col:
        with st.expander("كيف ارسل قاعدة بياناتي او مسودة الاستبيان للبدء في العمل؟"):
            st.write(
                "بعد اختيار الخدمات والباقات من النموذج ادناه والضغط على زر الارسال عبر البريد الالكتروني، "
                "يمكنك ارفاق ملف Excel او Word مباشرة في رسالة البريد الموجهة الينا."
            )
        with st.expander("ما هي المدة الزمنية المستغرقة لتسليم التحليل الاحصائي؟"):
            st.write(
                "تتراوح مدة الانجاز القياسية بين 3 الى 5 ايام عمل حسب حجم العينة وعدد الفرضيات، "
                "مع توفر خيار التسليم المستعجل لطلبة الماستر والدكتوراه المقبلين على الايداع."
            )
        with st.expander("هل تقومون بكتابة الاطار النظري او توفير بحوث جاهزة؟"):
            st.write(
                "لا. التزاما بميثاق النزاهة العلمية في Socio Lab، تقتصر خدماتنا على الاستشارة المنهجية، "
                "بناء ادوات القياس، التحليل الاحصائي والكيفي للبيانات الميدانية الحقيقية، وضبط التوثيق."
            )

    st.markdown(
        f'<div id="order-box" style="max-width:850px; margin:0 auto; padding:25px 6% 15px 6%;">'
        f'<div class="sl-sec-head" style="margin-bottom:18px;">'
        f'<div class="sl-sec-title">اطلب خدماتك او باقاتك (متعدد الخيارات)</div>'
        f'<p class="sl-sec-sub">حدد خدمة او اكثر من القائمة ادناه لتجهيز رسالة رسمية موجهة الى (<span class="ltr">{CONTACT_EMAIL}</span>).</p>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    options_list = [f"{v['num']}. {v['title']}" for v in SERVICES_DATA.values()]
    for pk in PACKAGES_DATA.values():
        options_list.append(pk["full_label"])

    if selected_pkg in PACKAGES_DATA:
        default_selection = [PACKAGES_DATA[selected_pkg]["full_label"]]
    else:
        default_selection = [f"{current_srv['num']}. {current_srv['title']}"]

    role_options = ["باحث ماستر", "باحث دكتوراه", "استاذ باحث", "مؤسسة / جمعية"]

    _, form_col, _ = st.columns([0.12, 0.76, 0.12])
    with form_col:
        with st.form("service_email_form"):
            selected_services = st.multiselect(
                "الخدمات والباقات المطلوبة (يمكنك اضافة اكثر من خيار معا من الـ 14 خدمة والباقات) *",
                options=options_list,
                default=default_selection,
                placeholder="اضغط هنا لاختيار خدمة او باقة اضافية..."
            )
            c1, c2 = st.columns(2)
            with c1:
                client_name = st.text_input("الاسم الكامل / المؤسسة *")
                client_role = st.selectbox("الصفة الاكاديمية او المهنية *", role_options)
            with c2:
                client_email = st.text_input("بريدك الالكتروني للتواصل والرد *")
                sample_info = st.text_input("حجم العينة والمنهج المعتمد (اختياري)", placeholder="مثال: 60 مفردة")

            study_details = st.text_area("عنوان الدراسة والتفاصيل المطلوبة *", height=105)
            submitted = st.form_submit_button("تجهيز رسالة الطلب للبريد الالكتروني", use_container_width=True)

            if submitted:
                if client_name and client_email and selected_services:
                    formatted_services = "\n".join([f"   * {item}" for item in selected_services])
                    subject = f"طلب خدمات بحثية من Socio Lab ({len(selected_services)} خيارات) - {client_name}"
                    body = (
                        f"السلام عليكم فريق Socio Lab،\n\n"
                        f"اود التقدم بطلب الخدمات والباقات التالية:\n"
                        f"{formatted_services}\n\n"
                        f"بيانات الباحث:\n"
                        f"- الاسم الكامل: {client_name}\n"
                        f"- الصفة الاكاديمية: {client_role}\n"
                        f"- البريد الالكتروني للرد: {client_email}\n"
                        f"- العينة والمنهج: {sample_info}\n"
                        f"- تفاصيل الدراسة:\n{study_details}\n\n"
                        f"مع خالص التقدير."
                    )
                    q_subj = urllib.parse.quote(subject)
                    q_body = urllib.parse.quote(body)
                    mailto_link = f"mailto:{CONTACT_EMAIL}?subject={q_subj}&body={q_body}"

                    st.success(f"تم تجهيز مسودة طلبك ({len(selected_services)} خيارات مختارة) بنجاح يا {client_name}!")
                    st.markdown(
                        f'<a href="{mailto_link}" class="sl-email-btn">ارسال الطلب الان عبر البريد الالكتروني (<span class="ltr">{CONTACT_EMAIL}</span>)</a>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.warning("يرجى اختيار خدمة واحدة على الاقل وكتابة الاسم وبريدك الالكتروني.")

if logo_b64:
    footer_brand = (
        f'<img src="data:image/jpeg;base64,{logo_b64}" alt="Logo" '
        f'style="height:68px; width:auto; border-radius:12px; margin:0 auto 10px auto; display:block;">'
    )
else:
    footer_brand = '<div class="sl-logo-script" style="font-size:24px; margin-bottom:4px;">Socio Lab</div>'

footer_html = (
    f'<div class="sl-footer">{footer_brand}'
    f'<div>فضاء علمي رقمي لانتاج المعرفة وتطوير البحث</div>'
    f'<div style="font-size:12px; color:#38BDF8; margin-top:6px;">البريد الرسمي للتواصل: <span class="ltr">{CONTACT_EMAIL}</span></div>'
    f'<div style="font-size:11px; color:#64748B; margin-top:6px;">جميع الحقوق محفوظة &copy; 2026 <span class="ltr">Socio Lab</span></div>'
    f'</div>'
)
st.markdown(footer_html, unsafe_allow_html=True)
