import streamlit as st
import pandas as pd
import numpy as np
import math
import io
import datetime
import base64
import os
import glob

try:
    import pyreadstat
    HAS_PYREADSTAT = True
except ImportError:
    HAS_PYREADSTAT = False

# ==========================================
# 1. إعدادات الصفحة والهوية البصرية المطابقة للشعار
# ==========================================
st.set_page_config(
    page_title="Socio Lab",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lobster&family=Pacifico&family=Readex+Pro:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

    html, body, [class*="css"], .stMarkdown, .stText, .stButton, .stSelectbox, .stMultiSelect, .stRadio, .stCheckbox {
        font-family: 'Readex Pro', sans-serif !important;
        direction: rtl;
        text-align: right;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    /* خلفية كحلية مطابقة لألوان الشعار */
    .stApp {
        background: radial-gradient(circle at 15% 10%, #0A2540 0%, #051324 55%, #020813 100%) !important;
        color: #F8FAFC !important;
    }

    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #F1F5F9 !important;
    }

    /* ضبط صناديق التنبيه الافتراضية لكي لا تظهر بيضاء أبدا */
    div[data-testid="stAlert"] {
        background: rgba(10, 32, 64, 0.92) !important;
        border: 1px solid rgba(56, 189, 248, 0.45) !important;
        border-right: 5px solid #38BDF8 !important;
        border-radius: 14px !important;
        color: #F8FAFC !important;
    }
    div[data-testid="stAlert"] * {
        color: #F8FA
