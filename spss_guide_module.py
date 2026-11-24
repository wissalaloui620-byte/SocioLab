import math
import streamlit as st


def _build_likert_intervals(scale_choice: str):
    if "الثلاثي" in scale_choice:
        min_v, max_v, k = 1.0, 3.0, 3
        labels = ["منخفض", "متوسط", "مرتفع"]
    elif "السباعي" in scale_choice:
        min_v, max_v, k = 1.0, 7.0, 7
        labels = [
            "منخفض جداً",
            "منخفض",
            "منخفض نسبياً",
            "متوسط",
            "مرتفع نسبياً",
            "مرتفع",
            "مرتفع جداً",
        ]
    else:
        min_v, max_v, k = 1.0, 5.0, 5
        labels = ["منخفض جداً", "منخفض", "متوسط", "مرتفع", "مرتفع جداً"]

    interval_len = (max_v - min_v) / k
    rows = []
    for idx, lbl in enumerate(labels):
        low = min_v + idx * interval_len
        high = max_v if idx == k - 1 else (low + interval_len - 0.01)
        rows.append({
            "المستوى / الوصف": lbl,
            "الحد الأدنى": round(low, 2),
            "الحد الأعلى": round(high, 2),
            "المدى": f"{low:.2f} – {high:.2f}",
        })
    return interval_len, rows


def _classify_mean(mean_val: float, rows: list, min_v: float, max_v: float) -> str:
    if mean_val < min_v or mean_val > max_v:
        return "خارج حدود المقياس المختار — يرجى التحقق من قيمة المتوسط أو نوع المقياس."
    for idx, r in enumerate(rows):
        low = r["الحد الأدنى"]
        high = max_v if idx == len(rows) - 1 else (r["الحد الأعلى"] + 0.009)
        if low <= mean_val <= high:
            return f"يقع المتوسط ({mean_val:.2f}) ضمن فئة: «{r['المستوى / الوصف']}» (المدى: {r['المدى']})."
    return rows[-1]["المستوى / الوصف"]


def _estimate_corr_reg_sample(mode_choice: str, effect_choice: str, num_predictors: int) -> tuple[int, str]:
    # تقدير تقريبي وفق قوة إحصائية 0.80 ومستوى دلالة alpha = 0.05
    if "الارتباط" in mode_choice:
        r_map = {
            "أثر صغير (r ≈ 0.10)": 0.10,
            "أثر متوسط (r ≈ 0.30)": 0.30,
            "أثر كبير (r ≈ 0.50)": 0.50,
        }
        r_val = r_map[effect_choice]
        # تقريب شائع: N ≈ ((z_alpha + z_beta) / z_r)^2 + 3 حيث z_alpha=1.96, z_beta=0.842
        z_r = 0.5 * math.log((1 + r_val) / (1 - r_val))
        n_est = math.ceil(((1.96 + 0.842) / z_r) ** 2 + 3)
        formula_note = f"تقدير أولي لعلاقة ارتباطية بحجم أثر ({r_val:.2f}) عند قوة إحصائية 0.80 ومستوى دلالة 0.05."
        return max(n_est, 15), formula_note

    # الانحدار الخطي / المتعدد (قاعدة عملية شائعة: 50 + 8*k للانحدار العام، أو 10-15 حالة لكل متنبئ)
    f2_map = {
        "أثر صغير (f² ≈ 0.02)": 0.02,
        "أثر متوسط (f² ≈ 0.15)": 0.15,
        "أثر كبير (f² ≈ 0.35)": 0.35,
    }
    f2_val = f2_map[effect_choice]
    # قاعدة Green للانحدار المتعدد: max(50 + 8*k, 104 + k)
    n_green = max(50 + 8 * num_predictors, 104 + num_predictors)
    factor = 1.35 if f2_val <= 0.02 else (1.0 if f2_val <= 0.15 else 0.72)
    n_est = math.ceil(n_green * factor)
    formula_note = (
        f"تقدير أولي لنموذج انحدار يضم ({num_predictors}) متغير(ات) مستقلة وحجم أثر ({f2_val:.2f}) "
        f"باستخدام معيار Green والحد الأدنى المنهجي للانحدار."
    )
    return max(n_est, 30), formula_note


def render_spss_output_lab():
    st.markdown(
        '<div class="sl-detail-box" style="border-top:4px solid var(--digital-indigo); margin-top:10px;">'
        '<div style="font-size:17px; font-weight:800; color:var(--text); margin-bottom:6px;">'
        'مختبر فحص الشروط وقراءة مخرجات <span class="ltr">SPSS</span> (<span class="ltr">Output &amp; Assumptions Lab</span>)</div>'
        '<p style="font-size:13px; color:var(--text-muted); margin-bottom:0;">'
        'أدخل القيم الظاهرة في جداول مخرجات برنامج SPSS للحصول على القرار الإحصائي، التوجيه المنهجي، طول الفئة، مصفوفة الاختبارات، وقائمة المراجعة قبل التسليم.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    spss_subtabs = st.tabs([
        "1. فحص الشروط (الطبيعية والتجانس)",
        "2. قارئ جدول الثبات (Cronbach's Alpha)",
        "3. مترجم جداول الفروق والارتباط والانحدار",
        "4. حاسبة طول الفئة لمقياس ليكرت",
        "5. مصفوفة المعلمي واللامعلمي",
        "6. عينة الارتباط والانحدار",
        "7. قائمة مراجعة ما قبل التسليم"
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
    # التبويب 4: حاسبة طول الفئة لمقياس ليكرت (الثلاثي، الخماسي، السباعي)
    # =================================================================
    with spss_subtabs[3]:
        st.markdown(
            '<div style="font-size:15.5px; font-weight:800; color:var(--text); margin:10px 0;">'
            'حاسبة طول الفئة لمقاييس ليكرت (<span class="ltr">Likert Scale Interval Calculator</span>)</div>',
            unsafe_allow_html=True,
        )
        lk1, lk2 = st.columns(2, gap="large")
        with lk1:
            likert_scale = st.selectbox(
                "اختر نوع مقياس ليكرت:",
                [
                    "مقياس ليكرت الخماسي (1 إلى 5)",
                    "مقياس ليكرت الثلاثي (1 إلى 3)",
                    "مقياس ليكرت السباعي (1 إلى 7)"
                ],
                key="likert_scale_choice",
            )
        with lk2:
            observed_mean = st.number_input(
                "أدخل قيمة المتوسط الحسابي (Mean) من SPSS لتصنيفها:",
                min_value=0.00,
                max_value=10.00,
                value=3.84,
                step=0.01,
                format="%.2f",
                key="likert_mean_val",
            )

        interval_len, interval_rows = _build_likert_intervals(likert_scale)
        min_bound = 1.0
        max_bound = 3.0 if "الثلاثي" in likert_scale else (7.0 if "السباعي" in likert_scale else 5.0)
        mean_msg = _classify_mean(observed_mean, interval_rows, min_bound, max_bound)

        st.markdown(
            f'<div class="sl-probe-result">'
            f'<div style="font-weight:800; color:var(--sky-blue); margin-bottom:6px;">'
            f'• طول الفئة المحسوب: <span class="ltr">{interval_len:.2f}</span> درجة '
            f'(المدى الكلي {max_bound - min_bound:.0f} ÷ {len(interval_rows)} فئات)</div>'
            f'<div style="font-weight:800; color:var(--mint-green);">• تصنيف المتوسط المدخل: {mean_msg}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.dataframe(interval_rows, use_container_width=True, hide_index=True)

    # =================================================================
    # التبويب 5: مقارن الاختبارات المعلمية واللامعلمية
    # =================================================================
    with spss_subtabs[4]:
        st.markdown(
            '<div style="font-size:15.5px; font-weight:800; color:var(--text); margin:10px 0;">'
            'مصفوفة المقارنة السريعة: الاختبارات المعلمية واللامعلمية (<span class="ltr">Parametric vs. Non-Parametric</span>)</div>',
            unsafe_allow_html=True,
        )
        matrix_rows = [
            {
                "الهدف البحثي": "الارتباط بين متغيرين",
                "الاختبار المعلمي": "Pearson Correlation (r)",
                "البديل اللامعلمي": "Spearman's Rho (ρ)",
                "الشروط الأساسية": "المعلمي: متغيران كميان متصلان + توزيع طبيعي وخطية. اللامعلمي: بيانات رتبية أو غير طبيعية."
            },
            {
                "الهدف البحثي": "الفروق بين مجموعتين مستقلتين",
                "الاختبار المعلمي": "Independent-Samples T-Test (t)",
                "البديل اللامعلمي": "Mann-Whitney U Test (U)",
                "الشروط الأساسية": "المعلمي: متغير تابع كمي + توزيع طبيعي وتجانس تباين. اللامعلمي: رتبي أو تباين/توزيع غير متحقق."
            },
            {
                "الهدف البحثي": "الفروق بين 3 مجموعات فأكثر",
                "الاختبار المعلمي": "One-Way ANOVA (F)",
                "البديل اللامعلمي": "Kruskal-Wallis H Test (H)",
                "الشروط الأساسية": "المعلمي: متغير تابع كمي + توزيع طبيعي وتجانس تباين. اللامعلمي: مجموعات مستقلة ببيانات رتبية/ملتوية."
            },
            {
                "الهدف البحثي": "الفروق القبلية والبعدية (نفس العينة)",
                "الاختبار المعلمي": "Paired-Samples T-Test (t)",
                "البديل اللامعلمي": "Wilcoxon Signed-Rank Test (Z)",
                "الشروط الأساسية": "المعلمي: قياسان مرتبطان لنفس العينة + الفروق تتبع التوزيع الطبيعي. اللامعلمي: بيانات رتبية أو غير طبيعية."
            },
            {
                "الهدف البحثي": "العلاقة بين متغيرين فئويين (اسمي)",
                "الاختبار المعلمي": "Chi-Square Test of Independence (χ²)",
                "البديل اللامعلمي": "Fisher's Exact Test (للجداول الصغيرة)",
                "الشروط الأساسية": "بيانات اسمية/فئوية؛ يُراعى أن لا يقل التكرار المتوقع عن 5 في أكثر من 20% من الخلايا."
            }
        ]
        st.dataframe(matrix_rows, use_container_width=True, hide_index=True)

    # =================================================================
    # التبويب 6: حاسبة حجم العينة للارتباط أو الانحدار
    # =================================================================
    with spss_subtabs[5]:
        st.markdown(
            '<div style="font-size:15.5px; font-weight:800; color:var(--text); margin:10px 0;">'
            'حاسبة تقدير حجم العينة للارتباط والانحدار (<span class="ltr">Correlation &amp; Regression Sample Estimator</span>)</div>',
            unsafe_allow_html=True,
        )
        cr1, cr2, cr3 = st.columns(3)
        with cr1:
            cr_mode = st.selectbox(
                "نوع التحليل المستهدف:",
                ["تحليل الارتباط (Correlation)", "تحليل الانحدار (Regression)"],
                key="cr_mode_select",
            )
        with cr2:
            if "الارتباط" in cr_mode:
                cr_effect = st.selectbox(
                    "حجم الأثر المتوقع (r):",
                    ["أثر صغير (r ≈ 0.10)", "أثر متوسط (r ≈ 0.30)", "أثر كبير (r ≈ 0.50)"],
                    index=1,
                    key="cr_eff_corr",
                )
                n_preds = 1
            else:
                cr_effect = st.selectbox(
                    "حجم الأثر المتوقع (f²):",
                    ["أثر صغير (f² ≈ 0.02)", "أثر متوسط (f² ≈ 0.15)", "أثر كبير (f² ≈ 0.35)"],
                    index=1,
                    key="cr_eff_reg",
                )
                n_preds = st.number_input("عدد المتغيرات المستقلة / المتنبئة:", min_value=1, max_value=30, value=3, step=1, key="cr_preds")
        with cr3:
            st.markdown("<div style='height:26px;'></div>", unsafe_allow_html=True)
            est_n, est_note = _estimate_corr_reg_sample(cr_mode, cr_effect, int(n_preds))
            st.markdown(
                f'<div class="sl-result-banner" style="margin-top:0;">'
                f'<strong>التقدير الأولي للعينة:</strong> <span style="font-size:17px; font-weight:800;">{est_n} مفردة</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            f'<div class="sl-probe-result">'
            f'<div style="font-size:12.8px; margin-bottom:4px;">• <strong>الأساس المنهجي للتقدير:</strong> {est_note}</div>'
            f'<div style="font-size:12.2px; color:var(--text-muted);">• ملاحظة: هذا تقدير استرشادي أولي؛ يُنصح برفع الحجم المستهدف قليلاً لمراعاة الاستمارات غير الصالحة أو القيم المفقودة.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # =================================================================
    # التبويب 7: قائمة مراجعة جاهزية الفصل الإحصائي قبل التسليم
    # =================================================================
    with spss_subtabs[6]:
        st.markdown(
            '<div style="font-size:15.5px; font-weight:800; color:var(--text); margin:10px 0;">'
            'قائمة مراجعة جاهزية الفصل الإحصائي قبل التسليم (<span class="ltr">Pre-Submission Checklist</span>)</div>',
            unsafe_allow_html=True,
        )

        chk_items = [
            ("chk_reverse", "هل تم توحيد اتجاه العبارات السالبة (Reverse Coding) قبل حساب المتوسطات أو معامل الثبات؟"),
            ("chk_n_match", "هل تتطابق أرقام حجم العينة (N) في الجداول الإحصائية مع النص المذكور في منهجية الدراسة وعرض النتائج؟"),
            ("chk_p_val", "هل كُتبت الدلالة الإحصائية بصيغة (p < .001) بدلاً من (0.000) وفق معايير APA 7؟"),
            ("chk_socio_comment", "هل توجد تعليقات منهجية وسوسيولوجية تربط الأرقام بالفرضيات والإطار النظري أسفل كل جدول؟"),
            ("chk_assumptions", "هل تم فحص الشروط القبلية (التوزيع الطبيعي / تجانس التباين / التعدد الخطي VIF) وتبرير الاختيار؟"),
            ("chk_tables_fmt", "هل عناوين الجداول وأرقامها منسقة بشكل متسلسل وواضح دون خلط بين المتغيرات والفرضيات؟"),
        ]

        checked_count = 0
        for key_id, label_txt in chk_items:
            if st.checkbox(label_txt, key=key_id):
                checked_count += 1

        total_chk = len(chk_items)
        if checked_count == total_chk:
            status_msg = f"ممتاز! اكتملت جميع بنود المراجعة ({checked_count}/{total_chk}) — الفصل الإحصائي جاهز للمراجعة النهائية أو التسليم."
            banner_cls = "sl-warn-banner"
        else:
            status_msg = f"تم التحقق من ({checked_count} من {total_chk}) بنود — راجعي البنود المتبقية قبل إرسال الفصل للمشرف أو النشر."
            banner_cls = "sl-result-banner"

        st.markdown(f'<div class="{banner_cls}"><strong>{status_msg}</strong></div>', unsafe_allow_html=True)
