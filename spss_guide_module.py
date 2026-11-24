import streamlit as st


def render_spss_output_lab():
    st.markdown(
        '<div class="sl-detail-box" style="border-top:4px solid var(--digital-indigo); margin-top:10px;">'
        '<div style="font-size:17px; font-weight:800; color:var(--text); margin-bottom:6px;">'
        'مختبر فحص الشروط وقراءة مخرجات <span class="ltr">SPSS</span> (<span class="ltr">Output &amp; Assumptions Lab</span>)</div>'
        '<p style="font-size:13px; color:var(--text-muted); margin-bottom:0;">'
        'أدخل القيم الظاهرة في جداول مخرجات برنامج SPSS للحصول على القرار الإحصائي، التوجيه المنهجي، وصياغة أكاديمية جاهزة وفق APA 7.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    spss_subtabs = st.tabs([
        "1. فحص الشروط (الطبيعية والتجانس)",
        "2. قارئ جدول الثبات (Cronbach's Alpha)",
        "3. مترجم جداول الفروق والارتباط والانحدار",
        "4. دليل حل مآزق البيانات الميدانية"
    ])

    # =================================================================
    # التبويب 1: فحص الشروط القبلية (Normality & Levene)
    # =================================================================
    with spss_subtabs[0]:
        c_norm, c_lev = st.columns(2, gap="large")

        with c_norm:
            st.markdown(
                '<div style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:8px;">'
                'أ. فحص التوزيع الطبيعي (<span class="ltr">Tests of Normality</span>)</div>',
                unsafe_allow_html=True,
            )
            n_sample = st.number_input("حجم العينة (N):", min_value=5, value=60, step=5, key="spss_n_norm")
            norm_sig = st.number_input("قيمة الدلالة (Sig.) في جدول Normality:", min_value=0.000, max_value=1.000, value=0.082, step=0.005, format="%.3f", key="spss_sig_norm")
            skew_val = st.number_input("معامل الالتواء (Skewness) إن وجد:", value=0.35, step=0.1, format="%.2f", key="spss_skew")

            rec_test_name = "Shapiro-Wilk" if n_sample < 50 else "Kolmogorov-Smirnov"
            if norm_sig > 0.05 or abs(skew_val) <= 1.0:
                norm_status = "البيانات تتبع التوزيع الطبيعي (معتدلة)"
                norm_action = "يمكنك استخدام الاختبارات المعلمية (Pearson, T-Test, ANOVA, Linear Regression) بثقة."
                norm_badge_color = "var(--mint-green)"
            else:
                norm_status = "البيانات لا تتبع التوزيع الطبيعي (ملتوية)"
                norm_action = "يُوصى بالانتقال إلى البدائل اللامعلمية (Spearman, Mann-Whitney U, Kruskal-Wallis H)."
                norm_badge_color = "var(--sky-blue)"

            st.markdown(
                f'<div class="sl-probe-result" style="border-right-color:{norm_badge_color};">'
                f'<div style="font-weight:800; color:var(--text); margin-bottom:5px;">• الاختبار المرجعي لحجم عينتك: <span class="ltr">{rec_test_name}</span></div>'
                f'<div style="font-weight:800; color:{norm_badge_color}; margin-bottom:5px;">• التشخيص: {norm_status}</div>'
                f'<div style="font-size:12.8px;">• <strong>التوجيه العملي:</strong> {norm_action}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with c_lev:
            st.markdown(
                '<div style="font-size:15px; font-weight:800; color:var(--text); margin-bottom:8px;">'
                'ب. قارئ اختبار ليفين لتجانس التباين (<span class="ltr">Levene\'s Test</span>)</div>',
                unsafe_allow_html=True,
            )
            lev_sig = st.number_input(
                "قيمة الدلالة (Sig.) في عمود Levene's Test:",
                min_value=0.000,
                max_value=1.000,
                value=0.240,
                step=0.010,
                format="%.3f",
                key="spss_lev_sig",
            )

            if lev_sig > 0.05:
                lev_row = "السطر الأول: Equal variances assumed (تجانس التباين متحقق)"
                lev_explain = "بما أن Sig أكبر من 0.05، فإن تباين المجموعتين متجانس؛ اقرأ قيمة t و Sig من السطر الأول."
            else:
                lev_row = "السطر الثاني: Equal variances not assumed (تجانس التباين غير متحقق)"
                lev_explain = "بما أن Sig أقل من أو تساوي 0.05، فقد اختل شرط التجانس؛ اقرأ قيمة t و Sig المعدّلة من السطر الثاني (Welch's t)."

            st.markdown(
                f'<div class="sl-probe-result">'
                f'<div style="font-weight:800; color:var(--sky-blue); margin-bottom:6px;">• السطر الواجب قراءته في جدول T-Test:</div>'
                f'<div style="font-weight:700; margin-bottom:6px;">{lev_row}</div>'
                f'<div style="font-size:12.8px;">• <strong>التفسير:</strong> {lev_explain}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # =================================================================
    # التبويب 2: قارئ جدول الثبات (Cronbach's Alpha)
    # =================================================================
    with spss_subtabs[1]:
        st.markdown(
            '<div style="font-size:15.5px; font-weight:800; color:var(--text); margin:10px 0;">'
            'مترجم جدول <span class="ltr">Reliability Statistics (Cronbach\'s Alpha)</span></div>',
            unsafe_allow_html=True,
        )
        r1, r2, r3 = st.columns(3)
        with r1:
            scale_label = st.text_input("اسم المقياس أو المحور:", value="مقياس السلوك الجانح", key="rel_scale_name")
        with r2:
            n_items = st.number_input("عدد العبارات (N of Items):", min_value=2, value=18, step=1, key="rel_items")
        with r3:
            alpha_input = st.number_input("قيمة Cronbach's Alpha:", min_value=0.000, max_value=1.000, value=0.864, step=0.005, format="%.3f", key="rel_alpha")

        if alpha_input >= 0.85:
            rel_level = "مرتفع جداً (ممتاز)"
            rel_advice = "الأداة تتمتع باتساق داخلي قوي جداً وصالحة للتطبيق الميداني دون الحاجة لحذف عبارات."
        elif alpha_input >= 0.70:
            rel_level = "جيد ومقبول إحصائياً"
            rel_advice = "الأداة مستوفية لشرط الثبات العلمي (≥ 0.70). يمكنك تفحص عمود (Alpha if Item Deleted) إذا رغبت في رفع القيمة أكثر."
        elif alpha_input >= 0.60:
            rel_level = "مقبول بصعوبة (حدّي)"
            rel_advice = "يُنصح بمراجعة جدول (Item-Total Statistics) وحذف العبارات ذات الارتباط الضعيف (< 0.30) أو التي يرتفع الثبات بحذفها."
        else:
            rel_level = "ضعيف (غير مستوفٍ لشرط الثبات)"
            rel_advice = "راجع الترميز العكسي للعبارات السالبة (Reverse Coding) وتأكد من عدم خلط أبعاد متناقضة في حساب واحد."

        apa_rel_text = (
            f"للتحقق من ثبات أداة الدراسة ({scale_label}) المكونة من ({n_items}) عبارة، تم حساب معامل الاتساق الداخلي "
            f"ألفا كرونباخ (Cronbach's Alpha)، حيث بلغت قيمته ({alpha_input:.3f})، وهو مؤشر ثبات {rel_level} يعكس صلاحية الأداة للقياس الميداني."
        )

        st.markdown(
            f'<div class="sl-probe-result">'
            f'<div style="font-size:15px; font-weight:800; color:var(--mint-green); margin-bottom:6px;">التقييم الإحصائي: {rel_level}</div>'
            f'<div style="margin-bottom:10px;"><strong>• التوجيه المنهجي:</strong> {rel_advice}</div>'
            f'<div class="sl-result-banner">'
            f'<div style="font-size:11.5px; font-weight:700; color:var(--sky-blue); margin-bottom:4px;">فقرة جاهزة للنسخ في فصل الإجراءات المنهجية (APA 7):</div>'
            f'<div style="font-size:13.2px; line-height:1.75;">"{apa_rel_text}"</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

    # =================================================================
    # التبويب 3: مترجم جداول الفروق والارتباط والانحدار
    # =================================================================
    with spss_subtabs[2]:
        st.markdown(
            '<div style="font-size:15.5px; font-weight:800; color:var(--text); margin:10px 0;">'
            'مترجم مخرجات اختبار الفرضيات (<span class="ltr">Hypothesis Output Translator</span>)</div>',
            unsafe_allow_html=True,
        )
        out_type = st.selectbox(
            "اختر الجدول الذي أمامك في شاشة مخرجات SPSS:",
            [
                "جدول الارتباط (Correlations: Pearson / Spearman)",
                "جدول الفروق بين مجموعتين (Independent-Samples T-Test)",
                "جدول تحليل التباين الأحادي (One-Way ANOVA)",
                "جداول الانحدار الخطي (Regression: Model Summary & Coefficients)"
            ],
            key="spss_out_type",
        )

        oc1, oc2, oc3 = st.columns(3)
        with oc1:
            stat_val = st.number_input("قيمة المؤشر الإحصائي (r / t / F / Beta):", value=0.542, step=0.010, format="%.3f", key="spss_stat_val")
        with oc2:
            sig_val = st.number_input("مستوى الدلالة (Sig. / p-value):", min_value=0.000, max_value=1.000, value=0.002, step=0.001, format="%.3f", key="spss_sig_val")
        with oc3:
            extra_val = st.number_input("قيمة إضافية (R² للانحدار أو df):", value=0.294, step=0.010, format="%.3f", key="spss_extra_val")

        is_sig = sig_val < 0.05
        sig_level_txt = "0.01" if sig_val < 0.01 else ("0.05" if sig_val < 0.05 else "غير دالة")

        if "الارتباط" in out_type:
            dir_txt = "طردية (موجبة)" if stat_val >= 0 else "عكسية (سالبة)"
            str_txt = "قوية" if abs(stat_val) >= 0.70 else ("متوسطة" if abs(stat_val) >= 0.40 else "ضعيفة")
            if is_sig:
                decision_txt = f"نرفض الفرضية الصفرية ونقبل الفرضية البديلة: توجد علاقة ارتباطية {dir_txt} و{str_txt} ذات دلالة إحصائية عند مستوى ({sig_level_txt})."
                apa_writeup = f"أظهرت نتائج معامل الارتباط وجود علاقة {dir_txt} {str_txt} ودالة إحصائياً بين متغيري الدراسة (r = {stat_val:.3f}, p = {sig_val:.3f})."
            else:
                decision_txt = "نقبل الفرضية الصفرية: لا توجد علاقة ارتباطية ذات دلالة إحصائية بين المتغيرين (Sig > 0.05)."
                apa_writeup = f"بينت النتائج عدم وجود علاقة ارتباطية ذات دلالة إحصائية بين المتغيرين (r = {stat_val:.3f}, p = {sig_val:.3f})."
            next_step_tip = "تأكد من فحص مخطط الانتشار (Scatterplot) للتأكد من عدم وجود قيم متطرفة تشوّه معامل الارتباط."

        elif "T-Test" in out_type:
            if is_sig:
                decision_txt = f"توجد فروق ذات دلالة إحصائية بين المجموعتين عند مستوى ({sig_level_txt})."
                apa_writeup = f"كشفت نتائج اختبار (ت) للعينات المستقلة عن وجود فروق ذات دلالة إحصائية بين المجموعتين (t = {stat_val:.3f}, p = {sig_val:.3f})، وتُحدد المجموعة الأعلى بالرجوع إلى عمود المتوسط الحسابي (Mean)."
            else:
                decision_txt = "لا توجد فروق ذات دلالة إحصائية بين المجموعتين (Sig > 0.05)."
                apa_writeup = f"أوضحت نتائج اختبار (ت) عدم وجود فروق ذات دلالة إحصائية تُعزى لمتغير التصنيف (t = {stat_val:.3f}, p = {sig_val:.3f})."
            next_step_tip = "اذكر في الجدول المتوسط الحسابي (M) والانحراف المعياري (SD) لكل مجموعة إلى جانب قيمة (t) ومستوى الدلالة."

        elif "ANOVA" in out_type:
            if is_sig:
                decision_txt = f"توجد فروق ذات دلالة إحصائية بين 3 مجموعات فأكثر عند مستوى ({sig_level_txt})."
                apa_writeup = f"أشارت نتائج تحليل التباين الأحادي إلى وجود فروق دالة إحصائياً بين المجموعات (F = {stat_val:.3f}, p = {sig_val:.3f})."
                next_step_tip = "مهم جداً: بما أن F دالة إحصائياً، انتقل فوراً إلى جدول المقارنات البعدية (Post-Hoc: Tukey أو Scheffé) لتحديد لصالح أي فئة تعود الفروق."
            else:
                decision_txt = "لا توجد فروق ذات دلالة إحصائية بين المجموعات (Sig > 0.05)."
                apa_writeup = f"أظهرت نتائج تحليل التباين الأحادي عدم وجود فروق ذات دلالة إحصائية بين المجموعات (F = {stat_val:.3f}, p = {sig_val:.3f})."
                next_step_tip = "بما أن قيمة F غير دالة، لا حاجة لقراءة أو عرض جداول المقارنات البعدية (Post-Hoc)."

        else:
            r2_pct = round(extra_val * 100, 1)
            if is_sig:
                decision_txt = f"يوجد أثر ذو دلالة إحصائية للمتغير المستقل في المتغير التابع عند مستوى ({sig_level_txt})، ويفسر النموذج ما نسبته ({r2_pct}%) من التباين."
                apa_writeup = f"كشفت نتائج الانحدار الخطي عن وجود أثر معنوي دال إحصائياً (Beta = {stat_val:.3f}, p = {sig_val:.3f})، حيث بلغ معامل التحديد (R² = {extra_val:.3f}) مما يعني أن المتغير المستقل يفسر {r2_pct}% من التغيرات الحاصلة في المتغير التابع."
            else:
                decision_txt = "لا يوجد أثر ذو دلالة إحصائية للمتغير المستقل في التنبؤ بالمتغير التابع (Sig > 0.05)."
                apa_writeup = f"أوضحت نتائج تحليل الانحدار عدم وجود أثر دال إحصائياً للمتغير المستقل في المتغير التابع (Beta = {stat_val:.3f}, p = {sig_val:.3f})."
            next_step_tip = "في الانحدار المتعدد، افحص عمود VIF للتأكد من أنه أقل من 5 (أو 10) لانتفاء مشكلة التعدد الخطي (Multicollinearity)."

        st.markdown(
            f'<div class="sl-probe-result">'
            f'<div style="font-weight:800; color:var(--sky-blue); margin-bottom:6px;">• القرار الإحصائي: {decision_txt}</div>'
            f'<div style="font-size:12.8px; margin-bottom:10px;">• <strong>خطوة التحقق المنهجي:</strong> {next_step_tip}</div>'
            f'<div class="sl-result-banner">'
            f'<div style="font-size:11.5px; font-weight:700; color:var(--mint-green); margin-bottom:4px;">صياغة أكاديمية جاهزة وفق APA 7:</div>'
            f'<div style="font-size:13.2px; line-height:1.75;">"{apa_writeup}"</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

    # =================================================================
    # التبويب 4: دليل حل مآزق البيانات الميدانية في SPSS
    # =================================================================
    with spss_subtabs[3]:
        pitfalls = [
            {
                "q": "1. مأزق العبارات السالبة (Reverse Coding)",
                "sol": "إذا تضمن الاستبيان عبارات معاكسة لاتجاه المقياس (مثل: 'أشعر بالرضا عن القوانين' مقابل 'أميل لمخالفة القوانين')، يجب عكس درجاتها قبل حساب ألفا كرونباخ أو المتوسط العام عبر: Transform > Recode into Different Variables (1->5, 2->4, 3->3, 4->2, 5->1)."
            },
            {
                "q": "2. مأزق القيم المفقودة (Missing Values)",
                "sol": "إذا كانت نسبة الفراغات في الاستمارة أقل من 5% وعشوائية، يمكن تعويضها بمتوسط السلسلة عبر: Transform > Replace Missing Values > Series Mean. أما إذا تجاوزت الفراغات 20% في استمارة واحدة، فيُفضّل استبعاد الاستمارة وتوثيق ذلك في وصف العينة."
            },
            {
                "q": "3. مأزق ظهور قيمة (Sig = .000) في جدول SPSS",
                "sol": "برنامج SPSS يقرب الأرقام إلى 3 خانات عشرية؛ لذلك لا نكتب في البحث (p = 0.000) أبداً لأن الاحتمال لا يساوي صفراً مطلقاً، بل نكتبها وفق معايير APA 7 بصيغة: (p < .001)."
            },
            {
                "q": "4. مأزق عدم دلالة الفرضية (Sig > 0.05)",
                "sol": "الفرضية غير الدالة ليست خطأً إحصائياً؛ بل تعني أن البيانات الميدانية لم تدعم وجود فرق أو علاقة. ناقشها سوسيولوجياً من خلال تجانس العينة، أو تدخل متغيرات ضابطة، أو خصوصية المجال المدروس."
            }
        ]
        for p_item in pitfalls:
            st.markdown(
                f'<div class="sl-deliv-item" style="padding:13px 16px;">'
                f'<div style="font-weight:800; color:var(--text); margin-bottom:4px;">{p_item["q"]}</div>'
                f'<div style="font-size:12.8px; color:var(--text-muted); line-height:1.7;">{p_item["sol"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
