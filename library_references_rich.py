import streamlit as st

RICH_REFERENCES_DB = [
    # --- 1. سوسيولوجيا الانحراف والجريمة ---
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "lang": "AR",
        "title": "الانتحار: دراسة في علم الاجتماع",
        "author_year": "دوركايم، إميل (2018)",
        "apa": "دوركايم، إميل. (2018). الانتحار: دراسة في علم الاجتماع (ترجمة حسن عودة). الهيئة العامة السورية للكتاب.",
        "benefit": "توظيف الإحصاء السوسيولوجي والاندماج/الضبط الاجتماعي ومفهوم اللامعيارية (Anomie) في تفسير الانحراف."
    },
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "lang": "AR",
        "title": "الجريمة والانحراف: دراسة في علم الاجتماع الجنائي",
        "author_year": "رشوان، حسين عبد الحميد أحمد (2015)",
        "apa": "رشوان، حسين عبد الحميد أحمد. (2015). الجريمة والانحراف: دراسة في علم الاجتماع الجنائي. المكتب الجامعي الحديث.",
        "benefit": "دراسة الأسرة، جماعة الرفاق، التنشئة، والبيئة الحضرية في جنوح الأحداث والانحراف الاجتماعي."
    },
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "lang": "AR",
        "title": "نظريات علم الجريمة والانحراف",
        "author_year": "الوريكات، عايد عواد (2017)",
        "apa": "الوريكات، عايد عواد. (2017). نظريات علم الجريمة. دار الشروق للنشر والتوزيع.",
        "benefit": "مقارنة بين المخالطة الفارقة، الضبط الاجتماعي، الوصم، والضغط البنائي."
    },
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "lang": "AR",
        "title": "علم الاجتماع الجنائي والانحراف",
        "author_year": "عكاشة، محمد فتحي (2016)",
        "apa": "عكاشة، محمد فتحي. (2016). علم الاجتماع الجنائي والانحراف. دار الوفاء لدنيا الطباعة والنشر.",
        "benefit": "تحليل آليات الضبط الاجتماعي الرسمي وغير الرسمي والظواهر الإجرامية المستحدثة."
    },
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "lang": "EN",
        "title": "Outsiders: Studies in the Sociology of Deviance",
        "author_year": "Becker, H. S. (2018)",
        "apa": "Becker, H. S. (2018). Outsiders: Studies in the sociology of deviance. Free Press.",
        "benefit": "المرجع التأسيسي لنظرية الوصم الاجتماعي (Labeling Theory) وكيفية تعريف السلوك المنحرف."
    },
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "lang": "EN",
        "title": "Causes of Delinquency",
        "author_year": "Hirschi, T. (2017)",
        "apa": "Hirschi, T. (2017). Causes of delinquency. Routledge.",
        "benefit": "نظرية الروابط الاجتماعية (التعلق، الالتزام، الانشغال، المعتقد) في فهم جنوح الأحداث."
    },
    {
        "field": "سوسيولوجيا الانحراف والجريمة",
        "lang": "EN",
        "title": "Social Theory and Social Structure",
        "author_year": "Merton, R. K. (1968)",
        "apa": "Merton, R. K. (1968). Social theory and social structure. Free Press.",
        "benefit": "صياغة الضغط البنائي واللامعيارية وأنماط التكيف الفردي مع الأهداف والوسائل المشروعة."
    },

    # --- 2. الإحصاء التطبيقي و SPSS ---
    {
        "field": "الإحصاء التطبيقي و SPSS",
        "lang": "AR",
        "title": "التحليل الإحصائي للبيانات باستخدام برنامج SPSS",
        "author_year": "أبو علام، رجاء محمود (2021)",
        "apa": "أبو علام، رجاء محمود. (2021). التحليل الإحصائي للبيانات باستخدام برنامج SPSS. دار النشر للجامعات.",
        "benefit": "تطبيق الاختبارات المعلمية واللامعلمية وتحليل التباين والارتباط والانحدار."
    },
    {
        "field": "الإحصاء التطبيقي و SPSS",
        "lang": "AR",
        "title": "الإحصاء وتطبيقاته في العلوم التربوية والنفسية والاجتماعية",
        "author_year": "البياتي، عبد الجبار توفيق (2016)",
        "apa": "البياتي، عبد الجبار توفيق. (2016). الإحصاء وتطبيقاته في العلوم التربوية والنفسية والاجتماعية. دار الثقافة.",
        "benefit": "حساب العينات، مقاييس النزعة والتشتت، وشروط اختيار الاختبارات الإحصائية."
    },
    {
        "field": "الإحصاء التطبيقي و SPSS",
        "lang": "AR",
        "title": "التحليل العاملي الاستكشافي والتوكيدي",
        "author_year": "تيغزة، أمحمد بوزيان (2012)",
        "apa": "تيغزة، أمحمد بوزيان. (2012). التحليل العاملي الاستكشافي والتوكيدي: مفاهيمهما ومنهجيتهما بتوظيف حزمة SPSS وليزرل. دار المسيرة.",
        "benefit": "فحص الصدق البنائي والتحليل العاملي الاستكشافي (EFA) والتوكيدي (CFA)."
    },
    {
        "field": "الإحصاء التطبيقي و SPSS",
        "lang": "EN",
        "title": "Discovering Statistics Using IBM SPSS Statistics",
        "author_year": "Field, A. (2024)",
        "apa": "Field, A. (2024). Discovering statistics using IBM SPSS statistics (6th ed.). SAGE Publications.",
        "benefit": "فهم المنطق الإحصائي، فحص الافتراضات، وقراءة مخرجات SPSS واختبارات الدلالة وحجم الأثر."
    },
    {
        "field": "الإحصاء التطبيقي و SPSS",
        "lang": "EN",
        "title": "SPSS Survival Manual",
        "author_year": "Pallant, J. (2020)",
        "apa": "Pallant, J. (2020). SPSS survival manual: A step by step guide to data analysis using IBM SPSS (7th ed.). Open University Press.",
        "benefit": "خطوات عملية لتجهيز البيانات، حساب الثبات، اختبار الفروق والارتباط، وتقديم النتائج."
    },
    {
        "field": "الإحصاء التطبيقي و SPSS",
        "lang": "EN",
        "title": "Using Multivariate Statistics",
        "author_year": "Tabachnick, B. G., & Fidell, L. S. (2019)",
        "apa": "Tabachnick, B. G., & Fidell, L. S. (2019). Using multivariate statistics (7th ed.). Pearson.",
        "benefit": "مرجع متقدم للانحدار المتعدد، التحليل العاملي، وتحليل التباين متعدد المتغيرات."
    },

    # --- 3. المنهجية ومناهج البحث العلمي ---
    {
        "field": "المنهجية ومناهج البحث العلمي",
        "lang": "AR",
        "title": "مناهج البحث العلمي وطرق إعداد البحوث",
        "author_year": "بوحوش، عمار، والذنيبات، محمد محمود (2019)",
        "apa": "بوحوش، عمار، والذنيبات، محمد محمود. (2019). مناهج البحث العلمي وطرق إعداد البحوث. ديوان المطبوعات الجامعية.",
        "benefit": "بناء الإشكالية، صياغة الفرضيات، اختيار المنهج والعينة، وتنظيم خطة البحث."
    },
    {
        "field": "المنهجية ومناهج البحث العلمي",
        "lang": "AR",
        "title": "أساليب البحث العلمي في العلوم الاجتماعية والإنسانية",
        "author_year": "غرايبة، فوزي، وآخرون (2015)",
        "apa": "غرايبة، فوزي، وآخرون. (2015). أساليب البحث العلمي في العلوم الاجتماعية والإنسانية. دار وائل للنشر.",
        "benefit": "تصميم الاستبيانات والمقابلات والملاحظة الميدانية وضبط الصدق والثبات."
    },
    {
        "field": "المنهجية ومناهج البحث العلمي",
        "lang": "AR",
        "title": "منهجية البحث الاجتماعي: أسسها وتقنياتها",
        "author_year": "عبيدات، ذوقان، وعدس، عبد الرحمن، وعبد الحق، كايد (2018)",
        "apa": "عبيدات، ذوقان، وعدس، عبد الرحمن، وعبد الحق، كايد. (2018). البحث العلمي: مفهومه، أدواته، وأساليبه. دار الفكر.",
        "benefit": "أساسيات المنهج الوصفي والمسحي والتجريبي وأدوات جمع البيانات."
    },
    {
        "field": "المنهجية ومناهج البحث العلمي",
        "lang": "EN",
        "title": "Research Design: Qualitative, Quantitative, and Mixed Methods Approaches",
        "author_year": "Creswell, J. W., & Creswell, J. D. (2023)",
        "apa": "Creswell, J. W., & Creswell, J. D. (2023). Research design: Qualitative, quantitative, and mixed methods approaches (6th ed.). SAGE Publications.",
        "benefit": "تصميم البحوث الكمية والكيفية والمختلطة والربط بين السؤال البحثي والمنهج."
    },
    {
        "field": "المنهجية ومناهج البحث العلمي",
        "lang": "FR",
        "title": "Manuel de recherche en sciences sociales",
        "author_year": "Van Campenhoudt, L., Marquet, J., & Quivy, R. (2022)",
        "apa": "Van Campenhoudt, L., Marquet, J., & Quivy, R. (2022). Manuel de recherche en sciences sociales (6e éd.). Dunod.",
        "benefit": "مراحل البحث السوسيولوجي: الإشكالية، البناء النظري، الملاحظة، وتحليل المعطيات."
    },

    # --- 4. علم الاجتماع العام والظواهر المعاصرة ---
    {
        "field": "علم الاجتماع العام والرقمية",
        "lang": "AR",
        "title": "قواعد المنهج في علم الاجتماع",
        "author_year": "دوركايم، إميل (2014)",
        "apa": "دوركايم، إميل. (2014). قواعد المنهج في علم الاجتماع (ترجمة محمود قاسم). دار المعرفة الجامعية.",
        "benefit": "تأسيس الموضوعية السوسيولوجية ومعالجة الظواهر الاجتماعية كحقائق مستقلة."
    },
    {
        "field": "علم الاجتماع العام والرقمية",
        "lang": "AR",
        "title": "الخيال السوسيولوجي",
        "author_year": "ميلز، تشارلز رايت (2017)",
        "apa": "ميلز، تشارلز رايت. (2017). الخيال السوسيولوجي (ترجمة عبد الباسط عبد المعطي). المركز القومي للترجمة.",
        "benefit": "الربط بين مشكلات الأفراد اليومية والبنى الاجتماعية والتاريخية الأوسع."
    },
    {
        "field": "علم الاجتماع العام والرقمية",
        "lang": "AR",
        "title": "مفاهيم أساسية في علم الاجتماع",
        "author_year": "فيبر، ماكس (2015)",
        "apa": "فيبر، ماكس. (2015). مفاهيم أساسية في علم الاجتماع (ترجمة صلاح هلال). المركز القومي للترجمة.",
        "benefit": "فهم الفعل الاجتماعي، التنظيم، العقلانية، والسلطة والشرعية."
    },
    {
        "field": "علم الاجتماع العام والرقمية",
        "lang": "AR",
        "title": "الرمز والسلطة (الهابيتوس والحقل)",
        "author_year": "بورديو، بيير (2016)",
        "apa": "بورديو، بيير. (2016). الرمز والسلطة (ترجمة عبد السلام بنعبد العالي). دار توبقال للنشر.",
        "benefit": "تحليل رأس المال الثقافي والاجتماعي والحقول الاجتماعية والممارسات الرمزية."
    },
    {
        "field": "علم الاجتماع العام والرقمية",
        "lang": "EN",
        "title": "The Rise of the Network Society",
        "author_year": "Castells, M. (2010)",
        "apa": "Castells, M. (2010). The rise of the network society (2nd ed.). Wiley-Blackwell.",
        "benefit": "فهم التحولات الرقمية، الشبكات الاجتماعية، والفجوة الرقمية في المجتمع المعاصر."
    }
]

QUICK_CATEGORIES = [
    "الكل",
    "سوسيولوجيا الانحراف والجريمة",
    "الإحصاء التطبيقي و SPSS",
    "المنهجية ومناهج البحث العلمي",
    "علم الاجتماع العام والرقمية",
]


def render_rich_references_library():
    if "rich_ref_cat" not in st.session_state:
        st.session_state.rich_ref_cat = "الكل"

    st.markdown(
        '<div class="sl-detail-box" style="border-top:4px solid var(--sky-blue); margin-top:10px;">'
        '<div style="font-size:17px; font-weight:800; color:var(--text); margin-bottom:6px;">'
        'الفهرس المرجعي الموسّع لعلم الاجتماع والإحصاء والمنهجية (<span class="ltr">APA 7</span>)</div>'
        '<p style="font-size:13px; color:var(--text-muted); margin-bottom:0;">'
        'اختر تخصصاً بنقرة واحدة أو ابحث باسم المؤلف أو العنوان أو النظرية للوصول السريع إلى التوثيق الجاهز.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # أزرار وصول سريع للتخصصات
    btn_cols = st.columns(len(QUICK_CATEGORIES))
    for idx, cat_name in enumerate(QUICK_CATEGORIES):
        with btn_cols[idx]:
            is_selected = st.session_state.rich_ref_cat == cat_name
            btn_type = "primary" if is_selected else "secondary"
            if st.button(cat_name, key=f"quick_cat_{idx}", type=btn_type, use_container_width=True):
                st.session_state.rich_ref_cat = cat_name
                st.rerun()

    f_left, f_right = st.columns([0.30, 0.70])
    with f_left:
        lang_filter = st.selectbox("اللغة:", ["الكل", "AR", "EN", "FR"], key="rich_ref_lang")
    with f_right:
        search_txt = st.text_input(
            "بحث فوري في المراجع:",
            placeholder="ابحث بمؤلف، كتاب، نظرية، أو أداة (مثال: دوركايم، الوصم، SPSS، كريسويل)...",
            key="rich_ref_search",
        ).strip().lower()

    active_cat = st.session_state.rich_ref_cat
    results = []
    for item in RICH_REFERENCES_DB:
        ok_cat = (active_cat == "الكل") or (item["field"] == active_cat)
        ok_lang = (lang_filter == "الكل") or (item["lang"] == lang_filter)
        ok_q = (
            not search_txt
            or search_txt in item["title"].lower()
            or search_txt in item["author_year"].lower()
            or search_txt in item["benefit"].lower()
            or search_txt in item["apa"].lower()
        )
        if ok_cat and ok_lang and ok_q:
            results.append(item)

    st.markdown(
        f'<div style="font-size:12.5px; color:var(--text-muted); margin:8px 0;">'
        f'عدد المراجع المتاحة وفق التصفية الحالية: <strong>{len(results)}</strong> مرجع</div>',
        unsafe_allow_html=True,
    )

    if results:
        txt_export = "\n".join([f"{i+1}. {r['apa']}" for i, r in enumerate(results)])
        st.download_button(
            label=f"تحميل المراجع الظاهرة ({len(results)}) بصيغة APA 7 (.txt)",
            data=txt_export,
            file_name="SocioLab_Rich_References_APA7.txt",
            mime="text/plain",
            use_container_width=True,
        )
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    for r in results:
        is_latin = r["apa"][0].isascii()
        dir_cls = "ltr-block" if is_latin else "rtl"
        accent = (
            "var(--mint-green)" if "انحراف" in r["field"]
            else ("var(--sky-blue)" if "SPSS" in r["field"] else "var(--digital-indigo)")
        )
        card = (
            f'<div class="sl-detail-box" style="padding:15px; margin-bottom:10px; border-right:4px solid {accent};">'
            f'<div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:5px;">'
            f'<span class="sl-sec-tag">{r["field"]} • {r["lang"]}</span>'
            f'<span style="font-size:12px; font-weight:700; color:var(--text-muted);">{r["author_year"]}</span>'
            f'</div>'
            f'<div style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:5px;">{r["title"]}</div>'
            f'<div style="font-size:12.6px; color:var(--text-muted); margin-bottom:7px;">• <strong>أهميته للباحث:</strong> {r["benefit"]}</div>'
            f'<div class="sl-result-banner" style="margin-top:4px; padding:10px 12px;">'
            f'<div class="{dir_cls}" style="font-size:12.8px; font-weight:600;">{r["apa"]}</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(card, unsafe_allow_html=True)

    if not results:
        st.info("لا توجد مراجع مطابقة للبحث الحالي؛ جرّبي اختيار «الكل» أو تقليل كلمات البحث.")
