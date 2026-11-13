import streamlit as st
import streamlit.components.v1 as components

# اعدادات الصفحة في Streamlit
st.set_page_config(
    page_title="Socio Lab | المختبر الاستشاري للبحث السوسيولوجي والتحليل الاحصائي",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# اخفاء الهوامش والقوائم الافتراضية لـ Streamlit لتظهر المنصة كأنها موقع مستقل
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
        }
        iframe {
            border: none !important;
            width: 100% !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# كود واجهة منصة Socio Lab الكامل داخل متغير نصي في بايثون
html_code = """
<!DOCTYPE html>
<html lang="ar" dir="rtl" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Socio Lab</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Great+Vibes&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        navy: {
                            900: '#0A192F',
                            800: '#0F2942',
                            700: '#163A5F'
                        },
                        teal: {
                            500: '#14B8A6',
                            400: '#2DD4BF'
                        },
                        amber: {
                            500: '#F59E0B',
                            600: '#D97706'
                        }
                    },
                    fontFamily: {
                        sans: ['Cairo', 'sans-serif'],
                        script: ['Great Vibes', 'cursive']
                    }
                }
            }
        }
    </script>
    <style>
        .bg-grid-pattern {
            background-image: radial-gradient(rgba(20, 184, 166, 0.15) 1px, transparent 1px);
            background-size: 28px 28px;
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 font-sans antialiased">

    <!-- 1. الشريط العلوي -->
    <header class="bg-navy-900/95 backdrop-blur-md text-white sticky top-0 z-50 border-b border-navy-700">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
            <a href="#" class="flex items-center gap-3">
                <div class="w-11 h-11 rounded-xl bg-navy-800 border border-teal-500/40 flex items-center justify-center text-teal-400 font-bold text-xl shadow-inner">
                    &Sigma;
                </div>
                <div class="flex flex-col">
                    <span class="font-script text-3xl text-white tracking-wider leading-none">Socio Lab</span>
                    <span class="text-[11px] text-teal-400 mt-1">للتحليل الاحصائي والمنهجية</span>
                </div>
            </a>

            <nav class="hidden md:flex items-center gap-8 text-sm font-semibold text-slate-200">
                <a href="#services" class="hover:text-teal-400 transition">خدماتنا</a>
                <a href="#tools" class="hover:text-teal-400 transition">الادوات التفاعلية</a>
                <a href="#integrity" class="hover:text-teal-400 transition">ميثاق النزاهة</a>
                <a href="#order" class="hover:text-teal-400 transition">اطلب خدمة</a>
            </nav>

            <a href="#order" class="bg-amber-500 hover:bg-amber-600 text-navy-900 font-bold px-5 py-2.5 rounded-lg text-sm transition shadow-lg shadow-amber-500/20">
                احجز استشارة
            </a>
        </div>
    </header>

    <!-- 2. الواجهة الترحيبية -->
    <section class="bg-navy-900 bg-grid-pattern text-white py-20 lg:py-24 relative overflow-hidden">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid lg:grid-cols-12 gap-12 items-center">
            
            <div class="lg:col-span-7 space-y-6">
                <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-navy-800 border border-teal-500/30 text-teal-400 text-xs font-semibold">
                    <span>&mu;</span>
                    <span>دقة منهجية • قراءة سوسيولوجية • توثيق APA</span>
                </div>
                <h1 class="text-3xl sm:text-5xl font-extrabold leading-tight">
                    من الفكرة البحثية الى النتائج المحكمة.. <span class="text-teal-400">شريكك المنهجي والاحصائي الدقيق</span>
                </h1>
                <p class="text-slate-300 text-base sm:text-lg leading-relaxed max-w-2xl">
                    في <span class="font-script text-2xl text-white mx-1">Socio Lab</span> نحول البيانات الميدانية الخام الى رؤى سوسيولوجية وعلمية رصينة. نرافق الباحثين، طلبة الدراسات العليا، والمؤسسات في تصميم ادوات القياس، تنظيف البيانات، والتحليل الاحصائي المتقدم عبر برنامج SPSS.
                </p>
                <div class="flex flex-wrap gap-4 pt-2">
                    <a href="#order" class="bg-amber-500 hover:bg-amber-600 text-navy-900 font-bold px-7 py-3.5 rounded-xl transition shadow-lg shadow-amber-500/20">
                        اطلب خدمتك البحثية الان
                    </a>
                    <a href="#tools" class="bg-navy-800 hover:bg-navy-700 border border-slate-700 text-white font-semibold px-7 py-3.5 rounded-xl transition">
                        جرب الادوات الاحصائية المجانية
                    </a>
                </div>
            </div>

            <div class="lg:col-span-5 bg-navy-800/90 border border-navy-700 p-6 rounded-2xl shadow-2xl space-y-5">
                <div class="flex items-center justify-between border-b border-navy-700 pb-4">
                    <div>
                        <span class="text-xs text-teal-400 font-semibold">نموذج مخرجات Socio Lab</span>
                        <h3 class="text-base font-bold text-white">تحليل التوزيع الطبيعي ومؤشرات الثبات</h3>
                    </div>
                    <span class="bg-teal-500/20 text-teal-400 text-xs font-mono px-2.5 py-1 rounded">SPSS v28</span>
                </div>

                <div class="bg-navy-900/80 p-4 rounded-xl border border-navy-700">
                    <svg viewBox="0 0 300 110" class="w-full h-28 overflow-visible">
                        <defs>
                            <linearGradient id="curveGrad" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0%" stop-color="#14B8A6" stop-opacity="0.45"/>
                                <stop offset="100%" stop-color="#14B8A6" stop-opacity="0.0"/>
                            </linearGradient>
                        </defs>
                        <line x1="10" y1="95" x2="290" y2="95" stroke="#334155" stroke-width="1"/>
                        <line x1="150" y1="15" x2="150" y2="95" stroke="#F59E0B" stroke-dasharray="3,3" stroke-width="1.5"/>
                        <path d="M 15 95 C 75 95, 105 15, 150 15 C 195 15, 225 95, 285 95 Z" fill="url(#curveGrad)"/>
                        <path d="M 15 95 C 75 95, 105 15, 150 15 C 195 15, 225 95, 285 95" fill="none" stroke="#14B8A6" stroke-width="2.5"/>
                        <text x="150" y="108" fill="#F59E0B" font-size="10" text-anchor="middle">&mu; = 3.84</text>
                    </svg>
                </div>

                <div class="grid grid-cols-3 gap-3 text-center">
                    <div class="bg-navy-900/60 p-3 rounded-lg border border-navy-700">
                        <div class="text-xs text-slate-400">الفا كرونباخ (&alpha;)</div>
                        <div class="text-lg font-bold text-teal-400 font-mono">0.892</div>
                    </div>
                    <div class="bg-navy-900/60 p-3 rounded-lg border border-navy-700">
                        <div class="text-xs text-slate-400">حجم العينة (N)</div>
                        <div class="text-lg font-bold text-white font-mono">60</div>
                    </div>
                    <div class="bg-navy-900/60 p-3 rounded-lg border border-navy-700">
                        <div class="text-xs text-slate-400">الدلالة (Sig)</div>
                        <div class="text-lg font-bold text-amber-500 font-mono">0.001</div>
                    </div>
                </div>

                <div class="text-xs text-slate-300 bg-navy-900/90 p-3.5 rounded-lg border-r-4 border-teal-500 leading-relaxed">
                    <strong>القراءة السوسيولوجية:</strong> تشير قيمة الفا كرونباخ (0.892) الى اتساق داخلي مرتفع جدا لاداة القياس، مع دلالة احصائية تؤكد اثر المتغير المستقل عند مستوى دلالة 0.01.
                </div>
            </div>

        </div>
    </section>

    <!-- 3. قسم الخدمات البحثية والاحصائية -->
    <section id="services" class="py-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-2xl mx-auto mb-12">
            <span class="text-teal-500 font-bold text-sm">حلول منهجية متكاملة</span>
            <h2 class="text-3xl font-extrabold text-navy-900 mt-1">خدمات منصة Socio Lab</h2>
            <p class="text-slate-600 mt-3 text-sm sm:text-base">نصمم الادوات ونحلل البيانات وفق الضوابط الاكاديمية المعتمدة في الجامعات والمجلات المحكمة.</p>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="bg-white p-7 rounded-2xl border border-slate-200 border-t-4 border-t-teal-500 shadow-sm hover:shadow-md transition">
                <div class="text-teal-500 font-bold text-2xl mb-3">01</div>
                <h3 class="text-xl font-bold text-navy-900 mb-2">تصميم وبناء ادوات البحث</h3>
                <p class="text-slate-600 text-sm leading-relaxed">صياغة الاستبيانات الورقية والالكترونية وبناء ادلة المقابلات المعمقة والملاحظة العلمية وفق ابعاد وفرضيات الدراسة مع دليل الترميز.</p>
            </div>

            <div class="bg-white p-7 rounded-2xl border border-slate-200 border-t-4 border-t-navy-900 shadow-sm hover:shadow-md transition">
                <div class="text-navy-900 font-bold text-2xl mb-3">02</div>
                <h3 class="text-xl font-bold text-navy-900 mb-2">التحليل الاحصائي وتنظيف البيانات (SPSS)</h3>
                <p class="text-slate-600 text-sm leading-relaxed">تفريغ البيانات وتنظيفها، حساب الصدق والثبات، واجراء الاختبارات الوصفية والاستدلالية مع قراءة سوسيولوجية معمقة للجداول.</p>
            </div>

            <div class="bg-white p-7 rounded-2xl border border-slate-200 border-t-4 border-t-amber-500 shadow-sm hover:shadow-md transition">
                <div class="text-amber-500 font-bold text-2xl mb-3">03</div>
                <h3 class="text-xl font-bold text-navy-900 mb-2">الضبط المنهجي وتحكيم المقاييس</h3>
                <p class="text-slate-600 text-sm leading-relaxed">مراجعة الاشكالية والفرضيات، ضبط المعاينة، وتقييم الخصائص السيكومترية للمقاييس لضمان سلامة البناء المنهجي للدراسة.</p>
            </div>

            <div class="bg-white p-7 rounded-2xl border border-slate-200 border-t-4 border-t-navy-900 shadow-sm hover:shadow-md transition">
                <div class="text-navy-900 font-bold text-2xl mb-3">04</div>
                <h3 class="text-xl font-bold text-navy-900 mb-2">تحليل البيانات الكيفية</h3>
                <p class="text-slate-600 text-sm leading-relaxed">تفريغ المقابلات المعمقة وتحليل المضمون والتحليل الموضوعاتي للدراسات الميدانية والدراسات المختلطة (الكمية والكيفية).</p>
            </div>

            <div class="bg-white p-7 rounded-2xl border border-slate-200 border-t-4 border-t-teal-500 shadow-sm hover:shadow-md transition">
                <div class="text-teal-500 font-bold text-2xl mb-3">05</div>
                <h3 class="text-xl font-bold text-navy-900 mb-2">التوثيق الاكاديمي (APA) والنشر</h3>
                <p class="text-slate-600 text-sm leading-relaxed">ضبط التوثيق في المتن وقائمة المراجع وفق معايير APA، وتنسيق اوراق المؤتمرات والمقالات العلمية للنشر في المجلات المحكمة.</p>
            </div>

            <div class="bg-white p-7 rounded-2xl border border-slate-200 border-t-4 border-t-amber-500 shadow-sm hover:shadow-md transition">
                <div class="text-amber-500 font-bold text-2xl mb-3">06</div>
                <h3 class="text-xl font-bold text-navy-900 mb-2">مسوح المؤسسات ودراسات الاثر</h3>
                <p class="text-slate-600 text-sm leading-relaxed">تصميم وتنفيذ استطلاعات الراي ودراسات قياس الاثر الاجتماعي للمؤسسات والجمعيات وتقديم تقارير تنفيذية لصناع القرار.</p>
            </div>
        </div>
    </section>

    <!-- 4. قسم الادوات التفاعلية الذكية -->
    <section id="tools" class="py-16 bg-slate-100 border-y border-slate-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center max-w-2xl mx-auto mb-12">
                <span class="text-teal-500 font-bold text-sm">مختبر الادوات المجانية</span>
                <h2 class="text-3xl font-extrabold text-navy-900 mt-1">الادوات التفاعلية لمساعدة الباحث</h2>
                <p class="text-slate-600 mt-2 text-sm">استخدم ادواتنا الذكية لتحديد الاختبار الاحصائي المناسب لفرضيتك او حساب حجم عينتك الممثلة فورا.</p>
            </div>

            <div class="grid lg:grid-cols-2 gap-8">
                <div class="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm space-y-5">
                    <div class="flex items-center justify-between border-b pb-4">
                        <h3 class="text-xl font-bold text-navy-900">1. مشخص الاختبار الاحصائي (SPSS)</h3>
                        <span class="text-xs bg-navy-900 text-teal-400 px-3 py-1 rounded-full font-semibold">اداة ذكية</span>
                    </div>
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-1">هدف الفرضية البحثية:</label>
                            <select id="goalSelect" class="w-full rounded-xl border border-slate-300 p-3 text-sm focus:border-teal-500 focus:outline-none">
                                <option value="corr">قياس العلاقة الارتباطية بين متغيرين</option>
                                <option value="diff2">قياس الفروق بين مجموعتين مستقلتين (مثل: ذكور / اناث)</option>
                                <option value="diff3">قياس الفروق بين 3 مجموعات فاكثر (مثل: المستويات التعليمية)</option>
                                <option value="impact">قياس اثر متغير مستقل على متغير تابع (التنبؤ)</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-1">طبيعة البيانات والتوزيع:</label>
                            <select id="distSelect" class="w-full rounded-xl border border-slate-300 p-3 text-sm focus:border-teal-500 focus:outline-none">
                                <option value="normal">بيانات كمية تتبع التوزيع الطبيعي (معلمية)</option>
                                <option value="nonnormal">بيانات رتبية او لا تتبع التوزيع الطبيعي (لامعلمية)</option>
                            </select>
                        </div>
                        <button onclick="findTest()" class="w-full bg-navy-900 hover:bg-navy-800 text-white font-bold py-3 rounded-xl transition">
                            اعرض الاختبار الاحصائي المناسب
                        </button>
                        <div id="testResult" class="p-4 rounded-xl bg-slate-50 border border-teal-500/40 text-sm space-y-1">
                            <div class="font-bold text-navy-900" id="testName">معامل ارتباط بيرسون (Pearson Correlation)</div>
                            <div class="text-xs text-teal-600 font-mono" id="testPath">Analyze > Correlate > Bivariate > Pearson</div>
                        </div>
                    </div>
                </div>

                <div class="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm space-y-5">
                    <div class="flex items-center justify-between border-b pb-4">
                        <h3 class="text-xl font-bold text-navy-900">2. حاسبة حجم العينة الممثلة</h3>
                        <span class="text-xs bg-teal-500/15 text-teal-600 px-3 py-1 rounded-full font-semibold">معادلة كوكران</span>
                    </div>
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-1">حجم مجتمع الدراسة الكلي (N):</label>
                            <input type="number" id="popSize" value="500" min="10" class="w-full rounded-xl border border-slate-300 p-3 text-sm focus:border-teal-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-1">هامش الخطا المسموح به:</label>
                            <select id="marginError" class="w-full rounded-xl border border-slate-300 p-3 text-sm focus:border-teal-500 focus:outline-none">
                                <option value="0.05">5% (مستوى ثقة 95% - القياسي في العلوم الاجتماعية)</option>
                                <option value="0.01">1% (مستوى ثقة 99% - دقة عالية جدا)</option>
                                <option value="0.10">10% (مستوى ثقة 90% - للدراسات الاستطلاعية)</option>
                            </select>
                        </div>
                        <button onclick="calcSample()" class="w-full bg-teal-500 hover:bg-teal-400 text-navy-900 font-bold py-3 rounded-xl transition">
                            احسب حجم العينة المطلوب
                        </button>
                        <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between">
                            <span class="text-sm font-semibold text-slate-700">الحد الادنى الممثل للعينة (n):</span>
                            <span id="sampleOutput" class="text-2xl font-extrabold text-navy-900 font-mono">218 مفردة</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- 5. قسم ميثاق النزاهة العلمية -->
    <section id="integrity" class="py-14 bg-navy-900 text-white">
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-5">
            <span class="bg-amber-500/20 text-amber-400 text-xs font-bold px-4 py-1.5 rounded-full">الالتزام الاخلاقي والعلمي</span>
            <h2 class="text-2xl sm:text-3xl font-extrabold">ميثاق النزاهة العلمية وسرية البيانات في Socio Lab</h2>
            <p class="text-slate-300 text-sm sm:text-base leading-relaxed max-w-3xl mx-auto">
                تلتزم منصة Socio Lab بتقديم الاستشارات المنهجية والتحليل الاحصائي للبيانات الميدانية الحقيقية فقط، وترفض رفضا قاطعا فبركة البيانات او بيع البحوث الجاهزة او اي ممارسة تخل بالامانة العلمية، مع ضمان السرية التامة لافكار الباحثين وبياناتهم.
            </p>
        </div>
    </section>

    <!-- 6. قسم طلب خدمة او استشارة -->
    <section id="order" class="py-16 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white p-8 sm:p-10 rounded-3xl border border-slate-200 shadow-lg">
            <div class="text-center mb-8">
                <h2 class="text-2xl sm:text-3xl font-extrabold text-navy-900">اطلب خدمتك البحثية او استشارتك</h2>
                <p class="text-slate-600 text-sm mt-2">املا النموذج التالي وسيتواصل معك فريق Socio Lab خلال 24 ساعة بخطة العمل والتكلفة.</p>
            </div>

            <form id="serviceForm" onsubmit="submitOrder(event)" class="space-y-5">
                <div class="grid sm:grid-cols-2 gap-5">
                    <div>
                        <label class="block text-sm font-bold text-slate-700 mb-1">الاسم الكامل / المؤسسة *</label>
                        <input type="text" id="clientName" required placeholder="مثال: محمد الامين" class="w-full rounded-xl border border-slate-300 p-3 text-sm focus:border-teal-500 focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-700 mb-1">الصفة الاكاديمية او المهنية *</label>
                        <select id="clientRole" class="w-full rounded-xl border border-slate-300 p-3 text-sm focus:border-teal-500 focus:outline-none">
                            <option>باحث ماستر</option>
                            <option>باحث دكتوراه</option>
                            <option>استاذ باحث</option>
                            <option>مؤسسة / جمعية</option>
                        </select>
                    </div>
                </div>

                <div class="grid sm:grid-cols-2 gap-5">
                    <div>
                        <label class="block text-sm font-bold text-slate-700 mb-1">نوع الخدمة المطلوبة *</label>
                        <select id="serviceType" class="w-full rounded-xl border border-slate-300 p-3 text-sm focus:border-teal-500 focus:outline-none">
                            <option>التحليل الاحصائي وتفريغ البيانات (SPSS)</option>
                            <option>تصميم وبناء استبيان او اداة بحث</option>
                            <option>الضبط المنهجي وتحكيم الادوات</option>
                            <option>تحليل المقابلات والبيانات الكيفية</option>
                            <option>التوثيق الاكاديمي (APA) وتنسيق المقالات</option>
                            <option>حجز جلسة استشارية فردية</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-700 mb-1">رقم الواتساب او البريد الالكتروني *</label>
                        <input type="text" id="clientContact" required placeholder="06XXXXXXXX / email@domain.com" class="w-full rounded-xl border border-slate-300 p-3 text-sm focus:border-teal-500 focus:outline-none">
                    </div>
                </div>

                <div>
                    <label class="block text-sm font-bold text-slate-700 mb-1">ملخص الدراسة وحجم العينة والتفاصيل المطلوبة *</label>
                    <textarea id="studyDetails" rows="4" required placeholder="اكتب عنوان الدراسة او الاشكالية وحجم العينة والموعد المقترح للتسليم..." class="w-full rounded-xl border border-slate-300 p-3 text-sm focus:border-teal-500 focus:outline-none"></textarea>
                </div>

                <button type="submit" class="w-full bg-amber-500 hover:bg-amber-600 text-navy-900 font-extrabold py-4 rounded-xl transition shadow-md">
                    ارسال الطلب الان
                </button>
                <p id="formFeedback" class="hidden text-center text-sm font-bold text-teal-600 bg-teal-50 p-3 rounded-xl"></p>
            </form>
        </div>
    </section>

    <!-- 7. التذييل -->
    <footer class="bg-navy-900 text-slate-400 py-10 border-t border-navy-800 text-center text-sm">
        <div class="max-w-7xl mx-auto px-4 space-y-2">
            <div class="font-script text-3xl text-white">Socio Lab</div>
            <p>المختبر الاستشاري للبحث السوسيولوجي والتحليل الاحصائي</p>
            <p class="text-xs text-slate-500 pt-2">جميع الحقوق محفوظة &copy; 2026 Socio Lab</p>
        </div>
    </footer>

    <script>
        function findTest() {
            const goal = document.getElementById('goalSelect').value;
            const dist = document.getElementById('distSelect').value;
            const nameEl = document.getElementById('testName');
            const pathEl = document.getElementById('testPath');

            const tests = {
                corr_normal: ['معامل ارتباط بيرسون (Pearson Correlation)', 'Analyze > Correlate > Bivariate > Pearson'],
                corr_nonnormal: ['معامل ارتباط سبيرمان للرتب (Spearman Rho)', 'Analyze > Correlate > Bivariate > Spearman'],
                diff2_normal: ['اختبار ت لعينتين مستقلتين (Independent Samples T-Test)', 'Analyze > Compare Means > Independent-Samples T Test'],
                diff2_nonnormal: ['اختبار مان-ويتني (Mann-Whitney U Test)', 'Analyze > Nonparametric Tests > Independent Samples'],
                diff3_normal: ['تحليل التباين الاحادي (One-Way ANOVA)', 'Analyze > Compare Means > One-Way ANOVA'],
                diff3_nonnormal: ['اختبار كروسكال-واليس (Kruskal-Wallis Test)', 'Analyze > Nonparametric Tests > K Independent Samples'],
                impact_normal: ['الانحدار الخطي البسيط/المتعدد (Linear Regression)', 'Analyze > Regression > Linear'],
                impact_nonnormal: ['الانحدار اللوجستي او الترتيبي (Ordinal / Logistic Regression)', 'Analyze > Regression > Ordinal']
            };

            const key = `${goal}_${dist}`;
            nameEl.textContent = tests[key][0];
            pathEl.textContent = tests[key][1];
        }

        function calcSample() {
            const N = parseFloat(document.getElementById('popSize').value) || 100;
            const e = parseFloat(document.getElementById('marginError').value);
            const z = e === 0.01 ? 2.576 : (e === 0.10 ? 1.645 : 1.96);
            const p = 0.5;
            const n0 = (Math.pow(z, 2) * p * (1 - p)) / Math.pow(e, 2);
            const n = Math.ceil(n0 / (1 + ((n0 - 1) / N)));
            document.getElementById('sampleOutput').textContent = n + ' مفردة';
        }

        function submitOrder(e) {
            e.preventDefault();
            const feedback = document.getElementById('formFeedback');
            feedback.textContent = 'تم تسجيل طلبك بنجاح! سنتواصل معك خلال 24 ساعة.';
            feedback.classList.remove('hidden');
        }
    </script>
</body>
</html>
"""

# عرض المنصة بالكامل داخل صفحة Streamlit
components.html(html_code, height=3100, scrolling=True)
