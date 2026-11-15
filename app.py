import base64
import os
import urllib.parse
import streamlit as st
from db import (
    add_office_request,
    delete_record,
    fetch_all,
    get_conn,
    get_request_by_code,
    init_db,
)
from lab_tools import render_lab_section

# تهيئة قاعدة البيانات عند تشغيل المنصة
init_db()

CONTACT_EMAIL = "contact@sociolab-dz.com"
LOGO_FILENAME = "logo.png.jpg"
ADMIN_PASS = st.secrets.get("ADMIN_PASSWORD", "sociolab2026")


def get_logo_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


logo_b64 = get_logo_base64(LOGO_FILENAME)
icon_val = LOGO_FILENAME if os.path.exists(LOGO_FILENAME) else "🔬"

st.set_page_config(
    page_title="SOCIO LAB | SCIENCE. DATA. SOCIETY.",
    page_icon=icon_val,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ادارة الصفحات (11 صفحة اساسية + لوحة الادارة)
PAGES = {
    "home": "الرئيسية",
    "about": "من نحن",
    "library": "المكتبة الرقمية",
    "knowledge": "مركز المعرفة",
    "lab": "المختبر الاحصائي",
    "observatory": "مرصد المجتمع",
    "researchers": "فضاء الباحثين",
    "academy": "الاكاديمية الرقمية",
    "projects": "المشاريع",
    "office": "المكتب العلمي",
    "contact": "اتصل بنا",
}

q_params = st.query_params
if "page" in q_params and (q_params["page"] in PAGES or q_params["page"] == "admin"):
    st.session_state.page = q_params["page"]
elif "page" not in st.session_state:
    st.session_state.page = "home"

# التنسيق العام والهوية البصرية (الازرق الداكن، الملكي، الفيروزي، الابيض)
css = (
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');"
    "#MainMenu, header, footer {visibility: hidden;}"
    ".block-container {padding: 0rem !important; max-width: 100% !important;}"
    ".stApp {background-color: #FFFFFF; font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; color: #0F172A;}"
    "h1, h2, h3, h4, p, span, div, label, input, select, textarea, button {font-family: 'Cairo', sans-serif;}"
    ".rtl {direction: rtl; text-align: right; unicode-bidi: isolate;}"
    ".ltr {direction: ltr; text-align: left; display: inline-block; unicode-bidi: isolate; font-family: sans-serif;}"
    ".ltr-block {direction: ltr; text-align: left; display: block; unicode-bidi: isolate;}"
    "input, textarea {unicode-bidi: plaintext !important; font-size: 13px !important; border-radius: 8px !important;}"
    "div[data-baseweb='select'] > div {direction: rtl; text-align: right; font-size: 13px !important;}"
    "label p {direction: rtl !important; text-align: right !important; font-size: 13px !important; font-weight: 700 !important;}"
    "/* الشريط العلوي */"
    ".sl-nav {background-color: #06182C; border-bottom: 1px solid #1E3A8A; padding: 10px 4%; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; position: sticky; top: 0; z-index: 999;}"
    ".sl-logo-box {display: flex; align-items: center; text-decoration: none;}"
    ".sl-logo-img {height: 52px; width: auto; object-fit: contain; border-radius: 8px;}"
    ".sl-menu {display: flex; flex-wrap: wrap; gap: 12px; align-items: center;}"
    ".sl-menu a {color: #E2E8F0; text-decoration: none !important; font-size: 12.5px; font-weight: 600; padding: 5px 8px; border-radius: 6px; transition: 0.2s;}"
    ".sl-menu a:hover, .sl-menu a.active {background-color: #1E3A8A; color: #2DD4BF;}"
    "/* الواجهة الترحيبية المؤسساتية */"
    ".sl-hero {background: linear-gradient(135deg, #06182C 0%, #0F2942 60%, #1E3A8A 100%); color: #FFFFFF; padding: 65px 6%; text-align: center; border-bottom: 3px solid #14B8A6;}"
    ".sl-motto {display: inline-block; letter-spacing: 3px; font-size: 12px; font-weight: 700; color: #2DD4BF; border: 1px solid rgba(45, 212, 191, 0.4); padding: 6px 18px; border-radius: 99px; margin-bottom: 18px; direction: ltr;}"
    ".sl-hero-h1 {font-size: 32px; font-weight: 800; color: #FFFFFF; margin-bottom: 14px; line-height: 1.4;}"
    ".sl-hero-p {font-size: 15.5px; color: #CBD5E1; max-width: 760px; margin: 0 auto 28px auto; line-height: 1.8;}"
    ".sl-hero-actions {display: flex; justify-content: center; gap: 14px; flex-wrap: wrap;}"
    ".sl-btn-primary {background-color: #14B8A6; color: #06182C !important; font-weight: 800; font-size: 13.5px; padding: 11px 24px; border-radius: 8px; text-decoration: none !important;}"
    ".sl-btn-secondary {background-color: rgba(255,255,255,0.08); border: 1px solid #38BDF8; color: #FFFFFF !important; font-weight: 700; font-size: 13.5px; padding: 11px 24px; border-radius: 8px; text-decoration: none !important;}"
    "/* الاقسام والبطاقات */"
    ".sl-wrap {max-width: 1180px; margin: 0 auto; padding: 45px 6%;}"
    ".sl-alt-bg {background-color: #F8FAFC; border-top: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0;}"
    ".sl-page-head {margin-bottom: 28px; border-bottom: 2px solid #E2E8F0; padding-bottom: 16px;}"
    ".sl-tag {color: #0284C7; font-size: 12.5px; font-weight: 800; margin-bottom: 4px;}"
    ".sl-title {font-size: 24px; font-weight: 800; color: #06182C; margin: 0 0 8px 0;}"
    ".sl-sub {font-size: 14px; color: #475569; margin: 0; line-height: 1.7;}"
    ".sl-grid-3 {display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px;}"
    ".sl-card {background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 3.5px solid #1E3A8A; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(6,24,44,0.03);}"
    ".sl-card.teal {border-top-color: #14B8A6;}"
    ".sl-card h3 {font-size: 16px; font-weight: 800; color: #06182C; margin: 0 0 8px 0;}"
    ".sl-card p {font-size: 13px; color: #475569; line-height: 1.7; margin: 0;}"
    ".sl-info-box {background-color: #F0F9FF; border: 1px solid #BAE6FD; border-right: 4px solid #0284C7; padding: 14px 18px; border-radius: 10px; margin-top: 12px; font-size: 13.5px; color: #0F2942; line-height: 1.7;}"
    ".sl-empty-state {background: #F8FAFC; border: 1px dashed #94A3B8; border-radius: 12px; padding: 28px; text-align: center; color: #475569; font-size: 14px;}"
    ".sl-footer {background-color: #06182C; color: #CBD5E1; padding: 40px 6%; text-align: center; border-top: 3px solid #1E3A8A; font-size: 13px;}"
    "</style>"
)
st.markdown(css, unsafe_allow_html=True)

# بناء الشريط العلوي بالقائمة الرئيسية المعتمدة (11 عنصرا)
if logo_b64:
    logo_html = f'<a href="?page=home" target="_self" class="sl-logo-box"><img src="data:image/jpeg;base64,{logo_b64}" alt="SOCIO LAB" class="sl-logo-img"></a>'
else:
    logo_html = '<a href="?page=home" target="_self" class="sl-logo-box"><strong style="color:#FFFFFF; font-size:18px;" class="ltr">SOCIO LAB</strong></a>'

menu_links = ""
for p_key, p_label in PAGES.items():
    act = "active" if st.session_state.page == p_key else ""
    menu_links += f'<a href="?page={p_key}" target="_self" class="{act}">{p_label}</a>'

navbar_html = f'<div class="sl-nav">{logo_html}<div class="sl-menu">{menu_links}</div></div>'
st.markdown(navbar_html, unsafe_allow_html=True)

curr_page = st.session_state.page

# =====================================================================
# 1. الواجهة الرئيسية (HOME - 9 اقسام علمية ومؤسساتية بدون تجارة)
# =====================================================================
if curr_page == "home":
    hero = (
        '<div class="sl-hero">'
        '<div class="sl-motto">SCIENCE. DATA. SOCIETY.</div>'
        '<div class="sl-hero-h1">نحو معرفة علمية تصنع اثرا في المجتمع</div>'
        '<p class="sl-hero-p">منصة علمية رقمية تجمع البحث والمعرفة والبيانات والتكنولوجيا، '
        'وتسهم في تطوير الدراسات الاجتماعية وتعزيز الابتكار العلمي في العلوم الاجتماعية والانسانية.</p>'
        '<div class="sl-hero-actions">'
        '<a href="?page=library" target="_self" class="sl-btn-primary">استكشف المكتبة الرقمية</a>'
        '<a href="?page=lab" target="_self" class="sl-btn-secondary">المختبر المنهجي والاحصائي</a>'
        '<a href="?page=observatory" target="_self" class="sl-btn-secondary">مرصد المجتمع والبيانات</a>'
        '</div></div>'
    )
    st.markdown(hero, unsafe_allow_html=True)

    # القسم 2: من نحن
    sec_about = (
        '<div class="sl-wrap">'
        '<div class="sl-page-head"><div class="sl-tag">الهوية المؤسساتية</div>'
        '<h2 class="sl-title">من نحن</h2></div>'
        '<p style="font-size:14.5px; color:#334155; line-height:1.9;">'
        '<strong class="ltr">SOCIO LAB</strong> هي منصة علمية رقمية متخصصة في العلوم الاجتماعية والانسانية، '
        'تهدف الى بناء فضاء رقمي متكامل يجمع بين البحث العلمي، وانتاج المعرفة، وتحليل البيانات، والابتكار الاجتماعي. '
        'تعمل المنصة على اتاحة الموارد الاكاديمية وتطوير الادوات البحثية لدعم الطلبة والباحثين والمؤسسات، '
        'بينما يمثل المكتب العلمي والاستشاري الجانب التطبيقي والمهني المستقل للمشروع.'
        '</p></div>'
    )
    st.markdown(sec_about, unsafe_allow_html=True)

    # القسم 3: مجالات اهتمامنا
    domains_html = (
        '<div class="sl-alt-bg"><div class="sl-wrap">'
        '<div class="sl-page-head"><div class="sl-tag">نطاق التخصص</div>'
        '<h2 class="sl-title">مجالات اهتمامنا البحثية</h2></div>'
        '<div class="sl-grid-3">'
        '<div class="sl-card"><h3>التحولات الاجتماعية والاسرة</h3><p>دراسة التغير الاجتماعي، البناء الاسري، التحولات الثقافية والاقتصادية، وقضايا الشباب والبطالة في المجتمع الجزائري.</p></div>'
        '<div class="sl-card teal"><h3>علم اجتماع الجريمة والانحراف</h3><p>تحليل ظواهر الانحراف، عصابات الاحياء، تعاطي المؤثرات العقلية، والعنف والمخاطر الاجتماعية برؤية سوسيولوجية ميدانية.</p></div>'
        '<div class="sl-card"><h3>المجتمع الرقمي والامن المعلوماتي</h3><p>رصد الانحراف الرقمي، المخاطر الاجتماعية للتكنولوجيا، وتحليل البيانات الاجتماعية وتوظيف الذكاء الاصطناعي بمسؤولية.</p></div>'
        '</div></div></div>'
    )
    st.markdown(domains_html, unsafe_allow_html=True)

    # القسم 4 و 5 و 6 و 7: المعرفة + المختبر + المشاريع + الاكاديمية
    pillars_html = (
        '<div class="sl-wrap">'
        '<div class="sl-page-head"><div class="sl-tag">البنية الوظيفية للمنصة</div>'
        '<h2 class="sl-title">فضاءات المعرفة والبحث والتكوين</h2></div>'
        '<div class="sl-grid-3">'
        '<div class="sl-card teal"><h3>مركز المعرفة والابحاث</h3><p>فضاء لنشر المقالات العلمية، التحليلات السوسيولوجية، مراجعات الادبيات، والملفات الموضوعية حول القضايا المجتمعية.</p>'
        '<div style="margin-top:12px;"><a href="?page=knowledge" target="_self" style="color:#0284C7; font-weight:700; font-size:13px;">الانتقال الى مركز المعرفة &larr;</a></div></div>'
        '<div class="sl-card"><h3>المختبر المنهجي والاحصائي</h3><p>ادوات تفاعلية لحساب حجم العينة، معامل الفا كرونباخ، الاحصاء الوصفي، مسبار الفرضيات، واختيار اختبارات SPSS.</p>'
        '<div style="margin-top:12px;"><a href="?page=lab" target="_self" style="color:#0284C7; font-weight:700; font-size:13px;">فتح المختبر الرقمي &larr;</a></div></div>'
        '<div class="sl-card teal"><h3>مرصد المجتمع والبيانات</h3><p>متابعة وتحليل الظواهر والتحولات الاجتماعية عبر مؤشرات احصائية موثقة وتقارير دورية تحترم الخصوصية والمنهجية.</p>'
        '<div style="margin-top:12px;"><a href="?page=observatory" target="_self" style="color:#0284C7; font-weight:700; font-size:13px;">استعراض المرصد الاجتماعي &larr;</a></div></div>'
        '<div class="sl-card"><h3>المشاريع والمبادرات العلمية</h3><p>عرض المشاريع البحثية الجارية والمنجزة، الدراسات الميدانية، وفرص الشراكة العلمية مع الجامعات والمؤسسات.</p>'
        '<div style="margin-top:12px;"><a href="?page=projects" target="_self" style="color:#0284C7; font-weight:700; font-size:13px;">تصفح المشاريع &larr;</a></div></div>'
        '<div class="sl-card teal"><h3>الاكاديمية الرقمية</h3><p>برامج تكوينية وورشات تطبيقية في منهجية البحث العلمي، التحليل الاحصائي SPSS، الكتابة الاكاديمية، وادارة المراجع.</p>'
        '<div style="margin-top:12px;"><a href="?page=academy" target="_self" style="color:#0284C7; font-weight:700; font-size:13px;">دخول الاكاديمية &larr;</a></div></div>'
        '<div class="sl-card"><h3>فضاء الباحثين</h3><p>شبكة اكاديمية للتعريف بالباحثين، تخصصاتهم، منشوراتهم العلمية، وفرص التعاون في الملتقيات والمؤتمرات.</p>'
        '<div style="margin-top:12px;"><a href="?page=researchers" target="_self" style="color:#0284C7; font-weight:700; font-size:13px;">استكشاف فضاء الباحثين &larr;</a></div></div>'
        '</div></div>'
    )
    st.markdown(pillars_html, unsafe_allow_html=True)

    # القسم 8 و 9: شركاؤنا ومجتمعنا العلمي + تواصل معنا
    partners_contact = (
        f'<div class="sl-alt-bg"><div class="sl-wrap">'
        f'<div class="sl-grid-3">'
        f'<div class="sl-card"><h3>شركاؤنا ومجتمعنا العلمي</h3>'
        f'<p>تنفتح <span class="ltr">SOCIO LAB</span> على التعاون البحثي مع مخابر البحث الجامعية، الجامعات، النوادي العلمية، والهيئات البحثية وفق اتفاقيات علمية موثقة.</p></div>'
        f'<div class="sl-card teal"><h3>تواصل معنا</h3>'
        f'<p>للاستفسارات العلمية، اقتراحات النشر، او الشراكات الاكاديمية:<br>'
        f'البريد الرسمي: <strong class="ltr">{CONTACT_EMAIL}</strong><br>'
        f'<a href="?page=contact" target="_self" style="color:#0284C7; font-weight:700;">انتقل الى صفحة الاتصال الرسمية &larr;</a></p></div>'
        f'</div></div></div>'
    )
    st.markdown(partners_contact, unsafe_allow_html=True)

# =====================================================================
# 2. صفحة من نحن (ABOUT)
# =====================================================================
elif curr_page == "about":
    st.markdown(
        '<div class="sl-wrap">'
        '<div class="sl-page-head"><div class="sl-tag">الرؤية والرسالة والاهداف</div>'
        '<h1 class="sl-title">عن منصة SOCIO LAB</h1></div>'
        '<div class="sl-grid-3" style="margin-bottom:24px;">'
        '<div class="sl-card teal"><h3>الرؤية</h3><p>ان تصبح SOCIO LAB منصة علمية رقمية رائدة على المستوى الوطني، وفضاء مرجعيا في البحث الاجتماعي وتحليل البيانات وانتاج المعرفة، مع التوجه نحو الانفتاح على المحيط الاكاديمي والمؤسساتي.</p></div>'
        '<div class="sl-card"><h3>الرسالة</h3><p>توظيف المعرفة العلمية والتكنولوجيا والبيانات لتطوير البحث في العلوم الاجتماعية والانسانية، وتوفير بيئة رقمية تساعد على الوصول الى المعرفة وانتاجها وتبادلها.</p></div>'
        '</div>'
        '<h3>الاهداف الاستراتيجية للمنصة</h3>'
        '<ul style="line-height:2; font-size:14px; color:#334155;">'
        '<li>تعزيز الوصول الرقمي الى المعرفة العلمية في العلوم الاجتماعية والانسانية.</li>'
        '<li>دعم الباحثين والطلبة في مساراتهم البحثية وتطوير ادوات رقمية للتحليل الاحصائي.</li>'
        '<li>تشجيع انتاج الدراسات الميدانية وتطوير ثقافة استخدام البيانات في فهم الظواهر المجتمعية.</li>'
        '<li>تعزيز التعاون بين الباحثين والجامعات والمؤسسات وتطوير برامج تكوينية متخصصة.</li>'
        '<li>المساهمة في دراسة المشكلات الاجتماعية في المجتمع الجزائري وتوظيف التقنيات الرقمية بمسؤولية.</li>'
        '</ul></div>',
        unsafe_allow_html=True,
    )

# =====================================================================
# 3. المكتبة العلمية الرقمية (DIGITAL LIBRARY)
# =====================================================================
elif curr_page == "library":
    st.markdown(
        '<div class="sl-wrap">'
        '<div class="sl-page-head"><div class="sl-tag">Digital Library</div>'
        '<h1 class="sl-title">المكتبة العلمية الرقمية</h1>'
        '<p class="sl-sub">ابحث وصنف المراجع العلمية، الكتب، المقالات، والرسائل الجامعية المتاحة قانونيا مع بيانات التوثيق.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    resources = fetch_all("library_resources")
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        q_search = st.text_input("بحث بالعنوان او المؤلف:")
    with sc2:
        q_type = st.selectbox("نوع المصدر:", ["الكل", "كتاب علمي", "مقال محكم", "رسالة ماستر / دكتوراه", "دليل منهجي"])
    with sc3:
        q_spec = st.text_input("التخصص:", placeholder="مثال: علم الاجتماع / احصاء")

    filtered = [
        r for r in resources
        if (not q_search or q_search.lower() in r["title"].lower() or q_search.lower() in r["author"].lower())
        and (q_type == "الكل" or r["res_type"] == q_type)
        and (not q_spec or q_spec.lower() in r["specialty"].lower())
    ]

    if not filtered:
        st.markdown(
            '<div class="sl-empty-state">لا توجد مراجع مسجلة حاليا تطابق البحث. '
            'يمكن لادارة المنصة اضافة المراجع الموثقة عبر لوحة الادارة (<a href="?page=admin" target="_self">لوحة التحكم</a>).</div>',
            unsafe_allow_html=True,
        )
    else:
        for item in filtered:
            link_html = f'<a href="{item["source_url"]}" target="_blank" style="color:#0284C7; font-weight:700;">الرابط الاصلي للمصدر &nearr;</a>' if item["source_url"] else ""
            st.markdown(
                f'<div class="sl-card" style="margin-bottom:14px;">'
                f'<span style="font-size:11.5px; background:#E0F2FE; color:#0369A1; padding:3px 10px; border-radius:99px; font-weight:700;">{item["res_type"]} • {item["specialty"]} • {item["pub_year"]}</span>'
                f'<h3 style="margin-top:8px;">{item["title"]} — <span style="font-weight:600; color:#475569;">{item["author"]}</span></h3>'
                f'<p style="font-size:12.5px; margin-bottom:6px;"><strong>التوثيق (APA):</strong> {item["apa_citation"]}</p>'
                f'{link_html}</div>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 4. مركز المعرفة والابحاث (RESEARCH & KNOWLEDGE CENTER)
# =====================================================================
elif curr_page == "knowledge":
    st.markdown(
        '<div class="sl-wrap">'
        '<div class="sl-page-head"><div class="sl-tag">Research &amp; Knowledge Center</div>'
        '<h1 class="sl-title">مركز المعرفة والابحاث</h1>'
        '<p class="sl-sub">مقالات علمية، تحليلات سوسيولوجية، مراجعات ادبيات، وقراءات في الظواهر الاجتماعية المعاصرة.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    articles = fetch_all("knowledge_articles")
    if not articles:
        st.markdown(
            '<div class="sl-empty-state">لا توجد مقالات منشورة بعد. يمكن نشر المقالات والدراسات من خلال <a href="?page=admin" target="_self">لوحة التحكم الادارية</a>.</div>',
            unsafe_allow_html=True,
        )
    else:
        for art in articles:
            with st.expander(f"{art['title']} | ({art['category']} - {art['pub_date']})"):
                st.markdown(f"**بقلم:** {art['author']}")
                st.markdown(f"**ملخص:** {art['summary']}")
                st.markdown("---")
                st.write(art["content"])
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 5. المختبر المنهجي والاحصائي (STATISTICAL & METHODOLOGICAL LAB)
# =====================================================================
elif curr_page == "lab":
    st.markdown('<div class="sl-wrap">', unsafe_allow_html=True)
    render_lab_section()
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 6. مرصد المجتمع والبيانات (SOCIAL OBSERVATORY)
# =====================================================================
elif curr_page == "observatory":
    st.markdown(
        '<div class="sl-wrap">'
        '<div class="sl-page-head"><div class="sl-tag">Social Observatory</div>'
        '<h1 class="sl-title">مرصد المجتمع والبيانات</h1>'
        '<p class="sl-sub">رصد وتحليل الظواهر والتحولات الاجتماعية في المجتمع الجزائري استنادا الى بيانات ومصادر رسمية موثقة.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    indicators = fetch_all("observatory_data")
    if not indicators:
        st.markdown(
            '<div class="sl-empty-state">لم يتم ادراج مؤشرات رقمية بعد. تلتزم المنصة بعدم عرض اي ارقام غير موثقة؛ '
            'يمكن اضافة المؤشرات مع ذكر مصدر البيانات وسنة الجمع عبر <a href="?page=admin" target="_self">لوحة الادارة</a>.</div>',
            unsafe_allow_html=True,
        )
    else:
        for ind in indicators:
            st.markdown(
                f'<div class="sl-card teal" style="margin-bottom:14px;">'
                f'<span style="font-size:11.5px; color:#0D9488; font-weight:800;">مجال الرصد: {ind["domain"]}</span>'
                f'<h3>{ind["title"]}: <span style="color:#1E3A8A;">{ind["indicator_val"]}</span></h3>'
                f'<p><strong>المصدر الرسمي:</strong> {ind["data_source"]} ({ind["data_year"]})<br>'
                f'<strong>المنهجية المتبعة:</strong> {ind["methodology"]}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 7. فضاء الباحثين (RESEARCHER SPACE)
# =====================================================================
elif curr_page == "researchers":
    st.markdown(
        '<div class="sl-wrap">'
        '<div class="sl-page-head"><div class="sl-tag">Researcher Space</div>'
        '<h1 class="sl-title">فضاء الباحثين والتعاون العلمي</h1>'
        '<p class="sl-sub">دليل الباحثين في العلوم الاجتماعية والانسانية وفرص التشبيك والتعاون الاكاديمي.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM researchers WHERE approved = 1 ORDER BY id DESC")
    approved_res = [dict(r) for r in cur.fetchall()]
    conn.close()

    if approved_res:
        for res in approved_res:
            st.markdown(
                f'<div class="sl-card" style="margin-bottom:12px;">'
                f'<h3>{res["full_name"]} — <span style="font-size:13px; color:#0284C7;">{res["academic_rank"]}</span></h3>'
                f'<p><strong>المؤسسة:</strong> {res["institution"]} | <strong>التخصص:</strong> {res["specialty"]}<br>'
                f'<strong>الاهتمامات البحثية:</strong> {res["interests"]}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown('<div class="sl-empty-state">دليل الباحثين قيد التحديث. يمكنك تسجيل ملفك البحثي ادناه.</div>', unsafe_allow_html=True)

    st.markdown("### طلب الانضمام الى دليل الباحثين (تسجيل اختياري)")
    with st.form("researcher_reg_form"):
        rc1, rc2 = st.columns(2)
        with rc1:
            r_name = st.text_input("الاسم الكامل للباحث *")
            r_rank = st.selectbox("الدرجة العلمية / الصفة *", ["طالب ماستر", "طالب دكتوراه", "استاذ باحث", "خبير / باحث مستقل"])
            r_inst = st.text_input("الجامعة او مخبر البحث *")
        with rc2:
            r_spec = st.text_input("التخصص الدقيق *")
            r_interests = st.text_input("الاهتمامات البحثية *")
            r_link = st.text_input("رابط ORCID او Google Scholar (اختياري)")
        agree = st.checkbox("اوافق على عرض بياناتي الاكاديمية في دليل الباحثين بعد مراجعة الادارة.")
        if st.form_submit_button("ارسال طلب التسجيل"):
            if r_name and r_inst and r_spec and agree:
                conn = get_conn()
                conn.execute(
                    "INSERT INTO researchers (full_name, academic_rank, institution, specialty, interests, contact_link, approved) "
                    "VALUES (?, ?, ?, ?, ?, ?, 0)",
                    (r_name, r_rank, r_inst, r_spec, r_interests, r_link),
                )
                conn.commit()
                conn.close()
                st.success("تم استلام ملفك البحثي بنجاح وسيظهر في الدليل فور اعتماد الادارة.")
            else:
                st.warning("يرجى ملء الحقول المطلوبة والموافقة على النشر.")
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 8. الاكاديمية الرقمية (DIGITAL ACADEMY)
# =====================================================================
elif curr_page == "academy":
    st.markdown(
        '<div class="sl-wrap">'
        '<div class="sl-page-head"><div class="sl-tag">Digital Academy</div>'
        '<h1 class="sl-title">الاكاديمية الرقمية والتكوين المنهجي</h1>'
        '<p class="sl-sub">دورات تدريبية، ورشات تطبيقية، وندوات علمية لتطوير مهارات البحث والتحليل الاحصائي.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    courses = fetch_all("academy_courses")
    if not courses:
        st.markdown(
            '<div class="sl-empty-state">سيتم الاعلان عن رزنامة الدورات والورشات العلمية قريبا عبر لوحة الادارة.</div>',
            unsafe_allow_html=True,
        )
    else:
        for crs in courses:
            st.markdown(
                f'<div class="sl-card teal" style="margin-bottom:14px;">'
                f'<span style="font-size:11.5px; color:#0D9488; font-weight:800;">{crs["track"]} • {crs["format"]}</span>'
                f'<h3>{crs["title"]}</h3>'
                f'<p>{crs["description"]}<br><strong>الموعد:</strong> {crs["schedule_info"]}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 9. المشاريع والمبادرات العلمية (RESEARCH PROJECTS)
# =====================================================================
elif curr_page == "projects":
    st.markdown(
        '<div class="sl-wrap">'
        '<div class="sl-page-head"><div class="sl-tag">Research Projects</div>'
        '<h1 class="sl-title">المشاريع والمبادرات العلمية</h1>'
        '<p class="sl-sub">المشاريع البحثية الجارية والمنجزة والدراسات الميدانية التي تنفذها المنصة او تشارك فيها.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    projects = fetch_all("projects")
    if not projects:
        st.markdown(
            '<div class="sl-empty-state">لا توجد مشاريع مدرجة حاليا. يمكن اضافة المشاريع الجارية والمنجزة من لوحة الادارة.</div>',
            unsafe_allow_html=True,
        )
    else:
        for prj in projects:
            st.markdown(
                f'<div class="sl-card" style="margin-bottom:14px;">'
                f'<span style="font-size:11.5px; background:#DBEAFE; color:#1E40AF; padding:3px 10px; border-radius:99px; font-weight:700;">{prj["status"]}</span>'
                f'<h3 style="margin-top:8px;">{prj["title"]}</h3>'
                f'<p>{prj["summary"]}<br><strong>الشركاء:</strong> {prj["partners"]}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 10. المكتب العلمي والاستشاري (SCIENTIFIC & CONSULTING OFFICE - مستقل)
# =====================================================================
elif curr_page == "office":
    st.markdown(
        '<div class="sl-wrap">'
        '<div class="sl-page-head"><div class="sl-tag">Scientific &amp; Consulting Office</div>'
        '<h1 class="sl-title">المكتب العلمي والاستشاري</h1>'
        '<p class="sl-sub">الجانب التطبيقي والمهني المستقل لـ SOCIO LAB: استقبال طلبات الدراسات الميدانية، الاستشارات المنهجية، والتحليل الاحصائي للمؤسسات والباحثين.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    tab_req, tab_track = st.tabs(["تقديم طلب دراسة او استشارة علمية", "متابعة حالة طلب سابق (برمز التتبع)"])

    with tab_req:
        req_options = [
            "تصميم وبناء ادوات البحث (استبيان / دليل مقابلة)",
            "التحليل الاحصائي وتنظيف البيانات (SPSS)",
            "الضبط المنهجي وتحكيم المقاييس",
            "تحليل البيانات الكيفية والدراسات المختلطة",
            "التوثيق الاكاديمي (APA 7) وتنسيق اوراق النشر",
            "نمذجة المعادلات البنية (SEM / SmartPLS)",
            "دراسة ميدانية او قياس اثر اجتماعي لمؤسسة",
            "مرافقة منهجية متكاملة (حسب مراحل البحث)"
        ]
        with st.form("office_request_form"):
            selected_reqs = st.multiselect("مجالات الاستشارة او الدراسة المطلوبة (متعدد الخيارات) *", req_options)
            oc1, oc2 = st.columns(2)
            with oc1:
                c_name = st.text_input("الاسم الكامل / اسم المؤسسة *")
                c_role = st.selectbox("الصفة *", ["طالب ماستر", "طالب دكتوراه", "استاذ باحث", "مؤسسة / جمعية / مخبر"])
            with oc2:
                c_email = st.text_input("البريد الالكتروني الرسمي للتواصل *")
            c_details = st.text_area("وصف موضوع الدراسة، طبيعة البيانات، والاهداف المطلوبة *", height=110)

            if st.form_submit_button("تسجيل الطلب في المكتب العلمي"):
                if c_name and c_email and selected_reqs and c_details:
                    req_str = " + ".join(selected_reqs)
                    t_code = add_office_request(c_name, c_email, c_role, req_str, c_details)
                    subj = urllib.parse.quote(f"طلب استشارة علمية ({t_code}) - {c_name}")
                    body = urllib.parse.quote(
                        f"السلام عليكم المكتب العلمي SOCIO LAB،\nرمز التتبع: {t_code}\nالاسم: {c_name}\nالمجالات: {req_str}\nالتفاصيل:\n{c_details}"
                    )
                    mailto = f"mailto:{CONTACT_EMAIL}?subject={subj}&body={body}"
                    st.success(f"تم تسجيل طلبك في قاعدة بيانات المكتب العلمي بنجاح! رمز التتبع الخاص بك هو: {t_code}")
                    st.markdown(
                        f'<div class="sl-info-box">احتفظ برمز التتبع (<strong>{t_code}</strong>) لمتابعة حالة طلبك في اي وقت. '
                        f'كما يمكنك ارسال نسخة مباشرة الى بريد المكتب: '
                        f'<a href="{mailto}" style="font-weight:800; color:#0284C7;">اضغط هنا للارسال عبر البريد الالكتروني</a></div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.warning("يرجى استكمال جميع الحقول المطلوبة.")

    with tab_track:
        track_input = st.text_input("ادخل رمز التتبع الخاص بطلبك (مثال: SL-A1B2C3):")
        if st.button("استعلام عن حالة الطلب"):
            if track_input:
                res_req = get_request_by_code(track_input)
                if res_req:
                    st.markdown(
                        f'<div class="sl-info-box">'
                        f'<strong>رمز الطلب:</strong> <span class="ltr">{res_req["tracking_code"]}</span><br>'
                        f'<strong>مقدم الطلب:</strong> {res_req["client_name"]} ({res_req["client_role"]})<br>'
                        f'<strong>تاريخ الايداع:</strong> {res_req["created_at"]}<br>'
                        f'<strong>الحالة الحالية:</strong> <span style="color:#0D9488; font-weight:800;">{res_req["status"]}</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.error("لم يتم العثور على طلب مطابق لهذا الرمز. يرجى التحقق من الرمز المدخل.")
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 11. اتصل بنا (CONTACT US)
# =====================================================================
elif curr_page == "contact":
    st.markdown(
        f'<div class="sl-wrap">'
        f'<div class="sl-page-head"><div class="sl-tag">Contact Us</div>'
        f'<h1 class="sl-title">اتصل بنا</h1>'
        f'<p class="sl-sub">قنوات التواصل الرسمية لمنصة <span class="ltr">SOCIO LAB</span> للاستفسارات العلمية والشراكات المؤسساتية.</p>'
        f'</div>'
        f'<div class="sl-info-box">'
        f'<strong>البريد الالكتروني الرسمي:</strong> <span class="ltr">{CONTACT_EMAIL}</span><br>'
        f'<strong>المقر:</strong> سوق اهراس، الجزائر<br>'
        f'<strong>مجالات المراسلة:</strong> النشر في مركز المعرفة، ايداع المراجع في المكتبة الرقمية، الشراكات الجامعية، او طلبات المكتب العلمي.'
        f'</div></div>',
        unsafe_allow_html=True,
    )

# =====================================================================
# لوحة التحكم الادارية (ADMIN CMS - محمية بكلمة مرور)
# =====================================================================
elif curr_page == "admin":
    st.markdown('<div class="sl-wrap"><h1>لوحة التحكم الادارية (SOCIO LAB CMS)</h1>', unsafe_allow_html=True)
    pwd = st.text_input("ادخل كلمة مرور الادارة:", type="password")
    if pwd == ADMIN_PASS:
        st.success("تم تسجيل الدخول الى لوحة الادارة بنجاح.")
        a_tabs = st.tabs([
            "اضافة مرجع للمكتبة",
            "نشر مقال في مركز المعرفة",
            "اضافة مؤشر للمرصد",
            "ادارة طلبات المكتب والباحثين"
        ])

        with a_tabs[0]:
            with st.form("add_lib_form"):
                lt = st.text_input("عنوان المرجع *")
                la = st.text_input("المؤلف *")
                ltype = st.selectbox("النوع", ["كتاب علمي", "مقال محكم", "رسالة ماستر / دكتوراه", "دليل منهجي"])
                lspec = st.text_input("التخصص *")
                lyear = st.text_input("سنة النشر *")
                lapa = st.text_input("التوثيق بصيغة APA")
                lurl = st.text_input("رابط المصدر (اختياري)")
                if st.form_submit_button("حفظ المرجع في المكتبة"):
                    if lt and la and lspec and lyear:
                        conn = get_conn()
                        conn.execute(
                            "INSERT INTO library_resources (title, author, res_type, specialty, pub_year, apa_citation, source_url) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (lt, la, ltype, lspec, lyear, lapa, lurl),
                        )
                        conn.commit()
                        conn.close()
                        st.success("تمت اضافة المرجع بنجاح.")

        with a_tabs[1]:
            with st.form("add_art_form"):
                at = st.text_input("عنوان المقال او الدراسة *")
                acat = st.text_input("التصنيف الموضوعي *")
                aauth = st.text_input("اسم الكاتب *")
                adate = st.text_input("تاريخ النشر *", value="2026-11")
                asum = st.text_area("ملخص المقال *")
                acont = st.text_area("النص الكامل *")
                if st.form_submit_button("نشر المقال"):
                    if at and acat and aauth and acont:
                        conn = get_conn()
                        conn.execute(
                            "INSERT INTO knowledge_articles (title, category, author, summary, content, pub_date) "
                            "VALUES (?, ?, ?, ?, ?, ?)",
                            (at, acat, aauth, asum, acont, adate),
                        )
                        conn.commit()
                        conn.close()
                        st.success("تم نشر المقال في مركز المعرفة.")

        with a_tabs[2]:
            with st.form("add_obs_form"):
                odom = st.text_input("مجال الظاهرة (مثل: الشباب والبطالة) *")
                otit = st.text_input("عنوان المؤشر *")
                oval = st.text_input("قيمة المؤشر الموثقة *")
                osrc = st.text_input("مصدر البيانات الرسمي *")
                oyr = st.text_input("سنة جمع البيانات *")
                ometh = st.text_area("المنهجية المستخدمة في التحليل *")
                if st.form_submit_button("نشر المؤشر في المرصد"):
                    if odom and otit and oval and osrc:
                        conn = get_conn()
                        conn.execute(
                            "INSERT INTO observatory_data (domain, title, indicator_val, data_source, data_year, methodology) "
                            "VALUES (?, ?, ?, ?, ?, ?)",
                            (odom, otit, oval, osrc, oyr, ometh),
                        )
                        conn.commit()
                        conn.close()
                        st.success("تم نشر المؤشر في مرصد المجتمع.")

        with a_tabs[3]:
            st.markdown("#### طلبات المكتب العلمي الواردة")
            reqs = fetch_all("office_requests")
            for rq in reqs:
                st.markdown(f"**{rq['tracking_code']}** | {rq['client_name']} ({rq['client_email']}) | {rq['req_type']} | الحالة: **{rq['status']}**")
                new_st = st.selectbox(
                    f"تحديث حالة {rq['tracking_code']}:",
                    ["قيد الدراسة المنهجية", "تم ارسال خطة العمل", "قيد التنفيذ", "مكتمل"],
                    key=f"st_{rq['id']}"
                )
                if st.button(f"حفظ الحالة لـ {rq['tracking_code']}", key=f"btn_{rq['id']}"):
                    conn = get_conn()
                    conn.execute("UPDATE office_requests SET status = ? WHERE id = ?", (new_st, rq["id"]))
                    conn.commit()
                    conn.close()
                    st.rerun()

            st.markdown("---")
            st.markdown("#### طلبات اعتماد الباحثين")
            conn = get_conn()
            pending = [dict(r) for r in conn.execute("SELECT * FROM researchers WHERE approved = 0").fetchall()]
            conn.close()
            for pr in pending:
                st.write(f"{pr['full_name']} - {pr['institution']} ({pr['specialty']})")
                if st.button(f"اعتماد الباحث {pr['full_name']}", key=f"app_{pr['id']}"):
                    conn = get_conn()
                    conn.execute("UPDATE researchers SET approved = 1 WHERE id = ?", (pr["id"],))
                    conn.commit()
                    conn.close()
                    st.rerun()
    elif pwd:
        st.error("كلمة المرور غير صحيحة.")
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# التذييل الموحد (FOOTER) مع الحفاظ على الشعار الاصلي
# =====================================================================
if logo_b64:
    footer_logo = f'<img src="data:image/jpeg;base64,{logo_b64}" alt="SOCIO LAB" style="height:64px; width:auto; margin:0 auto 12px auto; display:block; border-radius:8px;">'
else:
    footer_logo = '<div class="ltr" style="font-weight:800; font-size:20px; color:#FFFFFF; margin-bottom:8px;">SOCIO LAB</div>'

footer_html = (
    f'<div class="sl-footer">{footer_logo}'
    f'<div class="ltr" style="letter-spacing:2px; font-size:11px; color:#2DD4BF; margin-bottom:6px;">SCIENCE. DATA. SOCIETY.</div>'
    f'<div>منصة علمية رقمية متخصصة في العلوم الاجتماعية والانسانية</div>'
    f'<div style="margin-top:8px; font-size:12px;">البريد الرسمي: <span class="ltr">{CONTACT_EMAIL}</span> | '
    f'<a href="?page=admin" target="_self" style="color:#64748B; text-decoration:none;">ادارة المنصة</a></div>'
    f'<div style="font-size:11px; color:#64748B; margin-top:6px;">جميع الحقوق محفوظة &copy; 2026 <span class="ltr">SOCIO LAB</span></div>'
    f'</div>'
)
st.markdown(footer_html, unsafe_allow_html=True)
