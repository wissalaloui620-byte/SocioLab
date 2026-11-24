import datetime
import math
import random
import re
import urllib.parse
from collections import Counter
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

CONTACT_EMAIL = "sociolab.dz2026@gmail.com"
APP_URL = "https://sociolab-dz.streamlit.app"


def compute_cronbach_alpha(df_num):
    k = df_num.shape[1]
    if k < 2:
        return None
    item_vars = df_num.var(axis=0, ddof=1).sum()
    total_var = df_num.sum(axis=1).var(ddof=1)
    if total_var == 0:
        return None
    return (k / (k - 1)) * (1 - (item_vars / total_var))


st.set_page_config(
    page_title="Socio Lab | Arctic Blue Intelligence Platform",
    page_icon="💠",
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
        "btn_class": "mint",
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
        "btn_class": "mint",
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

# =====================================================================
# قاعدة بيانات المراجع العلمية (المنهجية، الإحصاء/SPSS، علم الاجتماع، انحراف وجريمة)
# =====================================================================
REFERENCES_LIST = [
    # سوسيولوجيا الانحراف والجريمة
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "title": "الانتحار: دراسة في علم الاجتماع",
        "apa": "دوركايم، إميل. (2018). الانتحار: دراسة في علم الاجتماع (ترجمة حسن عودة). الهيئة العامة السورية للكتاب.",
        "note": "مرجع كلاسيكي في توظيف الإحصاء السوسيولوجي ونظرية اللامعيارية (Anomie) لتفسير الانحراف."
    },
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "title": "جنوح الأحداث والانحراف الاجتماعي",
        "apa": "رشوان، حسين عبد الحميد أحمد. (2015). الجريمة والانحراف: دراسة في علم الاجتماع الجنائي. المكتب الجامعي الحديث.",
        "note": "يتناول أثر الأسرة، جماعة الرفاق، والوسط المدرسي في جنوح الأحداث."
    },
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "title": "نظريات علم الجريمة والانحراف",
        "apa": "الوريكات، عايد عواد. (2017). نظريات علم الجريمة. دار الشروق للنشر والتوزيع.",
        "note": "عرض للنظريات السوسيولوجية: المخالطة الفارقة، الضبط الاجتماعي، الوصم، والضغط."
    },
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "title": "Outsiders: Studies in the Sociology of Deviance",
        "apa": "Becker, H. S. (2018). Outsiders: Studies in the sociology of deviance. Free Press.",
        "note": "المرجع التأسيسي لنظرية الوصم الاجتماعي (Labeling Theory) في سوسيولوجيا الانحراف."
    },
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "title": "Causes of Delinquency",
        "apa": "Hirschi, T. (2017). Causes of delinquency. Routledge.",
        "note": "المرجع الأساسي لنظرية الروابط الاجتماعية في تفسير جنوح الأحداث."
    },
    # المنهجية ومناهج البحث العلمي
    {
        "field": "المنهجية ومناهج البحث العلمي",
        "title": "مناهج البحث العلمي وطرق إعداد البحوث",
        "apa": "بوحوش، عمار، والذنيبات، محمد محمود. (2019). مناهج البحث العلمي وطرق إعداد البحوث. ديوان المطبوعات الجامعية.",
        "note": "دليل منهجي لبناء الإشكالية، الفرضيات، وتحديد العينات في العلوم الاجتماعية."
    },
    {
        "field": "المنهجية ومناهج البحث العلمي",
        "title": "Research Design: Qualitative, Quantitative, and Mixed Methods",
        "apa": "Creswell, J. W., & Creswell, J. D. (2023). Research design: Qualitative, quantitative, and mixed methods approaches (6th ed.). SAGE Publications.",
        "note": "مرجع دولي في تصميم البحوث الكمية والكيفية والمختلطة."
    },
    {
        "field": "المنهجية ومناهج البحث العلمي",
        "title": "Manuel de recherche en sciences sociales",
        "apa": "Van Campenhoudt, L., Marquet, J., & Quivy, R. (2022). Manuel de recherche en sciences sociales (6e éd.). Dunod.",
        "note": "مرجع منهجي في صياغة الإشكالية السوسيولوجية والعمل الميداني."
    },
    # الإحصاء التطبيقي و SPSS
    {
        "field": "الإحصاء التطبيقي و SPSS",
        "title": "التحليل الإحصائي للبيانات باستخدام برنامج SPSS",
        "apa": "أبو علام، رجاء محمود. (2021). التحليل الإحصائي للبيانات باستخدام برنامج SPSS. دار النشر للجامعات.",
        "note": "شرح تطبيقي للاختبارات المعلمية واللامعلمية وتحليل التباين والانحدار."
    },
    {
        "field": "الإحصاء التطبيقي و SPSS",
        "title": "التحليل العاملي الاستكشافي والتوكيدي (SPSS & AMOS)",
        "apa": "تيغزة، أمحمد بوزيان. (2012). التحليل العاملي الاستكشافي والتوكيدي: مفاهيمهما ومنهجيتهما بتوظيف حزمة SPSS وليزرل. دار المسيرة.",
        "note": "مرجع في الصدق البنائي والتحليل العاملي EFA و CFA."
    },
    {
        "field": "الإحصاء التطبيقي و SPSS",
        "title": "Discovering Statistics Using IBM SPSS Statistics",
        "apa": "Field, A. (2024). Discovering statistics using IBM SPSS statistics (6th ed.). SAGE Publications.",
        "note": "مرجع شامل لتفسير مخرجات SPSS وفهم المنطق الإحصائي."
    },
    # علم الاجتماع العام
    {
        "field": "علم الاجتماع العام",
        "title": "قواعد المنهج في علم الاجتماع",
        "apa": "دوركايم، إميل. (2014). قواعد المنهج في علم الاجتماع (ترجمة محمود قاسم). دار المعرفة الجامعية.",
        "note": "النص التأسيسي لدراسة الظواهر الاجتماعية كحقائق مستقلة."
    },
    {
        "field": "علم الاجتماع العام",
        "title": "الخيال السوسيولوجي",
        "apa": "ميلز، تشارلز رايت. (2017). الخيال السوسيولوجي (ترجمة عبد الباسط عبد المعطي). المركز القومي للترجمة.",
        "note": "الربط بين التجارب الفردية والبنى الاجتماعية والتاريخية."
    }
]

# =====================================================================
# ادارة حالة الصفحة ووضع الاضاءة (Light / Dark Mode)
# =====================================================================
query_params = st.query_params
if "view" in query_params:
    st.session_state.current_view = query_params["view"]
elif "current_view" not in st.session_state:
    st.session_state.current_view = "home"

if "pil" in query_params and query_params["pil"] in PILLARS_DATA:
    st.session_state.selected_pil = query_params["pil"]
elif "selected_pil" not in st.session_state:
    st.session_state.selected_pil = "p01"

if "theme" in query_params and query_params["theme"] in ["light", "dark"]:
    st.session_state.theme_mode = query_params["theme"]
elif "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"

is_dark = st.session_state.theme_mode == "dark"
toggle_target = "light" if is_dark else "dark"
toggle_label = "☀️ الوضع الفاتح" if is_dark else "🌙 الوضع الداكن"

# =====================================================================
# ARCTIC BLUE INTELLIGENCE — DESIGN SYSTEM (Lucida Calligraphy + Glassmorphism)
# =====================================================================
if is_dark:
    theme_vars = (
        "--bg: #071120;"
        "--bg-grad: radial-gradient(circle at 12% 10%, #102647 0%, #071120 65%);"
        "--surface: rgba(16, 33, 62, 0.72);"
        "--surface-solid: #0F203D;"
        "--surface-soft: rgba(24, 48, 88, 0.65);"
        "--text: #EBF5FF;"
        "--text-muted: #93B4D8;"
        "--border: rgba(56, 189, 248, 0.24);"
        "--shadow-card: 0 8px 32px rgba(2, 8, 23, 0.45);"
    )
else:
    theme_vars = (
        "--bg: #EEF6FC;"
        "--bg-grad: linear-gradient(180deg, #E2F1FC 0%, #F2F8FD 45%, #EAF4FB 100%);"
        "--surface: rgba(255, 255, 255, 0.78);"
        "--surface-solid: #F7FBFF;"
        "--surface-soft: rgba(224, 242, 254, 0.65);"
        "--text: #0B2545;"
        "--text-muted: #47688A;"
        "--border: rgba(14, 165, 233, 0.25);"
        "--shadow-card: 0 8px 28px rgba(14, 116, 144, 0.08);"
    )

css_styles = (
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');"
    ":root {"
    "  --ice-blue: #E0F2FE;"
    "  --sky-blue: #0EA5E9;"
    "  --digital-indigo: #3B389C;"
    "  --mint-green: #10B981;"
    "  --mint-glow: #34D399;"
    "  --radius-card: 18px;"
    "  --radius-button: 11px;"
    f"  {theme_vars}"
    "}"
    "#MainMenu, header, footer {visibility: hidden;}"
    ".block-container {padding: 0rem !important; max-width: 100% !important;}"
    ".stApp {background: var(--bg-grad) !important; background-color: var(--bg) !important; font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; color: var(--text);}"
    "h1, h2, h3, h4, p, span, div, label, input, select, textarea, button {font-family: 'Cairo', sans-serif;}"
    ".rtl {direction: rtl; text-align: right; unicode-bidi: isolate;}"
    ".ltr {direction: ltr; text-align: left; display: inline-block; unicode-bidi: isolate; font-family: 'Plus Jakarta Sans', sans-serif;}"
    ".ltr-block {direction: ltr; text-align: left; display: block; unicode-bidi: isolate;}"
    "input, textarea {unicode-bidi: plaintext !important; font-size: 13px !important; border-radius: var(--radius-button) !important; border: 1px solid var(--border) !important; background-color: var(--surface-solid) !important; color: var(--text) !important;}"
    "div[data-baseweb='select'] > div {direction: rtl; text-align: right; font-size: 13px !important; border-radius: var(--radius-button) !important; border-color: var(--border) !important; background-color: var(--surface-solid) !important; color: var(--text) !important;}"
    "label p {direction: rtl !important; text-align: right !important; font-size: 13px !important; font-weight: 700 !important; color: var(--text) !important;}"

    "/* 01. Glassmorphic Floating Navbar */"
    ".sl-navbar {background: var(--surface); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border-bottom: 1.5px solid var(--border); padding: 11px 6%; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 999; direction: rtl; box-shadow: var(--shadow-card);}"
    ".sl-brand {display: flex; align-items: center; gap: 12px; text-decoration: none;}"
    ".sl-brand-title {font-family: 'Lucida Calligraphy', 'Brush Script MT', cursive !important; font-size: 24px; font-weight: 700; background: linear-gradient(90deg, var(--sky-blue), var(--digital-indigo), var(--mint-green)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.2; direction: ltr;}"
    ".sl-brand-sub {font-size: 10.5px; color: var(--text-muted); font-weight: 700; display: block;}"
    ".sl-nav-links {display: flex; gap: 10px; flex-wrap: wrap; align-items: center;}"
    ".sl-nav-links a {color: var(--text); text-decoration: none; font-size: 12.5px; font-weight: 700; padding: 6px 10px; border-radius: 9px; transition: all 0.25s ease;}"
    ".sl-nav-links a:hover, .sl-nav-links a.active {color: #FFFFFF; background: linear-gradient(135deg, var(--sky-blue), var(--digital-indigo)); box-shadow: 0 4px 12px rgba(14, 165, 233, 0.25);}"
    ".sl-nav-actions {display: flex; gap: 10px; align-items: center;}"
    ".sl-theme-btn {background: var(--surface-soft); border: 1px solid var(--border); color: var(--text) !important; font-size: 12px; font-weight: 700; padding: 7px 12px; border-radius: 9px; text-decoration: none; transition: all 0.2s ease;}"
    ".sl-theme-btn:hover {border-color: var(--sky-blue); transform: translateY(-1px);}"
    ".sl-cta-top {background: linear-gradient(135deg, var(--sky-blue), var(--digital-indigo)); color: #FFFFFF !important; font-weight: 700; font-size: 12.5px; padding: 8px 16px; border-radius: var(--radius-button); text-decoration: none; box-shadow: 0 4px 14px rgba(59, 56, 156, 0.28); transition: transform 0.2s ease;}"
    ".sl-cta-top:hover {transform: translateY(-2px);}"

    "/* 02. Arctic Hero Section */"
    ".sl-hero {background: linear-gradient(135deg, #091E3A 0%, #162B5C 55%, #1E3A70 100%); color: #FFFFFF; padding: 52px 6%; border-bottom: 2px solid var(--sky-blue); direction: rtl; text-align: right; position: relative; overflow: hidden;}"
    ".sl-hero-grid {max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 1.2fr 1fr; gap: 38px; align-items: center;}"
    "@media (max-width: 960px) {.sl-hero-grid {grid-template-columns: 1fr;} .sl-nav-links {display: none;}}"
    ".sl-badge {display: inline-flex; align-items: center; gap: 6px; background: rgba(16, 185, 129, 0.16); border: 1px solid var(--mint-glow); color: #A7F3D0; font-size: 12px; font-weight: 700; padding: 5px 15px; border-radius: 99px; margin-bottom: 15px;}"
    ".sl-hero-title {font-size: 29px; font-weight: 800; line-height: 1.45; color: #FFFFFF; margin-bottom: 15px;}"
    ".sl-hero-title span {background: linear-gradient(90deg, #38BDF8, #34D399); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}"
    ".sl-hero-desc {color: #CBD5E1; font-size: 14.2px; line-height: 1.85; margin-bottom: 24px;}"
    ".sl-hero-btns {display: flex; gap: 14px; flex-wrap: wrap;}"
    ".sl-btn-mint {background: linear-gradient(135deg, var(--mint-green), #059669); color: #FFFFFF !important; font-weight: 800; font-size: 13.5px; padding: 11px 24px; border-radius: var(--radius-button); text-decoration: none; box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3); transition: all 0.25s ease;}"
    ".sl-btn-mint:hover {transform: translateY(-2px);}"
    ".sl-btn-outline {background: rgba(255, 255, 255, 0.08); backdrop-filter: blur(8px); border: 1.5px solid #38BDF8; color: #FFFFFF !important; font-weight: 700; font-size: 13.5px; padding: 11px 24px; border-radius: var(--radius-button); text-decoration: none; transition: all 0.25s ease;}"
    ".sl-btn-outline:hover {background: rgba(56, 189, 248, 0.18); transform: translateY(-2px);}"

    "/* Glassmorphic Analytics Dashboard Preview */"
    ".sl-stat-card {background: rgba(15, 34, 66, 0.68); backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: var(--radius-card); padding: 20px; box-shadow: 0 20px 45px rgba(4, 13, 28, 0.4);}"
    ".sl-stat-header {display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(56, 189, 248, 0.22); padding-bottom: 10px; margin-bottom: 12px;}"
    ".sl-kpi-grid {display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 12px 0; text-align: center;}"
    ".sl-kpi-box {background: rgba(9, 24, 48, 0.78); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 12px; padding: 9px;}"
    ".sl-kpi-label {font-size: 11px; color: #94A3B8;}"
    ".sl-kpi-val {font-size: 15.5px; font-weight: 800; margin-top: 2px; direction: ltr;}"
    ".sl-reading-box {background: rgba(9, 24, 48, 0.82); border-right: 3.5px solid var(--mint-glow); padding: 11px 14px; border-radius: 9px; font-size: 12.2px; color: #E2E8F0; line-height: 1.65;}"

    "/* Sections & Grids */"
    ".sl-section {max-width: 1200px; margin: 0 auto; padding: 40px 6%; direction: rtl; text-align: right;}"
    ".sl-sec-head {text-align: center; max-width: 740px; margin: 0 auto 28px auto;}"
    ".sl-sec-num {font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11.5px; font-weight: 800; color: var(--mint-green); letter-spacing: 1px; display: block; margin-bottom: 4px;}"
    ".sl-sec-tag {color: var(--sky-blue); font-size: 12.5px; font-weight: 800; background: var(--surface-soft); border: 1px solid var(--border); display: inline-block; padding: 4px 14px; border-radius: 99px; margin-bottom: 6px;}"
    ".sl-sec-title {color: var(--text); font-size: 24px; font-weight: 800; margin: 4px 0 8px 0;}"
    ".sl-sec-sub {color: var(--text-muted); font-size: 13.8px; margin: 0;}"

    "/* 03. Core Services (6 Cards) */"
    ".sl-core-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); gap: 18px;}"
    ".sl-core-card {display: block; text-decoration: none !important; background: var(--surface); backdrop-filter: blur(14px); border: 1px solid var(--border); border-top: 4px solid var(--sky-blue); border-radius: var(--radius-card); padding: 22px; box-shadow: var(--shadow-card); transition: all 0.25s ease; text-align: right;}"
    ".sl-core-card:hover {transform: translateY(-4px); border-color: var(--mint-green);}"
    ".sl-core-card.ind {border-top-color: var(--digital-indigo);}"
    ".sl-core-card.mnt {border-top-color: var(--mint-green);}"

    "/* 05. How It Works (4 Steps) */"
    ".sl-steps-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 18px;}"
    ".sl-step-card {background: var(--surface); backdrop-filter: blur(12px); border: 1px solid var(--border); border-radius: var(--radius-card); padding: 22px; box-shadow: var(--shadow-card); position: relative; text-align: right; transition: transform 0.25s ease;}"
    ".sl-step-card:hover {transform: translateY(-3px); border-color: var(--sky-blue);}"
    ".sl-step-badge {width: 34px; height: 34px; border-radius: 10px; background: linear-gradient(135deg, var(--sky-blue), var(--digital-indigo)); color: #FFFFFF; font-weight: 800; font-size: 14px; display: flex; align-items: center; justify-content: center; margin-bottom: 12px;}"

    "/* 06 & 07. Academy & Scientific Resources */"
    ".sl-acad-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 18px;}"
    ".sl-acad-card {background: var(--surface); backdrop-filter: blur(12px); border: 1px solid var(--border); border-right: 4px solid var(--digital-indigo); border-radius: var(--radius-card); padding: 20px; box-shadow: var(--shadow-card); text-align: right;}"
    ".sl-res-card {background: var(--surface); backdrop-filter: blur(12px); border: 1px solid var(--border); border-top: 3.5px solid var(--mint-green); border-radius: var(--radius-card); padding: 20px; box-shadow: var(--shadow-card); text-align: right;}"

    "/* 08. Why Socio Lab */"
    ".sl-why-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 18px;}"
    ".sl-why-card {background: var(--surface); backdrop-filter: blur(12px); border: 1px solid var(--border); border-radius: var(--radius-card); padding: 22px; box-shadow: var(--shadow-card); text-align: right;}"

    "/* Service Cards & Packages */"
    ".sl-services-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(295px, 1fr)); gap: 18px;}"
    ".sl-srv-card {display: block; text-decoration: none !important; background: var(--surface); backdrop-filter: blur(12px); border: 1px solid var(--border); border-top: 4px solid var(--sky-blue); border-radius: var(--radius-card); padding: 20px; box-shadow: var(--shadow-card); transition: all 0.25s ease; text-align: right;}"
    ".sl-srv-card:hover {transform: translateY(-4px); border-color: var(--mint-green);}"
    ".sl-srv-card.active-card {border: 2px solid var(--sky-blue); background: var(--surface-soft);}"
    ".sl-srv-num {font-size: 14px; font-weight: 800; color: var(--mint-green); margin-bottom: 4px; direction: ltr; display: inline-block;}"
    ".sl-srv-cat {font-size: 11px; font-weight: 700; color: var(--sky-blue); background: var(--surface-soft); border: 1px solid var(--border); padding: 2px 10px; border-radius: 99px; float: left;}"
    ".sl-srv-title {font-size: 15.5px; font-weight: 800; color: var(--text); margin: 8px 0; clear: both;}"
    ".sl-srv-desc {font-size: 12.8px; color: var(--text-muted); line-height: 1.7; margin: 0 0 12px 0;}"
    ".sl-srv-link {font-size: 12.5px; font-weight: 800; color: var(--sky-blue); display: inline-flex; align-items: center; gap: 4px;}"

    ".sl-pkg-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 16px;}"
    ".sl-pkg-card {background: var(--surface); backdrop-filter: blur(12px); border: 1px solid var(--border); border-radius: var(--radius-card); padding: 22px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: var(--shadow-card); transition: transform 0.25s ease; text-align: right;}"
    ".sl-pkg-card:hover {transform: translateY(-4px);}"
    ".sl-pkg-card.featured {border: 2px solid var(--sky-blue); background: var(--surface-soft);}"
    ".sl-pkg-badge {display: inline-block; background: var(--surface-soft); border: 1px solid var(--border); color: var(--text); font-size: 11.5px; font-weight: 700; padding: 4px 12px; border-radius: 99px; margin-bottom: 10px;}"
    ".sl-pkg-badge.dark {background: linear-gradient(90deg, var(--sky-blue), var(--digital-indigo)); color: #FFFFFF; border: none;}"
    ".sl-pkg-item {font-size: 13px; color: var(--text); padding: 6px 0; border-bottom: 1px dashed var(--border);}"
    ".sl-pkg-btn {display: block; text-align: center; background: var(--digital-indigo); color: #FFFFFF !important; font-weight: 700; font-size: 13px; padding: 10px; border-radius: var(--radius-button); text-decoration: none !important; margin-top: 16px;}"
    ".sl-pkg-btn.mint {background: linear-gradient(135deg, var(--mint-green), #059669); color: #FFFFFF !important; font-weight: 800;}"

    "/* Containers & Banners */"
    ".sl-about-box, .sl-detail-box {background: var(--surface); backdrop-filter: blur(14px); border: 1px solid var(--border); border-radius: var(--radius-card); padding: 24px; margin-bottom: 18px; box-shadow: var(--shadow-card); text-align: right;}"
    ".sl-probe-result {background: var(--surface); backdrop-filter: blur(12px); border: 1px solid var(--border); border-right: 4px solid var(--sky-blue); border-radius: var(--radius-card); padding: 16px; margin-top: 12px; font-size: 13px; line-height: 1.75; color: var(--text); box-shadow: var(--shadow-card); text-align: right;}"
    ".sl-deliv-item {background: var(--surface-soft); border: 1px solid var(--border); border-right: 3.5px solid var(--mint-green); padding: 10px 14px; border-radius: var(--radius-button); font-size: 13px; color: var(--text); margin-bottom: 8px; text-align: right;}"
    ".sl-back-link {display: inline-block; color: var(--text) !important; font-weight: 800; font-size: 13px; text-decoration: none !important; margin-bottom: 16px; background: var(--surface); border: 1px solid var(--border); padding: 7px 16px; border-radius: var(--radius-button);}"
    ".sl-result-banner {background-color: var(--surface-soft); border: 1px solid var(--border); border-right: 4px solid var(--sky-blue); padding: 12px 15px; border-radius: var(--radius-button); margin-top: 10px; font-size: 13px; color: var(--text); text-align: right;}"
    ".sl-warn-banner {background-color: var(--surface-soft); border: 1px solid var(--mint-green); border-right: 4px solid var(--mint-green); padding: 12px 15px; border-radius: var(--radius-button); margin-top: 10px; font-size: 13px; color: var(--text); text-align: right;}"
    ".sl-cert-box {background: linear-gradient(135deg, #091E3A 0%, #1E3A70 100%); border: 2px solid var(--mint-glow); border-radius: var(--radius-card); padding: 20px; color: #FFFFFF; text-align: center; margin-top: 12px; box-shadow: var(--shadow-card);}"

    "/* APA 7 Tables */"
    ".sl-apa-table {width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 12.8px; direction: rtl; background: var(--surface-solid);}"
    ".sl-apa-table th {border-top: 2px solid var(--sky-blue); border-bottom: 1.5px solid var(--sky-blue); padding: 9px; color: var(--text); background: var(--surface-soft); text-align: right; font-weight: 800;}"
    ".sl-apa-table td {padding: 9px; border-bottom: 1px solid var(--border); text-align: right; vertical-align: middle; color: var(--text);}"
    ".sl-apa-table td.num-cell {direction: ltr; text-align: right; font-family: 'Plus Jakarta Sans', sans-serif; display: table-cell;}"
    ".sl-apa-table tr:last-child td {border-bottom: 2px solid var(--sky-blue);}"

    ".sl-email-btn {display: block; text-align: center; background: linear-gradient(90deg, var(--sky-blue), var(--digital-indigo)); color: #FFFFFF !important; font-weight: 800; font-size: 14px; padding: 12px 20px; border-radius: var(--radius-button); text-decoration: none !important; margin-top: 12px;}"
    ".sl-footer {background-color: #051224; color: #93B4D8; text-align: center; padding: 36px 6%; font-size: 12.5px; border-top: 2px solid var(--sky-blue); margin-top: 30px;}"
    ".sl-footer-links {display: flex; justify-content: center; gap: 18px; flex-wrap: wrap; margin: 14px 0;}"
    ".sl-footer-links a {color: #CBD5E1; text-decoration: none; font-size: 12.5px; font-weight: 600;}"
    ".sl-footer-links a:hover {color: #38BDF8;}"
    "</style>"
)

st.markdown(css_styles, unsafe_allow_html=True)

active_home = "active" if st.session_state.current_view == "home" else ""
active_srv = "active" if st.session_state.current_view == "services" else ""
active_app = "active" if st.session_state.current_view == "applied_lab" else ""

arctic_logo_svg = (
    '<svg width="42" height="42" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<defs>'
    '<linearGradient id="arcticGrad" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse">'
    '<stop offset="0%" stop-color="#0EA5E9"/>'
    '<stop offset="55%" stop-color="#3B389C"/>'
    '<stop offset="100%" stop-color="#10B981"/>'
    '</linearGradient>'
    '</defs>'
    '<rect width="48" height="48" rx="13" fill="url(#arcticGrad)"/>'
    '<rect x="11" y="25" width="5" height="12" rx="2.5" fill="#E0F2FE"/>'
    '<rect x="19" y="19" width="5" height="18" rx="2.5" fill="#7DD3FC"/>'
    '<rect x="27" y="13" width="5" height="24" rx="2.5" fill="#34D399"/>'
    '<path d="M12 22L21.5 16L30 11L37 14" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
    '<circle cx="37" cy="14" r="3" fill="#34D399"/>'
    '</svg>'
)

# =====================================================================
# 01. NAVIGATION BAR
# =====================================================================
brand_html = (
    f'<a href="?view=home&theme={st.session_state.theme_mode}" target="_self" class="sl-brand">'
    f'{arctic_logo_svg}'
    f'<div><div class="sl-brand-title">Socio Lab</div>'
    f'<span class="sl-brand-sub">Arctic Blue Intelligence</span></div></a>'
)

navbar_html = (
    f'<div class="sl-navbar">{brand_html}'
    f'<div class="sl-nav-links">'
    f'<a href="?view=home&theme={st.session_state.theme_mode}" target="_self" class="{active_home}">الرئيسية</a>'
    f'<a href="?view=home&theme={st.session_state.theme_mode}#core-services" target="_self">الخدمات</a>'
    f'<a href="?view=home&theme={st.session_state.theme_mode}#research-tools" target="_self">الادوات</a>'
    f'<a href="?view=home&theme={st.session_state.theme_mode}#training-academy" target="_self">الاكاديمية</a>'
    f'<a href="?view=home&theme={st.session_state.theme_mode}#scientific-resources" target="_self">المكتبة والمراجع</a>'
    f'<a href="?view=applied_lab&theme={st.session_state.theme_mode}" target="_self" class="{active_app}">استوديو البحث</a>'
    f'</div>'
    f'<div class="sl-nav-actions">'
    f'<a href="?view={st.session_state.current_view}&theme={toggle_target}" target="_self" class="sl-theme-btn">{toggle_label}</a>'
    f'<a href="?view=services&pil=p01&theme={st.session_state.theme_mode}#order-box" target="_self" class="sl-cta-top">بوابة الباحث / اطلب</a>'
    f'</div></div>'
)
st.markdown(navbar_html, unsafe_allow_html=True)

# =====================================================================
# الصفحة الاولى: الواجهة الرئيسية وفق معمارية Socio Lab (01 -> 10)
# =====================================================================
if st.session_state.current_view == "home":
    # 02. HERO SECTION
    hero_html = (
        f'<div class="sl-hero"><div class="sl-hero-grid">'
        f'<div>'
        f'<div class="sl-badge">&mu; ذكاء احصائي • قراءة سوسيولوجية • توثيق <span class="ltr">APA 7</span></div>'
        f'<div class="sl-hero-title">قراءة أعمق للبيانات، وبناء أقوى للبحث.. '
        f'<span>منصتك الإحصائية والمنهجية المتكاملة</span></div>'
        f'<p class="sl-hero-desc">في <strong class="ltr">Socio Lab</strong> نحول البيانات الميدانية الخام '
        f'الى رؤى سوسيولوجية وعلمية رصينة. نرافق طلبة الليسانس والماستر والدكتوراه، والاساتذة، '
        f'ومخابر البحث، والمؤسسات في التحليل الاحصائي، التصميم المنهجي، والبحث النوعي والمختلط.</p>'
        f'<div class="sl-hero-btns">'
        f'<a href="?view=services&pil=p01&theme={st.session_state.theme_mode}" target="_self" class="sl-btn-mint">تصفح المنظومة الكاملة (14 محورا)</a>'
        f'<a href="#scientific-resources" class="sl-btn-outline">استعرض المراجع والمكتبة</a>'
        f'</div></div>'
        f'<div class="sl-stat-card">'
        f'<div class="sl-stat-header"><div>'
        f'<div style="font-size:11px; color:#34D399; font-weight:700;">لوحة المؤشرات الذكية <span class="ltr">Analytics Dashboard</span></div>'
        f'<div style="font-size:14.5px; font-weight:800; color:#FFFFFF;">تحليل التوزيع الطبيعي ومؤشرات الثبات</div>'
        f'</div>'
        f'<span class="ltr" style="background:rgba(56,189,248,0.2); color:#38BDF8; font-size:11px; padding:4px 10px; border-radius:8px; font-weight:700;">SPSS &amp; PLS</span>'
        f'</div>'
        f'<div style="background:rgba(9,24,48,0.85); padding:12px; border-radius:12px; border:1px solid rgba(56,189,248,0.25);">'
        f'<svg viewBox="0 0 300 95" style="width:100%; height:88px; display:block;">'
        f'<defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="#38BDF8" stop-opacity="0.55"/>'
        f'<stop offset="100%" stop-color="#10B981" stop-opacity="0.0"/>'
        f'</linearGradient></defs>'
        f'<line x1="10" y1="80" x2="290" y2="80" stroke="rgba(148,163,184,0.35)" stroke-width="1"/>'
        f'<line x1="150" y1="12" x2="150" y2="80" stroke="#34D399" stroke-dasharray="3,3" stroke-width="1.6"/>'
        f'<path d="M 15 80 C 75 80, 105 12, 150 12 C 195 12, 225 80, 285 80 Z" fill="url(#g1)"/>'
        f'<path d="M 15 80 C 75 80, 105 12, 150 12 C 195 12, 225 80, 285 80" fill="none" stroke="#38BDF8" stroke-width="2.6"/>'
        f'<text x="150" y="92" fill="#34D399" font-size="9.5" font-weight="bold" text-anchor="middle">&mu; = 3.84</text>'
        f'</svg></div>'
        f'<div class="sl-kpi-grid">'
        f'<div class="sl-kpi-box"><div class="sl-kpi-label">الفا كرونباخ (<span class="ltr">&alpha;</span>)</div>'
        f'<div class="sl-kpi-val" style="color:#38BDF8;">0.892</div></div>'
        f'<div class="sl-kpi-box"><div class="sl-kpi-label">حجم العينة (<span class="ltr">N</span>)</div>'
        f'<div class="sl-kpi-val" style="color:#FFFFFF;">60</div></div>'
        f'<div class="sl-kpi-box"><div class="sl-kpi-label">الدلالة (<span class="ltr">Sig</span>)</div>'
        f'<div class="sl-kpi-val" style="color:#34D399;">0.001</div></div>'
        f'</div>'
        f'<div class="sl-reading-box"><strong>القراءة السوسيولوجية:</strong> تشير قيمة الفا كرونباخ (0.892) '
        f'الى اتساق داخلي مرتفع جدا لاداة القياس، مع دلالة احصائية تؤكد اثر المتغير المستقل عند مستوى 0.01.</div>'
        f'</div>'
        f'</div></div>'
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    # 03. CORE SERVICES
    core_services_html = (
        f'<div id="core-services" class="sl-section">'
        f'<div class="sl-sec-head">'
        f'<span class="sl-sec-num">03 • CORE SERVICES</span>'
        f'<div class="sl-sec-title">الخدمات العلمية والاحصائية الست الرئيسية</div>'
        f'<p class="sl-sec-sub">حلول متكاملة تغطي كافة مراحل البحث العلمي من التصميم المنهجي الى النمذجة المتقدمة والنشر الدولي.</p>'
        f'</div>'
        f'<div class="sl-core-grid">'
        f'<a href="?view=services&pil=p01&theme={st.session_state.theme_mode}#pillar-details" target="_self" class="sl-core-card">'
        f'<div style="font-size:12px; color:var(--sky-blue); font-weight:800;">01 • التحليل الاساسي والمتقدم</div>'
        f'<div style="font-size:16px; font-weight:800; color:var(--text); margin:6px 0;">التحليل الاحصائي الشامل عبر SPSS</div>'
        f'<p style="font-size:13px; color:var(--text-muted); line-height:1.7; margin-bottom:10px;">الاختبارات الوصفية والاستدلالية، المعلمية واللامعلمية، الانحدار، والتحليل العاملي EFA/CFA مع جداول APA 7.</p>'
        f'<span class="sl-srv-link">استكشف التفاصيل &larr;</span>'
        f'</a>'
        f'<a href="?view=services&pil=p02&theme={st.session_state.theme_mode}#pillar-details" target="_self" class="sl-core-card ind">'
        f'<div style="font-size:12px; color:var(--digital-indigo); font-weight:800;">02 • الضبط المنهجي</div>'
        f'<div style="font-size:16px; font-weight:800; color:var(--text); margin:6px 0;">الاستشارات المنهجية وتحديد العينات</div>'
        f'<p style="font-size:13px; color:var(--text-muted); line-height:1.7; margin-bottom:10px;">بناء الاشكالية، صياغة الفرضيات، تحديد مجتمع الدراسة وحساب حجم العينة وخطة التحليل قبل جمع البيانات.</p>'
        f'<span class="sl-srv-link">استكشف التفاصيل &larr;</span>'
        f'</a>'
        f'<a href="?view=services&pil=p03&theme={st.session_state.theme_mode}#pillar-details" target="_self" class="sl-core-card mnt">'
        f'<div style="font-size:12px; color:var(--mint-green); font-weight:800;">03 • ادوات القياس</div>'
        f'<div style="font-size:16px; font-weight:800; color:var(--text); margin:6px 0;">تصميم الاستبيانات والمقاييس</div>'
        f'<p style="font-size:13px; color:var(--text-muted); line-height:1.7; margin-bottom:10px;">تحويل المفاهيم النظرية الى مؤشرات قابلة للقياس، التحكيم العلمي، وبرمجة الاستمارات الرقمية وقاعدة الترميز.</p>'
        f'<span class="sl-srv-link">استكشف التفاصيل &larr;</span>'
        f'</a>'
        f'<a href="?view=services&pil=p04&theme={st.session_state.theme_mode}#pillar-details" target="_self" class="sl-core-card ind">'
        f'<div style="font-size:12px; color:var(--digital-indigo); font-weight:800;">04 • النمذجة المتعددة</div>'
        f'<div style="font-size:16px; font-weight:800; color:var(--text); margin:6px 0;">تحليل البيانات المتقدم (SmartPLS / R / Python)</div>'
        f'<p style="font-size:13px; color:var(--text-muted); line-height:1.7; margin-bottom:10px;">نمذجة المعادلات الهيكلية SEM، تحليل المسار، الوساطة والتعديل، وبناء لوحات البيانات التفاعلية Dashboards.</p>'
        f'<span class="sl-srv-link">استكشف التفاصيل &larr;</span>'
        f'</a>'
        f'<a href="?view=services&pil=p05&theme={st.session_state.theme_mode}#pillar-details" target="_self" class="sl-core-card">'
        f'<div style="font-size:12px; color:var(--sky-blue); font-weight:800;">05 • المقاربات الكيفية</div>'
        f'<div style="font-size:16px; font-weight:800; color:var(--text); margin:6px 0;">مختبر البحث النوعي والمختلط (NVivo)</div>'
        f'<p style="font-size:13px; color:var(--text-muted); line-height:1.7; margin-bottom:10px;">تحليل المقابلات المعمقة، مجموعات التركيز، التحليل الموضوعاتي، ودمج النتائج الكمية والنوعية.</p>'
        f'<span class="sl-srv-link">استكشف التفاصيل &larr;</span>'
        f'</a>'
        f'<a href="?view=services&pil=p09&theme={st.session_state.theme_mode}#pillar-details" target="_self" class="sl-core-card mnt">'
        f'<div style="font-size:12px; color:var(--mint-green); font-weight:800;">06 • النشر الدولي</div>'
        f'<div style="font-size:16px; font-weight:800; color:var(--text); margin:6px 0;">مركز النشر الاكاديمي والتوثيق</div>'
        f'<p style="font-size:13px; color:var(--text-muted); line-height:1.7; margin-bottom:10px;">هيكلة المقالات وفق IMRAD، التوجيه لاختيار المجلات المحكمة، وضبط المراجع عبر Zotero و APA 7.</p>'
        f'<span class="sl-srv-link">استكشف التفاصيل &larr;</span>'
        f'</a>'
        f'</div>'
        f'<div style="text-align:center; margin-top:20px;">'
        f'<a href="?view=services&pil=p01&theme={st.session_state.theme_mode}" target="_self" class="sl-srv-link" style="font-size:13.5px;">'
        f'عرض كافة اقسام المنصة الـ 14 والباقات الاستشارية &larr;</a></div>'
        f'</div>'
    )
    st.markdown(core_services_html, unsafe_allow_html=True)

    # =================================================================
    # 04. RESEARCH TOOLS
    # =================================================================
    lab_header = (
        '<div id="research-tools" style="max-width:1200px; margin:0 auto; padding:25px 6% 10px 6%;">'
        '<div class="sl-sec-head" style="margin-bottom:16px;">'
        '<span class="sl-sec-num">04 • RESEARCH TOOLS</span>'
        '<div class="sl-sec-title">الادوات الرقمية والتفاعلية المجانية</div>'
        '<p class="sl-sec-sub">ادوات حسابية ومنهجية فورية داخل المتصفح لفحص قواعد البيانات، اختيار الاختبار الاحصائي، وبناء الجداول.</p>'
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
                    t_interp = "اذا كانت Sig اقل من 0.05 توجد فروق ذات دلالة احصائيا لصالح المجموعة ذات المتوسط الاعلى."
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
                f'<div style="font-size:16px; font-weight:800; color:var(--sky-blue); margin-bottom:10px;">الاختبار المقترح: {t_title}</div>'
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
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 220" style="width:100%; max-height:220px; background:var(--surface-solid); border:1px solid var(--border); border-radius:16px;">'
                f'<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
                f'<path d="M 0 1 L 10 5 L 0 9 z" fill="#0EA5E9"/></marker></defs>'
                f'<rect x="460" y="110" width="200" height="55" rx="10" fill="#091E3A" stroke="#38BDF8" stroke-width="2"/>'
                f'<text x="560" y="133" fill="#38BDF8" font-size="11" text-anchor="middle" font-family="Cairo, sans-serif">المتغير المستقل (X)</text>'
                f'<text x="560" y="152" fill="#FFFFFF" font-size="13" font-weight="bold" text-anchor="middle" font-family="Cairo, sans-serif">{v_indep}</text>'
                f'<rect x="250" y="25" width="200" height="55" rx="10" fill="#3B389C" stroke="#7DD3FC" stroke-width="2"/>'
                f'<text x="350" y="48" fill="#E0F2FE" font-size="11" text-anchor="middle" font-family="Cairo, sans-serif">المتغير الوسيط (M)</text>'
                f'<text x="350" y="67" fill="#FFFFFF" font-size="13" font-weight="bold" text-anchor="middle" font-family="Cairo, sans-serif">{v_med}</text>'
                f'<rect x="40" y="110" width="200" height="55" rx="10" fill="#065F46" stroke="#34D399" stroke-width="2"/>'
                f'<text x="140" y="133" fill="#A7F3D0" font-size="11" text-anchor="middle" font-family="Cairo, sans-serif">المتغير التابع (Y)</text>'
                f'<text x="140" y="152" fill="#FFFFFF" font-size="13" font-weight="bold" text-anchor="middle" font-family="Cairo, sans-serif">{v_dep}</text>'
                f'<line x1="460" y1="138" x2="246" y2="138" stroke="#0EA5E9" stroke-width="2.2" marker-end="url(#arrow)"/>'
                f'<text x="350" y="155" fill="#0EA5E9" font-size="11" font-weight="bold" text-anchor="middle">الاثر المباشر (H1)</text>'
                f'<line x1="520" y1="110" x2="410" y2="82" stroke="#10B981" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrow)"/>'
                f'<line x1="290" y1="80" x2="180" y2="108" stroke="#10B981" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrow)"/>'
                f'</svg>'
            )
            st.markdown(svg_diagram, unsafe_allow_html=True)

        with tab_socio:
            st.markdown(
                '<div style="font-size:16px; font-weight:800; color:var(--text); margin:10px 0;">'
                'مترجم الاحصاء الى خطاب سوسيولوجي (<span class="ltr">Stats-to-Sociology Translator</span>)</div>',
                unsafe_allow_html=True,
            )
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
            st.markdown(f'<div class="sl-probe-result">"{socio_templates[res_pattern]}"</div>', unsafe_allow_html=True)

        with tab_defense:
            dc1, dc2 = st.columns(2, gap="large")
            with dc1:
                st.markdown('<div style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:8px;">مولد المراجع (<span class="ltr">APA 7th</span>)</div>', unsafe_allow_html=True)
                ref_author = st.text_input("المؤلف:", placeholder="مثال: دوركايم، إميل")
                ref_year = st.text_input("السنة:", placeholder="2018")
                ref_title = st.text_input("العنوان:", placeholder="الانتحار: دراسة في علم الاجتماع")
                ref_source = st.text_input("المصدر:", placeholder="الهيئة العامة للكتاب")
                if ref_author and ref_year and ref_title:
                    st.markdown(f'<div class="sl-result-banner">{ref_author} ({ref_year}). <em>{ref_title}</em>. {ref_source}.</div>', unsafe_allow_html=True)

            with dc2:
                st.markdown('<div style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:8px;">شهادة الجاهزية المنهجية الاولية</div>', unsafe_allow_html=True)
                cert_name = st.text_input("اسم الباحث(ة):", placeholder="مثال: علوي وصال")
                cert_study = st.text_input("عنوان البحث:", placeholder="مثال: جنوح الأحداث وأثر جماعة الرفاق")
                if cert_name and cert_study:
                    today_str = datetime.date.today().strftime("%Y-%m-%d")
                    cert_code = f"SL-CERT-{random.randint(1000, 9999)}"
                    st.markdown(
                        f'<div class="sl-cert-box" style="padding:16px;">'
                        f'<div style="font-size:11px; color:#34D399; font-weight:700;">مختبر Socio Lab</div>'
                        f'<div style="font-size:16px; font-weight:800; margin:4px 0;">شهادة اجتياز الفحص المنهجي الاولي</div>'
                        f'<div style="font-size:12.5px;">الباحث(ة): <strong>{cert_name}</strong> | رمز: <span class="ltr">{cert_code}</span> ({today_str})</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

    # =================================================================
    # 05. HOW IT WORKS
    # =================================================================
    how_html = (
        '<div id="how-it-works" class="sl-section" style="padding-bottom:15px;">'
        '<div class="sl-sec-head">'
        '<span class="sl-sec-num">05 • HOW IT WORKS</span>'
        '<div class="sl-sec-title">طريقة الاستفادة من خدمات <span class="ltr">Socio Lab</span></div>'
        '</div>'
        '<div class="sl-steps-grid">'
        '<div class="sl-step-card"><div class="sl-step-badge">1</div><div style="font-size:15.5px; font-weight:800; color:var(--text); margin-bottom:6px;">تحديد المسار او الخدمة</div><p style="font-size:12.8px; color:var(--text-muted); margin:0;">اختر الخدمة المطلوبة من بين المحاور الـ 14 او حدد احدى الباقات المتكاملة.</p></div>'
        '<div class="sl-step-card"><div class="sl-step-badge">2</div><div style="font-size:15.5px; font-weight:800; color:var(--text); margin-bottom:6px;">ارسال البيانات والاشكالية</div><p style="font-size:12.8px; color:var(--text-muted); margin:0;">ارسل عنوان دراستك، فرضياتك، او قاعدة بياناتك الميدانية عبر نموذج الطلب.</p></div>'
        '<div class="sl-step-card"><div class="sl-step-badge">3</div><div style="font-size:15.5px; font-weight:800; color:var(--text); margin-bottom:6px;">المعالجة والتحليل السوسيولوجي</div><p style="font-size:12.8px; color:var(--text-muted); margin:0;">تنظيف البيانات، اجراء الاختبارات الدقيقة، وصياغة القراءة السوسيولوجية.</p></div>'
        '<div class="sl-step-card"><div class="sl-step-badge">4</div><div style="font-size:15.5px; font-weight:800; color:var(--text); margin-bottom:6px;">الاستلام والمرافقة للمناقشة</div><p style="font-size:12.8px; color:var(--text-muted); margin:0;">استلام الملفات منسقة وفق APA 7 مع ضمان تنفيذ تعديلات المشرف.</p></div>'
        '</div></div>'
    )
    st.markdown(how_html, unsafe_allow_html=True)

    # =================================================================
    # 06. TRAINING ACADEMY
    # =================================================================
    academy_html = (
        f'<div id="training-academy" class="sl-section" style="padding-bottom:15px;">'
        f'<div class="sl-sec-head">'
        f'<span class="sl-sec-num">06 • TRAINING ACADEMY</span>'
        f'<div class="sl-sec-title">اكاديمية <span class="ltr">Socio Lab</span> للتكوين الاحصائي والمنهجي</div>'
        f'</div>'
        f'<div class="sl-acad-grid">'
        f'<div class="sl-acad-card"><div style="font-size:16px; font-weight:800; color:var(--text); margin-bottom:6px;">SPSS من الصفر الى الاحتراف</div><p style="font-size:12.8px; color:var(--text-muted); margin:0;">الترميز، تنظيف البيانات، الاختبارات المعلمية واللامعلمية، والتحليل العاملي.</p></div>'
        f'<div class="sl-acad-card" style="border-right-color:var(--mint-green);"><div style="font-size:16px; font-weight:800; color:var(--text); margin-bottom:6px;">هندسة البحث العلمي وبناء المقاييس</div><p style="font-size:12.8px; color:var(--text-muted); margin:0;">صياغة الاشكالية والفرضيات، اختيار العينات، وضبط الصدق والثبات.</p></div>'
        f'<div class="sl-acad-card" style="border-right-color:var(--sky-blue);"><div style="font-size:16px; font-weight:800; color:var(--text); margin-bottom:6px;">SmartPLS, R, Python &amp; NVivo</div><p style="font-size:12.8px; color:var(--text-muted); margin:0;">نمذجة المعادلات الهيكلية SEM، تحليل البيانات، والتحليل الكيفي.</p></div>'
        f'</div></div>'
    )
    st.markdown(academy_html, unsafe_allow_html=True)

    # =================================================================
    # 07. SCIENTIFIC RESOURCES (المكتبة والمراجع العلمية الموثقة APA 7)
    # =================================================================
    st.markdown(
        '<div id="scientific-resources" class="sl-section" style="padding-bottom:10px;">'
        '<div class="sl-sec-head" style="margin-bottom:18px;">'
        '<span class="sl-sec-num">07 • SCIENTIFIC RESOURCES &amp; BIBLIOGRAPHY</span>'
        '<div class="sl-sec-title">المكتبة العلمية وفهرس المراجع (المنهجية، الإحصاء/SPSS، علم الاجتماع، انحراف وجريمة)</div>'
        '<p class="sl-sec-sub">اختر التخصص أو ابحث عن مرجع أو نظرية للحصول على التوثيق الجاهز وفق معايير APA 7.</p>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    _, ref_col, _ = st.columns([0.05, 0.90, 0.05])
    with ref_col:
        rf1, rf2 = st.columns([0.45, 0.55])
        with rf1:
            ref_fields = [
                "جميع التخصصات",
                "سوسيولوجيا الانحراف والجريمة",
                "المنهجية ومناهج البحث العلمي",
                "الإحصاء التطبيقي و SPSS",
                "علم الاجتماع العام"
            ]
            selected_ref_field = st.selectbox("اختر التخصص:", ref_fields, key="home_ref_field")
        with rf2:
            ref_query = st.text_input("ابحث في المراجع (مؤلف، عنوان، موضوع):", placeholder="مثال: دوركايم، جنوح، بوحوش، SPSS...", key="home_ref_search").strip().lower()

        filtered_refs = []
        for r_item in REFERENCES_LIST:
            ok_f = (selected_ref_field == "جميع التخصصات") or (r_item["field"] == selected_ref_field)
            ok_q = (
                not ref_query
                or ref_query in r_item["title"].lower()
                or ref_query in r_item["apa"].lower()
                or ref_query in r_item["note"].lower()
            )
            if ok_f and ok_q:
                filtered_refs.append(r_item)

        if filtered_refs:
            export_txt = "\n".join([f"{i+1}. {item['apa']}" for i, item in enumerate(filtered_refs)])
            st.download_button(
                label=f"تحميل قائمة المراجع المعروضة ({len(filtered_refs)} مرجع) بصيغة APA 7 (.txt)",
                data=export_txt,
                file_name="SocioLab_References_APA7.txt",
                mime="text/plain",
                use_container_width=True,
            )

        for r_item in filtered_refs:
            is_latin_ref = r_item["apa"][0].isascii()
            dir_cls_ref = "ltr-block" if is_latin_ref else "rtl"
            border_c = "var(--mint-green)" if "انحراف" in r_item["field"] else (
                "var(--sky-blue)" if "SPSS" in r_item["field"] else "var(--digital-indigo)"
            )
            ref_card_html = (
                f'<div class="sl-detail-box" style="padding:16px; margin-bottom:10px; border-right:4px solid {border_c};">'
                f'<span class="sl-sec-tag" style="margin-bottom:4px;">{r_item["field"]}</span>'
                f'<div style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:6px;">{r_item["title"]}</div>'
                f'<div class="sl-result-banner" style="margin-top:4px;">'
                f'<div style="font-size:11px; font-weight:700; color:var(--sky-blue); margin-bottom:2px;">التوثيق (APA 7th):</div>'
                f'<div class="{dir_cls_ref}" style="font-size:13px; font-weight:600;">{r_item["apa"]}</div>'
                f'</div>'
                f'<div style="font-size:12px; color:var(--text-muted); margin-top:6px;">• {r_item["note"]}</div>'
                f'</div>'
            )
            st.markdown(ref_card_html, unsafe_allow_html=True)

    # =================================================================
    # 08. WHY SOCIO LAB
    # =================================================================
    why_html = (
        '<div id="why-sociolab" class="sl-section" style="padding-bottom:15px;">'
        '<div class="sl-sec-head">'
        '<span class="sl-sec-num">08 • WHY SOCIO LAB</span>'
        '<div class="sl-sec-title">لماذا يختار الباحثون منصة <span class="ltr">Socio Lab</span>؟</div>'
        '</div>'
        '<div class="sl-why-grid">'
        '<div class="sl-why-card"><div style="font-size:16px; font-weight:800; color:var(--sky-blue); margin-bottom:4px;">01. قراءة سوسيولوجية عميقة</div><p style="font-size:12.8px; color:var(--text-muted); margin:0;">ربط المؤشرات الاحصائية بالاطر النظرية والسياق الاجتماعي.</p></div>'
        '<div class="sl-why-card"><div style="font-size:16px; font-weight:800; color:var(--mint-green); margin-bottom:4px;">02. التزام صارم بالنزاهة العلمية</div><p style="font-size:12.8px; color:var(--text-muted); margin:0;">العمل حصريا على البيانات الميدانية الحقيقية مع السرية التامة.</p></div>'
        '<div class="sl-why-card"><div style="font-size:16px; font-weight:800; color:var(--digital-indigo); margin-bottom:4px;">03. معايير النشر الدولي APA 7</div><p style="font-size:12.8px; color:var(--text-muted); margin:0;">تسليم الجداول والمراجع والملاحق وفق معايير APA 7.</p></div>'
        '<div class="sl-why-card"><div style="font-size:16px; font-weight:800; color:var(--sky-blue); margin-bottom:4px;">04. مرافقة حتى المناقشة</div><p style="font-size:12.8px; color:var(--text-muted); margin:0;">تنفيذ تعديلات الاستاذ المشرف لضمان جودة المخرجات.</p></div>'
        '</div></div>'
    )
    st.markdown(why_html, unsafe_allow_html=True)

    # =================================================================
    # 09. FAQ & CONTACT
    # =================================================================
    st.markdown(
        '<div id="faq-contact" class="sl-section" style="padding-bottom:10px;">'
        '<div class="sl-sec-head" style="margin-bottom:20px;">'
        '<span class="sl-sec-num">09 • FAQ &amp; CONTACT</span>'
        '<div class="sl-sec-title">الاسئلة الشائعة والتواصل المباشر</div>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    _, faq_col, contact_col, _ = st.columns([0.05, 0.45, 0.45, 0.05], gap="large")
    with faq_col:
        st.markdown('<div style="font-size:16px; font-weight:800; color:var(--text); margin-bottom:10px;">الاسئلة الشائعة للباحثين</div>', unsafe_allow_html=True)
        faq_items = {
            "ما هي الملفات التي استلمها بعد انتهاء التحليل الاحصائي؟": "تستلم قاعدة البيانات المرمزة (.sav)، ملف مخرجات البرنامج (.spv)، وتقرير Word منسق وفق معايير APA 7.",
            "هل تلتزمون بتنفيذ ملاحظات وتعديلات الاستاذ المشرف؟": "نعم، نتكفل بتنفيذ التعديلات الاحصائية او المنهجية المطلوبة من الاستاذ المشرف.",
            "هل بيانات الاستبيان او اطروحتي محفوظة بسرية؟": "نعم، تخضع جميع البيانات لبروتوكول سرية صارم."
        }
        sel_faq = st.selectbox("اختر سؤالا للاطلاع على الاجابة:", list(faq_items.keys()))
        st.markdown(f'<div class="sl-result-banner">{faq_items[sel_faq]}</div>', unsafe_allow_html=True)

    with contact_col:
        qr_img_url = f"https://api.qrserver.com/v1/create-qr-code/?size=115x115&data={urllib.parse.quote(APP_URL)}"
        contact_card_html = (
            f'<div class="sl-about-box" style="display:grid; grid-template-columns: 1fr auto; gap:18px; align-items:center; margin-bottom:0;">'
            f'<div>'
            f'<div style="font-size:16px; font-weight:800; color:var(--text); margin-bottom:6px;">ابدأ مشروعك البحثي الان</div>'
            f'<p style="font-size:13px; color:var(--text-muted); line-height:1.7; margin-bottom:12px;">'
            f'فريق <strong class="ltr">Socio Lab</strong> جاهز لمرافقتك في التحليل الاحصائي والاستشارات المنهجية.</p>'
            f'<a href="?view=services&pil=p01&theme={st.session_state.theme_mode}#order-box" target="_self" class="sl-btn-mint" style="display:inline-block; padding:9px 18px; font-size:13px;">انتقل الى نموذج الطلب &larr;</a>'
            f'</div>'
            f'<div style="text-align:center; background:var(--surface-soft); padding:10px; border-radius:12px; border:1px solid var(--border);">'
            f'<img src="{qr_img_url}" alt="QR Code" style="width:105px; height:105px; display:block; margin:0 auto 4px auto;">'
            f'<div style="font-size:10.5px; font-weight:700; color:var(--text);">امسح للمشاركة</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(contact_card_html, unsafe_allow_html=True)

# =====================================================================
# الصفحة الثانية: المنظومة المتكاملة للخدمات والباقات (14 محورا)
# =====================================================================
elif st.session_state.current_view == "services":
    current_key = st.session_state.selected_pil
    current_pil = PILLARS_DATA[current_key]
    selected_pkg = query_params.get("pkg", "")

    st.markdown(
        f'<div class="sl-section" style="padding-top:28px; padding-bottom:10px;">'
        f'<a href="?view=home&theme={st.session_state.theme_mode}" target="_self" class="sl-back-link">&rarr; العودة الى الواجهة الرئيسية</a>'
        f'<div class="sl-sec-head" style="margin-bottom:18px;">'
        f'<div class="sl-sec-tag">الهيكلة الشاملة لمنصة Socio Lab</div>'
        f'<div class="sl-sec-title">الاقسام والخدمات العلمية والاحصائية (14 محورا)</div>'
        f'<p class="sl-sec-sub">تصفح الاقسام حسب التخصص، واضغط على اي قسم لعرض خدماته التفصيلية او اطلب خدماتك مباشرة في الاسفل.</p>'
        f'</div></div>',
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
                    f'<a href="?view=services&pil={k}&theme={st.session_state.theme_mode}#pillar-details" target="_self" class="sl-srv-card {act_cls}">'
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
        f'<div class="sl-detail-box" style="border-top: 4px solid var(--sky-blue);">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:10px;">'
        f'<span style="background:linear-gradient(90deg, var(--sky-blue), var(--digital-indigo)); color:#FFFFFF; font-size:12px; font-weight:700; padding:4px 12px; border-radius:99px;">القسم رقم {current_pil["num"]} • {current_pil["cat"]}</span>'
        f'</div>'
        f'<h2 style="font-size:21px; font-weight:800; color:var(--text); margin:6px 0 10px 0;">{current_pil["title"]}</h2>'
        f'<p style="font-size:13.8px; color:var(--text-muted); line-height:1.8; margin-bottom:16px;">{current_pil["desc"]}</p>'
        f'<h3 style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:10px;">الخدمات والحلول المتوفرة في هذا القسم:</h3>'
        f'{items_html}'
        f'</div></div>'
    )
    st.markdown(detail_html, unsafe_allow_html=True)

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
            f'<a href="?view=services&pil={pk["ref"]}&pkg={pk_key}&theme={st.session_state.theme_mode}#order-box" target="_self" class="sl-pkg-btn {pk["btn_class"]}">'
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
        f'<div class="sl-section" style="padding-top:28px; padding-bottom:10px;">'
        f'<a href="?view=home&theme={st.session_state.theme_mode}" target="_self" class="sl-back-link">&rarr; العودة الى الواجهة الرئيسية</a>'
        f'<div class="sl-sec-head" style="margin-bottom:22px;">'
        f'<div class="sl-sec-tag">بيئة العمل التطبيقية المتقدمة</div>'
        f'<div class="sl-sec-title">استوديو البحث الميداني والاحصائي (<span class="ltr">Applied Research Studio</span>)</div>'
        f'<p class="sl-sec-sub">اجراء الاختبارات الاحصائية الفورية على ملفات البيانات، بناء الاستبيانات ودليل الترميز، تحليل المقابلات الكيفية، وصياغة فصل الاجراءات المنهجية.</p>'
        f'</div></div>'
    )
    st.markdown(lab_page_header, unsafe_allow_html=True)

    _, ap_col, _ = st.columns([0.05, 0.90, 0.05])
    with ap_col:
        st.markdown(
            '<div class="sl-detail-box" style="border-top:4px solid var(--sky-blue);">'
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
            '<div class="sl-detail-box" style="border-top:4px solid var(--mint-green);">'
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

# =====================================================================
# 10. FOOTER
# =====================================================================
footer_html = (
    f'<div class="sl-footer">'
    f'<div style="display:flex; justify-content:center; align-items:center; gap:10px; margin-bottom:10px;">'
    f'{arctic_logo_svg}'
    f'<span style="font-family:\'Lucida Calligraphy\', cursive; font-size:22px; color:#FFFFFF; font-weight:700;">Socio Lab</span>'
    f'</div>'
    f'<div style="color:#E2E8F0; font-weight:700; max-width:750px; margin:0 auto 10px auto; line-height:1.7;">'
    f'ميثاق النزاهة العلمية: تلتزم منصة Socio Lab بتقديم الاستشارات المنهجية والتحليل الاحصائي للبيانات الميدانية الحقيقية فقط، '
    f'وترفض فبركة البيانات او بيع البحوث الجاهزة مع ضمان السرية التامة لبيانات الباحثين.</div>'
    f'<div class="sl-footer-links">'
    f'<a href="?view=home&theme={st.session_state.theme_mode}" target="_self">الرئيسية</a>'
    f'<a href="?view=services&pil=p01&theme={st.session_state.theme_mode}" target="_self">الخدمات الـ 14 والباقات</a>'
    f'<a href="?view=applied_lab&theme={st.session_state.theme_mode}" target="_self">استوديو البحث الميداني</a>'
    f'<a href="?view=home&theme={st.session_state.theme_mode}#scientific-resources" target="_self">المكتبة والمراجع</a>'
    f'</div>'
    f'<div style="font-size:12px; color:#38BDF8; margin-top:6px;">البريد الرسمي للتواصل: <span class="ltr">{CONTACT_EMAIL}</span></div>'
    f'<div style="font-size:11px; color:#93B4D8; margin-top:6px;">جميع الحقوق محفوظة &copy; 2026 <span class="ltr">Socio Lab</span> • Arctic Blue Intelligence</div>'
    f'</div>'
)
st.markdown(footer_html, unsafe_allow_html=True)
