import streamlit as st
import pandas as pd

# قاعدة بيانات القاموس الإحصائي والمنهجي الثلاثي
DICTIONARY_DB = [
    {
        "ar": "معامل الثبات ألفا كرونباخ",
        "fr": "Coefficient Alpha de Cronbach",
        "en": "Cronbach's Alpha",
        "cat": "القياس والسيكومترية",
        "def": "مؤشر إحصائي يقيس الاتساق الداخلي (التجانس) بين عبارات المقياس أو الاستبيان.",
        "usage": "يُقبل المقياس إحصائياً إذا كانت القيمة 0.70 فأكثر، وتُعد ممتازة فوق 0.85.",
        "spss": "Analyze > Scale > Reliability Analysis"
    },
    {
        "ar": "مستوى الدلالة الإحصائية",
        "fr": "Seuil de signification (Valeur p)",
        "en": "P-Value (Sig)",
        "cat": "الاستدلال الإحصائي",
        "def": "احتمال الحصول على النتيجة الإحصائية عن طريق الصدفة بفرض صحة الفرضية الصفرية.",
        "usage": "إذا كانت Sig أقل من 0.05 نرفض الفرضية الصفرية ونقبل الفرضية البديلة بوجود أثر أو فرق.",
        "spss": "يظهر تلقائياً في عمود (Sig.) في معظم جداول مخرجات SPSS"
    },
    {
        "ar": "التوزيع الطبيعي",
        "fr": "Distribution normale",
        "en": "Normal Distribution",
        "cat": "فحص البيانات",
        "def": "توزيع اعتدالي متماثل للبيانات حول المتوسط الحسابي على شكل منحنى الجرس.",
        "usage": "يحدد ما إذا كنا سنستخدم الاختبارات المعلمية (عند تحقق الاعتدالية) أو اللامعلمية (عند اختلالها).",
        "spss": "Analyze > Descriptive Statistics > Explore > Normality plots with tests"
    },
    {
        "ar": "المتغير الوسيط",
        "fr": "Variable médiatrice",
        "en": "Mediating Variable",
        "cat": "النمذجة المتقدمة",
        "def": "متغير يقع في المنتصف ويفسر الآلية أو المسار الذي ينتقل عبره أثر المتغير المستقل إلى التابع.",
        "usage": "يُختبر عبر تحليل المسار (Path Analysis) أو Process Macro أو SmartPLS.",
        "spss": "Analyze > Regression > PROCESS (Andrew Hayes)"
    },
    {
        "ar": "المتغير المعدِّل",
        "fr": "Variable modératrice",
        "en": "Moderating Variable",
        "cat": "النمذجة المتقدمة",
        "def": "متغير يغير من قوة أو اتجاه العلاقة بين المتغير المستقل والمتغير التابع (مثل الجنس أو الخبرة).",
        "usage": "يُقاس عبر إدخال حد التفاعل (Interaction Term) في نموذج الانحدار أو النمذجة الهيكلية.",
        "spss": "Analyze > Regression > Linear (بعد توسيط المتغيرات وحساب حاصل الضرب)"
    },
    {
        "ar": "الانحراف المعياري",
        "fr": "Écart-type",
        "en": "Standard Deviation (SD)",
        "cat": "الإحصاء الوصفي",
        "def": "مقياس تشتت يوضح مدى تقارب أو تباعد استجابات أفراد العينة عن متوسطهم الحسابي.",
        "usage": "كلما صغرت قيمة SD دلّ ذلك على تجانس آراء المبحوثين واتفاقهم حول العبارة.",
        "spss": "Analyze > Descriptive Statistics > Descriptives"
    },
    {
        "ar": "التحليل العاملي الاستكشافي",
        "fr": "Analyse factorielle exploratoire",
        "en": "Exploratory Factor Analysis (EFA)",
        "cat": "القياس والسيكومترية",
        "def": "أسلوب إحصائي لاختزال عدد كبير من العبارات وتجميعها في أبعاد أو عوامل كامنة.",
        "usage": "يُستخدم للتحقق من الصدق البنائي للمقاييس الجديدة مع فحص مؤشر KMO واختبار بارتليت.",
        "spss": "Analyze > Dimension Reduction > Factor"
    },
    {
        "ar": "اللامعيارية (الأنومي)",
        "fr": "Anomie",
        "en": "Anomie",
        "cat": "المفاهيم السوسيولوجية",
        "def": "حالة من تفكك المعايير والقيم الاجتماعية وضعف الضبط الاجتماعي في فترات التحول السريع.",
        "usage": "مفهوم مركزي عند إميل دوركايم وروبرت ميرتون لتفسير الانحراف والجريمة والسلوك الانتحاري.",
        "spss": "يُقاس ميدانياً عبر مقاييس الاغتراب القيمي وضعف الامتثال المعياري"
    },
    {
        "ar": "المخالطة الفارقة",
        "fr": "Association différentielle",
        "en": "Differential Association",
        "cat": "المفاهيم السوسيولوجية",
        "def": "نظرية تفسر السلوك الإجرامي والانحرافي بوصفه سلوكاً متعلماً عبر التفاعل مع جماعات الرفاق.",
        "usage": "تُستخدم لتحليل أثر جماعة الأقران في اكتساب تقنيات الانحراف وتبريراته لدى الأحداث والشباب.",
        "spss": "يُقاس عبر مقاييس ضغط الرفاق والانتماء للجماعات غير المعيارية"
    }
]

# قاعدة بيانات المراجع الأكاديمية المصنفة والموثقة وفق APA 7th
BIBLIOGRAPHY_DB = [
    # 1. مراجع المنهجية ومناهج البحث العلمي
    {
        "field": "المنهجية ومناهج البحث العلمي",
        "title": "مناهج البحث العلمي وطرق إعداد البحوث",
        "apa": "بوحوش، عمار، والذنيبات، محمد محمود. (2019). مناهج البحث العلمي وطرق إعداد البحوث. ديوان المطبوعات الجامعية.",
        "note": "مرجع منهجي أساسي في الجامعات الجزائرية والعربية لبناء الإشكالية، الفرضيات، وتحديد العينات."
    },
    {
        "field": "المنهجية ومناهج البحث العلمي",
        "title": "مناهج البحث في العلوم الاجتماعية",
        "apa": "غرايبة، فوزي، وآخرون. (2015). أساليب البحث العلمي في العلوم الاجتماعية والإنسانية. دار وائل للنشر.",
        "note": "يتناول تصميم أدوات جمع البيانات الميدانية (الاستبيان، المقابلة، والملاحظة) وضبط الصدق والثبات."
    },
    {
        "field": "المنهجية ومناهج البحث العلمي",
        "title": "البحث الكيفي في العلوم الاجتماعية",
        "apa": "قباري، محمد إسماعيل. (2014). مناهج البحث في علم الاجتماع والأنثروبولوجيا. منشأة المعارف.",
        "note": "مرجع معمق في المنهج الوصفي، دراسة الحالة، وتحليل المضمون في الدراسات السوسيولوجية."
    },
    {
        "field": "المنهجية ومناهج البحث العلمي",
        "title": "Research Design: Qualitative, Quantitative, and Mixed Methods Approaches",
        "apa": "Creswell, J. W., & Creswell, J. D. (2023). Research design: Qualitative, quantitative, and mixed methods approaches (6th ed.). SAGE Publications.",
        "note": "المرجع الدولي الأول في هندسة البحوث الكمية والكيفية والمختلطة."
    },
    {
        "field": "المنهجية ومناهج البحث العلمي",
        "title": "Manuel de recherche en sciences sociales",
        "apa": "Van Campenhoudt, L., Marquet, J., & Quivy, R. (2022). Manuel de recherche en sciences sociales (6e éd.). Dunod.",
        "note": "المرجع الفرانكفوني الكلاسيكي لبناء الإشكالية السوسيولوجية والقطيعة الإبستمولوجية."
    },

    # 2. مراجع الإحصاء التطبيقي و SPSS
    {
        "field": "الإحصاء التطبيقي و SPSS",
        "title": "التحليل الإحصائي للبيانات باستخدام برنامج SPSS",
        "apa": "أبو علام، رجاء محمود. (2021). التحليل الإحصائي للبيانات باستخدام برنامج SPSS. دار النشر للجامعات.",
        "note": "يغطي الإحصاء الوصفي، الاختبارات المعلمية واللامعلمية، تحليل التباين، والانحدار خطوة بخطوة."
    },
    {
        "field": "الإحصاء التطبيقي و SPSS",
        "title": "الإحصاء التطبيقي في العلوم الاجتماعية والتربوية",
        "apa": "البياتي، عبد الجبار توفيق. (2016). الإحصاء وتطبيقاته في العلوم التربوية والنفسية والاجتماعية. دار الثقافة.",
        "note": "مرجع تطبيقي لشرح شروط استخدام الاختبارات الإحصائية وحساب حجم العينة وطول الفئة."
    },
    {
        "field": "الإحصاء التطبيقي و SPSS",
        "title": "التحليل الإحصائي المتقدم باستخدام SPSS و AMOS",
        "apa": "تيغزة، أمحمد بوزيان. (2012). التحليل العاملي الاستكشافي والتوكيدي: مفاهيمهما ومنهجيتهما بتوظيف حزمة SPSS وليزرل. دار المسيرة.",
        "note": "أفضل مرجع عربي لفهم الصدق البنائي والتحليل العاملي EFA و CFA."
    },
    {
        "field": "الإحصاء التطبيقي و SPSS",
        "title": "Discovering Statistics Using IBM SPSS Statistics",
        "apa": "Field, A. (2024). Discovering statistics using IBM SPSS statistics (6th ed.). SAGE Publications.",
        "note": "المرجع العالمي الأبرز لفهم المنطق الإحصائي وتفسير مخرجات SPSS بأسلوب تطبيقي."
    },
    {
        "field": "الإحصاء التطبيقي و SPSS",
        "title": "SPSS Survival Manual",
        "apa": "Pallant, J. (2020). SPSS survival manual: A step by step guide to data analysis using IBM SPSS (7th ed.). Open University Press.",
        "note": "دليل عملي سريع لتجهيز البيانات، فحص الثبات، وكتابة النتائج وفق معايير APA."
    },

    # 3. مراجع علم الاجتماع العام
    {
        "field": "علم الاجتماع العام",
        "title": "قواعد المنهج في علم الاجتماع",
        "apa": "دوركايم، إميل. (2014). قواعد المنهج في علم الاجتماع (ترجمة محمود قاسم). دار المعرفة الجامعية.",
        "note": "النص التأسيسي لدراسة الظواهر الاجتماعية بوصفها أشياء مستقلة وتفسير الاجتماعي بالاجتماعي."
    },
    {
        "field": "علم الاجتماع العام",
        "title": "الخيال السوسيولوجي",
        "apa": "ميلز، تشارلز رايت. (2017). الخيال السوسيولوجي (ترجمة عبد الباسط عبد المعطي). المركز القومي للترجمة.",
        "note": "مرجع جوهري للربط بين المشكلات الفردية والبنى الاجتماعية والتاريخية."
    },
    {
        "field": "علم الاجتماع العام",
        "title": "التمييز: نقد اجتماعي للحكم",
        "apa": "بورديو، بيير. (2016). الرمز والسلطة (ترجمة عبد السلام بنعبد العالي). دار توبقال للنشر.",
        "note": "مدخل لفهم مفاهيم الهابيتوس، الحقل، ورأس المال الثقافي والاجتماعي."
    },
    {
        "field": "علم الاجتماع العام",
        "title": "الاقتصاد والمجتمع",
        "apa": "فيبر، ماكس. (2015). مفاهيم أساسية في علم الاجتماع (ترجمة صلاح هلال). المركز القومي للترجمة.",
        "note": "تأسيس السوسيولوجيا الفهمية وتحليل الفعل الاجتماعي والعقلانية والبيروقراطية."
    },

    # 4. مراجع تخصص انحراف وجريمة
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "title": "علم اجتماع الانحراف والجريمة",
        "apa": "الوريكات، عايد عواد. (2017). نظريات علم الجريمة. دار الشروق للنشر والتوزيع.",
        "note": "عرض شامل للنظريات السوسيولوجية المفسرة للجريمة: المخالطة الفارقة، الضبط الاجتماعي، الوصم، والأنومي."
    },
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "title": "جنوح الأحداث والانحراف الاجتماعي",
        "apa": "رشوان، حسين عبد الحميد أحمد. (2015). الجريمة والانحراف: دراسة في علم الاجتماع الجنائي. المكتب الجامعي الحديث.",
        "note": "يتناول العوامل الأسرية، جماعة الرفاق، والبيئة المدرسية في تشكل السلوك الجانح لدى الأحداث."
    },
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "title": "الانتحار: دراسة في علم الاجتماع",
        "apa": "دوركايم، إميل. (2018). الانتحار: دراسة في علم الاجتماع (ترجمة حسن عودة). الهيئة العامة السورية للكتاب.",
        "note": "النموذج الكلاسيكي لتوظيف الإحصاء السوسيولوجي ونظرية اللامعيارية (Anomie) في تفسير الانحراف."
    },
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "title": "الضبط الاجتماعي والانحراف في المجتمع المعاصر",
        "apa": "عكاشة، محمد فتحي. (2016). علم الاجتماع الجنائي والانحراف. دار الوفاء لدنيا الطباعة والنشر.",
        "note": "دراسة في آليات الضبط الاجتماعي الرسمي وغير الرسمي وتأثير التغير القيمي والرقمي."
    },
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "title": "Outsiders: Studies in the Sociology of Deviance",
        "apa": "Becker, H. S. (2018). Outsiders: Studies in the sociology of deviance. Free Press.",
        "note": "المرجع التأسيسي لنظرية الوصم الاجتماعي (Labeling Theory) في سوسيولوجيا الانحراف."
    },
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "title": "Social Theory and Social Structure (Anomie & Strain)",
        "apa": "Merton, R. K. (1968). Social theory and social structure. Free Press.",
        "note": "يتضمن صياغة ميرتون لنظرية الضغط البنائي واللامعيارية وتكيفات الفرد مع الأهداف والوسائل."
    },
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "title": "Causes of Delinquency (Social Bond Theory)",
        "apa": "Hirschi, T. (2017). Causes of delinquency. Routledge.",
        "note": "المرجع الأساسي لنظرية الروابط الاجتماعية (التعلق، الالتزام، الانشغال، والمعتقد) في تفسير جنوح الأحداث."
    }
]


def render_library_page(theme_mode):
    st.markdown(
        f'<div class="sl-section" style="padding-top:28px; padding-bottom:10px;">'
        f'<a href="?view=home&theme={theme_mode}" target="_self" class="sl-back-link">&rarr; العودة الى الواجهة الرئيسية</a>'
        f'<div class="sl-sec-head" style="margin-bottom:20px;">'
        f'<span class="sl-sec-num">SOCIO LIBRARY • DIGITAL REPOSITORY</span>'
        f'<div class="sl-sec-title">المكتبة العلمية الرقمية والقاموس الإحصائي الثلاثي</div>'
        f'<p class="sl-sec-sub">ابحث في المصطلحات الإحصائية باللغات الثلاث، حمّل قوالب الجداول والأدلة الجاهزة، واستعرض المراجع الموثقة وفق APA 7.</p>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    _, lib_wrap, _ = st.columns([0.05, 0.90, 0.05])
    with lib_wrap:
        lib_tabs = st.tabs([
            "1. فهرس المراجع الأكاديمية المتخصصة (APA 7th)",
            "2. محرك البحث في القاموس الثلاثي (AR / FR / EN)",
            "3. مستودع القوالب والأدلة القابلة للتحميل"
        ])

        # التبويب 1: فهرس المراجع الأكاديمية المصنفة (المنهجية، الإحصاء/SPSS، علم الاجتماع، انحراف وجريمة)
        with lib_tabs[0]:
            f_col1, f_col2 = st.columns([0.45, 0.55])
            with f_col1:
                fields = [
                    "جميع التخصصات",
                    "سوسيولوجيا الانحراف والجريمة",
                    "المنهجية ومناهج البحث العلمي",
                    "الإحصاء التطبيقي و SPSS",
                    "علم الاجتماع العام"
                ]
                sel_field = st.selectbox("تصفية المراجع حسب التخصص العلمي:", fields)
            with f_col2:
                bib_search = st.text_input(
                    "ابحث باسم المؤلف أو عنوان المرجع أو النظرية:",
                    placeholder="مثال: دوركايم ، بوحوش ، سذرلاند ، جنوح ، SPSS..."
                ).strip().lower()

            matched_books = []
            for book in BIBLIOGRAPHY_DB:
                match_f = (sel_field == "جميع التخصصات") or (book["field"] == sel_field)
                match_s = (
                    not bib_search
                    or bib_search in book["title"].lower()
                    or bib_search in book["apa"].lower()
                    or bib_search in book["note"].lower()
                )
                if match_f and match_s:
                    matched_books.append(book)

            st.markdown(
                f'<div style="font-size:12.5px; color:var(--text-muted); margin-bottom:12px;">'
                f'عدد المراجع المعروضة: <strong>{len(matched_books)}</strong> مرجع أكاديمي موثق</div>',
                unsafe_allow_html=True,
            )

            # زر تحميل القائمة الببليوغرافية المعروضة كاملة بصيغة نصية جاهزة
            if matched_books:
                bib_export_lines = [
                    f"قائمة المراجع الأكاديمية ({sel_field}) - مكتبة Socio Lab",
                    "==========================================================",
                    ""
                ]
                for idx, b in enumerate(matched_books, start=1):
                    bib_export_lines.append(f"{idx}. {b['apa']}")
                st.download_button(
                    label=f"تحميل قائمة المراجع المعروضة بصيغة APA 7 (.txt)",
                    data="\n".join(bib_export_lines),
                    file_name="SocioLab_Bibliography_APA7.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
                st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

            for book in matched_books:
                is_en = book["apa"][0].isascii()
                dir_cls = "ltr-block" if is_en else "rtl"
                badge_color = "var(--mint-green)" if "انحراف" in book["field"] else (
                    "var(--sky-blue)" if "SPSS" in book["field"] else "var(--digital-indigo)"
                )
                book_html = (
                    f'<div class="sl-detail-box" style="padding:18px; margin-bottom:12px; border-right:4px solid {badge_color};">'
                    f'<span class="sl-sec-tag" style="margin-bottom:6px;">{book["field"]}</span>'
                    f'<div style="font-size:15.5px; font-weight:800; color:var(--text); margin-bottom:6px;">{book["title"]}</div>'
                    f'<div class="sl-result-banner" style="margin-top:6px;">'
                    f'<div style="font-size:11.5px; font-weight:700; color:var(--sky-blue); margin-bottom:3px;">التوثيق الجاهز للنسخ (APA 7th):</div>'
                    f'<div class="{dir_cls}" style="font-size:13.2px; font-weight:600;">{book["apa"]}</div>'
                    f'</div>'
                    f'<div style="font-size:12.2px; color:var(--text-muted); margin-top:8px;">• {book["note"]}</div>'
                    f'</div>'
                )
                st.markdown(book_html, unsafe_allow_html=True)

        # التبويب 2: القاموس الثلاثي التفاعلي
        with lib_tabs[1]:
            s_col1, s_col2 = st.columns([0.65, 0.35])
            with s_col1:
                search_q = st.text_input(
                    "ابحث عن مصطلح بالعربية أو الفرنسية أو الإنجليزية:",
                    placeholder="مثال: ألفا كرونباخ ، Anomie ، المخالطة الفارقة ، Normal..."
                ).strip().lower()
            with s_col2:
                cats = ["الكل"] + sorted(list({item["cat"] for item in DICTIONARY_DB}))
                sel_cat = st.selectbox("تصفية حسب المجال:", cats)

            filtered_terms = []
            for item in DICTIONARY_DB:
                match_cat = (sel_cat == "الكل") or (item["cat"] == sel_cat)
                match_txt = (
                    not search_q
                    or search_q in item["ar"].lower()
                    or search_q in item["fr"].lower()
                    or search_q in item["en"].lower()
                    or search_q in item["def"].lower()
                )
                if match_cat and match_txt:
                    filtered_terms.append(item)

            for term in filtered_terms:
                term_card = (
                    f'<div class="sl-detail-box" style="padding:18px; margin-bottom:14px; border-right:4px solid var(--sky-blue);">'
                    f'<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:8px;">'
                    f'<span style="font-size:16px; font-weight:800; color:var(--text);">{term["ar"]}</span>'
                    f'<span class="ltr" style="font-size:12.5px; font-weight:700; color:var(--sky-blue); background:var(--surface-soft); padding:3px 10px; border-radius:8px; border:1px solid var(--border);">'
                    f'{term["fr"]} &nbsp;|&nbsp; {term["en"]}</span>'
                    f'</div>'
                    f'<div style="font-size:13.2px; color:var(--text); margin-bottom:6px;"><strong>التعريف العلمي:</strong> {term["def"]}</div>'
                    f'<div style="font-size:12.8px; color:var(--text-muted); margin-bottom:6px;"><strong>الاستخدام والتفسير:</strong> {term["usage"]}</div>'
                    f'<div style="font-size:12px; color:var(--mint-green); font-weight:700;">'
                    f'المسار / القياس: <span class="ltr" style="font-family:monospace;">{term["spss"]}</span></div>'
                    f'</div>'
                )
                st.markdown(term_card, unsafe_allow_html=True)

        # التبويب 3: مستودع القوالب والأدلة الجاهزة
        with lib_tabs[2]:
            st.markdown(
                '<div style="font-size:15.5px; font-weight:800; color:var(--text); margin:10px 0 14px 0;">'
                'قوالب وأدلة منهجية وإحصائية جاهزة للتحميل الفوري:</div>',
                unsafe_allow_html=True,
            )

            t_c1, t_c2 = st.columns(2, gap="large")
            with t_c1:
                st.markdown(
                    '<div class="sl-detail-box" style="padding:18px;">'
                    '<div style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:6px;">'
                    '1. قالب تقرير التحليل الإحصائي وفق APA 7</div>'
                    '<p style="font-size:12.5px; color:var(--text-muted); line-height:1.65;">'
                    'هيكل نصي منظم لكتابة فصل عرض وتحليل نتائج الدراسة الميدانية وربطها بالفرضيات.</p>'
                    '</div>',
                    unsafe_allow_html=True,
                )
                apa_report_tpl = (
                    "نموذج هيكلة فصل عرض وتحليل البيانات الميدانية (وفق معايير APA 7) - Socio Lab\n"
                    "==============================================================================\n\n"
                    "أولاً: الخصائص السيكومترية لأداة الدراسة:\n"
                    "1. الصدق الظاهري (صدق المحكمين) والصدق البنائي (الاتساق الداخلي).\n"
                    "2. الثبات: بلغ معامل ألفا كرونباخ الكلي (0.XXX) وهو مؤشر مرتفع يعكس صلاحية الأداة.\n\n"
                    "ثانياً: وصف خصائص عينة الدراسة (المتغيرات السوسيو-ديمغرافية):\n"
                    "- جدول رقم (01): توزيع أفراد العينة حسب الجنس، السن، والمستوى التعليمي.\n\n"
                    "ثالثاً: اختبار فرضيات الدراسة ومناقشتها:\n"
                    "- عرض جدول الاختبار الإحصائي (بدون خطوط عمودية وفق APA 7).\n"
                    "- القراءة الإحصائية: قيمة المؤشر (r / t / F) ومستوى الدلالة (Sig).\n"
                    "- التفسير السوسيولوجي: ربط النتيجة بالإطار النظري والدراسات السابقة.\n"
                )
                st.download_button(
                    label="تحميل قالب تقرير التحليل الإحصائي (.txt)",
                    data=apa_report_tpl,
                    file_name="SocioLab_APA7_Report_Template.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

                st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

                st.markdown(
                    '<div class="sl-detail-box" style="padding:18px;">'
                    '<div style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:6px;">'
                    '2. قالب دليل الترميز لبرنامج SPSS (Codebook)</div>'
                    '<p style="font-size:12.5px; color:var(--text-muted); line-height:1.65;">'
                    'ملف CSV جاهز لتوثيق أسماء المتغيرات، رموز الإجابات، ومستويات القياس قبل التفريغ.</p>'
                    '</div>',
                    unsafe_allow_html=True,
                )
                codebook_tpl = (
                    "Variable_Name,Question_Text,Coding_Values,Measurement_Level\n"
                    "ID,رقم الاستمارة,1 to N,Nominal\n"
                    "Gender,الجنس,1=ذكر | 2=أنثى,Nominal\n"
                    "Age_Group,الفئة العمرية,1=أقل من 20 | 2=20-30 | 3=أكثر من 30,Ordinal\n"
                    "Axis1_Q1,العبارة الأولى من المحور الأول,1=معارض بشدة ... 5=موافق بشدة,Ordinal\n"
                )
                st.download_button(
                    label="تحميل قالب دليل الترميز Codebook (.csv)",
                    data=codebook_tpl,
                    file_name="SocioLab_Codebook_Template.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            with t_c2:
                st.markdown(
                    '<div class="sl-detail-box" style="padding:18px;">'
                    '<div style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:6px;">'
                    '3. الدليل العملي السريع لاختبارات SPSS</div>'
                    '<p style="font-size:12.5px; color:var(--text-muted); line-height:1.65;">'
                    'ملخص تنفيذي يوضح الاختبار المعلمي والبديل اللامعلمي لكل حالة بحثية ومساره في البرنامج.</p>'
                    '</div>',
                    unsafe_allow_html=True,
                )
                spss_cheat_sheet = (
                    "الدليل العملي السريع لاختيار الاختبارات الإحصائية في SPSS - Socio Lab\n"
                    "=====================================================================\n"
                    "1. العلاقة بين متغيرين:\n"
                    "   - بيانات كمية طبيعية -> Pearson Correlation\n"
                    "   - بيانات رتبية أو غير طبيعية -> Spearman's Rho\n\n"
                    "2. الفروق بين مجموعتين مستقلتين (مثل: ذكور / إناث):\n"
                    "   - بيانات طبيعية -> Independent-Samples T-Test\n"
                    "   - بيانات غير طبيعية -> Mann-Whitney U Test\n\n"
                    "3. الفروق بين 3 مجموعات فأكثر:\n"
                    "   - بيانات طبيعية -> One-Way ANOVA\n"
                    "   - بيانات غير طبيعية -> Kruskal-Wallis H Test\n\n"
                    "4. الفروق القبلية والبعدية لنفس العينة:\n"
                    "   - بيانات طبيعية -> Paired-Samples T-Test\n"
                    "   - بيانات غير طبيعية -> Wilcoxon Signed-Rank Test\n"
                )
                st.download_button(
                    label="تحميل الدليل العملي السريع لـ SPSS (.txt)",
                    data=spss_cheat_sheet,
                    file_name="SocioLab_SPSS_Quick_Guide.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

                st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

                st.markdown(
                    '<div class="sl-detail-box" style="padding:18px;">'
                    '<div style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:6px;">'
                    '4. ديباجة ميثاق السرية ومقدمة الاستبيان</div>'
                    '<p style="font-size:12.5px; color:var(--text-muted); line-height:1.65;">'
                    'صياغة أكاديمية جاهزة لوضعها في صدر الاستمارة الميدانية لطمأنة المبحوثين وضمان الصدق.</p>'
                    '</div>',
                    unsafe_allow_html=True,
                )
                ethics_intro = (
                    "بسم الله الرحمن الرحيم\n"
                    "استمارة بحث علمي - مقدمة للمبحوثين\n"
                    "===================================\n"
                    "تحية طيبة وبعد،\n"
                    "في إطار إنجاز دراسة علمية أكاديمية، نضع بين أيديكم هذه الاستمارة التي تهدف إلى جمع بيانات "
                    "ميدانية دقيقة حول موضوع الدراسة. نؤكد لكم أن جميع إجاباتكم ستظل سرية للغاية ولن تُستخدم "
                    "إلا لأغراض البحث العلمي البحت، ولا داعي لذكر الاسم أو أي بيانات كاشفة للهوية.\n"
                    "شاكرين لكم حسن تعاونكم ومساهمتكم في خدمة البحث العلمي.\n"
                )
                st.download_button(
                    label="تحميل ديباجة الاستبيان وميثاق السرية (.txt)",
                    data=ethics_intro,
                    file_name="SocioLab_Questionnaire_Intro.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
