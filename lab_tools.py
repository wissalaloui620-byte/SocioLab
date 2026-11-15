import math
import numpy as np
import pandas as pd
import streamlit as st


def render_lab_section():
    st.markdown(
        '<div class="sl-page-head">'
        '<div class="sl-tag">المختبر المنهجي والاحصائي الرقمي</div>'
        '<h1 class="sl-title">ادوات البحث والتحليل الاحصائي التفاعلية</h1>'
        '<p class="sl-sub">ادوات علمية عملية مصممة لدعم الباحثين في بناء الادوات، '
        'اختيار الاختبارات المناسبة، وحساب المؤشرات الاحصائية بدقة مع توضيح شروط الاستخدام.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "1. الحاسبات الاحصائية الفعلية (بيانات حقيقية)",
        "2. مسبار الفرضيات ومشخص SPSS",
        "3. ادوات التصميم والميدان (التأسيس)",
        "4. التوثيق الاكاديمي (APA 7) والادلة المنهجية"
    ])

    with tab1:
        c1, c2 = st.columns(2, gap="large")

        with c1:
            st.markdown("### حاسبة معامل الثبات (الفا كرونباخ) والاحصاء الوصفي")
            st.info(
                "شروط الاستخدام: يتطلب حساب الفا كرونباخ مصفوفة بيانات رقمية "
                "(صفوف تمثل المبحوثين واعمدة تمثل فقرات المقياس) لعدد لا يقل عن 3 فقرات."
            )
            uploaded_file = st.file_uploader(
                "ارفع ملف بيانات رقمية بصيغة CSV لحساب الثبات والوصف فورا:",
                type=["csv"]
            )
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    num_df = df.select_dtypes(include=[np.number]).dropna()
                    k = num_df.shape[1]
                    n_cases = num_df.shape[0]
                    if k >= 2 and n_cases >= 2:
                        item_vars = num_df.var(axis=0, ddof=1)
                        total_var = num_df.sum(axis=1).var(ddof=1)
                        alpha = (k / (k - 1)) * (1 - (item_vars.sum() / total_var))
                        mean_val = num_df.mean().mean()
                        std_val = num_df.stack().std(ddof=1)

                        st.success(f"تم تحليل {n_cases} حالة و {k} متغيرات رقمية بنجاح:")
                        m1, m2, m3 = st.columns(3)
                        m1.metric("الفا كرونباخ", f"{alpha:.3f}")
                        m2.metric("المتوسط العام", f"{mean_val:.2f}")
                        m3.metric("الانحراف المعياري", f"{std_val:.2f}")
                        st.caption(
                            "حدود التفسير: القيمة >= 0.70 تشير الى ثبات مقبول في العلوم الاجتماعية. "
                            "لا يعوض الثبات المرتفع عن الصدق البنائي للاداة."
                        )
                    else:
                        st.warning("يجب ان يحتوي الملف على عمودين رقميين وحالتين على الاقل.")
                except Exception as exc:
                    st.error(f"تعذر قراءة الملف: {exc}")

            st.markdown("---")
            st.markdown("#### حاسبة سريعة للمتوسط الحسابي والانحراف المعياري")
            raw_nums = st.text_input(
                "ادخل قيما رقمية مفصولة بفاصلة لحساب مؤشراتها:",
                placeholder="مثال: 12, 15, 14, 18, 16, 13"
            )
            if raw_nums:
                try:
                    vals = [float(x.strip()) for x in raw_nums.split(",") if x.strip()]
                    if len(vals) >= 2:
                        arr = np.array(vals)
                        st.markdown(
                            f'<div class="sl-info-box">'
                            f'<strong>عدد القيم (N):</strong> {len(vals)} | '
                            f'<strong>المتوسط الحسابي:</strong> {np.mean(arr):.3f} | '
                            f'<strong>الانحراف المعياري:</strong> {np.std(arr, ddof=1):.3f}'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                except ValueError:
                    st.warning("يرجى ادخال ارقام صحيحة او عشرية مفصولة بفاصلة فقط.")

        with c2:
            st.markdown("### حاسبة حجم العينة الممثلة (معادلة كوكران)")
            st.info(
                "شروط الاستخدام: تطبق هذه المعادلة في حالة المعاينة العشوائية الاحتمالية "
                "عندما يكون حجم مجتمع البحث معلوما ومحددا."
            )
            pop_size = st.number_input("حجم مجتمع الدراسة الكلي (N):", min_value=10, value=500, step=10)
            margin_opts = [
                "5% (مستوى ثقة 95% - القياسي في العلوم الاجتماعية)",
                "1% (مستوى ثقة 99% - دقة عالية جدا)",
                "10% (مستوى ثقة 90% - للدراسات الاستطلاعية)",
            ]
            margin_label = st.selectbox("هامش الخطا المسموح به:", margin_opts)

            e = 0.05 if "5%" in margin_label else (0.01 if "1%" in margin_label else 0.10)
            z = 1.96 if e == 0.05 else (2.576 if e == 0.01 else 1.645)
            n0 = (z**2 * 0.25) / (e**2)
            sample_n = math.ceil(n0 / (1 + ((n0 - 1) / pop_size)))

            st.markdown(
                f'<div class="sl-info-box">'
                f'<strong>الحد الادنى لحجم العينة الممثلة (n):</strong> '
                f'<span style="font-size:18px; font-weight:800; color:#06182C;">{sample_n} مفردة</span><br>'
                f'<span style="font-size:12px; color:#475569;">حدود التحليل: في العينات القصدية او كرة الثلج '
                f'لا يعتمد على الحجم الاحصائي بل على التشبع النظري.</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with tab2:
        st.markdown("### مسبار الفرضيات وصياغة التساؤلات البحثية")
        pc1, pc2, pc3 = st.columns(3)
        with pc1:
            indep_var = st.text_input("المتغير المستقل (X):", placeholder="مثال: جماعة الرفاق")
        with pc2:
            dep_var = st.text_input("المتغير التابع (Y):", placeholder="مثال: السلوك الجانح")
        with pc3:
            study_sample = st.text_input("عينة الدراسة:", placeholder="مثال: تلاميذ الطور الثانوي")

        if indep_var and dep_var:
            s_txt = f"لدى ({study_sample})" if study_sample else "لدى عينة الدراسة"
            st.markdown(
                f'<div class="sl-info-box">'
                f'<strong>• التساؤل الرئيسي:</strong> هل توجد علاقة ذات دلالة احصائية بين <strong>{indep_var}</strong> و<strong>{dep_var}</strong> {s_txt}؟<br>'
                f'<strong>• الفرضية الصفرية (<span class="ltr">H0</span>):</strong> لا توجد علاقة ارتباطية او اثر دال احصائيا عند مستوى (0.05) بين <strong>{indep_var}</strong> و<strong>{dep_var}</strong> {s_txt}.<br>'
                f'<strong>• الفرضية البديلة (<span class="ltr">H1</span>):</strong> توجد علاقة ارتباطية او اثر دال احصائيا عند مستوى (0.05) بين <strong>{indep_var}</strong> و<strong>{dep_var}</strong> {s_txt}.'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown("### مشخص الاختبار الاحصائي المناسب في SPSS")
        goal_opts = [
            "قياس العلاقة الارتباطية بين متغيرين",
            "قياس الفروق بين مجموعتين مستقلتين",
            "قياس الفروق بين 3 مجموعات فاكثر",
            "قياس اثر متغير مستقل على متغير تابع",
        ]
        dist_opts = [
            "بيانات كمية تتبع التوزيع الطبيعي (اختبارات معلمية)",
            "بيانات رتبية او لا تتبع التوزيع الطبيعي (اختبارات لامعلمية)",
        ]
        sc1, sc2 = st.columns(2)
        with sc1:
            goal = st.selectbox("هدف الفرضية:", goal_opts)
        with sc2:
            dist = st.selectbox("طبيعة التوزيع ومستوى القياس:", dist_opts)

        is_normal = "معلمية" in dist
        if "العلاقة" in goal:
            t_name = "معامل ارتباط بيرسون (Pearson)" if is_normal else "معامل ارتباط سبيرمان (Spearman)"
            t_path = "Analyze > Correlate > Bivariate > Pearson" if is_normal else "Analyze > Correlate > Bivariate > Spearman"
            cond = "يشترط خطية العلاقة وتوزيعا طبيعيا للمتغيرين في حالة بيرسون."
        elif "مجموعتين" in goal:
            t_name = "اختبار ت لعينتين مستقلتين (T-Test)" if is_normal else "اختبار مان-ويتني (Mann-Whitney U)"
            t_path = "Analyze > Compare Means > Independent-Samples T Test" if is_normal else "Analyze > Nonparametric Tests > Independent Samples"
            cond = "يشترط تجانس التباين (اختبار Levene) واستقلالية العينتين."
        elif "3 مجموعات" in goal:
            t_name = "تحليل التباين الاحادي (One-Way ANOVA)" if is_normal else "اختبار كروسكال-واليس (Kruskal-Wallis)"
            t_path = "Analyze > Compare Means > One-Way ANOVA" if is_normal else "Analyze > Nonparametric Tests > K Independent Samples"
            cond = "يتطلب اختبارات المقارنات البعدية (Post-Hoc) عند وجود فروق دالة."
        else:
            t_name = "الانحدار الخطي (Linear Regression)" if is_normal else "الانحدار اللوجستي او الترتيبي"
            t_path = "Analyze > Regression > Linear" if is_normal else "Analyze > Regression > Ordinal"
            cond = "يشترط عدم وجود تعدد خطي مرتفع بين المتغيرات المستقلة."

        st.markdown(
            f'<div class="sl-info-box">'
            f'<strong>الاختبار المقترح:</strong> {t_name}<br>'
            f'<strong>المسار في البرنامج:</strong> <span class="ltr">{t_path}</span><br>'
            f'<strong>شروط التطبيق:</strong> {cond}'
            f'</div>',
            unsafe_allow_html=True,
        )

    with tab3:
        fc1, fc2 = st.columns(2, gap="large")
        with fc1:
            st.markdown("### دليل المفاهيم والمصطلحات المنهجية")
            glossary_dict = {
                "مجتمع البحث والعينة": "مجتمع البحث هو جميع مفردات الظاهرة المدروسة، والعينة هي الجزء الممثل الذي نختاره وفق قواعد علمية.",
                "المتغير المستقل والتابع": "المستقل هو العامل المؤثر او السبب، والتابع هو الظاهرة المتأثرة التي نقيس تغيرها.",
                "المتغير الوسيط (Mediator)": "متغير يفسر الآلية التي ينتقل بها الاثر من المتغير المستقل الى التابع.",
                "المنهج الكمي والمنهج الكيفي": "الكمي يعتمد القياس الرقمي والاستمارة لتعميم النتائج، والكيفي يعتمد المقابلة والملاحظة لفهم المعاني والدوافع.",
                "الصدق والثبات": "الصدق هو قياس الاداة لما وضعت له فعلا، والثبات هو استقرار نتائجها عند اعادة التطبيق.",
            }
            term = st.selectbox("اختر المفهوم المنهجي:", list(glossary_dict.keys()))
            st.markdown(f'<div class="sl-info-box">{glossary_dict[term]}</div>', unsafe_allow_html=True)

            st.markdown("### تقدير الزمن الميداني لجمع البيانات")
            fw_sample = st.number_input("عدد الاستمارات او المقابلات:", min_value=5, value=60, step=5)
            fw_q = st.number_input("عدد الاسئلة او المحاور:", min_value=5, value=25, step=5)
            mins_form = round(5 + (fw_q * 0.4))
            est_days = math.ceil((fw_sample * mins_form) / 180)
            st.markdown(
                f'<div class="sl-info-box">الزمن التقديري للمفردة: <strong>{mins_form} دقيقة</strong> | '
                f'المدة المقترحة لانجاز العمل الميداني: <strong>{est_days} ايام</strong>.</div>',
                unsafe_allow_html=True,
            )

        with fc2:
            st.markdown("### قائمة التحقق المنهجي لجودة الاستمارة")
            q1 = st.checkbox("خلو الاسئلة من الازدواجية (كل سؤال يقيس فكرة واحدة).", value=True)
            q2 = st.checkbox("حياد الصياغة وعدم الايحاء للمبحوث باجابة محددة.", value=True)
            q3 = st.checkbox("تضمين فقرة اخلاقية تؤكد سرية البيانات لاغراض البحث العلمي.", value=True)
            q4 = st.checkbox("تطابق سلم الاجابة (ليكرت) مع صياغة العبارات.", value=True)
            q5 = st.checkbox("تغطية كافة مؤشرات الفرضيات والابعاد النظرية.", value=False)
            q6 = st.checkbox("اخضاع الاداة للتحكيم العلمي والدراسة الاستطلاعية.", value=False)
            sc = sum([q1, q2, q3, q4, q5, q6])
            st.markdown(
                f'<div class="sl-info-box"><strong>مؤشر الجاهزية المنهجية للاداة:</strong> {sc} من 6 معايير مستوفاة.</div>',
                unsafe_allow_html=True,
            )

    with tab4:
        st.markdown("### مولد التوثيق العلمي وفق الاصدار السابع (APA 7th Edition)")
        rc1, rc2 = st.columns(2)
        with rc1:
            ref_type = st.selectbox("نوع المصدر:", ["كتاب اكاديمي", "مقال في مجلة محكمة", "رسالة ماستر / اطروحة دكتوراه"])
            ref_author = st.text_input("المؤلف (عربي او اجنبي):", placeholder="مثال: العلوي، وصال / Bourdieu, P.")
            ref_year = st.text_input("سنة النشر:", placeholder="2026")
        with rc2:
            ref_title = st.text_input("عنوان العمل:", placeholder="عنوان الكتاب او المقال")
            ref_source = st.text_input("دار النشر / المجلة والعدد / الجامعة:", placeholder="بيانات النشر")

        if ref_author and ref_year and ref_title:
            is_latin = ref_author.strip()[0].isascii()
            dir_cls = "ltr-block" if is_latin else "rtl"
            sep = ", " if is_latin else "، "
            if ref_type == "كتاب اكاديمي":
                out_ref = f"{ref_author} ({ref_year}). <em>{ref_title}</em>. {ref_source}."
            elif ref_type == "مقال في مجلة محكمة":
                out_ref = f"{ref_author} ({ref_year}). {ref_title}. <em>{ref_source}</em>."
            else:
                lbl = "[Unpublished thesis]" if is_latin else "[رسالة غير منشورة]"
                out_ref = f"{ref_author} ({ref_year}). <em>{ref_title}</em> {lbl}. {ref_source}."

            in_txt = f"({ref_author.split(',')[0].split('،')[0]}{sep}{ref_year})"
            st.markdown(
                f'<div class="sl-info-box">'
                f'<strong>التوثيق في المتن:</strong> <span class="{"ltr" if is_latin else "rtl"}">{in_txt}</span><br>'
                f'<strong>في قائمة المراجع:</strong><div class="{dir_cls}" style="margin-top:4px;">{out_ref}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
