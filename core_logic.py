from nicegui import ui
from core_logic import calculate_sample_size_thompson, recommend_statistical_test

ui.add_head_html(
    """
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        html, body {
            direction: rtl;
            text-align: right;
            font-family: 'Cairo', sans-serif !important;
        }
        .q-markdown, .q-field__label, .q-btn, .q-card, input, label, div {
            font-family: 'Cairo', sans-serif !important;
        }
    </style>
    """,
    shared=True,
)

dark = ui.dark_mode(False)


def toggle_theme() -> None:
    dark.toggle()
    theme_btn.text = "الوضع الفاتح" if dark.value else "الوضع الداكن"


def on_calculate_sample() -> None:
    try:
        pop_n = int(pop_input.value or 0)
    except ValueError:
        pop_n = 0

    res = calculate_sample_size_thompson(pop_n, margin_select.value)
    sample_result_card.visible = True
    sample_result_title.text = res["title"]
    sample_result_body.text = res["body"]


def on_suggest_test() -> None:
    res = recommend_statistical_test(goal_select.value, norm_select.value)
    test_result_card.visible = True
    test_result_title.text = res["title"]
    test_result_body.text = res["body"]


# =====================================================================
# 01. الشريط العلوي
# =====================================================================
with ui.header(elevated=True).classes("bg-slate-900 text-white px-6 py-3 items-center justify-between"):
    with ui.row().classes("items-center gap-3"):
        ui.icon("analytics", size="28px").classes("text-sky-400")
        with ui.column().classes("gap-0"):
            ui.label("Socio Lab").classes("text-lg font-extrabold tracking-wide text-white")
            ui.label("فضاء علمي رقمي للتحليل الإحصائي والمنهجية").classes("text-xs text-sky-200")

    with ui.row().classes("items-center gap-4"):
        ui.link("حجم العينة", "#sample-tool").classes("text-white no-underline text-sm font-semibold hover:text-sky-300")
        ui.link("اختيار الاختبار", "#test-tool").classes("text-white no-underline text-sm font-semibold hover:text-sky-300")
        theme_btn = ui.button("الوضع الداكن", on_click=toggle_theme).props("outline dense color=white").classes("px-3")

# =====================================================================
# 02. الأداة الأولى: حاسبة حجم العينة
# =====================================================================
with ui.column().props("id=sample-tool").classes("w-full max-w-5xl mx-auto px-4 pt-8 pb-4 gap-4"):
    with ui.card().classes("w-full p-6 rounded-2xl shadow-sm border border-sky-500/20"):
        ui.label("1. حاسبة حجم العينة (ستيفن ثامبسون)").classes("text-lg font-extrabold text-sky-700 dark:text-sky-300")
        with ui.row().classes("w-full gap-4 items-end flex-wrap mt-2"):
            pop_input = ui.number("حجم مجتمع الدراسة (N)", value=500, min=10, step=10).classes("flex-1 min-w-56")
            margin_select = ui.select(
                "هامش الخطأ ومستوى الثقة",
                options=["5% (مستوى ثقة 95%)", "1% (مستوى ثقة 99%)", "10% (مستوى ثقة 90%)"],
                value="5% (مستوى ثقة 95%)",
            ).classes("flex-1 min-w-56")
            ui.button("احسب العينة", on_click=on_calculate_sample).props("color=primary").classes("px-6 py-2 font-bold")

        sample_result_card = ui.card().classes("w-full mt-4 p-4 rounded-xl bg-sky-50 dark:bg-slate-800 border-r-4 border-sky-500")
        sample_result_card.visible = False
        with sample_result_card:
            sample_result_title = ui.label("").classes("text-base font-extrabold text-sky-900 dark:text-sky-200")
            sample_result_body = ui.label("").classes("text-sm text-slate-700 dark:text-slate-200 mt-1 leading-relaxed")

# =====================================================================
# 03. الأداة الثانية: اختيار الاختبار الإحصائي
# =====================================================================
with ui.column().props("id=test-tool").classes("w-full max-w-5xl mx-auto px-4 pb-12 gap-4"):
    with ui.card().classes("w-full p-6 rounded-2xl shadow-sm border border-sky-500/20"):
        ui.label("2. مساعد اختيار الاختبار الإحصائي").classes("text-lg font-extrabold text-sky-700 dark:text-sky-300")
        with ui.row().classes("w-full gap-4 items-end flex-wrap mt-2"):
            goal_select = ui.select(
                "الهدف البحثي",
                options=[
                    "قياس العلاقة الارتباطية بين متغيرين",
                    "مقارنة الفروق بين مجموعتين مستقلتين",
                    "قياس أثر متغير مستقل في متغير تابع",
                ],
                value="قياس العلاقة الارتباطية بين متغيرين",
            ).classes("flex-1 min-w-56")
            norm_select = ui.select(
                "التوزيع الطبيعي للبيانات",
                options=[
                    "يتبع التوزيع الطبيعي (Sig > 0.05)",
                    "لا يتبع التوزيع الطبيعي (Sig < 0.05)",
                ],
                value="يتبع التوزيع الطبيعي (Sig > 0.05)",
            ).classes("flex-1 min-w-56")
            ui.button("اقترح الاختبار", on_click=on_suggest_test).props("color=secondary").classes("px-6 py-2 font-bold")

        test_result_card = ui.card().classes("w-full mt-4 p-4 rounded-xl bg-emerald-50 dark:bg-slate-800 border-r-4 border-emerald-500")
        test_result_card.visible = False
        with test_result_card:
            test_result_title = ui.label("").classes("text-base font-extrabold text-emerald-900 dark:text-emerald-200")
            test_result_body = ui.label("").classes("text-sm text-slate-700 dark:text-slate-200 mt-1 leading-relaxed")

ui.run(title="Socio Lab | NiceGUI Prototype", reload=False)
