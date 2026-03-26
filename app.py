import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import sqlite3
import os
import time
import hashlib
from datetime import datetime, timedelta

# ==============================================================================
# 1. תצורת תשתית וניהול הגדרות גלובליות (Global System Infrastructure)
# ==============================================================================

"""
הגדרת הגדרות העמוד המרכזיות של אפליקציית Streamlit.
אנו משתמשים בפריסה רחבה (Wide Layout) כדי לאפשר תצוגה מקסימלית של נתונים,
ומגדירים את תפריט הצד (Sidebar) להיות פתוח כברירת מחדל לנוחות המשתמש.
הגדרת העמוד חייבת להיות הפקודה הראשונה בהרצת הסקריפט למניעת שגיאות הרצה.
"""
st.set_page_config(
    page_title="Elite Strategic Trading Terminal | Ultimate Edition 2026",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. מנוע עיצוב ממשק משתמש מתקדם (Advanced Elite CSS Engine)
# ==============================================================================

def apply_elite_styles():
    """
    פונקציית העיצוב המרכזית של הטרמינל האסטרטגי.
    מחיל הגדרות CSS מורחבות ומקיפות לערכת נושא לבנה (Light Mode) נקייה.
    מבצע יישור לימין (RTL) אבסולוטי לכל רכיבי המערכת.
    כולל עיצוב ייחודי לכפתורים, טבלאות נתונים, כרטיסיות מידע ותיקון ויזואלי למספרים.
    הפונקציה משתמשת בפונטים מודרניים כדי להקנות למערכת מראה של טרמינל בנקאי יוקרתי.
    """
    st.markdown("""
    <style>
        /* הגדרות כיווניות ויישור לימין לכל גוף האפליקציה */
        .main .block-container {
            direction: rtl;
            text-align: right;
            background-color: #ffffff;
            color: #1a1a1a;
            padding-top: 2rem;
            padding-bottom: 8rem;
            font-family: 'Assistant', 'Segoe UI', Tahoma, sans-serif;
        }

        /* עיצוב Sidebar בסגנון טרמינל מקצועי ובהיר */
        section[data-testid="stSidebar"] {
            direction: rtl;
            background-color: #f8f9fa;
            border-left: 1px solid #dee2e6;
            padding: 2.5rem 1.5rem;
            box-shadow: 2px 0 15px rgba(0,0,0,0.03);
        }

        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] .stText,
        section[data-testid="stSidebar"] div {
            text-align: right !important;
            color: #1a1a1a !important;
            direction: rtl !important;
            font-weight: 700;
            font-size: 1.15rem;
        }

        /* כותרת ראשית */
        h1 {
            color: #000000;
            font-family: 'Assistant', sans-serif;
            font-weight: 900;
            font-size: 4.8rem !important;
            margin-bottom: 1rem;
            text-align: center !important;
            letter-spacing: -2px;
            border-bottom: 8px solid #007bff;
            padding-bottom: 30px;
            text-shadow: 2px 2px 15px rgba(0,0,0,0.06);
        }

        h2, h3, h4 {
            color: #2c3e50;
            font-weight: 800;
            margin-top: 3.5rem;
            margin-bottom: 1.5rem;
            text-align: right !important;
            border-right: 10px solid #007bff;
            padding-right: 25px;
        }

        /* טבלאות נתונים */
        .stDataFrame {
            border: 2px solid #e9ecef;
            border-radius: 30px;
            background-color: #ffffff;
            margin: auto;
            max-width: 99%;
            box-shadow: 0 25px 70px rgba(0,0,0,0.08);
            overflow: hidden;
            padding: 12px;
        }

        /* כפתורים */
        div.stButton > button {
            border-radius: 22px;
            font-weight: 900;
            border: 2px solid #dee2e6;
            background-color: #ffffff;
            color: #1a1a1a;
            height: 4.8em;
            width: 100%;
            font-size: 1.35rem;
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            margin-top: 25px;
            box-shadow: 0 5px 8px rgba(0,0,0,0.02);
        }

        div.stButton > button:hover {
            border-color: #007bff;
            color: #007bff;
            background-color: #f8fbff;
            box-shadow: 0 25px 55px rgba(0,123,255,0.28);
            transform: translateY(-10px);
        }

        div.stButton > button:active {
            transform: translateY(-2px);
        }

        /* התראות */
        .stInfo {
            border-right: 25px solid #007bff !important;
            border-left: 0px !important;
            background-color: #f0f7ff !important;
            color: #004085 !important;
            border-radius: 30px;
            padding: 3rem;
            text-align: right !important;
            box-shadow: 0 10px 25px rgba(0,123,255,0.15);
            font-size: 1.3rem;
            line-height: 1.9;
        }

        .stSuccess {
            border-right: 25px solid #28a745 !important;
            border-left: 0px !important;
            background-color: #f1fdf5 !important;
            color: #155724 !important;
            border-radius: 30px;
            padding: 3rem;
            text-align: right !important;
            box-shadow: 0 10px 25px rgba(40,167,69,0.15);
            font-size: 1.3rem;
            line-height: 1.9;
        }

        .stWarning {
            border-right: 25px solid #ffc107 !important;
            border-left: 0px !important;
            background-color: #fffef2 !important;
            color: #856404 !important;
            border-radius: 30px;
            padding: 3rem;
            text-align: right !important;
            box-shadow: 0 10px 25px rgba(255,193,7,0.15);
            font-size: 1.3rem;
            line-height: 1.9;
        }

        /* תיקון מספרים */
        .num-fix {
            direction: ltr !important;
            display: inline-block;
            unicode-bidi: embed;
            font-family: 'Assistant', sans-serif;
            font-weight: 850;
            color: #000000;
        }

        /* קלט */
        input, textarea, [data-baseweb="select"], .stNumberInput {
            direction: rtl;
            text-align: right !important;
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 2px solid #e9ecef !important;
            border-radius: 20px !important;
            padding: 18px !important;
            font-size: 1.2rem !important;
        }

        /* לשוניות */
        .stTabs [data-baseweb="tab-list"] {
            gap: 3rem;
            direction: rtl;
            border-bottom: 5px solid #f1f3f5;
            margin-bottom: 5rem;
        }

        .stTabs [data-baseweb="tab"] {
            font-size: 1.55rem;
            font-weight: 900;
            color: #495057;
            padding: 28px 40px;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .stTabs [aria-selected="true"] {
            color: #007bff !important;
            border-bottom: 8px solid #007bff !important;
            transform: scale(1.08);
        }

        /* פרוטוקול אסטרטגי */
        .protocol-wrapper {
            background-color: #ffffff;
            border: 2px solid #e9ecef;
            border-right: 30px solid #007bff;
            border-radius: 40px;
            padding: 60px;
            box-shadow: 0 30px 80px rgba(0,0,0,0.12);
            margin-bottom: 50px;
            direction: rtl;
            text-align: right;
        }

        /* AI Insight */
        .ai-insight-card {
            background: linear-gradient(135deg, #f0f7ff 0%, #ffffff 100%);
            border: 2px solid #cce5ff;
            border-right: 20px solid #007bff;
            border-radius: 40px;
            padding: 50px 60px;
            box-shadow: 0 20px 60px rgba(0,123,255,0.10);
            margin-bottom: 40px;
            direction: rtl;
            text-align: right;
            line-height: 2.2;
        }

        /* Multi-Chart header */
        .multichart-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 35px;
            padding: 40px 60px;
            margin-bottom: 40px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        }

        /* Market Overview banner */
        .market-overview-banner {
            background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
            border-radius: 30px;
            padding: 35px 50px;
            margin-bottom: 40px;
            box-shadow: 0 15px 50px rgba(0,0,0,0.18);
        }

        /* Portfolio card */
        .portfolio-summary-card {
            background: linear-gradient(135deg, #f0f7ff 0%, #e8f4fd 100%);
            border: 2px solid #bee3f8;
            border-right: 18px solid #007bff;
            border-radius: 35px;
            padding: 45px 55px;
            margin-bottom: 35px;
            box-shadow: 0 15px 45px rgba(0,123,255,0.09);
            direction: rtl;
            text-align: right;
        }

        .portfolio-profit { color: #1a7a40; font-weight: 900; }
        .portfolio-loss   { color: #c0392b; font-weight: 900; }

        /* Heatmap header */
        .heatmap-header {
            background: linear-gradient(135deg, #0a0a1a 0%, #12122a 50%, #1a1a3e 100%);
            border-radius: 35px;
            padding: 40px 60px;
            margin-bottom: 40px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.25);
        }

        /* TradingView container */
        .tradingview-container {
            background: #ffffff;
            border: 2px solid #e9ecef;
            border-radius: 30px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.08);
            margin-bottom: 30px;
        }

        /* Alert card */
        .alert-card-active {
            background: linear-gradient(135deg, #fff9f0 0%, #fffbf5 100%);
            border: 2px solid #ffc107;
            border-right: 16px solid #ff9800;
            border-radius: 28px;
            padding: 28px 35px;
            margin-bottom: 18px;
            box-shadow: 0 8px 28px rgba(255,152,0,0.12);
            direction: rtl;
            text-align: right;
        }

        .alert-card-triggered {
            background: linear-gradient(135deg, #fff5f5 0%, #fffafa 100%);
            border: 2px solid #dc3545;
            border-right: 16px solid #dc3545;
            border-radius: 28px;
            padding: 28px 35px;
            margin-bottom: 18px;
            box-shadow: 0 8px 28px rgba(220,53,69,0.14);
            direction: rtl;
            text-align: right;
        }

        /* רספונסיביות */
        @media (max-width: 1400px) {
            h1 { font-size: 3.5rem !important; }
            .stTabs [data-baseweb="tab"] { font-size: 1.3rem; padding: 20px 30px; }
        }
    </style>
    """, unsafe_allow_html=True)

# הפעלת פונקציית העיצוב הגלובלית
apply_elite_styles()

# ==============================================================================
# 3. ניהול מסד נתונים — Multi-User SaaS Engine
# ==============================================================================

# ---- נתיב מסד נתונים: קובץ מקומי קבוע — לא נמחק בין הפעלות ----
# שינוי: 'users.db' במקום שם זמני, כדי שהמשתמשים נשמרים לצמיתות.
DB_PATH      = 'users.db'
ADMIN_USER   = 'admin'

# חשוב: _hash_password מוגדרת לפני השימוש ב-ADMIN_PASS_H
# כדי שה-hash של Admin ייוצר עם אותו salt בדיוק כמו שאר המשתמשים.
def _hash_password(password: str) -> str:
    """SHA-256 hash עם salt קבוע — מבטיח עקביות לכל המשתמשים כולל Admin."""
    salted = f"elite_saas_salt_2026_{password}_end"
    return hashlib.sha256(salted.encode()).hexdigest()

# סיסמת Admin: Admin@2026  (ללא !)
# ADMIN_PASS_H נוצר עם אותה פונקציה שמשמשת גם ל-auth_login ← אין חוסר התאמה.
ADMIN_PASS_H = _hash_password('Admin@2026')


def setup_database():
    """
    מנגנון האתחול של מסד הנתונים הראשי — גרסה SaaS Multi-User.
    טבלאות:
      - users              : רישום משתמשים (username, password_hash, display_name, email, created_at, is_admin)
      - elite_journal_v5   : יומן מסחר — מסונן לפי user_id
      - elite_portfolio_v1 : תיק השקעות — מסונן לפי user_id
      - price_alerts_v1    : התראות מחיר — מסונן לפי user_id
    כל טבלת נתונים כוללת עמודת user_id להפרדה מלאה בין משתמשים.
    """
    try:
        conn   = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # טבלת משתמשים
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                username     TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                display_name TEXT,
                email        TEXT,
                created_at   TEXT,
                is_admin     INTEGER DEFAULT 0
            )
        ''')

        # ---- יצירת / עדכון Admin בכל הפעלה ----
        # הפונקציה בודקת אם Admin קיים. אם לא — יוצרת אותו.
        # אם קיים אך ה-hash שגוי (מ-migration ישנה) — מעדכנת את הסיסמה.
        existing_admin = cursor.execute(
            "SELECT id, password_hash FROM users WHERE username=?", (ADMIN_USER,)
        ).fetchone()
        if not existing_admin:
            # יצירה ראשונית
            cursor.execute(
                "INSERT INTO users (username, password_hash, display_name, email, created_at, is_admin) "
                "VALUES (?, ?, ?, ?, ?, 1)",
                (ADMIN_USER, ADMIN_PASS_H, 'מנהל מערכת', 'admin@elite.com',
                 datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            )
        elif existing_admin[1] != ADMIN_PASS_H:
            # תיקון hash ישן (migration מגרסאות קודמות)
            cursor.execute(
                "UPDATE users SET password_hash=?, is_admin=1 WHERE username=?",
                (ADMIN_PASS_H, ADMIN_USER)
            )

        # יומן מסחר — עם user_id
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS elite_journal_v5 (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id      INTEGER NOT NULL DEFAULT 0,
                ticker_symbol TEXT NOT NULL,
                user_notes   TEXT,
                date_saved   TEXT,
                risk_metric  REAL,
                tp_recommended REAL,
                UNIQUE(user_id, ticker_symbol)
            )
        ''')
        # Migration: הוסף user_id אם חסר (גרסאות ישנות)
        try:
            cursor.execute("SELECT user_id FROM elite_journal_v5 LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE elite_journal_v5 ADD COLUMN user_id INTEGER NOT NULL DEFAULT 0")

        # תיק השקעות — עם user_id
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS elite_portfolio_v1 (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id       INTEGER NOT NULL DEFAULT 0,
                ticker_symbol TEXT NOT NULL,
                quantity      REAL NOT NULL,
                avg_buy_price REAL NOT NULL,
                date_added    TEXT,
                notes         TEXT
            )
        ''')
        try:
            cursor.execute("SELECT user_id FROM elite_portfolio_v1 LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE elite_portfolio_v1 ADD COLUMN user_id INTEGER NOT NULL DEFAULT 0")

        # התראות מחיר — עם user_id
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_alerts_v1 (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id        INTEGER NOT NULL DEFAULT 0,
                ticker_symbol  TEXT NOT NULL,
                target_price   REAL NOT NULL,
                direction      TEXT NOT NULL,
                note           TEXT,
                is_triggered   INTEGER DEFAULT 0,
                date_created   TEXT,
                date_triggered TEXT
            )
        ''')
        try:
            cursor.execute("SELECT user_id FROM price_alerts_v1 LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE price_alerts_v1 ADD COLUMN user_id INTEGER NOT NULL DEFAULT 0")

        conn.commit()
        conn.close()
    except Exception as err:
        st.error(f"שגיאה קריטית באתחול בסיס הנתונים: {err}")


# ---- פונקציות אימות משתמשים (Auth) ----

def auth_register(username: str, password: str, display_name: str, email: str = "") -> tuple:
    """
    רישום משתמש חדש.
    מחזיר (True, user_id) בהצלחה, (False, reason_str) בכשלון.
    """
    username = username.strip().lower()
    if not username or len(username) < 3:
        return False, "שם משתמש חייב להכיל לפחות 3 תווים."
    if not password or len(password) < 6:
        return False, "סיסמה חייבת להכיל לפחות 6 תווים."
    if not display_name.strip():
        return False, "אנא הכנס שם תצוגה."

    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        ph = _hash_password(password)
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO users (username, password_hash, display_name, email, created_at, is_admin) "
            "VALUES (?, ?, ?, ?, ?, 0)",
            (username, ph, display_name.strip(), email.strip(), ts)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return True, user_id
    except sqlite3.IntegrityError:
        return False, "שם המשתמש כבר קיים. אנא בחר שם אחר."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()


def auth_login(username: str, password: str) -> tuple:
    """
    אימות משתמש קיים.
    מחזיר (True, user_dict) בהצלחה, (False, reason_str) בכשלון.
    """
    username = username.strip().lower()
    ph       = _hash_password(password)

    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    row    = cursor.execute(
        "SELECT id, username, display_name, email, is_admin FROM users WHERE username=? AND password_hash=?",
        (username, ph)
    ).fetchone()
    conn.close()

    if row:
        return True, {
            "id":           row[0],
            "username":     row[1],
            "display_name": row[2],
            "email":        row[3],
            "is_admin":     bool(row[4]),
        }
    return False, "שם משתמש או סיסמה שגויים."


def auth_get_all_users():
    """Admin only — שליפת כל המשתמשים הרשומים."""
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    rows   = cursor.execute(
        "SELECT id, username, display_name, email, created_at, is_admin FROM users ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return rows


def auth_get_user_count():
    """מחזיר מספר כולל של משתמשים רשומים (לא כולל Admin)."""
    conn   = sqlite3.connect(DB_PATH)
    count  = conn.execute("SELECT COUNT(*) FROM users WHERE is_admin=0").fetchone()[0]
    conn.close()
    return count


def _get_uid() -> int:
    """מחזיר את ה-user_id של המשתמש המחובר כרגע מ-session_state."""
    return st.session_state.get('auth_user', {}).get('id', 0)


# ---- פונקציות יומן מסחר (user-scoped) ----

def save_to_journal(ticker_id, notes=""):
    """שמירת מניה ליומן המסחר של המשתמש הנוכחי."""
    uid    = _get_uid()
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    ts     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute(
            "INSERT INTO elite_journal_v5 (user_id, ticker_symbol, user_notes, date_saved) VALUES (?, ?, ?, ?)",
            (uid, ticker_id, notes, ts)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def delete_from_journal(ticker_id):
    """מחיקת רשומה מיומן המשתמש הנוכחי."""
    uid    = _get_uid()
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM elite_journal_v5 WHERE user_id=? AND ticker_symbol=?", (uid, ticker_id))
    conn.commit()
    conn.close()

def fetch_journal():
    """שליפת יומן המשתמש הנוכחי, מהחדש לישן."""
    uid    = _get_uid()
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT ticker_symbol, user_notes, date_saved FROM elite_journal_v5 "
            "WHERE user_id=? ORDER BY date_saved DESC",
            (uid,)
        )
        rows = cursor.fetchall()
    except Exception:
        rows = []
    conn.close()
    return rows


# ---- פונקציות תיק השקעות (user-scoped) ----

def add_to_portfolio(ticker, quantity, avg_price, notes=""):
    """הוספת פוזיציה לתיק של המשתמש הנוכחי."""
    uid    = _get_uid()
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    ts     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO elite_portfolio_v1 (user_id, ticker_symbol, quantity, avg_buy_price, date_added, notes) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (uid, ticker.upper(), quantity, avg_price, ts, notes)
    )
    conn.commit()
    conn.close()

def fetch_portfolio():
    """שליפת הפוזיציות של המשתמש הנוכחי."""
    uid    = _get_uid()
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, ticker_symbol, quantity, avg_buy_price, date_added, notes "
        "FROM elite_portfolio_v1 WHERE user_id=? ORDER BY date_added DESC",
        (uid,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_from_portfolio(row_id):
    """מחיקת פוזיציה — רק אם שייכת למשתמש הנוכחי."""
    uid    = _get_uid()
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM elite_portfolio_v1 WHERE id=? AND user_id=?", (row_id, uid))
    conn.commit()
    conn.close()


# ---- פונקציות התראות מחיר (user-scoped) ----

def add_price_alert(ticker, target_price, direction, note=""):
    """הוספת התראת מחיר למשתמש הנוכחי."""
    uid    = _get_uid()
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    ts     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO price_alerts_v1 (user_id, ticker_symbol, target_price, direction, note, is_triggered, date_created) "
        "VALUES (?, ?, ?, ?, ?, 0, ?)",
        (uid, ticker.upper(), target_price, direction, note, ts)
    )
    conn.commit()
    conn.close()

def fetch_alerts(include_triggered=False):
    """שליפת התראות המשתמש הנוכחי."""
    uid    = _get_uid()
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if include_triggered:
        cursor.execute(
            "SELECT id, ticker_symbol, target_price, direction, note, is_triggered, date_created, date_triggered "
            "FROM price_alerts_v1 WHERE user_id=? ORDER BY date_created DESC",
            (uid,)
        )
    else:
        cursor.execute(
            "SELECT id, ticker_symbol, target_price, direction, note, is_triggered, date_created, date_triggered "
            "FROM price_alerts_v1 WHERE user_id=? AND is_triggered=0 ORDER BY date_created DESC",
            (uid,)
        )
    rows = cursor.fetchall()
    conn.close()
    return rows

def mark_alert_triggered(alert_id):
    """סימון התראה כמופעלת."""
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    ts     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE price_alerts_v1 SET is_triggered=1, date_triggered=? WHERE id=?", (ts, alert_id))
    conn.commit()
    conn.close()

def delete_alert(alert_id):
    """מחיקת התראה — רק אם שייכת למשתמש הנוכחי."""
    uid    = _get_uid()
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM price_alerts_v1 WHERE id=? AND user_id=?", (alert_id, uid))
    conn.commit()
    conn.close()

def check_alerts_against_prices(current_prices_dict):
    """בדיקת התראות פעילות של המשתמש הנוכחי מול מחירים נוכחיים."""
    triggered_now = []
    active_alerts = fetch_alerts(include_triggered=False)
    for alert in active_alerts:
        alert_id, ticker, target, direction, note, _, _, _ = alert
        cur = current_prices_dict.get(ticker.upper())
        if cur is None:
            continue
        if direction == 'above' and float(cur) >= float(target):
            mark_alert_triggered(alert_id)
            triggered_now.append((ticker, target, direction, note, cur))
        elif direction == 'below' and float(cur) <= float(target):
            mark_alert_triggered(alert_id)
            triggered_now.append((ticker, target, direction, note, cur))
    return triggered_now


# אתחול מסד הנתונים
setup_database()

# ==============================================================================
# 4. ניהול זיכרון וסנכרון מצב (Application Dynamic State)
# ==============================================================================

# ---- Auth session state ----
if 'auth_user' not in st.session_state:
    st.session_state.auth_user = None          # None = לא מחובר

if 'auth_page' not in st.session_state:
    st.session_state.auth_page = 'login'       # 'login' | 'register'

# ---- App session state ----
if 'h_master_scan_results' not in st.session_state:
    st.session_state.h_master_scan_results = None

if 'h_scan_time_reference' not in st.session_state:
    st.session_state.h_scan_time_reference = None

if 'alerts_triggered_display' not in st.session_state:
    st.session_state.alerts_triggered_display = []

if 'show_admin_panel' not in st.session_state:
    st.session_state.show_admin_panel = False

# ==============================================================================
# 5. מנוע ניתוח נתונים קוונטי (Quantitative Strategic Intelligence)
# ==============================================================================

def calculate_rsi(prices, window=14):
    """
    חישוב RSI (Relative Strength Index) מדויק.
    מבצע החלקה של השינויים במחירי הסגירה לזיהוי רמות קיצון (Oversold/Overbought).
    מדד בסיסי לזיהוי היפוכי מגמה בשוק האמריקאי.
    """
    diff     = prices.diff()
    gain     = diff.mask(diff < 0, 0)
    loss     = -diff.mask(diff > 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs       = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def analyze_stock(symbol):
    """
    פונקציית הניתוח האסטרטגי הממשי.
    מבצעת:
      1. הורדת נתוני OHLCV (60 ימים) מ-Yahoo Finance.
      2. חישוב RSI, MACD, Bollinger Bands.
      3. קביעת רמות Stop Loss ו-Target Price מ-Bollinger Bands.
      4. מנוע החלטות: STRONG BUY / BUY / SELL / TRENDING / HOLD.
      5. שליפת נתוני חברה: סקטור, דוח קרוב, המלצת אנליסטים.
    מחזירה dict מלא של נתוני הניתוח, או None בכישלון.
    """
    try:
        ticker_obj = yf.Ticker(symbol)
        raw_df     = ticker_obj.history(period="60d")

        if raw_df.empty or len(raw_df) < 30:
            return None

        close = raw_df['Close']

        # RSI
        rsi_s   = calculate_rsi(close)
        rsi_val = float(rsi_s.iloc[-1])

        # MACD
        ema12       = close.ewm(span=12, adjust=False).mean()
        ema26       = close.ewm(span=26, adjust=False).mean()
        macd_line   = ema12 - ema26
        macd_signal = macd_line.ewm(span=9, adjust=False).mean()
        momentum    = "Bullish 🟢" if macd_line.iloc[-1] > macd_signal.iloc[-1] else "Bearish 🔴"

        # Bollinger Bands (20, 2)
        sma20    = close.rolling(window=20).mean()
        std20    = close.rolling(window=20).std()
        bb_upper = sma20 + (std20 * 2)
        bb_lower = sma20 - (std20 * 2)

        # מחיר ושינוי יומי
        price_now  = float(close.iloc[-1])
        price_prev = float(close.iloc[-2])
        daily_chg  = ((price_now - price_prev) / price_prev) * 100
        sl_level   = float(bb_lower.iloc[-1])
        tp_level   = float(bb_upper.iloc[-1])

        # מנוע החלטות
        signal = 'HOLD ⏸️'
        if rsi_val < 32 and price_now <= (sl_level * 1.03):
            signal = 'STRONG BUY 🚀🚀'
        elif rsi_val < 35:
            signal = 'BUY (OVERSOLD) 🛒'
        elif rsi_val > 69 or price_now >= (float(bb_upper.iloc[-1]) * 0.98):
            signal = 'SELL (OVERBOUGHT) ⚠️'
        elif price_now > float(sma20.iloc[-1]) and macd_line.iloc[-1] > macd_signal.iloc[-1]:
            signal = 'TRENDING UP 📈'

        # נתוני חברה
        info          = ticker_obj.info
        earnings_date = "N/A"
        try:
            cal = ticker_obj.calendar
            if cal is not None and not cal.empty:
                earnings_date = cal.iloc[0, 0].strftime('%Y-%m-%d')
        except:
            pass

        return {
            'מניה':            symbol,
            'מחיר ($)':        f"{price_now:.2f}",
            'שינוי (%)':       f"{daily_chg:+.2f}",
            'RSI':             f"{rsi_val:.1f}",
            'MACD מגמה':       momentum,
            'Stop Loss':       f"{sl_level:.2f}",
            'Target Price':    f"{tp_level:.2f}",
            'סקטור':           info.get('sector', 'N/A'),
            'דוח קרוב':        earnings_date,
            'המלצת אנליסטים': str(info.get('recommendationKey', 'N/A')).title().replace('_', ' '),
            'סיגנל':           signal
        }
    except:
        return None

# ==============================================================================
# 6. Market Overview — סקירת שוק בזמן אמת (S&P 500 + Nasdaq + Dow + VIX)
# ==============================================================================

def render_market_overview():
    """
    מנגנון סקירת השוק הגלובלי בראש עמוד הבית.
    שולף נתוני מחיר ושינוי יומי לארבעת המדדים המרכזיים:
      - S&P 500  (^GSPC) — המדד הרחב של השוק האמריקאי.
      - Nasdaq 100 (^NDX) — מדד טכנולוגיה ומניות צמיחה.
      - Dow Jones  (^DJI) — מדד התעשייה האמריקאי הוותיק.
      - VIX       (^VIX) — מדד הפחד — רמת התנודתיות הצפויה.
    מציג Sparkline עם fill ב-rgba ותיקון מלא ל-MultiIndex.
    כל מדד עטוף ב-try/except עצמאי — כשל אחד לא חוסם את השאר.
    """
    indices = [
        {"symbol": "^GSPC", "label": "S&P 500",    "color": "#007bff", "fill": "rgba(0, 123, 255, 0.10)"},
        {"symbol": "^NDX",  "label": "Nasdaq 100", "color": "#28a745", "fill": "rgba(40, 167, 69, 0.10)"},
        {"symbol": "^DJI",  "label": "Dow Jones",  "color": "#ff7f0e", "fill": "rgba(255, 127, 14, 0.10)"},
        {"symbol": "^VIX",  "label": "VIX (פחד)",  "color": "#dc3545", "fill": "rgba(220, 53, 69, 0.10)"},
    ]

    st.markdown("""
    <div class="market-overview-banner">
        <p style="color:#a0bfd0; font-size:1.2rem; margin:0 0 8px 0;
                  text-align:center; letter-spacing:3px; font-weight:700;">
            LIVE MARKET OVERVIEW
        </p>
        <p style="color:#ffffff; font-size:1.5rem; margin:0;
                  text-align:center; font-weight:600; opacity:0.7;">
            מדדי שוק בזמן אמת — נתונים מעודכנים מ-Yahoo Finance
        </p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    for i, idx in enumerate(indices):
        with cols[i]:
            try:
                raw = yf.download(
                    idx["symbol"], period="1mo", interval="1d",
                    progress=False, auto_adjust=True
                )
                if isinstance(raw.columns, pd.MultiIndex):
                    raw.columns = raw.columns.get_level_values(0)
                if raw.empty or len(raw) < 2:
                    raise ValueError("אין נתונים")

                cur_price    = float(raw['Close'].iloc[-1])
                prev_close   = float(raw['Close'].iloc[-2])
                chg_pct      = ((cur_price - prev_close) / prev_close) * 100
                chg_color    = "#2ecc71" if chg_pct >= 0 else "#e74c3c"
                chg_arrow    = "▲" if chg_pct >= 0 else "▼"

                spark = go.Figure()
                spark.add_trace(go.Scatter(
                    x=list(range(len(raw))), y=raw['Close'],
                    mode='lines', line=dict(color=idx["color"], width=2.5),
                    fill='tozeroy', fillcolor=idx["fill"], showlegend=False
                ))
                spark.update_layout(
                    height=90, margin=dict(l=0, r=0, t=0, b=0),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(visible=False), yaxis=dict(visible=False)
                )
                price_fmt = f"{cur_price:,.2f}" if cur_price > 100 else f"{cur_price:.2f}"
                st.markdown(f"""
                <div style="background:#ffffff; border-radius:22px; padding:22px 28px 12px 28px;
                     border:1.5px solid #e9ecef; box-shadow:0 8px 28px rgba(0,0,0,0.07);
                     text-align:center; margin-bottom:6px;">
                    <p style="font-size:1.05rem; color:#888; margin:0 0 4px 0;
                              font-weight:700; letter-spacing:1px;">{idx['label']}</p>
                    <p style="font-size:1.9rem; font-weight:900; color:#1a1a1a;
                              margin:0 0 4px 0; direction:ltr;">{price_fmt}</p>
                    <p style="font-size:1.25rem; font-weight:800; color:{chg_color};
                              margin:0; direction:ltr;">{chg_arrow} {abs(chg_pct):.2f}%</p>
                </div>
                """, unsafe_allow_html=True)
                st.plotly_chart(spark, use_container_width=True, config={"displayModeBar": False})

            except Exception:
                st.markdown(f"""
                <div style="background:#fff8f8; border-radius:22px; padding:22px 28px;
                     border:1.5px solid #f5c6cb; text-align:center; margin-bottom:6px;">
                    <p style="font-size:1.05rem; color:#888; margin:0 0 8px 0; font-weight:700;">
                        {idx['label']}</p>
                    <p style="font-size:1.4rem; color:#dc3545; margin:0; font-weight:700;">
                        ⚠️ לא זמין כרגע</p>
                    <p style="font-size:0.95rem; color:#aaa; margin:6px 0 0 0;">{idx['symbol']}</p>
                </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# 7. רכיב ויזואלי: מדד סיכון RSI (Risk Gauge)
# ==============================================================================

def render_risk_gauge(stock_row):
    """
    Gauge Indicator המציג את רמת הסיכון לפי ערך ה-RSI.
    ירוק (0-35) = אזור oversold/הזדמנות.
    צהוב (35-70) = ניטרלי.
    אדום (70-100) = קנייה יתרה / סיכון גבוה.
    """
    rsi_val  = float(stock_row['RSI'])
    gauge    = go.Figure(go.Indicator(
        mode="gauge+number",
        value=rsi_val,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "מדד סיכון כניסה (RSI)", 'font': {'size': 32, 'color': '#1a1a1a'}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "#000"},
            'bar': {'color': "#212529"},
            'bgcolor': "#ffffff",
            'borderwidth': 6,
            'bordercolor': "#dee2e6",
            'steps': [
                {'range': [0,   35], 'color': '#28a745'},
                {'range': [35,  70], 'color': '#ffc107'},
                {'range': [70, 100], 'color': '#dc3545'}
            ],
            'threshold': {'line': {'color': "black", 'width': 10}, 'thickness': 0.95, 'value': rsi_val}
        }
    ))
    gauge.update_layout(
        paper_bgcolor="white",
        font={'color': "black", 'family': "Assistant"},
        height=480,
        margin=dict(l=60, r=60, t=110, b=60)
    )
    st.plotly_chart(gauge, use_container_width=True)

# ==============================================================================
# 8. פרוטוקול פעולה טקטי (Operational Action Protocol)
# ==============================================================================

def render_action_protocol(row_data):
    """
    פרוטוקול הפעולה האסטרטגי — ממיר נתונים טכניים להוראות ביצוע בשפה אנושית.
    מציג: כותרת צבעונית, כרטיסי Entry/SL, ותוכנית פעולה מפורטת.
    """
    ticker       = row_data['מניה']
    signal       = row_data['סיגנל']
    price        = float(row_data['מחיר ($)'])
    sl           = float(row_data['Stop Loss'])
    tp           = float(row_data['Target Price'])
    color_map    = {'STRONG BUY': '#28a745', 'BUY': '#28a745', 'SELL': '#dc3545', 'TRENDING': '#007bff', 'HOLD': '#ffc107'}
    active_color = color_map.get(signal.split()[0], '#000000')

    st.markdown(f"""
    <div style="background-color:#ffffff; border-right:32px solid {active_color}; padding:55px;
         border-radius:45px; border:1px solid #e9ecef; box-shadow:0 25px 80px rgba(0,0,0,0.08);
         margin-bottom:45px;">
        <h2 style="margin-top:0; color:{active_color}; font-size:3.2rem; font-weight:950;
                   direction:rtl; text-align:right; border:none; padding:0;">
            ⚡ פרוטוקול ביצוע: {ticker}
        </h2>
        <p style="font-size:1.9rem; color:#555; direction:rtl; text-align:right; margin-top:15px;">
            <b>החלטת המערכת:</b>
            <span style="color:{active_color}; font-weight:900;">{signal}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div style="background:#f8f9fa; padding:45px; border-radius:40px; border:1px solid #eee;
             text-align:right; direction:rtl; box-shadow:0 12px 30px rgba(0,0,0,0.025);">
            <b style="color:#28a745; font-size:2rem;">📍 נקודת כניסה (Entry)</b><br>
            <div style="margin-top:25px; font-size:1.7rem; line-height:1.8;">
                מחיר שוק נוכחי: <span class="num-fix">${price}</span><br>
                טווח כניסה מקסימלי: <span class="num-fix">${price * 1.01:.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        risk_pct = ((price - sl) / price) * 100
        st.markdown(f"""
        <div style="background:#f8f9fa; padding:45px; border-radius:40px; border:1px solid #eee;
             text-align:right; direction:rtl; box-shadow:0 12px 30px rgba(0,0,0,0.025);">
            <b style="color:#dc3545; font-size:2rem;">🛑 פקודת הגנה (Stop Loss)</b><br>
            <div style="margin-top:25px; font-size:1.7rem; line-height:1.8;">
                יציאה בשבירת: <span class="num-fix">${sl}</span><br>
                סיכון בעסקה: <span class="num-fix">{risk_pct:.1f}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if "BUY" in signal:
        plan = "המניה נמצאת במחיר 'מציאה' טכני קיצוני ביחס לממוצע 20 הימים. פתח פוזיציה והגדר סטופ לוס קשיח בערך המצוין."
    elif "TRENDING" in signal:
        plan = "המומנטום כרגע לטובתך. הצטרף לגל העליות הקיים והעלה את פקודת הסטופ לוס (Trailing SL) בכל שיא יומי חדש."
    elif "SELL" in signal:
        plan = "אזהרה: המניה מתוחה כלפי מעלה (Overextended). אל תפתח פוזיציה חדשה. שקול מימוש רווחים חלקי."
    else:
        plan = f"המתנה מחוץ לשוק (No Trade Zone). המחיר רחוק מרמת התמיכה האידיאלית. מומלץ לחכות לתיקון (Pullback) לאזור ${sl}."

    potential = ((tp - price) / price) * 100
    st.markdown(f"""
    <div style="margin-top:60px; background:#ffffff; padding:60px; border-radius:45px;
         border:5px dashed #007bff; direction:rtl; text-align:right;
         box-shadow:0 25px 60px rgba(0,123,255,0.07);">
        <b style="color:#007bff; font-size:2.3rem;">📝 הנחיות ביצוע:</b><br>
        <div style="margin-top:40px; font-size:1.8rem; line-height:2.5;">
            <p>• {plan}</p>
            <p style="border-top:4px solid #f1f3f5; padding-top:35px; margin-top:35px;">
                🎯 <b>יעד מימוש רווחים (Take Profit):</b>
                <span class="num-fix">${tp}</span>
                (פוטנציאל: <span class="num-fix">{potential:.1f}%</span>)
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 9. [שדרוג] גרף TradingView Advanced Chart Widget
# ==============================================================================

def render_tradingview_chart(ticker_str):
    """
    [שדרוג מרכזי] גרף TradingView Advanced Chart Widget — מחליף את גרף Plotly הרגיל.
    TradingView מציע:
      - כלי ציור מלאים: קווי מגמה, ערוצים, מנהרות Fibonacci, אנכי/אופקי.
      - אינדיקטורים ידניים: RSI, MACD, Bollinger, Ichimoku, EMA, SMA ועוד 100+.
      - בחירת timeframe: 1m, 5m, 15m, 1h, 4h, 1D, 1W, 1M.
      - מצב כהה/בהיר, שמירת layout, חיפוש מניות.
    הוזרק דרך st.components.v1.html() עם iframe מלא-רוחב.

    הערה: TradingView Widget הינו שירות חינמי ל-Webmaster. הנתונים
    מוצגים כגרף interactive מלא, כולל L2 data ו-replay mode.
    """
    # נרמול הסימול לפורמט TradingView (NASDAQ:AAPL)
    tv_symbol_map = {
        "AAPL": "NASDAQ:AAPL", "MSFT": "NASDAQ:MSFT", "GOOGL": "NASDAQ:GOOGL",
        "GOOG": "NASDAQ:GOOG", "AMZN": "NASDAQ:AMZN", "TSLA": "NASDAQ:TSLA",
        "NVDA": "NASDAQ:NVDA", "META": "NASDAQ:META", "NFLX": "NASDAQ:NFLX",
        "AMD":  "NASDAQ:AMD",  "INTC": "NASDAQ:INTC", "CSCO": "NASDAQ:CSCO",
        "ADBE": "NASDAQ:ADBE", "QCOM": "NASDAQ:QCOM", "TXN":  "NASDAQ:TXN",
        "AVGO": "NASDAQ:AVGO", "COST": "NASDAQ:COST", "PEP":  "NASDAQ:PEP",
        "TMUS": "NASDAQ:TMUS", "INTU": "NASDAQ:INTU", "AMAT": "NASDAQ:AMAT",
        "ISRG": "NASDAQ:ISRG", "HON":  "NASDAQ:HON",  "AMGN": "NASDAQ:AMGN",
        "VRTX": "NASDAQ:VRTX", "SBUX": "NASDAQ:SBUX", "PLTR": "NYSE:PLTR",
        "COIN": "NASDAQ:COIN", "MSTR": "NASDAQ:MSTR", "JPM":  "NYSE:JPM",
        "BAC":  "NYSE:BAC",    "GS":   "NYSE:GS",     "WMT":  "NYSE:WMT",
        "DIS":  "NYSE:DIS",    "BA":   "NYSE:BA",      "XOM":  "NYSE:XOM",
        "CVX":  "NYSE:CVX",    "JNJ":  "NYSE:JNJ",     "UNH":  "NYSE:UNH",
    }
    tv_symbol = tv_symbol_map.get(ticker_str.upper(), f"NASDAQ:{ticker_str.upper()}")

    tradingview_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                margin: 0;
                padding: 0;
                background: #ffffff;
                font-family: 'Assistant', sans-serif;
            }}
            .tv-header {{
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                padding: 14px 24px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-radius: 18px 18px 0 0;
            }}
            .tv-header-title {{
                color: #ffffff;
                font-size: 1.2rem;
                font-weight: 800;
                letter-spacing: 1px;
            }}
            .tv-header-badge {{
                background: rgba(0,123,255,0.25);
                color: #66b2ff;
                padding: 4px 14px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 700;
                border: 1px solid rgba(0,123,255,0.4);
            }}
            .tradingview-widget-container {{
                width: 100%;
                height: 650px;
            }}
        </style>
    </head>
    <body>
        <div class="tv-header">
            <div class="tv-header-title">
                📈 TradingView Advanced Chart — {ticker_str.upper()}
            </div>
            <div class="tv-header-badge">
                ✏️ כלי ציור | 📊 100+ אינדיקטורים | 🕐 Multi-Timeframe
            </div>
        </div>

        <div class="tradingview-widget-container">
            <div id="tradingview_chart"></div>
            <script type="text/javascript"
                src="https://s3.tradingview.com/tv.js">
            </script>
            <script type="text/javascript">
            new TradingView.widget({{
                "width":            "100%",
                "height":           650,
                "symbol":           "{tv_symbol}",
                "interval":         "D",
                "timezone":         "America/New_York",
                "theme":            "light",
                "style":            "1",
                "locale":           "en",
                "toolbar_bg":       "#f1f3f6",
                "enable_publishing": false,
                "allow_symbol_change": true,
                "watchlist":        [
                    "NASDAQ:NVDA", "NASDAQ:TSLA", "NASDAQ:AAPL",
                    "NASDAQ:MSFT", "NASDAQ:META", "NASDAQ:GOOGL",
                    "NASDAQ:AMD",  "NASDAQ:AMZN", "NYSE:PLTR"
                ],
                "details":          true,
                "hotlist":          true,
                "calendar":         true,
                "studies":          [
                    "MASimple@tv-builtin",
                    "RSI@tv-builtin",
                    "MACD@tv-builtin",
                    "BB@tv-builtin"
                ],
                "show_popup_button": true,
                "popup_width":      "1000",
                "popup_height":     "650",
                "container_id":     "tradingview_chart"
            }});
            </script>
        </div>
    </body>
    </html>
    """
    components.html(tradingview_html, height=710, scrolling=False)


def render_advanced_chart_fallback(ticker_str):
    """
    גרף Plotly רגיל — פלבק לסביבות שלא תומכות ב-components.v1.html.
    כולל: נרות יפניים + MA20 + MA50 + Volume צבעוני.
    """
    try:
        df = yf.download(ticker_str, period="4mo", interval="1d", progress=False)
        if df.empty:
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        ma20      = df['Close'].rolling(window=20).mean()
        ma50      = df['Close'].rolling(window=50).mean()
        vol_colors = [
            '#2ecc71' if float(df['Close'].iloc[i]) >= float(df['Open'].iloc[i]) else '#e74c3c'
            for i in range(len(df))
        ]

        fig = make_subplots(
            rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.04,
            row_heights=[0.73, 0.27],
            subplot_titles=(f"נרות + MA20/MA50: {ticker_str}", "Volume")
        )
        fig.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], name=ticker_str,
            increasing_line_color='#2ecc71', decreasing_line_color='#e74c3c'
        ), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=ma20, mode='lines', name='MA 20',
            line=dict(color='#007bff', width=2.5)), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=ma50, mode='lines', name='MA 50',
            line=dict(color='#ff7f0e', width=2.5)), row=1, col=1)
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=vol_colors,
            opacity=0.75, showlegend=False), row=2, col=1)
        fig.update_layout(
            template="plotly_white", xaxis_rangeslider_visible=False, height=700,
            margin=dict(l=50, r=50, t=80, b=50),
            font=dict(family="Assistant", size=16),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified"
        )
        return fig
    except:
        return None

# ==============================================================================
# 10. השוואת ביצועים ראש-בראש (Stock Versus)
# ==============================================================================

def render_versus_chart(ticker_a, ticker_b):
    """
    גרף השוואת ביצועים מנורמל (Base 100) ל-6 חודשים.
    מאפשר זיהוי עוצמה יחסית (Relative Strength) בין שתי מניות.
    """
    try:
        data = yf.download([ticker_a, ticker_b], period="6mo", interval="1d", progress=False)['Close']
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(1)
        norm = (data / data.iloc[0]) * 100

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=norm.index, y=norm[ticker_a], name=ticker_a,
            line=dict(color='#007bff', width=6)))
        fig.add_trace(go.Scatter(x=norm.index, y=norm[ticker_b], name=ticker_b,
            line=dict(color='#ff7f0e', width=6)))
        fig.update_layout(
            title=f"⚔️ השוואת ביצועים: {ticker_a} מול {ticker_b} (6 חודשים)",
            yaxis_title="תשואה מנורמלת (%)", template="plotly_white", height=700,
            margin=dict(l=50, r=50, t=110, b=50),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=18)),
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
        ret_a = norm[ticker_a].iloc[-1] - 100
        ret_b = norm[ticker_b].iloc[-1] - 100
        st.success(f"📈 **תוצאות:** {ticker_a}: {ret_a:+.1f}% | {ticker_b}: {ret_b:+.1f}%")
    except Exception as e:
        st.error(f"שגיאה בהשוואה: {e}")

# ==============================================================================
# 11. חדשות חיות (Live News Feed)
# ==============================================================================

def render_live_news(ticker_id):
    """
    פיד חדשות חיות מ-Yahoo Finance — 3 כתבות אחרונות בעיצוב כרטיסיות.
    תמיכה רב-מבנית ב-API ה-content החדש של Yahoo Finance.
    """
    try:
        news_items = yf.Ticker(ticker_id).news
        if not news_items:
            st.write(f"לא נמצאו חדשות עבור {ticker_id}.")
            return
        st.markdown(f"#### 📰 כותרות אחרונות: {ticker_id}")
        shown = 0
        for item in news_items:
            if shown >= 3:
                break
            content  = item.get('content', item)
            headline = content.get('title', None)
            if not headline:
                continue
            link     = content.get('clickThroughUrl', {}).get('url', None) or content.get('link', '#')
            provider = content.get('provider', {}).get('displayName', None) or content.get('publisher', 'מקור חדשותי')
            st.markdown(f"""
            <div style="background:#fff; padding:35px; border-radius:30px; margin-bottom:25px;
                 border-right:12px solid #007bff; border:1px solid #e9ecef;
                 box-shadow:0 10px 30px rgba(0,0,0,0.05);">
                <a href="{link}" target="_blank"
                   style="color:#007bff; text-decoration:none; font-weight:900; font-size:1.65rem;">
                    {headline}
                </a><br>
                <div style="margin-top:18px; color:#6c757d; font-size:1.25rem; font-weight:700;">
                    מקור: {provider}
                </div>
            </div>
            """, unsafe_allow_html=True)
            shown += 1
    except Exception as e:
        st.write(f"שגיאה בטעינת חדשות: {e}")

# ==============================================================================
# 12. מנוע AI Insight — ניתוח מילולי מפורט (P/E + Sentiment)
# ==============================================================================

def render_ai_insight(ticker_symbol):
    """
    AI Insight — ניתוח מילולי אינטליגנטי בשני ממדים:
    א. ניתוח P/E: Trailing, Forward, השוואה לסקטור, P/B, מרווח, צמיחה.
    ב. סנטימנט: קונצנזוס אנליסטים, יעד מחיר, Beta, טווח שנתי.
    כל נתונים מ-Yahoo Finance, מוצגים בכרטיס HTML מעוצב.
    """
    try:
        info          = yf.Ticker(ticker_symbol).info
        trailing_pe   = info.get('trailingPE', None)
        forward_pe    = info.get('forwardPE', None)
        pb_ratio      = info.get('priceToBook', None)
        sector        = info.get('sector', 'N/A')
        industry      = info.get('industry', 'N/A')
        market_cap    = info.get('marketCap', None)
        rev_growth    = info.get('revenueGrowth', None)
        earn_growth   = info.get('earningsGrowth', None)
        profit_margin = info.get('profitMargins', None)
        analyst_target = info.get('targetMeanPrice', None)
        analyst_rec   = str(info.get('recommendationKey', 'N/A')).title().replace('_', ' ')
        current_price = info.get('currentPrice', None)
        beta          = info.get('beta', None)
        high_52w      = info.get('fiftyTwoWeekHigh', None)
        low_52w       = info.get('fiftyTwoWeekLow', None)

        sector_pe_map = {
            'Technology': 28.0, 'Healthcare': 22.0, 'Financial Services': 14.0,
            'Consumer Cyclical': 20.0, 'Communication Services': 22.0,
            'Industrials': 19.0, 'Consumer Defensive': 21.0, 'Energy': 12.0,
            'Basic Materials': 16.0, 'Real Estate': 30.0, 'Utilities': 18.0,
        }
        sector_pe_ref = sector_pe_map.get(sector, 20.0)

        if trailing_pe is not None and trailing_pe > 0:
            pe_num  = float(trailing_pe)
            pe_diff = ((pe_num - sector_pe_ref) / sector_pe_ref) * 100
            if pe_num < sector_pe_ref * 0.80:
                pe_verdict = "🟢 <b>זול משמעותית</b> ביחס לממוצע הסקטור"
                pe_text = f"מכפיל {pe_num:.1f}x — נמוך ב-{abs(pe_diff):.0f}% מהממוצע ({sector_pe_ref:.0f}x). תמחור חסר פוטנציאלי."
            elif pe_num < sector_pe_ref * 1.15:
                pe_verdict = "🟡 <b>הערכת שווי הוגנת</b>"
                pe_text = f"מכפיל {pe_num:.1f}x — קרוב לממוצע הסקטור ({sector_pe_ref:.0f}x). תמחור שוויוני ומאוזן."
            elif pe_num < sector_pe_ref * 1.50:
                pe_verdict = "🟠 <b>נסחרת בפרמיה</b> מעל ממוצע הסקטור"
                pe_text = f"מכפיל {pe_num:.1f}x — גבוה ב-{pe_diff:.0f}% מהממוצע. פרמיה מוצדקת ע"
                pe_text += "י צמיחה ויתרון תחרותי."
            else:
                pe_verdict = "🔴 <b>מכפיל גבוה מאוד</b> — סיכון תמחור"
                pe_text = f"מכפיל {pe_num:.1f}x — גבוה ב-{pe_diff:.0f}% מהממוצע ההיסטורי. ציפיות אגרסיביות."
        else:
            pe_num = None
            pe_verdict = "⚪ <b>נתון חסר</b> — P/E לא זמין"
            pe_text = "מכפיל הרווח אינו זמין. ייתכן שהחברה אינה רווחית. יש להתמקד בניתוח טכני."

        if forward_pe is not None and forward_pe > 0:
            fwd = float(forward_pe)
            if pe_num and pe_num > 0:
                comp = pe_num - fwd
                if comp > 2:
                    fwd_text = f"Forward P/E: {fwd:.1f}x — נמוך ב-{comp:.1f} נקודות. <b>ציפיות צמיחה חיוביות.</b>"
                elif comp < -2:
                    fwd_text = f"Forward P/E: {fwd:.1f}x — גבוה ב-{abs(comp):.1f} נקודות. <b>ציפיות להאטה ברווחים.</b>"
                else:
                    fwd_text = f"Forward P/E: {fwd:.1f}x — דומה לנוכחי. <b>יציבות בציפיות.</b>"
            else:
                fwd_text = f"Forward P/E: {fwd:.1f}x."
        else:
            fwd_text = "Forward P/E אינו זמין."

        sentiment_map = {
            'Strong Buy':  ('🟢', 'חיובי ביותר', 'קנייה חזקה — ציפיות גבוהות'),
            'Buy':         ('🟢', 'חיובי', 'רוב האנליסטים ממליצים קנייה'),
            'Hold':        ('🟡', 'ניטרלי', 'חוסר ודאות — המתן לאות ברור'),
            'Sell':        ('🔴', 'שלילי', 'המלצת מכירה — השוק כבר מגלם את הפוטנציאל'),
            'Strong Sell': ('🔴', 'שלילי ביותר', 'סיכון גבוה לירידה משמעותית'),
        }
        s_icon, s_label, s_desc = sentiment_map.get(analyst_rec, ('⚪', 'לא ידוע', 'אין המלצת אנליסטים'))

        if analyst_target and current_price and float(current_price) > 0:
            upside = ((float(analyst_target) - float(current_price)) / float(current_price)) * 100
            tp_fmt = f"${float(analyst_target):.2f}"
            if upside > 15:
                target_text = f"יעד מחיר: <b>{tp_fmt}</b> — פוטנציאל <b>{upside:.1f}%</b>. אטרקטיבי ביותר."
            elif upside > 5:
                target_text = f"יעד מחיר: <b>{tp_fmt}</b> — פוטנציאל מתון <b>{upside:.1f}%</b>."
            elif upside > -5:
                target_text = f"יעד מחיר: <b>{tp_fmt}</b> — קרוב למחיר הנוכחי (Fair Value)."
            else:
                target_text = f"יעד מחיר: <b>{tp_fmt}</b> — נמוך ב-<b>{abs(upside):.1f}%</b> מהנוכחי. סיכון תמחור יתר."
        else:
            target_text = "יעד מחיר ממוצע אינו זמין."

        if beta is not None:
            b = float(beta)
            b_fmt = f"{b:.2f}"
            if b > 1.5:
                beta_text = f"<b>Beta={b_fmt}</b> — תנודתיות גבוהה מאוד."
            elif b > 1.0:
                beta_text = f"<b>Beta={b_fmt}</b> — תנודתיות מעל ממוצע."
            elif b > 0.5:
                beta_text = f"<b>Beta={b_fmt}</b> — תנודתיות נמוכה יחסית."
            else:
                beta_text = f"<b>Beta={b_fmt}</b> — תנודתיות נמוכה מאוד. עוגן יציב."
        else:
            beta_text = "Beta אינו זמין."

        if high_52w and low_52w and current_price:
            rng    = ((float(current_price) - float(low_52w)) / (float(high_52w) - float(low_52w))) * 100
            r_fmt  = f"{rng:.0f}%"
            h_fmt  = f"${float(high_52w):.2f}"
            l_fmt  = f"${float(low_52w):.2f}"
            if rng > 80:
                range_text = f"נסחרת ב-<b>{r_fmt}</b> מהטווח השנתי — קרובה לשיא ({h_fmt})."
            elif rng > 40:
                range_text = f"נסחרת ב-<b>{r_fmt}</b> מהטווח השנתי — אזור ביניים ({l_fmt}–{h_fmt})."
            else:
                range_text = f"נסחרת ב-<b>{r_fmt}</b> מהטווח השנתי — קרובה למינימום ({l_fmt})."
        else:
            range_text = "נתוני טווח שנתי אינם זמינים."

        cap_html    = f' | שווי שוק: <b>${market_cap/1e9:.1f}B</b>' if market_cap else ""
        pb_html     = f'<p style="font-size:1.3rem; color:#666;">P/B: <b>{float(pb_ratio):.1f}x</b></p>' if pb_ratio else ""
        margin_html = f'<p style="font-size:1.3rem; color:#666;">מרווח רווח נקי: <b>{float(profit_margin)*100:.1f}%</b></p>' if profit_margin else ""
        rev_html    = (f'<p style="font-size:1.3rem; color:{"#28a745" if rev_growth and rev_growth>0 else "#dc3545"};">צמיחת הכנסות: <b>{float(rev_growth)*100:+.1f}%</b></p>' if rev_growth else "")
        earn_html   = (f'<p style="font-size:1.3rem; color:{"#28a745" if earn_growth and earn_growth>0 else "#dc3545"};">צמיחת רווחים: <b>{float(earn_growth)*100:+.1f}%</b></p>' if earn_growth else "")

        card = (
            '<div class="ai-insight-card">'
            '<h3 style="color:#007bff; font-size:2.4rem; margin-top:0; border:none; padding:0;">'
            + f'🤖 AI Insight — ניתוח אינטליגנטי: {ticker_symbol}</h3>'
            + f'<p style="color:#6c757d; font-size:1.3rem; margin-bottom:40px;">סקטור: <b>{sector}</b> | תעשייה: <b>{industry}</b>' + cap_html + '</p>'
            + '<hr style="border-color:#e9ecef; margin:30px 0;">'
            + '<h4 style="color:#2c3e50; font-size:1.9rem; border:none; padding:0; margin-top:0;">📊 חלק א׳: P/E Analysis</h4>'
            + f'<p style="font-size:1.5rem;"><b>הערכת שווי:</b> {pe_verdict}</p>'
            + f'<p style="font-size:1.4rem; color:#444; line-height:2.0;">{pe_text}</p>'
            + f'<p style="font-size:1.4rem; color:#444; line-height:2.0;">{fwd_text}</p>'
            + pb_html + margin_html + rev_html + earn_html
            + '<hr style="border-color:#e9ecef; margin:30px 0;">'
            + '<h4 style="color:#2c3e50; font-size:1.9rem; border:none; padding:0; margin-top:0;">🌡️ חלק ב׳: Market Sentiment</h4>'
            + f'<p style="font-size:1.5rem;"><b>קונצנזוס:</b> {s_icon} <b>{analyst_rec}</b> — {s_label}</p>'
            + f'<p style="font-size:1.4rem; color:#444;">{s_desc}</p>'
            + f'<p style="font-size:1.4rem; color:#444; line-height:2.0;">{target_text}</p>'
            + f'<p style="font-size:1.4rem; color:#444; line-height:2.0;">{beta_text}</p>'
            + f'<p style="font-size:1.4rem; color:#444; line-height:2.0;">{range_text}</p>'
            + '<hr style="border-color:#e9ecef; margin:30px 0;">'
            + '<p style="font-size:1.2rem; color:#adb5bd; text-align:center;">* הניתוח נוצר אוטומטית על בסיס Yahoo Finance | אינו מהווה המלצת השקעה</p>'
            + '</div>'
        )
        st.markdown(card, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"שגיאה במנוע AI Insight: {e}")

# ==============================================================================
# 13. Multi-Chart — 4 מניות במקביל
# ==============================================================================

def render_multi_chart(ticker_list):
    """
    Multi-Chart Dashboard — פריסת 2×2 עם עד 4 מניות.
    כל פאנל: נרות יפניים + MA20 (כחול) + MA50 (כתום) + Volume צבעוני.
    מאפשר השוואה ויזואלית מהירה של דפוסי מסחר מרובים בלחיצה אחת.
    """
    if not ticker_list:
        st.warning("לא נבחרו מניות.")
        return

    tickers = ticker_list[:4]
    layout  = ([[tickers[0]]] if len(tickers) == 1 else
               [[tickers[0], tickers[1]]] if len(tickers) == 2 else
               [[tickers[0], tickers[1]], [tickers[2]]] if len(tickers) == 3 else
               [[tickers[0], tickers[1]], [tickers[2], tickers[3]]])

    for row in layout:
        cols = st.columns(len(row))
        for ci, t in enumerate(row):
            with cols[ci]:
                try:
                    df = yf.download(t, period="2mo", interval="1d", progress=False)
                    if df.empty:
                        st.error(f"אין נתונים: {t}")
                        continue
                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = df.columns.get_level_values(0)

                    ma20 = df['Close'].rolling(20).mean()
                    ma50 = df['Close'].rolling(50).mean()
                    vcol = ['#2ecc71' if float(df['Close'].iloc[i]) >= float(df['Open'].iloc[i]) else '#e74c3c'
                            for i in range(len(df))]
                    chg     = ((float(df['Close'].iloc[-1]) - float(df['Close'].iloc[0])) / float(df['Close'].iloc[0])) * 100
                    chg_col = "#28a745" if chg >= 0 else "#e74c3c"
                    chg_sym = "▲" if chg >= 0 else "▼"

                    mf = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                       vertical_spacing=0.05, row_heights=[0.72, 0.28])
                    mf.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                        low=df['Low'], close=df['Close'], name=t,
                        increasing_line_color='#2ecc71', decreasing_line_color='#e74c3c',
                        showlegend=False), row=1, col=1)
                    mf.add_trace(go.Scatter(x=df.index, y=ma20, mode='lines', name='MA20',
                        line=dict(color='#007bff', width=1.8), showlegend=False), row=1, col=1)
                    mf.add_trace(go.Scatter(x=df.index, y=ma50, mode='lines', name='MA50',
                        line=dict(color='#ff7f0e', width=1.8), showlegend=False), row=1, col=1)
                    mf.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=vcol,
                        opacity=0.70, showlegend=False), row=2, col=1)
                    mf.update_layout(
                        title=dict(text=f"<b>{t}</b>  <span style='color:{chg_col};'>"
                                        f"{chg_sym}{abs(chg):.1f}%</span>  | ${float(df['Close'].iloc[-1]):.2f}",
                                   font=dict(size=16, family="Assistant")),
                        template="plotly_white", xaxis_rangeslider_visible=False,
                        height=480, margin=dict(l=25, r=25, t=70, b=25),
                        font=dict(family="Assistant", size=12), hovermode="x unified"
                    )
                    mf.update_yaxes(title_text="$",   row=1, col=1, title_font_size=11)
                    mf.update_yaxes(title_text="Vol", row=2, col=1, title_font_size=11)
                    st.plotly_chart(mf, use_container_width=True)
                except Exception as e:
                    st.error(f"שגיאה ב-{t}: {e}")

# ==============================================================================
# 14. [שדרוג] Portfolio Manager — עם % מהתיק + Pie Chart הקצאת נכסים
# ==============================================================================

def render_portfolio_manager():
    """
    Portfolio Manager Advanced — ניהול תיק השקעות אישי בזמן אמת.

    שדרוגים חדשים בגרסה זו:
      - [חדש] חישוב '% מהתיק' לכל פוזיציה (Portfolio Weight).
      - [חדש] גרף עוגה (Pie Chart) אינטראקטיבי של הקצאת הנכסים.
      - רווח/הפסד בזמן אמת עם צביעה ירוקה/אדומה.
      - כרטיס סיכום כולל: שווי תיק, עלות, P&L $ ו-%.
      - ייצוא ל-CSV.
    """
    st.subheader("💼 Portfolio Manager Advanced — ניהול תיק + הקצאת נכסים")

    # --- הוספת פוזיציה ---
    st.markdown("""
    <div style="background:#f8f9fa; border-right:15px solid #007bff; border-radius:25px;
         padding:30px 40px; margin-bottom:35px; direction:rtl; text-align:right;">
        <b style="font-size:1.5rem; color:#007bff;">➕ הוסף פוזיציה חדשה לתיק</b>
    </div>
    """, unsafe_allow_html=True)

    pf_c1, pf_c2, pf_c3, pf_c4 = st.columns([2, 1.5, 1.5, 1.5])
    with pf_c1:
        pf_ticker    = st.text_input("סימול מניה", placeholder="לדוגמה: AAPL").strip().upper()
    with pf_c2:
        pf_qty       = st.number_input("כמות מניות", min_value=0.01, value=1.0, step=0.1, format="%.2f")
    with pf_c3:
        pf_avg_price = st.number_input("מחיר קנייה ($)", min_value=0.01, value=100.0, step=0.5, format="%.2f")
    with pf_c4:
        pf_notes     = st.text_input("הערה (אופציונלי)", placeholder="כניסה ראשונה")

    if st.button("➕ הוסף לתיק", type="primary", use_container_width=True):
        if pf_ticker:
            add_to_portfolio(pf_ticker, pf_qty, pf_avg_price, pf_notes)
            st.success(f"✅ {pf_ticker} נוסף לתיק!")
            st.rerun()
        else:
            st.warning("אנא הכנס סימול מניה תקין.")

    st.divider()

    portfolio_rows = fetch_portfolio()
    if not portfolio_rows:
        st.info("**התיק שלך ריק.** הוסף פוזיציות בעזרת הטופס למעלה.")
        return

    # שליפת מחירים בזמן אמת
    unique_tickers = list({row[1] for row in portfolio_rows})
    with st.spinner("מעדכן מחירים בזמן אמת..."):
        current_prices = {}
        for tk in unique_tickers:
            try:
                tk_data = yf.Ticker(tk).history(period="2d")
                current_prices[tk] = float(tk_data['Close'].iloc[-1]) if not tk_data.empty else None
            except:
                current_prices[tk] = None

    # בניית רשומות P&L
    pf_records  = []
    total_value = 0.0
    total_cost  = 0.0
    total_pnl   = 0.0

    for row in portfolio_rows:
        row_id, ticker, qty, avg_price, date_added, notes = row
        cur = current_prices.get(ticker)
        if cur is not None:
            cost    = qty * avg_price
            val     = qty * cur
            pnl_d   = val - cost
            pnl_pct = ((cur - avg_price) / avg_price) * 100
            total_value += val
            total_cost  += cost
            total_pnl   += pnl_d
            pf_records.append({
                'ID': row_id, 'מניה': ticker, 'כמות': qty,
                'מחיר קנייה': avg_price, 'מחיר נוכחי': cur,
                'שווי נוכחי': val, 'P&L ($)': pnl_d, 'P&L (%)': pnl_pct,
                'Weight (%)': 0.0,  # יחושב אחרי
                'תאריך': date_added[:10] if date_added else 'N/A',
                'הערה': notes or ''
            })
        else:
            pf_records.append({
                'ID': row_id, 'מניה': ticker, 'כמות': qty,
                'מחיר קנייה': avg_price, 'מחיר נוכחי': None,
                'שווי נוכחי': 0.0, 'P&L ($)': 0.0, 'P&L (%)': 0.0,
                'Weight (%)': 0.0,
                'תאריך': date_added[:10] if date_added else 'N/A',
                'הערה': notes or ''
            })

    # [חדש] חישוב % מהתיק (Portfolio Weight) לכל פוזיציה
    for rec in pf_records:
        if total_value > 0 and rec['מחיר נוכחי'] is not None:
            rec['Weight (%)'] = (rec['שווי נוכחי'] / total_value) * 100

    # --- סיכום תיק ---
    total_ret_pct = ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0
    pnl_color     = "#1a7a40" if total_pnl >= 0 else "#c0392b"
    pnl_bg        = "#f1fdf5" if total_pnl >= 0 else "#fff5f5"
    pnl_border    = "#28a745" if total_pnl >= 0 else "#dc3545"
    pnl_icon      = "📈" if total_pnl >= 0 else "📉"

    st.markdown(f"""
    <div class="portfolio-summary-card">
        <h3 style="color:#007bff; margin-top:0; border:none; padding:0; font-size:2rem;">
            💼 סיכום תיק ההשקעות
        </h3>
        <div style="display:flex; gap:60px; margin-top:25px; flex-wrap:wrap; justify-content:flex-end;">
            <div style="text-align:center;">
                <p style="color:#888; font-size:1.1rem; margin:0;">שווי תיק כולל</p>
                <p style="font-size:2rem; font-weight:900; color:#1a1a1a; margin:4px 0; direction:ltr;">
                    ${total_value:,.2f}</p>
            </div>
            <div style="text-align:center;">
                <p style="color:#888; font-size:1.1rem; margin:0;">עלות השקעה</p>
                <p style="font-size:2rem; font-weight:900; color:#555; margin:4px 0; direction:ltr;">
                    ${total_cost:,.2f}</p>
            </div>
            <div style="background:{pnl_bg}; border:2px solid {pnl_border}; border-radius:18px;
                 padding:16px 30px; text-align:center;">
                <p style="color:#888; font-size:1.1rem; margin:0;">{pnl_icon} רווח / הפסד כולל</p>
                <p style="font-size:2.2rem; font-weight:900; color:{pnl_color}; margin:4px 0; direction:ltr;">
                    ${total_pnl:+,.2f}</p>
                <p style="font-size:1.4rem; font-weight:800; color:{pnl_color}; margin:0; direction:ltr;">
                    {total_ret_pct:+.2f}%</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- [חדש] Pie Chart הקצאת נכסים ---
    valid_recs = [r for r in pf_records if r['מחיר נוכחי'] is not None and r['שווי נוכחי'] > 0]
    if valid_recs and total_value > 0:
        st.markdown("#### 🥧 הקצאת נכסים — Asset Allocation Pie Chart")
        pie_labels  = [r['מניה'] for r in valid_recs]
        pie_values  = [r['שווי נוכחי'] for r in valid_recs]
        pie_weights = [r['Weight (%)'] for r in valid_recs]

        # צבעים מגוונים לעוגה
        pie_colors  = [
            '#007bff', '#28a745', '#ff7f0e', '#dc3545',
            '#9b59b6', '#1abc9c', '#e67e22', '#2c3e50',
            '#e74c3c', '#3498db', '#f39c12', '#27ae60'
        ]

        pie_fig = go.Figure(go.Pie(
            labels=pie_labels,
            values=pie_values,
            hole=0.42,
            texttemplate='<b>%{label}</b><br>%{percent:.1%}',
            hovertemplate='<b>%{label}</b><br>שווי: $%{value:,.2f}<br>%{percent:.1%}<extra></extra>',
            marker=dict(
                colors=pie_colors[:len(pie_labels)],
                line=dict(color='#ffffff', width=3)
            ),
            textfont=dict(size=14, family="Assistant"),
            pull=[0.03] * len(pie_labels)
        ))

        # טקסט מרכזי בתוך ה-Donut
        pie_fig.add_annotation(
            text=f"<b>תיק כולל</b><br>${total_value:,.0f}",
            x=0.5, y=0.5,
            font=dict(size=16, family="Assistant", color="#1a1a1a"),
            showarrow=False
        )

        pie_fig.update_layout(
            template="plotly_white",
            height=480,
            margin=dict(l=30, r=30, t=40, b=30),
            legend=dict(
                orientation="v", yanchor="middle", y=0.5,
                xanchor="left", x=1.02,
                font=dict(size=13, family="Assistant"),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="#e9ecef", borderwidth=1
            ),
            font=dict(family="Assistant")
        )
        st.plotly_chart(pie_fig, use_container_width=True)

        # --- [חדש] Sector Allocation Pie ---
        render_portfolio_sector_pie(pf_records, total_value)

        # --- [חדש] טבלת Weight % ---
        st.markdown("#### 📊 משקל כל פוזיציה בתיק")
        weight_data = []
        for r in valid_recs:
            pnl_pct_fmt = f"{r['P&L (%)']:+.2f}%" if r['P&L (%)'] is not None else 'N/A'
            weight_data.append({
                'מניה':         r['מניה'],
                'שווי נוכחי':  f"${r['שווי נוכחי']:,.2f}",
                'משקל בתיק':   f"{r['Weight (%)']:.1f}%",
                'P&L (%)':      pnl_pct_fmt,
            })
        weight_df = pd.DataFrame(weight_data)
        st.dataframe(weight_df, use_container_width=True, hide_index=True)

    st.divider()

    # --- פירוט פוזיציות ---
    st.markdown("#### 📋 פירוט פוזיציות התיק")
    for rec in pf_records:
        pnl_d_val     = rec['P&L ($)']
        is_profit     = pnl_d_val > 0 if rec['מחיר נוכחי'] is not None else None
        card_border   = "#28a745" if is_profit else ("#dc3545" if is_profit is False else "#dee2e6")
        weight_str    = f"{rec['Weight (%)']:.1f}%" if rec['מחיר נוכחי'] is not None else "N/A"
        pnl_d_str     = f"${pnl_d_val:+,.2f}" if rec['מחיר נוכחי'] is not None else "N/A"
        pnl_pct_str   = f"{rec['P&L (%)']:+.2f}%" if rec['מחיר נוכחי'] is not None else "N/A"
        cur_str       = f"${rec['מחיר נוכחי']:.2f}" if rec['מחיר נוכחי'] is not None else "שגיאה"
        val_str       = f"${rec['שווי נוכחי']:,.2f}" if rec['מחיר נוכחי'] is not None else "N/A"
        status_icon   = '✅' if is_profit else ('❌' if is_profit is False else '⏳')

        with st.expander(
            f"{status_icon} {rec['מניה']} | {rec['כמות']:.2f} מניות | "
            f"קנייה: ${rec['מחיר קנייה']:.2f} | P&L: {pnl_d_str} ({pnl_pct_str}) | "
            f"משקל: {weight_str} | נוכחי: {cur_str}"
        ):
            ec1, ec2, ec3 = st.columns([2, 2, 1])
            with ec1:
                st.markdown(f"""
                <div style="direction:rtl; text-align:right; font-size:1.2rem; line-height:2;">
                    <b>מניה:</b> {rec['מניה']}<br>
                    <b>כמות:</b> {rec['כמות']:.2f}<br>
                    <b>מחיר קנייה:</b> ${rec['מחיר קנייה']:.2f}<br>
                    <b>מחיר נוכחי:</b> {cur_str}<br>
                    <b>תאריך כניסה:</b> {rec['תאריך']}
                </div>
                """, unsafe_allow_html=True)
            with ec2:
                st.markdown(f"""
                <div style="direction:rtl; text-align:right; font-size:1.2rem; line-height:2;">
                    <b>שווי נוכחי:</b> {val_str}<br>
                    <b>P&L ($):</b> <span style="color:{card_border}; font-weight:900;">{pnl_d_str}</span><br>
                    <b>P&L (%):</b> <span style="color:{card_border}; font-weight:900;">{pnl_pct_str}</span><br>
                    <b>% מהתיק:</b> <span style="color:#007bff; font-weight:900;">{weight_str}</span><br>
                    <b>הערה:</b> {rec['הערה'] or '—'}
                </div>
                """, unsafe_allow_html=True)
            with ec3:
                if st.button("🗑️ מחק", key=f"del_pf_{rec['ID']}"):
                    delete_from_portfolio(rec['ID'])
                    st.toast(f"הפוזיציה {rec['מניה']} נמחקה.")
                    st.rerun()

    st.divider()

    # ייצוא CSV
    if pf_records:
        export_rows = []
        for r in pf_records:
            export_rows.append({
                'מניה':         r['מניה'],
                'כמות':         r['כמות'],
                'מחיר קנייה':  r['מחיר קנייה'],
                'מחיר נוכחי':  r['מחיר נוכחי'],
                'שווי נוכחי':  r['שווי נוכחי'],
                'P&L ($)':      r['P&L ($)'],
                'P&L (%)':      r['P&L (%)'],
                'משקל בתיק (%)': r['Weight (%)'],
                'תאריך':        r['תאריך'],
                'הערה':         r['הערה'],
            })
        csv = pd.DataFrame(export_rows).to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 ייצוא תיק ל-CSV", csv, "portfolio_export.csv", "text/csv", use_container_width=True)


# ==============================================================================
# 15-A. [חדש] Fear & Greed Gauge — מדד פחד ותאוות בצע
# ==============================================================================

@st.cache_data(ttl=300, show_spinner=False)
def _fetch_fear_greed_data():
    """
    מחשב מדד Fear & Greed מורכב מ-4 גורמים:
      1. VIX level    — תנודתיות ציפויה (Volatility).
      2. SPY RSI(14)  — מומנטום שוק (Momentum).
      3. SPY vs MA50  — מרחק ממגמה (Trend Strength).
      4. SPY 30d return — מומנטום חודשי (Market Momentum).
    כל גורם מתרגם לציון 0-100, הממוצע הוא מדד הפחד/תאוות.
    מוחזר: (score 0-100, label, color, breakdown_dict).
    """
    try:
        # SPY data — 60 ימים לחישוב RSI + MA50
        spy_hist = yf.Ticker("SPY").history(period="60d")
        vix_hist = yf.Ticker("^VIX").history(period="5d")

        if spy_hist.empty or vix_hist.empty:
            return 50, "Neutral", "#ffc107", {}

        spy_close = spy_hist["Close"]
        vix_val   = float(vix_hist["Close"].iloc[-1])

        # 1. VIX Score: VIX<12→100 (greedy), VIX>35→0 (fear)
        vix_score = max(0, min(100, (35 - vix_val) / (35 - 10) * 100))

        # 2. RSI Score: RSI<30→0, RSI>70→100
        spy_rsi   = calculate_rsi(spy_close, 14)
        rsi_val   = float(spy_rsi.iloc[-1]) if not spy_rsi.isna().all() else 50
        rsi_score = max(0, min(100, rsi_val))

        # 3. MA50 Distance Score: price>MA50 by >5% → 100, <5% below → 0
        spy_ma50   = spy_close.rolling(50).mean()
        ma50_val   = float(spy_ma50.iloc[-1]) if not spy_ma50.isna().all() else float(spy_close.iloc[-1])
        spy_now    = float(spy_close.iloc[-1])
        ma50_dist  = (spy_now - ma50_val) / ma50_val * 100   # % above/below MA50
        ma50_score = max(0, min(100, (ma50_dist + 10) / 20 * 100))   # -10%→0, +10%→100

        # 4. 30-day Momentum Score
        spy_30d_ago = float(spy_close.iloc[-min(30, len(spy_close))]) if len(spy_close) >= 5 else spy_now
        mom_30d     = (spy_now - spy_30d_ago) / spy_30d_ago * 100
        mom_score   = max(0, min(100, (mom_30d + 10) / 20 * 100))   # -10%→0, +10%→100

        # ממוצע משוקלל: VIX x1.5, RSI x1, MA50 x1, Momentum x0.5
        total_score = (vix_score * 1.5 + rsi_score * 1.0 + ma50_score * 1.0 + mom_score * 0.5) / 4.0
        total_score = round(max(0, min(100, total_score)), 1)

        # Label + Color
        if total_score >= 75:
            label = "Extreme Greed 🤑"
            color = "#006400"
        elif total_score >= 60:
            label = "Greed 😀"
            color = "#1e8b40"
        elif total_score >= 45:
            label = "Neutral 😐"
            color = "#ffc107"
        elif total_score >= 30:
            label = "Fear 😨"
            color = "#e07030"
        else:
            label = "Extreme Fear 😱"
            color = "#c0392b"

        breakdown = {
            "VIX":        (round(vix_score, 1),   f"VIX={vix_val:.1f}"),
            "RSI(SPY)":   (round(rsi_score, 1),   f"RSI={rsi_val:.1f}"),
            "MA50 Dist":  (round(ma50_score, 1),  f"{ma50_dist:+.1f}%"),
            "Momentum":   (round(mom_score, 1),   f"30d={mom_30d:+.1f}%"),
        }
        return total_score, label, color, breakdown

    except Exception:
        return 50, "Neutral", "#ffc107", {}


def render_fear_greed_gauge():
    """
    Fear & Greed Gauge — מחוגה של מדד הפחד/תאוות בצע.
    מחושב מ-4 גורמים: VIX, RSI(SPY), מרחק MA50, ומומנטום 30 ימים.
    מוצג כ-Plotly Gauge עם breakdown מפורט לפי גורמים.
    מוטמע במסך הבית מתחת ל-Market Overview.

    תיקונים ויזואליים (v2):
      - ללא כותרת כפולה: title="" — הכותרת היחידה היא בבלוק הכהה שמעל.
      - צבעי דרגות תואמי פלטה: אדום יין (#6b1414) → אפור בהיר (#e8ecf0) → ירוק יער (#0d4f2a).
      - פונט 'Assistant' אחיד בכל אלמנט הגרף.
      - Layout מורחב: עמודות [3,2] + גובה 340 → גרף תופס רוחב מלא ללא חלל ריק.
      - Breakdown card: פינות עגולות 22px + box-shadow תואם כרטיסי Market Overview.
    """
    score, label, color, breakdown = _fetch_fear_greed_data()

    # ---- פלטת צבעי דרגות מותאמת לעיצוב האתר ----
    # אדום יין כהה (Extreme Fear) → אדום בהיר → אפור ניטרלי → ירוק בהיר → ירוק יער (Extreme Greed)
    STEP_COLORS = [
        {"range": [0,  20], "color": "#5c1212"},   # אדום יין כהה — Extreme Fear
        {"range": [20, 40], "color": "#c0392b"},   # אדום — Fear
        {"range": [40, 47], "color": "#f0d0c0"},   # ורוד בהיר — Light Fear
        {"range": [47, 53], "color": "#e8ecf0"},   # אפור בהיר — Neutral
        {"range": [53, 60], "color": "#c8e8d0"},   # ירוק בהיר — Light Greed
        {"range": [60, 80], "color": "#1e8b40"},   # ירוק — Greed
        {"range": [80, 100],"color": "#0d4f2a"},   # ירוק יער כהה — Extreme Greed
    ]

    # ---- Gauge Figure ----
    # mode="gauge" בלבד — המספר והlabel מוצגים ב-st.markdown נפרד מתחת לגרף,
    # כדי למנוע לחלוטין חפיפה בין number לבין annotation שגורמת לטקסט דרוס.
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge",
        value=score,
        domain={"x": [0, 1], "y": [0, 1]},
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": "#888",
                "tickvals": [0, 25, 50, 75, 100],
                "ticktext": ["0", "25", "50", "75", "100"],
                "tickfont": {"size": 13, "family": "Assistant, sans-serif", "color": "#555"},
            },
            "bar":        {"color": color, "thickness": 0.28},
            "bgcolor":    "#f0f2f5",
            "borderwidth": 2,
            "bordercolor": "#dee2e6",
            "steps":      STEP_COLORS,
            "threshold":  {
                "line":      {"color": "#1a1a1a", "width": 5},
                "thickness": 0.88,
                "value":     score,
            },
        },
    ))

    gauge_fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={"family": "Assistant, sans-serif", "color": "#1a1a1a"},
        height=280,
        margin=dict(l=40, r=40, t=15, b=5),
    )

    # ---- Breakdown mini-bars — עיצוב תואם כרטיסי Market Overview ----
    breakdown_html = ""
    if breakdown:
        for factor, (factor_score, detail) in breakdown.items():
            bar_w   = max(4, min(100, int(factor_score)))
            if factor_score >= 58:
                bar_col = "#1e8b40"
            elif factor_score <= 42:
                bar_col = "#c0392b"
            else:
                bar_col = "#ffc107"
            breakdown_html += f"""
            <div style="margin-bottom:10px; direction:ltr; text-align:left;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="width:78px; font-size:0.8rem; color:#495057;
                          font-weight:700; font-family:'Assistant',sans-serif;
                          flex-shrink:0;">{factor}</span>
                    <div style="flex:1; height:10px; background:#e9ecef;
                                border-radius:6px; overflow:hidden;">
                        <div style="width:{bar_w}%; height:10px; background:{bar_col};
                                    border-radius:6px; transition:width 0.3s;"></div>
                    </div>
                    <span style="width:52px; font-size:0.75rem; color:#888;
                          text-align:right; font-family:'Assistant',sans-serif;
                          flex-shrink:0;">{detail}</span>
                </div>
            </div>"""

    # ---- Layout: [3, 2] — גרף רחב + Breakdown ----
    fg_c1, fg_c2 = st.columns([3, 2])
    with fg_c1:
        st.plotly_chart(
            gauge_fig, use_container_width=True,
            config={"displayModeBar": False}
        )
        # ---- מספר + label — HTML נפרד, ללא Plotly positioning ----
        # מוצג כ-block HTML עצמאי מתחת לגרף: מספר בשורה עליונה, label בשורה נפרדת.
        # text-align:center + margin נקי — ללא absolute positioning.
        st.markdown(
            f"<div style='text-align:center; margin-top:4px; margin-bottom:8px;"
            f"font-family:Assistant,sans-serif;'>"
            f"<span style='display:block; font-size:3rem; font-weight:900;"
            f"color:{color}; line-height:1.1;'>{score}</span>"
            f"<span style='display:block; font-size:1.25rem; font-weight:700;"
            f"color:{color}; margin-top:6px;'>{label}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with fg_c2:
        # Breakdown card built with pure concatenation — NO f-string nesting.
        # This prevents Streamlit from displaying raw HTML tags.
        _bd_pieces = []
        _bd_pieces.append("<div style='background:#ffffff;border:1.5px solid #e9ecef;")
        _bd_pieces.append("border-radius:22px;padding:24px 26px;margin-top:28px;")
        _bd_pieces.append("box-shadow:0 8px 28px rgba(0,0,0,0.07);")
        _bd_pieces.append("font-family:Assistant,sans-serif;")
        _bd_pieces.append(">")
        _bd_pieces.append("<p style='font-size:0.8rem;color:#888;margin:0 0 14px 0;")
        _bd_pieces.append("font-weight:800;letter-spacing:1.5px;text-align:center;")
        _bd_pieces.append("text-transform:uppercase;'>Breakdown &mdash; \u05d2\u05d5\u05e8\u05de\u05d9 \u05d4\u05de\u05d3\u05d3</p>")
        _bd_pieces.append(breakdown_html)
        _bd_pieces.append("<div style='border-top:1px solid #f0f2f5;")
        _bd_pieces.append("margin-top:12px;padding-top:10px;'>")
        _bd_pieces.append("<p style='font-size:0.7rem;color:#bbb;margin:0;text-align:center;'>")
        _bd_pieces.append("VIX &times;1.5 &middot; RSI &times;1 &middot; ")
        _bd_pieces.append("MA50 &times;1 &middot; Momentum &times;0.5</p></div></div>")
        st.markdown("".join(_bd_pieces), unsafe_allow_html=True)


# ==============================================================================
# 15-B. [חדש] Insider & Institutional Stats — החזקות מוסדיות ובעלי עניין
# ==============================================================================

def render_insider_institutional(ticker_symbol):
    """
    Insider & Institutional Stats — נתוני החזקות מוסדיות ובעלי עניין.

    מציג:
      - אחוז החזקת המוסדיים (Institutional Ownership %).
      - אחוז החזקת בעלי עניין פנים (Insider Ownership %).
      - מניות צפות חופשית (Float Shares).
      - Short Interest % (מוכרים בחסר).
      - Progress bars ויזואליים לכל מדד.
      - הערת AI אוטומטית: תובנה אסטרטגית לפי ערכי ההחזקה.
    """
    try:
        info = yf.Ticker(ticker_symbol).info

        inst_pct     = info.get("institutionPercent",  info.get("heldPercentInstitutions", None))
        insider_pct  = info.get("insiderPercent",       info.get("heldPercentInsiders",     None))
        short_pct    = info.get("shortPercentOfFloat",  None)
        float_shares = info.get("floatShares",          None)
        shares_out   = info.get("sharesOutstanding",    None)

        # Convert to %
        if inst_pct   and inst_pct   <= 1: inst_pct   = inst_pct   * 100
        if insider_pct and insider_pct <= 1: insider_pct = insider_pct * 100
        if short_pct  and short_pct  <= 1: short_pct  = short_pct  * 100

        # ---- AI Commentary ----
        ai_notes = []
        ai_color = "#007bff"

        if inst_pct is not None:
            if inst_pct > 80:
                ai_notes.append(f"החזקה מוסדית גבוהה מאוד ({inst_pct:.1f}%) — "
                                 "מחקר עמוק של קרנות גדולות מאחורי המניה. "
                                 "אות אמון חזק, אך גם סיכון לתנודתיות גבוהה בעת מכירה מרוכזת.")
                ai_color = "#1e8b40"
            elif inst_pct > 60:
                ai_notes.append(f"החזקה מוסדית גבוהה ({inst_pct:.1f}%) — "
                                 "מניה 'מוחזקת' על ידי קרנות פנסיה, hedge funds וETFs. "
                                 "מגבירה יציבות ואמינות, ועשויה להעיד על קונצנזוס חיובי.")
                ai_color = "#28a745"
            elif inst_pct > 30:
                ai_notes.append(f"החזקה מוסדית בינונית ({inst_pct:.1f}%) — "
                                 "מניה עם תמיכה מוסדית מאוזנת. "
                                 "מרחב לצמיחה נוספת בהחזקות מוסדיות עם שיפור בביצועים.")
                ai_color = "#ffc107"
            else:
                ai_notes.append(f"החזקה מוסדית נמוכה ({inst_pct:.1f}%) — "
                                 "מוסדיים טרם גילו עניין, או מניה קטנה/מחלוקתית. "
                                 "עלולה להיות פחות מנוטרת ולהציג תנודתיות גבוהה יותר.")
                ai_color = "#e07030"

        if insider_pct is not None and insider_pct > 20:
            ai_notes.append(f"בעלי עניין מחזיקים {insider_pct:.1f}% — "
                             "אחוז גבוה מצביע על מנהלים/מייסדים עם אמון גבוה בעסק, "
                             "ועל יישור אינטרסים בין הנהלה למשקיעים.")

        if short_pct is not None and short_pct > 10:
            ai_notes.append(f"⚠️ Short Interest גבוה: {short_pct:.1f}% — "
                             "אחוז מוכרים בחסר גבוה. עלול לגרום ל-Short Squeeze "
                             "בעת עלייה חדה, אך גם מעיד על ספקנות בשוק.")

        # ---- Visual Cards ----
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#f0f7ff 0%,#fafcff 100%);
             border:2px solid #cce5ff; border-right:16px solid #007bff;
             border-radius:32px; padding:35px 45px; margin-bottom:25px;
             box-shadow:0 12px 40px rgba(0,123,255,0.09);
             direction:rtl; text-align:right;">
            <h4 style="color:#007bff; font-size:1.8rem; margin:0 0 20px 0;
                       border:none; padding:0;">
                🏛️ Insider &amp; Institutional Ownership — {ticker_symbol}
            </h4>
        </div>
        """, unsafe_allow_html=True)

        ic1, ic2, ic3, ic4 = st.columns(4)

        def _ownership_card(col, label, value, unit, bar_color, icon):
            """Helper: renders a single ownership metric card."""
            with col:
                if value is not None:
                    bar_w = max(2, min(100, int(value)))
                    val_str = f"{value:.1f}{unit}"
                else:
                    bar_w   = 0
                    val_str = "N/A"
                col.markdown(f"""
                <div style="background:#ffffff; border:1.5px solid #e9ecef;
                     border-radius:20px; padding:22px 18px; text-align:center;
                     box-shadow:0 6px 20px rgba(0,0,0,0.05); height:140px;">
                    <p style="font-size:1.8rem; margin:0 0 4px 0;">{icon}</p>
                    <p style="font-size:0.85rem; color:#888; margin:0 0 8px 0;
                              font-weight:700; letter-spacing:0.5px;">{label}</p>
                    <p style="font-size:1.6rem; font-weight:900; color:#1a1a1a;
                              margin:0 0 8px 0; direction:ltr;">{val_str}</p>
                    <div style="width:100%; height:8px; background:#e9ecef;
                                border-radius:4px; overflow:hidden;">
                        <div style="width:{bar_w}%; height:8px;
                                    background:{bar_color}; border-radius:4px;">
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        _ownership_card(ic1, "מוסדיים %",  inst_pct,    "%",  "#007bff", "🏦")
        _ownership_card(ic2, "Insiders %",  insider_pct, "%",  "#28a745", "👔")
        _ownership_card(ic3, "Short Float", short_pct,   "%",  "#dc3545", "📉")

        with ic4:
            float_str = (f"${float_shares/1e9:.2f}B" if float_shares and float_shares > 1e9
                         else f"{float_shares/1e6:.0f}M" if float_shares else "N/A")
            ic4.markdown(f"""
            <div style="background:#ffffff; border:1.5px solid #e9ecef;
                 border-radius:20px; padding:22px 18px; text-align:center;
                 box-shadow:0 6px 20px rgba(0,0,0,0.05); height:140px;">
                <p style="font-size:1.8rem; margin:0 0 4px 0;">📊</p>
                <p style="font-size:0.85rem; color:#888; margin:0 0 8px 0;
                          font-weight:700; letter-spacing:0.5px;">Float Shares</p>
                <p style="font-size:1.5rem; font-weight:900; color:#1a1a1a;
                          margin:0 0 8px 0; direction:ltr;">{float_str}</p>
                <p style="font-size:0.75rem; color:#aaa; margin:0;">מניות חופשיות לסחר</p>
            </div>
            """, unsafe_allow_html=True)

        # ---- AI Commentary Box ----
        if ai_notes:
            full_note = " ".join(ai_notes)
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#fffef0 0%,#fff9e6 100%);
                 border:2px solid #ffc107; border-right:14px solid #ff9800;
                 border-radius:22px; padding:22px 30px; margin-top:20px;
                 direction:rtl; text-align:right;
                 box-shadow:0 8px 25px rgba(255,152,0,0.10);">
                <p style="font-size:0.9rem; color:#856404; font-weight:800;
                          margin:0 0 8px 0; letter-spacing:0.5px;">
                    🤖 AI INSIGHT — ניתוח החזקות
                </p>
                <p style="font-size:1.15rem; color:#4a3600; line-height:1.8; margin:0;">
                    {full_note}
                </p>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.warning(f"לא ניתן לטעון נתוני החזקות עבור {ticker_symbol}: {e}")


# ==============================================================================
# 15-C. [חדש] Performance Alpha — ביצועים vs S&P 500 YTD
# ==============================================================================

@st.cache_data(ttl=600, show_spinner=False)
def _fetch_ytd_data(ticker_symbol):
    """
    שולף נתוני YTD (מתחילת השנה הנוכחית) עבור המניה הנבחרת ועבור SPY.
    מחזיר DataFrame עם עמודות: Date, stock_pct, spy_pct.
    """
    try:
        year_start = f"{datetime.now().year}-01-01"
        raw = yf.download(
            [ticker_symbol, "SPY"],
            start=year_start,
            interval="1d",
            progress=False,
            auto_adjust=True
        )
        if raw.empty:
            return None

        if isinstance(raw.columns, pd.MultiIndex):
            close_df = raw["Close"]
        else:
            close_df = raw[["Close"]].rename(columns={"Close": ticker_symbol})

        # נרמול לנקודת התחלה 0%
        norm = (close_df / close_df.iloc[0] - 1) * 100
        norm.columns = [c.upper() for c in norm.columns]

        sym_up = ticker_symbol.upper()
        if sym_up not in norm.columns or "SPY" not in norm.columns:
            return None

        return norm[[sym_up, "SPY"]].dropna()

    except Exception:
        return None


def render_performance_alpha(ticker_symbol):
    """
    Performance Alpha Chart — ביצועי המניה מול S&P 500 מתחילת השנה (YTD).

    מציג:
      - קו ביצועי המניה (% שינוי מ-1 בינואר).
      - קו SPY (קו ייחוס כחול).
      - אזור fill ירוק/אדום כשהמניה מעל/מתחת ל-SPY.
      - Alpha Score: כמה % המניה הכתה/הפסידה מול SPY.
      - כרטיס סיכום: YTD%, Alpha%, ציון ביצועים.
    """
    with st.spinner(f"טוען נתוני YTD עבור {ticker_symbol} vs S&P 500..."):
        ytd_df = _fetch_ytd_data(ticker_symbol)

    if ytd_df is None or ytd_df.empty:
        st.warning(f"לא ניתן לטעון נתוני YTD עבור {ticker_symbol}.")
        return

    sym_up        = ticker_symbol.upper()
    stock_ytd     = round(float(ytd_df[sym_up].iloc[-1]),  2)
    spy_ytd       = round(float(ytd_df["SPY"].iloc[-1]),   2)
    alpha         = round(stock_ytd - spy_ytd,              2)
    alpha_color   = "#1e8b40" if alpha >= 0 else "#c0392b"
    alpha_icon    = "▲" if alpha >= 0 else "▼"
    alpha_label   = "Outperform 🏆" if alpha >= 0 else "Underperform 📉"

    # ---- Chart ----
    perf_fig = go.Figure()

    # Fill area between stock and SPY
    perf_fig.add_trace(go.Scatter(
        x=ytd_df.index, y=ytd_df[sym_up],
        name=sym_up,
        line=dict(color="#007bff", width=3),
        fill=None,
        mode="lines"
    ))
    perf_fig.add_trace(go.Scatter(
        x=ytd_df.index, y=ytd_df["SPY"],
        name="S&P 500 (SPY)",
        line=dict(color="#ff7f0e", width=2, dash="dot"),
        fill="tonexty",
        fillcolor="rgba(0,123,255,0.07)",
        mode="lines"
    ))

    # Zero line
    perf_fig.add_hline(y=0, line_dash="dash", line_color="#dee2e6", line_width=1.5)

    perf_fig.update_layout(
        title=dict(
            text=f"📈 Performance Alpha: {sym_up} vs S&P 500 — YTD {datetime.now().year}",
            font=dict(size=16, family="Assistant", color="#2c3e50"),
            x=0.01, xanchor="left"
        ),
        template="plotly_white",
        height=380,
        margin=dict(l=40, r=40, t=55, b=40),
        yaxis=dict(title="שינוי % מתחילת השנה", ticksuffix="%",
                   zeroline=True, zerolinecolor="#dee2e6", zerolinewidth=2),
        xaxis=dict(title="תאריך"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1, font=dict(size=13)),
        hovermode="x unified",
        font=dict(family="Assistant")
    )

    st.plotly_chart(perf_fig, use_container_width=True)

    # ---- Summary Cards ----
    pa_c1, pa_c2, pa_c3 = st.columns(3)
    with pa_c1:
        stk_color = "#1e8b40" if stock_ytd >= 0 else "#c0392b"
        st.markdown(f"""
        <div style="background:#ffffff; border:1.5px solid #e9ecef; border-radius:18px;
             padding:20px; text-align:center; box-shadow:0 5px 18px rgba(0,0,0,0.05);">
            <p style="font-size:0.85rem; color:#888; margin:0 0 5px 0; font-weight:700;">
                {sym_up} — תשואה YTD
            </p>
            <p style="font-size:2rem; font-weight:900; color:{stk_color};
                      direction:ltr; margin:0;">{stock_ytd:+.2f}%</p>
        </div>
        """, unsafe_allow_html=True)
    with pa_c2:
        spy_color = "#1e8b40" if spy_ytd >= 0 else "#c0392b"
        st.markdown(f"""
        <div style="background:#ffffff; border:1.5px solid #e9ecef; border-radius:18px;
             padding:20px; text-align:center; box-shadow:0 5px 18px rgba(0,0,0,0.05);">
            <p style="font-size:0.85rem; color:#888; margin:0 0 5px 0; font-weight:700;">
                S&P 500 (SPY) — YTD
            </p>
            <p style="font-size:2rem; font-weight:900; color:{spy_color};
                      direction:ltr; margin:0;">{spy_ytd:+.2f}%</p>
        </div>
        """, unsafe_allow_html=True)
    with pa_c3:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,
                    {'#f0fdf4' if alpha>=0 else '#fff5f5'} 0%,
                    {'#e8f8ee' if alpha>=0 else '#ffe8e8'} 100%);
             border:2px solid {alpha_color}; border-radius:18px;
             padding:20px; text-align:center;
             box-shadow:0 5px 18px rgba(0,0,0,0.07);">
            <p style="font-size:0.85rem; color:#888; margin:0 0 5px 0; font-weight:700;">
                Alpha Score
            </p>
            <p style="font-size:2rem; font-weight:900; color:{alpha_color};
                      direction:ltr; margin:0 0 2px 0;">{alpha_icon}{abs(alpha):.2f}%</p>
            <p style="font-size:0.8rem; color:{alpha_color}; margin:0; font-weight:700;">
                {alpha_label}
            </p>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# 15-D. [חדש] Portfolio Sector Pie — חלוקת תיק לפי סקטורים
# ==============================================================================

# מיפוי מניות לסקטורים — hardcoded לביצועים מהירים
STOCK_SECTOR_MAP = {
    # Technology
    "AAPL":"Technology","MSFT":"Technology","NVDA":"Technology","AMD":"Technology",
    "INTC":"Technology","AVGO":"Technology","QCOM":"Technology","TXN":"Technology",
    "AMAT":"Technology","ADBE":"Technology","CRM":"Technology","NOW":"Technology",
    "ORCL":"Technology","PANW":"Technology","CRWD":"Technology","PLTR":"Technology",
    "NET":"Technology","ZS":"Technology","FTNT":"Technology","SNOW":"Technology",
    "DDOG":"Technology","KLAC":"Technology","LRCX":"Technology","MU":"Technology",
    "MRVL":"Technology","ADI":"Technology","CDNS":"Technology","SNPS":"Technology",
    # Communication
    "GOOGL":"Communication","META":"Communication","NFLX":"Communication",
    "TMUS":"Communication","DIS":"Communication","CMCSA":"Communication",
    "T":"Communication","VZ":"Communication","WBD":"Communication","EA":"Communication",
    # Consumer Cyclical
    "AMZN":"Consumer Cyclical","TSLA":"Consumer Cyclical","HD":"Consumer Cyclical",
    "MCD":"Consumer Cyclical","LOW":"Consumer Cyclical","BKNG":"Consumer Cyclical",
    "NKE":"Consumer Cyclical","SBUX":"Consumer Cyclical","TGT":"Consumer Cyclical",
    "ORLY":"Consumer Cyclical","ABNB":"Consumer Cyclical","MAR":"Consumer Cyclical",
    # Healthcare
    "LLY":"Healthcare","UNH":"Healthcare","JNJ":"Healthcare","ABBV":"Healthcare",
    "MRK":"Healthcare","TMO":"Healthcare","AMGN":"Healthcare","ISRG":"Healthcare",
    "VRTX":"Healthcare","REGN":"Healthcare","PFE":"Healthcare","GILD":"Healthcare",
    "BSX":"Healthcare","DHR":"Healthcare","MRNA":"Healthcare","DXCM":"Healthcare",
    # Financials
    "JPM":"Financials","V":"Financials","MA":"Financials","BAC":"Financials",
    "WFC":"Financials","GS":"Financials","MS":"Financials","AXP":"Financials",
    "BLK":"Financials","SCHW":"Financials","C":"Financials","PGR":"Financials",
    "PYPL":"Financials","COIN":"Financials","MSTR":"Financials","SQ":"Financials",
    # Industrials
    "GE":"Industrials","CAT":"Industrials","HON":"Industrials","RTX":"Industrials",
    "UPS":"Industrials","LMT":"Industrials","DE":"Industrials","BA":"Industrials",
    "NOC":"Industrials","FDX":"Industrials","GD":"Industrials","ETN":"Industrials",
    # Consumer Defensive
    "WMT":"Consumer Defensive","PG":"Consumer Defensive","COST":"Consumer Defensive",
    "KO":"Consumer Defensive","PEP":"Consumer Defensive","PM":"Consumer Defensive",
    # Energy
    "XOM":"Energy","CVX":"Energy","COP":"Energy","SLB":"Energy","EOG":"Energy",
    "MPC":"Energy","OXY":"Energy","DVN":"Energy","HAL":"Energy",
    # Materials
    "LIN":"Materials","SHW":"Materials","APD":"Materials","FCX":"Materials",
    "NEM":"Materials","DOW":"Materials","PPG":"Materials",
    # Real Estate
    "PLD":"Real Estate","AMT":"Real Estate","EQIX":"Real Estate","PSA":"Real Estate",
    "DLR":"Real Estate","O":"Real Estate","CCI":"Real Estate","SPG":"Real Estate",
    # Utilities
    "NEE":"Utilities","SO":"Utilities","DUK":"Utilities","AEP":"Utilities",
    "D":"Utilities","EXC":"Utilities","NEE":"Utilities",
}

SECTOR_COLORS = {
    "Technology":         "#007bff",
    "Communication":      "#17a2b8",
    "Consumer Cyclical":  "#fd7e14",
    "Healthcare":         "#20c997",
    "Financials":         "#6f42c1",
    "Industrials":        "#868e96",
    "Consumer Defensive": "#28a745",
    "Energy":             "#ffc107",
    "Materials":          "#e83e8c",
    "Real Estate":        "#dc3545",
    "Utilities":          "#6c757d",
    "Other":              "#adb5bd",
}


def render_portfolio_sector_pie(pf_records, total_value):
    """
    Portfolio Sector Allocation Pie Chart — חלוקת התיק לפי סקטורים.

    משתמש ב-STOCK_SECTOR_MAP המובנה לסיווג מהיר, ומציג:
      - גרף עוגה (Donut) של הקצאה לפי סקטורים.
      - % כל סקטור מהתיק הכולל.
      - טבלת סיכום: שווי כל סקטור, % מהתיק, P&L לסקטור.
    """
    if not pf_records or total_value <= 0:
        return

    # צבירה לפי סקטור
    sector_value = {}
    sector_pnl   = {}

    for rec in pf_records:
        if rec["מחיר נוכחי"] is None or rec["שווי נוכחי"] <= 0:
            continue
        ticker  = rec["מניה"].upper()
        sector  = STOCK_SECTOR_MAP.get(ticker, "Other")
        val     = rec["שווי נוכחי"]
        pnl_d   = rec["P&L ($)"]

        sector_value[sector] = sector_value.get(sector, 0.0) + val
        sector_pnl[sector]   = sector_pnl.get(sector,   0.0) + pnl_d

    if not sector_value:
        return

    sec_labels = list(sector_value.keys())
    sec_values = [sector_value[s] for s in sec_labels]
    sec_colors = [SECTOR_COLORS.get(s, "#adb5bd") for s in sec_labels]
    sec_pcts   = [v / total_value * 100 for v in sec_values]

    st.markdown("#### 🗂️ חלוקת התיק לפי סקטורים")

    sec_pie = go.Figure(go.Pie(
        labels=sec_labels,
        values=sec_values,
        hole=0.44,
        texttemplate="<b>%{label}</b><br>%{percent:.1%}",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "שווי: $%{value:,.0f}<br>"
            "%{percent:.1%} מהתיק<extra></extra>"
        ),
        marker=dict(
            colors=sec_colors,
            line=dict(color="#ffffff", width=2.5)
        ),
        textfont=dict(size=13, family="Assistant"),
        pull=[0.03] * len(sec_labels),
    ))
    sec_pie.add_annotation(
        text=f"<b>סקטורים</b><br>{len(sec_labels)}",
        x=0.5, y=0.5,
        font=dict(size=15, family="Assistant", color="#1a1a1a"),
        showarrow=False
    )
    sec_pie.update_layout(
        template="plotly_white",
        height=420,
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(
            orientation="v", yanchor="middle", y=0.5,
            xanchor="left", x=1.02,
            font=dict(size=12, family="Assistant"),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#e9ecef", borderwidth=1
        ),
        font=dict(family="Assistant")
    )
    st.plotly_chart(sec_pie, use_container_width=True)

    # טבלת סיכום לפי סקטור
    sec_rows = []
    for sec in sorted(sector_value.keys(), key=lambda s: sector_value[s], reverse=True):
        pnl_d = sector_pnl.get(sec, 0.0)
        pct   = sector_value[sec] / total_value * 100
        icon  = "🟢" if pnl_d >= 0 else "🔴"
        sec_rows.append({
            "סקטור":         sec,
            "שווי נוכחי":   f"${sector_value[sec]:,.0f}",
            "% מהתיק":       f"{pct:.1f}%",
            "P&L סקטור":     f"{icon} ${pnl_d:+,.0f}",
        })
    st.dataframe(pd.DataFrame(sec_rows), use_container_width=True, hide_index=True)



# ==============================================================================
# 15. Market Heatmap — מפת חום אינטראקטיבית (S&P 500 + Nasdaq 100)
# ==============================================================================

# ---- 50 מניות Top S&P 500 — Hardcoded, ממוינות לפי סקטור ----
# רשימה קבועה ומאומתת של 50 המניות הגדולות ביותר לפי Market Cap.
# גודל הריבוע = market_cap_b (ביליארד $) — ערך יציב מובנה.
# שינוי יומי % נשלף מ-Yahoo Finance דרך cache.
HEATMAP_SP500_STOCKS = [
    # (symbol,  sector_label,          company_name,          market_cap_b)
    ("AAPL",  "💻 Technology",         "Apple",                3200),
    ("MSFT",  "💻 Technology",         "Microsoft",            3100),
    ("NVDA",  "💻 Technology",         "Nvidia",               2800),
    ("AVGO",  "💻 Technology",         "Broadcom",              820),
    ("ORCL",  "💻 Technology",         "Oracle",                400),
    ("AMD",   "💻 Technology",         "AMD",                   270),
    ("QCOM",  "💻 Technology",         "Qualcomm",              175),
    ("TXN",   "💻 Technology",         "Texas Instruments",     175),
    ("AMAT",  "💻 Technology",         "Applied Materials",     190),
    ("INTC",  "💻 Technology",         "Intel",                  95),
    ("GOOGL", "📡 Communication",      "Alphabet",             2100),
    ("META",  "📡 Communication",      "Meta Platforms",       1400),
    ("NFLX",  "📡 Communication",      "Netflix",               310),
    ("TMUS",  "📡 Communication",      "T-Mobile",              200),
    ("DIS",   "📡 Communication",      "Walt Disney",           170),
    ("AMZN",  "🛍️ Consumer Cyclical",  "Amazon",               2200),
    ("TSLA",  "🛍️ Consumer Cyclical",  "Tesla",                 700),
    ("HD",    "🛍️ Consumer Cyclical",  "Home Depot",            320),
    ("MCD",   "🛍️ Consumer Cyclical",  "McDonald's",            200),
    ("BKNG",  "🛍️ Consumer Cyclical",  "Booking Holdings",      150),
    ("LLY",   "🏥 Healthcare",         "Eli Lilly",             750),
    ("UNH",   "🏥 Healthcare",         "UnitedHealth",          490),
    ("JNJ",   "🏥 Healthcare",         "Johnson & Johnson",     370),
    ("ABBV",  "🏥 Healthcare",         "AbbVie",                330),
    ("MRK",   "🏥 Healthcare",         "Merck",                 270),
    ("TMO",   "🏥 Healthcare",         "Thermo Fisher",         185),
    ("ISRG",  "🏥 Healthcare",         "Intuitive Surgical",    175),
    ("JPM",   "🏦 Financials",         "JPMorgan Chase",        580),
    ("V",     "🏦 Financials",         "Visa",                  560),
    ("MA",    "🏦 Financials",         "Mastercard",            440),
    ("BAC",   "🏦 Financials",         "Bank of America",       310),
    ("GS",    "🏦 Financials",         "Goldman Sachs",         165),
    ("WFC",   "🏦 Financials",         "Wells Fargo",           200),
    ("AXP",   "🏦 Financials",         "American Express",      175),
    ("WMT",   "🛒 Consumer Defensive", "Walmart",               550),
    ("PG",    "🛒 Consumer Defensive", "Procter & Gamble",      380),
    ("COST",  "🛒 Consumer Defensive", "Costco",                370),
    ("KO",    "🛒 Consumer Defensive", "Coca-Cola",             260),
    ("PEP",   "🛒 Consumer Defensive", "PepsiCo",               220),
    ("XOM",   "⚡ Energy",             "ExxonMobil",            490),
    ("CVX",   "⚡ Energy",             "Chevron",               290),
    ("COP",   "⚡ Energy",             "ConocoPhillips",        130),
    ("SLB",   "⚡ Energy",             "Schlumberger",           65),
    ("EOG",   "⚡ Energy",             "EOG Resources",          65),
    ("GE",    "🏭 Industrials",        "GE Aerospace",          200),
    ("CAT",   "🏭 Industrials",        "Caterpillar",           175),
    ("HON",   "🏭 Industrials",        "Honeywell",             145),
    ("RTX",   "🏭 Industrials",        "RTX Corp",              140),
    ("BA",    "🏭 Industrials",        "Boeing",                 95),
    ("LMT",   "🏭 Industrials",        "Lockheed Martin",       115),
]

# ---- 50 מניות Top Nasdaq 100 — Hardcoded ----
HEATMAP_NDX_STOCKS = [
    # (symbol,  sector_label,          company_name,          market_cap_b)
    ("AAPL",  "🖥️ Tech Hardware",      "Apple",                3200),
    ("MSFT",  "☁️ Software & Cloud",   "Microsoft",            3100),
    ("NVDA",  "🤖 AI & Semiconductors","Nvidia",               2800),
    ("GOOGL", "☁️ Software & Cloud",   "Alphabet",             2100),
    ("META",  "📱 Social & Media",     "Meta Platforms",       1400),
    ("AMZN",  "🛒 E-Commerce & Cloud", "Amazon",               2200),
    ("TSLA",  "⚡ EV & Energy",        "Tesla",                 700),
    ("AVGO",  "🖥️ Tech Hardware",      "Broadcom",              820),
    ("LLY",   "💊 Biotech",            "Eli Lilly",             750),
    ("ORCL",  "☁️ Software & Cloud",   "Oracle",                400),
    ("NFLX",  "📱 Social & Media",     "Netflix",               310),
    ("AMD",   "🤖 AI & Semiconductors","AMD",                   270),
    ("ADBE",  "☁️ Software & Cloud",   "Adobe",                 250),
    ("QCOM",  "🖥️ Tech Hardware",      "Qualcomm",              175),
    ("AMAT",  "🤖 AI & Semiconductors","Applied Materials",     190),
    ("PANW",  "🔐 Cybersecurity",      "Palo Alto Networks",    115),
    ("CRWD",  "🔐 Cybersecurity",      "CrowdStrike",            90),
    ("FTNT",  "🔐 Cybersecurity",      "Fortinet",               55),
    ("PLTR",  "🤖 AI & Semiconductors","Palantir",               85),
    ("CRM",   "☁️ Software & Cloud",   "Salesforce",            250),
    ("INTU",  "☁️ Software & Cloud",   "Intuit",                175),
    ("NOW",   "☁️ Software & Cloud",   "ServiceNow",            200),
    ("SNOW",  "☁️ Software & Cloud",   "Snowflake",              45),
    ("DDOG",  "☁️ Software & Cloud",   "Datadog",                38),
    ("NET",   "🔐 Cybersecurity",      "Cloudflare",             38),
    ("ZS",    "🔐 Cybersecurity",      "Zscaler",                30),
    ("ISRG",  "💊 Biotech",            "Intuitive Surgical",    175),
    ("VRTX",  "💊 Biotech",            "Vertex Pharma",         130),
    ("AMGN",  "💊 Biotech",            "Amgen",                 160),
    ("REGN",  "💊 Biotech",            "Regeneron",              95),
    ("COIN",  "💳 Fintech",            "Coinbase",               55),
    ("V",     "💳 Fintech",            "Visa",                  560),
    ("MA",    "💳 Fintech",            "Mastercard",            440),
    ("PYPL",  "💳 Fintech",            "PayPal",                 70),
    ("TMUS",  "📡 Telecom",            "T-Mobile",              200),
    ("CMCSA", "📡 Telecom",            "Comcast",               155),
    ("WBD",   "📱 Social & Media",     "Warner Bros Discovery",  22),
    ("EA",    "🎮 Gaming",             "Electronic Arts",        38),
    ("TTWO",  "🎮 Gaming",             "Take-Two Interactive",   25),
    ("BKNG",  "🛒 E-Commerce & Cloud", "Booking Holdings",      150),
    ("ABNB",  "🛒 E-Commerce & Cloud", "Airbnb",                 90),
    ("TXN",   "🖥️ Tech Hardware",      "Texas Instruments",     175),
    ("INTC",  "🖥️ Tech Hardware",      "Intel",                  95),
    ("MU",    "🖥️ Tech Hardware",      "Micron Technology",     110),
    ("KLAC",  "🤖 AI & Semiconductors","KLA Corp",               85),
    ("LRCX",  "🤖 AI & Semiconductors","Lam Research",           90),
    ("MRVL",  "🤖 AI & Semiconductors","Marvell Technology",     75),
    ("ADI",   "🖥️ Tech Hardware",      "Analog Devices",         95),
    ("CDNS",  "☁️ Software & Cloud",   "Cadence Design",         75),
    ("SNPS",  "☁️ Software & Cloud",   "Synopsys",               75),
]


@st.cache_data(ttl=600, show_spinner=False)
def _fetch_heatmap_prices(symbols_tuple):
    """
    פונקציית שליפת מחירים עם cache — נטענת פעם אחת ל-10 דקות.

    משתמשת ב-yf.download() עם רשימה מוגבלת של סימולים,
    ומפענחת MultiIndex בצורה אמינה.

    מחזירה dict: {symbol: (price, change_pct, change_dollar)}.

    הטריק: במקום לפענח MultiIndex מורכב, משתמשת ב-
    yf.Ticker().history() לכל מניה בנפרד —
    פשוט, אמין, ומוקש לאחסון ב-cache.
    """
    results = {}
    symbols = list(symbols_tuple)

    for sym in symbols:
        try:
            ticker_hist = yf.Ticker(sym).history(period="5d")
            if ticker_hist.empty or len(ticker_hist) < 2:
                results[sym] = (None, 0.0, 0.0)
                continue

            # סגירה אחרונה ולפניה
            price_now  = float(ticker_hist['Close'].iloc[-1])
            price_prev = float(ticker_hist['Close'].iloc[-2])

            if price_prev == 0:
                results[sym] = (price_now, 0.0, 0.0)
                continue

            chg_pct    = ((price_now - price_prev) / price_prev) * 100
            chg_dollar = price_now - price_prev
            results[sym] = (price_now, round(chg_pct, 3), round(chg_dollar, 3))
        except Exception:
            results[sym] = (None, 0.0, 0.0)

    return results


def render_sector_heatmap():
    """
    Market Heatmap — מפת חום אינטראקטיבית מקצועית.

    ארכיטקטורה אמינה ומהירה:
      - 50 מניות Top hardcoded לכל מדד (S&P 500 / Nasdaq 100).
      - @st.cache_data (ttl=10 דקות) — טעינה חד-פעמית, ללא reload בכל לחיצה.
      - yf.Ticker().history() לכל מניה — פשוט ואמין, ללא MultiIndex בעייתי.
      - st.spinner להצגת התקדמות בזמן הטעינה.

    Treemap היררכי 2 רמות (סקטורים → מניות):
      - גודל ריבוע = Market Cap ($B) — ממילון מובנה.
      - צבע = שינוי יומי % — אדום ↔ אפור ↔ ירוק.

    Hover tooltip מפורט:
      - שם מניה + שם חברה מלא.
      - מחיר נוכחי ($).
      - שינוי יומי (% ו-$).
      - Market Cap ($B).
    """

    # =====================================================================
    # A. כותרת ובחירת מדד
    # =====================================================================
    st.markdown("""
    <div class="heatmap-header">
        <h2 style="color:#ffffff; font-size:2.6rem; margin:0; border:none;
                   padding:0; text-align:center;">
            🗺️ Market Heatmap — מפת חום אינטראקטיבית
        </h2>
        <p style="color:#a0b4d0; font-size:1.3rem; margin-top:12px; text-align:center;">
            גודל ריבוע = Market Cap | צבע = שינוי יומי % | Hover לנתוני מניה
        </p>
    </div>
    """, unsafe_allow_html=True)

    hm_col1, hm_col2, hm_col3 = st.columns([2, 2, 2])
    with hm_col1:
        hm_index = st.radio(
            "בחר מדד:",
            ["S&P 500 — 50 מניות גדולות", "Nasdaq 100 — 50 מניות גדולות"],
            horizontal=True
        )
    with hm_col2:
        hm_colorset = st.radio(
            "ערכת צבעים:",
            ["🟢🔴 ירוק/אדום", "🔵🟠 כחול/כתום"],
            horizontal=True
        )
    with hm_col3:
        hm_load_btn = st.button(
            "🔄 טען / רענן מפת חום",
            type="primary",
            use_container_width=True
        )

    # הסבר ראשוני לפני טעינה
    if not hm_load_btn:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0a0a1a 0%,#12122a 100%);
             border-radius:25px; padding:40px 60px; margin:20px 0;
             border:1px solid rgba(255,255,255,0.08);">
            <p style="color:#a0bfd0; font-size:1.4rem; margin:0 0 18px 0;
                      font-weight:700; text-align:center;">
                🗺️ כיצד להשתמש ב-Market Heatmap
            </p>
            <div style="color:#8090a0; font-size:1.15rem; line-height:2.3;
                        text-align:right; direction:rtl;">
                • בחר מדד:
                  <b style="color:#fff;">S&P 500</b> (7 סקטורים, 50 מניות)
                  או <b style="color:#fff;">Nasdaq 100</b> (8 סקטורים, 50 מניות)<br>
                • גודל ריבוע =
                  <b style="color:#fff;">Market Cap</b> — Apple גדולה מ-Intel<br>
                • <b style="color:#2ecc71;">ירוק</b> = עלייה יומית |
                  <b style="color:#e74c3c;">אדום</b> = ירידה יומית<br>
                • <b style="color:#fff;">Hover</b> על ריבוע: מחיר, שינוי $/%,
                  Market Cap, שם חברה<br>
                • <b style="color:#fff;">לחץ</b> על סקטור להתמקדות |
                  לחץ שוב לחזרה<br>
                • הנתונים נשמרים ב-<b style="color:#fff;">cache 10 דקות</b>
                  — לחץ רענן לנתונים חדשים
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # =====================================================================
    # B. בחירת רשימת מניות לפי מדד
    # =====================================================================
    use_sp500     = "S&P 500" in hm_index
    stocks_list   = HEATMAP_SP500_STOCKS if use_sp500 else HEATMAP_NDX_STOCKS
    root_label    = "S&P 500" if use_sp500 else "Nasdaq 100"

    # =====================================================================
    # C. שליפת מחירים עם cache + spinner
    # =====================================================================
    symbols_tuple = tuple(s[0] for s in stocks_list)  # tuple לhashable cache key

    with st.spinner(f"⏳ טוען נתוני שוק עבור {len(symbols_tuple)} מניות... (עד 20 שניות)"):
        price_data = _fetch_heatmap_prices(symbols_tuple)

    # בדיקה שיש נתונים תקינים
    valid_count = sum(1 for p, c, d in price_data.values() if p is not None)
    if valid_count == 0:
        st.error(
            "⚠️ לא הצלחנו לטעון נתוני מחירים. "
            "בדוק חיבור אינטרנט ולחץ שוב על 'טען מפת חום'."
        )
        return

    st.success(f"✅ נטענו נתוני {valid_count}/{len(symbols_tuple)} מניות בהצלחה")

    # =====================================================================
    # D. בניית מבנה הנתונים לTreemap
    # =====================================================================
    # צבירת סקטורים — שווי שוק מצטבר לכל סקטור
    sector_cap   = {}   # sector_label → total market cap
    sector_chg   = {}   # sector_label → weighted avg change
    sector_weight= {}   # sector_label → total weight for avg

    for sym, sec_label, company, cap_b in stocks_list:
        price, chg_pct, chg_dollar = price_data.get(sym, (None, 0.0, 0.0))
        if sec_label not in sector_cap:
            sector_cap[sec_label]    = 0
            sector_chg[sec_label]    = 0.0
            sector_weight[sec_label] = 0
        sector_cap[sec_label]    += cap_b
        sector_chg[sec_label]    += chg_pct * cap_b   # weighted
        sector_weight[sec_label] += cap_b

    # ממוצע משוקלל שינוי לסקטור
    for sec_label in sector_chg:
        if sector_weight[sec_label] > 0:
            sector_chg[sec_label] = sector_chg[sec_label] / sector_weight[sec_label]

    # בניית arrays לTreemap
    hm_ids      = []
    hm_labels   = []
    hm_parents  = []
    hm_values   = []
    hm_colors   = []   # שינוי % לצביעה
    hm_custom   = []   # [sym/label, chg_pct, price, cap_b, chg_dollar, company]

    # שורש
    total_cap_root = sum(sector_cap.values())
    hm_ids.append(root_label)
    hm_labels.append(root_label)
    hm_parents.append("")
    hm_values.append(total_cap_root)
    hm_colors.append(0.0)
    hm_custom.append([root_label, 0.0, 0.0, total_cap_root, 0.0, root_label])

    # סקטורים
    seen_sectors = []
    for sym, sec_label, company, cap_b in stocks_list:
        if sec_label not in seen_sectors:
            seen_sectors.append(sec_label)
            sec_id  = f"SEC_{sec_label}"
            sec_c   = sector_cap.get(sec_label, 0)
            sec_chg = round(sector_chg.get(sec_label, 0.0), 2)
            hm_ids.append(sec_id)
            hm_labels.append(sec_label)
            hm_parents.append(root_label)
            hm_values.append(sec_c)
            hm_colors.append(sec_chg)
            hm_custom.append([sec_label, sec_chg, 0.0, sec_c, 0.0, "סקטור"])

    # מניות
    for sym, sec_label, company, cap_b in stocks_list:
        price, chg_pct, chg_dollar = price_data.get(sym, (None, 0.0, 0.0))
        sec_id    = f"SEC_{sec_label}"
        stock_id  = f"STK_{sym}"
        price_val = price if price is not None else 0.0

        hm_ids.append(stock_id)
        hm_labels.append(sym)
        hm_parents.append(sec_id)
        hm_values.append(max(cap_b, 1))
        hm_colors.append(round(chg_pct, 3))
        hm_custom.append([sym, chg_pct, price_val, cap_b, chg_dollar, company])

    # =====================================================================
    # E. סקלת צבעים
    # =====================================================================
    if "כחול" in hm_colorset:
        colorscale_def = [
            [0.00, '#082567'], [0.22, '#1a5fc8'], [0.40, '#7ab4f5'],
            [0.47, '#d0d8e8'], [0.53, '#d0d8e8'],
            [0.60, '#f4b860'], [0.78, '#d4680a'], [1.00, '#6b2d00'],
        ]
    else:
        # ירוק/אדום קלאסי
        colorscale_def = [
            [0.00, '#5c0000'], [0.20, '#c0392b'], [0.38, '#e88a8a'],
            [0.47, '#d5dce8'], [0.53, '#d5dce8'],
            [0.62, '#7fc87f'], [0.80, '#1a7a3a'], [1.00, '#003a10'],
        ]

    # =====================================================================
    # F. בניית ה-Treemap
    # =====================================================================
    custom_arr = [
        [c[0], c[1], c[2], c[3], c[4], c[5]]
        for c in hm_custom
    ]

    treemap_fig = go.Figure(go.Treemap(
        ids=hm_ids,
        labels=hm_labels,
        parents=hm_parents,
        values=hm_values,
        customdata=custom_arr,
        # טקסט בתוך הריבוע: שם מניה + שינוי %
        texttemplate=(
            "<b>%{label}</b><br>"
            "%{customdata[1]:+.2f}%"
        ),
        # Hover: פרטי מניה מלאים
        hovertemplate=(
            "<b>%{customdata[0]}</b>  —  %{customdata[5]}<br>"
            "━━━━━━━━━━━━━━━━━━━━━━<br>"
            "💰 מחיר: <b>$%{customdata[2]:.2f}</b><br>"
            "📊 שינוי יומי: <b>%{customdata[1]:+.2f}%</b>"
            "   ($%{customdata[4]:+.2f})<br>"
            "🏦 Market Cap: <b>$%{customdata[3]:,.0f}B</b><br>"
            "<extra></extra>"
        ),
        marker=dict(
            colors=hm_colors,
            colorscale=colorscale_def,
            cmin=-3.5,
            cmax=3.5,
            showscale=True,
            colorbar=dict(
                title=dict(
                    text="שינוי יומי %",
                    font=dict(size=13, family="Assistant")
                ),
                tickvals=[-3, -2, -1, 0, 1, 2, 3],
                ticktext=["-3%", "-2%", "-1%", " 0%", "+1%", "+2%", "+3%"],
                tickfont=dict(size=11, family="Assistant"),
                thickness=20,
                len=0.82,
                bgcolor="rgba(248,249,250,0.95)",
                bordercolor="#ced4da",
                borderwidth=1.5,
                x=1.01,
                xpad=6
            ),
            pad=dict(t=4, l=4, r=4, b=4),
            line=dict(width=2, color="#ffffff")
        ),
        textfont=dict(size=13, family="Assistant", color="#0a0a0a"),
        tiling=dict(squarifyratio=1.618),
        maxdepth=3,
        branchvalues="total",
        pathbar=dict(
            visible=True,
            thickness=26,
            textfont=dict(size=13, family="Assistant", color="#ffffff"),
            edgeshape=">",
        ),
        root=dict(color="#e8ecf0"),
    ))

    treemap_fig.update_layout(
        title=dict(
            text=(
                f"{root_label} Market Heatmap  |  "
                f"{valid_count} מניות  |  "
                f"גודל = Market Cap  |  צבע = שינוי יומי %"
            ),
            font=dict(size=14, family="Assistant", color="#2c3e50"),
            x=0.01, xanchor="left"
        ),
        margin=dict(l=8, r=90, t=52, b=8),
        height=740,
        paper_bgcolor="#f0f2f5",
        plot_bgcolor="#f0f2f5",
        font=dict(family="Assistant"),
        hoverlabel=dict(
            bgcolor="#1a1a2e",
            bordercolor="#4a90d9",
            font=dict(size=13, family="Assistant", color="#ffffff")
        )
    )

    st.plotly_chart(treemap_fig, use_container_width=True)

    # =====================================================================
    # G. Bar Chart — שינוי יומי לפי סקטור
    # =====================================================================
    st.markdown("#### 📊 שינוי יומי ממוצע לפי סקטור")

    bar_data = [
        {"label": lab, "chg": round(sector_chg.get(lab, 0.0), 2)}
        for lab in seen_sectors
    ]
    bar_data.sort(key=lambda x: x["chg"], reverse=True)

    bar_labels = [b["label"] for b in bar_data]
    bar_values = [b["chg"] for b in bar_data]
    bar_colors = ["#1a7a3a" if v >= 0 else "#c0392b" for v in bar_values]
    bar_texts  = [f"{v:+.2f}%" for v in bar_values]

    bar_fig = go.Figure(go.Bar(
        x=bar_labels,
        y=bar_values,
        marker_color=bar_colors,
        text=bar_texts,
        textposition="outside",
        textfont=dict(size=13, family="Assistant", color="#1a1a1a"),
        hovertemplate="<b>%{x}</b><br>שינוי: %{y:+.2f}%<extra></extra>"
    ))
    bar_fig.update_layout(
        template="plotly_white",
        height=320,
        margin=dict(l=20, r=20, t=20, b=120),
        xaxis=dict(tickangle=-30, tickfont=dict(size=11, family="Assistant")),
        yaxis=dict(
            title="שינוי יומי ממוצע %",
            ticksuffix="%",
            zeroline=True,
            zerolinecolor="#dee2e6",
            zerolinewidth=2
        ),
        font=dict(family="Assistant"),
        showlegend=False,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff"
    )
    st.plotly_chart(bar_fig, use_container_width=True)

    # =====================================================================
    # H. טבלת סיכום מפורטת
    # =====================================================================
    st.markdown("#### 📋 טבלת שינויים — כל הסקטורים")
    summary_rows = []
    for sec_label in seen_sectors:
        chg  = round(sector_chg.get(sec_label, 0.0), 2)
        icon = "🟢" if chg > 0.15 else ("🔴" if chg < -0.15 else "⚪")
        cap  = sector_cap.get(sec_label, 0)
        summary_rows.append({
            "סקטור":       sec_label,
            "שינוי יומי":  f"{icon} {chg:+.2f}%",
            "שווי שוק $B": f"${cap:,}B",
        })
    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)



# ==============================================================================
# 16. [חדש] Expert Alerts Engine — התראות מחיר חכמות
# ==============================================================================

def render_expert_alerts_section(selected_ticker, current_price):
    """
    [פיצ'ר חדש] מנוע התראות מחיר Expert Alerts — מוטמע בתוך לשונית הסורק.
    מאפשר להגדיר התראות מחיר פשוטות לכל מניה שנבחרה בסורק:
      - התראה כשהמחיר עובר מעל סף מוגדר (Above Alert).
      - התראה כשהמחיר יורד מתחת לסף מוגדר (Below Alert).
    כל ההתראות נשמרות ב-SQLite ונבדקות בזמן הסריקה.
    מציג: רשימת התראות פעילות, התראות שהופעלו והיסטוריה.
    """
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #fff9f0 0%, #fffbf5 100%);
         border:2px solid #ffc107; border-right:18px solid #ff9800;
         border-radius:30px; padding:30px 40px; margin-bottom:30px;
         direction:rtl; text-align:right;
         box-shadow:0 10px 35px rgba(255,152,0,0.12);">
        <b style="font-size:1.6rem; color:#e67e00;">🔔 Expert Alerts Engine — התראות מחיר עבור {selected_ticker}</b><br>
        <p style="font-size:1.2rem; color:#856404; margin-top:10px; margin-bottom:0;">
            מחיר נוכחי: <b>${current_price:.2f}</b> | הגדר התראה — תקבל אינדיקציה בפעם הבאה שתסרוק
        </p>
    </div>
    """, unsafe_allow_html=True)

    # טופס הגדרת התראה
    al_c1, al_c2, al_c3, al_c4 = st.columns([1.5, 2, 1.5, 1.5])
    with al_c1:
        alert_direction = st.selectbox(
            "סוג התראה:",
            options=["above", "below"],
            format_func=lambda x: "📈 מעל מחיר" if x == "above" else "📉 מתחת למחיר",
            key=f"alert_dir_{selected_ticker}"
        )
    with al_c2:
        # ברירת מחדל: +5% מעל או -5% מתחת
        default_target = current_price * 1.05 if alert_direction == 'above' else current_price * 0.95
        alert_target = st.number_input(
            "מחיר יעד ($):",
            min_value=0.01,
            value=round(default_target, 2),
            step=0.5,
            format="%.2f",
            key=f"alert_target_{selected_ticker}"
        )
    with al_c3:
        alert_note = st.text_input("תזכורת (אופציונלי):", placeholder="לדוגמה: פריצת ריסיסטנס", key=f"alert_note_{selected_ticker}")
    with al_c4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔔 הוסף התראה", key=f"add_alert_{selected_ticker}", use_container_width=True):
            if alert_target > 0:
                add_price_alert(selected_ticker, alert_target, alert_direction, alert_note)
                direction_heb = "מעל" if alert_direction == "above" else "מתחת ל"
                st.toast(f"✅ התראה נוספה: {selected_ticker} {direction_heb} ${alert_target:.2f}")
                st.rerun()

    # הצגת התראות פעילות לסימול הנבחר
    active_alerts = [a for a in fetch_alerts(include_triggered=False) if a[1].upper() == selected_ticker.upper()]
    triggered_alerts = [a for a in fetch_alerts(include_triggered=True) if a[1].upper() == selected_ticker.upper() and a[5] == 1]

    if active_alerts:
        st.markdown(f"**🔔 התראות פעילות עבור {selected_ticker}:**")
        for alert in active_alerts:
            alert_id, ticker, target, direction, note, _, date_created, _ = alert
            dir_heb  = "📈 מעל" if direction == 'above' else "📉 מתחת ל"
            gap_pct  = ((target - current_price) / current_price) * 100
            gap_str  = f"{gap_pct:+.1f}% מהמחיר הנוכחי"
            st.markdown(f"""
            <div class="alert-card-active">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:1.25rem; font-weight:800; color:#e67e00;">
                        {dir_heb} <span style="direction:ltr; display:inline-block;">${target:.2f}</span>
                        &nbsp;|&nbsp; {gap_str}
                    </span>
                    <span style="font-size:1.1rem; color:#888;">{date_created[:10] if date_created else ''}</span>
                </div>
                {f'<p style="margin:8px 0 0 0; font-size:1.1rem; color:#555;">📝 {note}</p>' if note else ''}
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🗑️ מחק התראה #{alert_id}", key=f"del_alert_{alert_id}"):
                delete_alert(alert_id)
                st.rerun()

    if triggered_alerts:
        st.markdown(f"**✅ התראות שהופעלו עבור {selected_ticker} (היסטוריה):**")
        for alert in triggered_alerts[:3]:
            alert_id, ticker, target, direction, note, _, date_created, date_triggered = alert
            dir_heb = "מעל" if direction == 'above' else "מתחת ל"
            st.markdown(f"""
            <div class="alert-card-triggered">
                <span style="font-size:1.2rem; font-weight:800; color:#dc3545;">
                    ✅ הופעל: {dir_heb} ${target:.2f}
                </span>
                <span style="font-size:1.0rem; color:#888;"> | הופעל ב-{date_triggered[:10] if date_triggered else 'N/A'}</span>
                {f'<p style="margin:6px 0 0 0; font-size:1.1rem; color:#555;">📝 {note}</p>' if note else ''}
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# 17. בדיקת התראות גלובלית (Global Alert Check on Scan)
# ==============================================================================

def check_and_display_global_alerts(scan_df):
    """
    בדיקת כל ההתראות הפעילות מול תוצאות הסריקה האחרונה.
    מציגה banner בולט לכל התראה שהופעלה.
    """
    if scan_df is None or scan_df.empty:
        return

    prices_dict = {}
    for _, row in scan_df.iterrows():
        try:
            prices_dict[row['מניה']] = float(row['מחיר ($)'])
        except:
            pass

    triggered = check_alerts_against_prices(prices_dict)
    if triggered:
        for ticker, target, direction, note, cur in triggered:
            dir_heb = "עלה מעל" if direction == 'above' else "ירד מתחת ל"
            st.markdown(f"""
            <div style="background:linear-gradient(135deg, #fff0f0, #ffe8e8);
                 border:3px solid #dc3545; border-radius:25px; padding:25px 35px;
                 margin-bottom:20px; direction:rtl; text-align:right;
                 box-shadow:0 10px 35px rgba(220,53,69,0.2);">
                <b style="font-size:1.5rem; color:#dc3545;">
                    🚨 התראת מחיר הופעלה! {ticker} {dir_heb} ${target:.2f}
                </b><br>
                <span style="font-size:1.2rem; color:#555;">
                    מחיר נוכחי: <b>${cur:.2f}</b>
                    {f" | הערה: {note}" if note else ""}
                </span>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# 18. ממשק המשתמש הראשי — Ultimate Terminal
# ==============================================================================

# ==============================================================================
# AUTH-1. מסך כניסה / הרשמה (Login & Register Wall)
# ==============================================================================

def render_auth_wall():
    """
    מסך ההתחברות/הרשמה — Login Wall שנעול לפני כל הפיצ'רים.
    מציג טופס Login ברירת מחדל, עם כפתור מעבר להרשמה.
    עיצוב מלא תואם לפלטת הצבעים הקיימת.
    """

    # כותרת ומיתוג
    st.markdown("<h1>📈 Elite Strategic Trading Terminal</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; font-size:1.5rem; color:#555; "
        "font-weight:700; margin-bottom:2.5rem;'>"
        "מסוף ניתוח וניהול תיקי השקעות מקצועי | SaaS Edition 2026"
        "</p>",
        unsafe_allow_html=True
    )

    # כרטיס מרכזי
    _, card_col, _ = st.columns([1, 2, 1])
    with card_col:
        if st.session_state.auth_page == 'login':
            _render_login_form()
        else:
            _render_register_form()


def _render_login_form():
    """טופס התחברות."""
    st.markdown("""
    <div style="background:#ffffff; border:2px solid #e9ecef; border-radius:30px;
         padding:45px 50px; box-shadow:0 20px 60px rgba(0,0,0,0.08);
         direction:rtl; text-align:right;">
        <h3 style="color:#007bff; font-size:2rem; margin-top:0; border:none; padding:0;
                   text-align:center;">
            🔐 התחברות למערכת
        </h3>
        <p style="color:#888; font-size:1rem; text-align:center; margin-bottom:30px;">
            הכנס את פרטי החשבון שלך
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        login_user = st.text_input(
            "שם משתמש", placeholder="הכנס שם משתמש",
            key="login_username"
        )
        login_pass = st.text_input(
            "סיסמה", type="password", placeholder="הכנס סיסמה",
            key="login_password"
        )
        login_submitted = st.form_submit_button(
            "🔐 התחבר", type="primary", use_container_width=True
        )

    if login_submitted:
        if not login_user or not login_pass:
            st.error("אנא מלא את כל השדות.")
        else:
            ok, result = auth_login(login_user, login_pass)
            if ok:
                st.session_state.auth_user = result
                st.session_state.h_master_scan_results = None
                st.session_state.h_scan_time_reference = None
                st.toast(f"✅ ברוך הבא, {result['display_name']}!")
                st.rerun()
            else:
                st.error(f"❌ {result}")

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown(
            "<p style='text-align:center; color:#888; font-size:0.9rem;'>"
            "אין לך חשבון עדיין?</p>",
            unsafe_allow_html=True
        )
    with col_b:
        if st.button("📝 הירשם עכשיו", use_container_width=True):
            st.session_state.auth_page = 'register'
            st.rerun()




def _render_register_form():
    """טופס הרשמה."""
    st.markdown("""
    <div style="background:#ffffff; border:2px solid #e9ecef; border-radius:30px;
         padding:45px 50px; box-shadow:0 20px 60px rgba(0,0,0,0.08);
         direction:rtl; text-align:right;">
        <h3 style="color:#28a745; font-size:2rem; margin-top:0; border:none; padding:0;
                   text-align:center;">
            📝 הרשמה — צור חשבון חדש
        </h3>
        <p style="color:#888; font-size:1rem; text-align:center; margin-bottom:30px;">
            פתח חשבון אישי וגשה לכל הפיצ'רים
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("register_form", clear_on_submit=False):
        reg_display = st.text_input(
            "שם תצוגה (שמך)", placeholder="לדוגמה: דן כהן",
            key="reg_display"
        )
        reg_user = st.text_input(
            "שם משתמש (אנגלית, לפחות 3 תווים)",
            placeholder="לדוגמה: dank2026",
            key="reg_username"
        )
        reg_email = st.text_input(
            "אימייל (אופציונלי)", placeholder="your@email.com",
            key="reg_email"
        )
        reg_pass = st.text_input(
            "סיסמה (לפחות 6 תווים)", type="password",
            placeholder="בחר סיסמה חזקה", key="reg_pass"
        )
        reg_pass2 = st.text_input(
            "אישור סיסמה", type="password",
            placeholder="הכנס שוב את הסיסמה", key="reg_pass2"
        )
        reg_submitted = st.form_submit_button(
            "✅ צור חשבון", type="primary", use_container_width=True
        )

    if reg_submitted:
        if reg_pass != reg_pass2:
            st.error("❌ הסיסמאות אינן תואמות.")
        else:
            ok, result = auth_register(reg_user, reg_pass, reg_display, reg_email)
            if ok:
                st.success("✅ החשבון נוצר בהצלחה! עכשיו התחבר.")
                st.session_state.auth_page = 'login'
                st.rerun()
            else:
                st.error(f"❌ {result}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← חזור להתחברות", use_container_width=True):
        st.session_state.auth_page = 'login'
        st.rerun()


# ==============================================================================
# AUTH-2. Header Bar — סרגל עליון עם שם משתמש + כפתור יציאה
# ==============================================================================

def render_user_header():
    """
    סרגל עליון (Header Bar) המציג:
      - שם המשתמש המחובר ('שלום, [שם]').
      - תפקיד (👑 Admin / 👤 משתמש).
      - כפתור יציאה (Logout) בצד שמאל.
    מוצג בראש כל עמוד לאחר התחברות.
    """
    user = st.session_state.auth_user
    if not user:
        return

    role_icon  = "👑 Admin" if user.get("is_admin") else "👤 משתמש"
    user_color = "#e67e00" if user.get("is_admin") else "#007bff"

    hdr_left, hdr_right = st.columns([3, 1])
    with hdr_left:
        st.markdown(
            f"<div style='padding:10px 0; direction:rtl;'>"
            f"<span style='font-size:1.2rem; font-weight:800; color:{user_color};'>"
            f"{role_icon}</span>"
            f"<span style='font-size:1.2rem; color:#1a1a1a; margin-right:10px;'>"
            f" | שלום, <b>{user['display_name']}</b></span>"
            f"<span style='font-size:0.9rem; color:#aaa; margin-right:8px;'>"
            f"({user['username']})</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with hdr_right:
        if st.button("🚪 יציאה", key="logout_btn", use_container_width=True):
            st.session_state.auth_user          = None
            st.session_state.auth_page          = 'login'
            st.session_state.h_master_scan_results = None
            st.session_state.h_scan_time_reference = None
            st.rerun()


# ==============================================================================
# AUTH-3. Admin Panel — לוח ניהול מערכת
# ==============================================================================

def render_admin_panel():
    """
    Admin Panel — לוח ניהול נגיש רק למשתמש Admin.
    מציג:
      - סה"כ משתמשים רשומים (לא כולל Admin).
      - טבלת כל המשתמשים: שם, שם תצוגה, אימייל, תאריך הצטרפות.
      - סטטיסטיקות תיקים: כמה פוזיציות לכל משתמש.
    """
    user = st.session_state.auth_user
    if not user or not user.get("is_admin"):
        st.error("⛔ גישה נדחית — הדף זמין למנהלי מערכת בלבד.")
        return

    st.markdown("""
    <div style="background:linear-gradient(135deg,#1a0a2e 0%,#2a1a4e 100%);
         border-radius:28px; padding:30px 50px; margin-bottom:30px; text-align:center;
         box-shadow:0 15px 50px rgba(0,0,0,0.2);">
        <h2 style="color:#ffffff; font-size:2.4rem; margin:0; border:none; padding:0;">
            👑 Admin Control Panel
        </h2>
        <p style="color:#a090d0; font-size:1.2rem; margin-top:10px;">
            ניהול משתמשים ונתוני מערכת
        </p>
    </div>
    """, unsafe_allow_html=True)

    # מספר משתמשים
    total_users = auth_get_user_count()
    all_users   = auth_get_all_users()

    # סטטיסטיקות תיקים
    conn    = sqlite3.connect(DB_PATH)
    pf_stats = conn.execute(
        "SELECT user_id, COUNT(*) as positions FROM elite_portfolio_v1 GROUP BY user_id"
    ).fetchall()
    jn_stats = conn.execute(
        "SELECT user_id, COUNT(*) as items FROM elite_journal_v5 GROUP BY user_id"
    ).fetchall()
    conn.close()

    pf_map = {row[0]: row[1] for row in pf_stats}
    jn_map = {row[0]: row[1] for row in jn_stats}

    # כרטיסי סטטיסטיקות
    adm_c1, adm_c2, adm_c3 = st.columns(3)
    with adm_c1:
        st.markdown(f"""
        <div style="background:#ffffff; border:2px solid #e9ecef; border-radius:22px;
             padding:30px; text-align:center; box-shadow:0 8px 28px rgba(0,0,0,0.07);">
            <p style="font-size:3.5rem; font-weight:900; color:#007bff; margin:0;">{total_users}</p>
            <p style="color:#888; margin:8px 0 0 0; font-weight:700;">משתמשים רשומים</p>
        </div>
        """, unsafe_allow_html=True)
    with adm_c2:
        total_pf = sum(pf_map.values())
        st.markdown(f"""
        <div style="background:#ffffff; border:2px solid #e9ecef; border-radius:22px;
             padding:30px; text-align:center; box-shadow:0 8px 28px rgba(0,0,0,0.07);">
            <p style="font-size:3.5rem; font-weight:900; color:#28a745; margin:0;">{total_pf}</p>
            <p style="color:#888; margin:8px 0 0 0; font-weight:700;">פוזיציות בתיקים</p>
        </div>
        """, unsafe_allow_html=True)
    with adm_c3:
        total_jn = sum(jn_map.values())
        st.markdown(f"""
        <div style="background:#ffffff; border:2px solid #e9ecef; border-radius:22px;
             padding:30px; text-align:center; box-shadow:0 8px 28px rgba(0,0,0,0.07);">
            <p style="font-size:3.5rem; font-weight:900; color:#ff7f0e; margin:0;">{total_jn}</p>
            <p style="color:#888; margin:8px 0 0 0; font-weight:700;">רשומות ביומן</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # טבלת משתמשים מלאה
    st.markdown("#### 👥 כל המשתמשים הרשומים")
    if all_users:
        user_rows = []
        for u in all_users:
            uid, uname, dname, email, created, is_admin = u
            role   = "👑 Admin" if is_admin else "👤 משתמש"
            pf_cnt = pf_map.get(uid, 0)
            jn_cnt = jn_map.get(uid, 0)
            user_rows.append({
                "ID":              uid,
                "שם משתמש":        uname,
                "שם תצוגה":        dname,
                "אימייל":          email or "—",
                "תאריך הצטרפות":  (created or "")[:10],
                "תפקיד":           role,
                "פוזיציות בתיק":  pf_cnt,
                "רשומות ביומן":   jn_cnt,
            })
        st.dataframe(pd.DataFrame(user_rows), use_container_width=True, hide_index=True)
    else:
        st.info("אין משתמשים רשומים עדיין.")

    st.divider()
    st.markdown(
        "<p style='text-align:center; color:#bbb; font-size:0.85rem;'>"
        f"Elite Trading Terminal — Admin Panel | {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        "</p>",
        unsafe_allow_html=True
    )


def run_terminal():
    """
    הפונקציה המנהלת הראשית של הטרמינל האסטרטגי — Ultimate Edition.
    מנהלת 8 לשוניות:
      1. סורק שוק — עם TradingView widget ו-Expert Alerts.
      2. AI Insight — ניתוח P/E + Sentiment.
      3. Multi-Chart — 4 מניות במקביל.
      4. Portfolio Manager — עם Pie Chart ו-% מהתיק.
      5. Market Heatmap — [חדש] Treemap של 11 סקטורים.
      6. יומן מסחר.
      7. קרב ביצועים (Versus).
    """

    # כותרת ראשית + פרסונליזציה
    user = st.session_state.get('auth_user', {})
    display_name = user.get('display_name', '') if user else ''
    welcome_suffix = f" — ברוך הבא, {display_name}!" if display_name else ""

    st.markdown("<h1>📈 Elite Strategic Trading Terminal</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='text-align:center; font-size:1.8rem; color:#555; font-weight:700; margin-bottom:3rem;'>"
        f"מסוף ניתוח וניהול תיקי השקעות | Ultimate Professional Edition 2026"
        f"{welcome_suffix}</p>",
        unsafe_allow_html=True
    )

    # Market Overview
    render_market_overview()

    # ---- Fear & Greed Gauge — מדד פחד ותאוות בצע ----
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
         border-radius: 28px; padding: 16px 40px 6px 40px;
         margin-bottom: 8px; text-align: center;
         box-shadow: 0 10px 35px rgba(0,0,0,0.18);">
        <p style="color: #a0bfd0; font-size: 1rem; margin: 0;
                  font-weight: 800; letter-spacing: 2.5px;
                  font-family: 'Assistant', sans-serif; text-transform: uppercase;">
            Fear &amp; Greed Index — מדד פחד ותאוות בצע
        </p>
    </div>
    """, unsafe_allow_html=True)
    render_fear_greed_gauge()

    st.divider()

    # ---- לשוניות ראשיות ----
    (tab_scanner, tab_ai, tab_multi,
     tab_portfolio, tab_heatmap,
     tab_journal, tab_versus) = st.tabs([
        "🔍 סורק שוק",
        "🤖 AI Insight",
        "📊 Multi-Chart",
        "💼 Portfolio",
        "🗺️ Market Heatmap",
        "📝 יומן מסחר",
        "⚔️ קרב ביצועים",
    ])

    # ==========================================================
    # Sidebar: Admin section (visible always for admin users)
    # ==========================================================
    _auth_user_now = st.session_state.get('auth_user', {})
    if _auth_user_now and _auth_user_now.get('is_admin'):
        st.sidebar.markdown("---")
        st.sidebar.markdown(
            "<div style='background:linear-gradient(135deg,#1a0a2e,#2a1a4e);"
            "border-radius:14px; padding:12px 16px; text-align:center;"
            "margin-bottom:8px;'>"
            "<p style='color:#e0c8ff; font-size:0.95rem; margin:0; font-weight:800;"
            "letter-spacing:1px;'>👑 Admin Dashboard</p>"
            "</div>",
            unsafe_allow_html=True
        )
        st.sidebar.markdown(
            f"<p style='font-size:0.8rem; color:#888; margin:0 0 8px 0; text-align:center;'>"
            f"משתמשים: <b>{auth_get_user_count()}</b></p>",
            unsafe_allow_html=True
        )
        if st.sidebar.button("👑 פתח Admin Dashboard", key="sidebar_admin_btn",
                             use_container_width=True):
            st.session_state['show_admin_panel'] = True
        st.sidebar.markdown("---")

    # Admin panel full-page overlay (triggered from sidebar button)
    if st.session_state.get('show_admin_panel') and _auth_user_now.get('is_admin'):
        render_admin_panel()
        if st.button("← חזור לטרמינל", key="admin_back_btn"):
            st.session_state['show_admin_panel'] = False
            st.rerun()
        return   # don't render terminal while admin panel is open

    # ==========================================================
    # לשונית 1: סורק שוק + TradingView + Expert Alerts
    # ==========================================================
    with tab_scanner:
        st.sidebar.header("⚙️ לוח בקרה — מנוע סריקה")
        scan_mode = st.sidebar.radio(
            "בחר קבוצת מניות לסריקה:",
            ["רשימה אישית (Custom List)", "Top 24 Nasdaq Elite"]
        )

        if scan_mode == "רשימה אישית (Custom List)":
            raw_input = st.sidebar.text_area(
                "סימולי מניות (מופרדים בפסיק):",
                "NVDA, TSLA, AAPL, MSFT, AMD, META, GOOGL, PLTR, COIN, MSTR, AMZN, NFLX"
            )
            scan_list = [s.strip().upper() for s in raw_input.split(',')]
        else:
            scan_list = [
                'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META', 'TSLA', 'AVGO',
                'PEP', 'COST', 'CSCO', 'TMUS', 'ADBE', 'TXN', 'NFLX', 'QCOM',
                'AMD', 'INTU', 'AMAT', 'ISRG', 'HON', 'AMGN', 'VRTX', 'SBUX'
            ]

        if st.sidebar.button("🚀 הפעל מנוע סריקה", type="primary", use_container_width=True):
            results  = []
            progress = st.progress(0, text="מתחבר לבורסה...")
            for i, sym in enumerate(scan_list):
                pct = int(((i + 1) / len(scan_list)) * 100)
                progress.progress(pct, text=f"מנתח: {sym}...")
                result = analyze_stock(sym)
                if result:
                    results.append(result)
                time.sleep(0.01)
            progress.empty()

            if results:
                st.session_state.h_master_scan_results = pd.DataFrame(results)
                st.session_state.h_scan_time_reference = datetime.now().strftime("%H:%M:%S")
                # בדיקת התראות מול תוצאות הסריקה
                check_and_display_global_alerts(st.session_state.h_master_scan_results)
            else:
                st.error("לא הצלחנו למשוך נתונים. בדוק חיבור אינטרנט.")

        # הצגת בנר התראות גלובלי
        if st.session_state.h_master_scan_results is not None:
            check_and_display_global_alerts(st.session_state.h_master_scan_results)

        # הצגת תוצאות סריקה
        if st.session_state.h_master_scan_results is not None:
            df = st.session_state.h_master_scan_results
            st.subheader(f"📊 תמונת שוק — סריקה אחרונה ({st.session_state.h_scan_time_reference})")

            fcol1, _ = st.columns([3, 1])
            with fcol1:
                filt = st.radio(
                    "סינון מהיר:",
                    ["הכל", "🚀 הזדמנויות קנייה (BUY)", "📈 מומנטום (TRENDING)"],
                    horizontal=True
                )
            if "קנייה" in filt:
                display_df = df[df['סיגנל'].str.contains('BUY', na=False)]
            elif "מומנטום" in filt:
                display_df = df[df['סיגנל'].str.contains('TRENDING', na=False)]
            else:
                display_df = df

            st.dataframe(display_df, use_container_width=True, hide_index=True)
            csv = display_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 ייצוא ל-CSV", csv, "scan_results.csv", "text/csv", use_container_width=True)
            st.divider()

            # ניתוח מפורט
            main_col, side_col = st.columns([2, 1])

            with main_col:
                st.subheader("🔍 ניתוח מפורט + TradingView")
                selected = st.selectbox("בחר מניה לניתוח:", df['מניה'].tolist())
                row      = df[df['מניה'] == selected].iloc[0]
                cur_px   = float(row['מחיר ($)'])

                render_action_protocol(row)

                # ---- [שדרוג] TradingView Advanced Chart ----
                st.markdown("---")
                st.markdown("""
                <div style="background:linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                     border-radius:20px; padding:18px 30px; margin-bottom:18px; text-align:center;">
                    <p style="color:#a0bfd0; font-size:1.1rem; margin:0; font-weight:700; letter-spacing:2px;">
                        TRADINGVIEW ADVANCED CHART
                    </p>
                    <p style="color:#ffffff; font-size:0.95rem; margin:6px 0 0 0; opacity:0.7;">
                        ✏️ כלי ציור | 📊 אינדיקטורים | 🕐 Multi-Timeframe | 📋 Watchlist
                    </p>
                </div>
                """, unsafe_allow_html=True)
                render_tradingview_chart(selected)

                # Plotly fallback option
                with st.expander("📊 הצג גרף Plotly נוסף (נרות + MA + Volume)"):
                    fallback_chart = render_advanced_chart_fallback(selected)
                    if fallback_chart:
                        st.plotly_chart(fallback_chart, use_container_width=True)

                st.divider()
                render_live_news(selected)

                # ---- [חדש] Performance Alpha — YTD vs S&P 500 ----
                st.divider()
                st.markdown("#### 📊 Performance Alpha — ביצועים מול S&P 500 מתחילת השנה")
                render_performance_alpha(selected)

                # ---- [חדש] Insider & Institutional Stats ----
                st.divider()
                render_insider_institutional(selected)

                # ---- [חדש] Expert Alerts Section ----
                st.divider()
                render_expert_alerts_section(selected, cur_px)

            with side_col:
                render_risk_gauge(row)

                st.subheader("🧮 מחשבון פוזיציה")
                sl_price = float(row['Stop Loss'])
                st.markdown(f"**מניה:** `{selected}` | **מחיר:** `${cur_px:.2f}`")

                invest_sum = st.number_input("סכום השקעה ($):", min_value=100, value=1000, step=100)
                risk_pct   = ((cur_px - sl_price) / cur_px) * 100
                st.warning(f"Stop Loss: `${sl_price}` ({risk_pct:.1f}% סיכון)")

                qty_calc = invest_sum / cur_px
                usd_risk = invest_sum * (risk_pct / 100)
                tp_calc  = cur_px * (1 + (risk_pct * 2 / 100))

                st.success(f"""
                **תוכנית עבודה:**
                * 🛒 כמות: `{qty_calc:.2f}`
                * 🛑 SL: `${sl_price:.2f}`
                * 🎯 TP: `${tp_calc:.2f}`
                * 📉 סיכון: `${usd_risk:.2f}`
                """)

                st.subheader("⭐ שמירה ליומן")
                note_input = st.text_area("הערה אישית:")
                if st.button("💾 שמור ביומן", type="primary", use_container_width=True):
                    if save_to_journal(selected, note_input):
                        st.toast(f"✅ {selected} נשמר!")
                    else:
                        st.warning("המניה כבר קיימת ביומן.")

                # סיכום התראות פעילות בסיידבר
                all_active = fetch_alerts(include_triggered=False)
                if all_active:
                    st.divider()
                    st.markdown(f"**🔔 סה\"כ {len(all_active)} התראות פעילות**")
                    for a in all_active[:5]:
                        dir_heb = "↑" if a[3] == 'above' else "↓"
                        st.markdown(f"• `{a[1]}` {dir_heb} ${a[2]:.2f}")

    # ==========================================================
    # לשונית 2: AI Insight
    # ==========================================================
    with tab_ai:
        st.subheader("🤖 AI Insight — ניתוח אינטליגנטי מפורט")
        st.markdown("""
        <div style="background:#f0f7ff; border-right:15px solid #007bff; border-radius:25px;
             padding:30px 40px; margin-bottom:35px; direction:rtl; text-align:right;">
            <p style="font-size:1.4rem; color:#004085; line-height:2.0; margin:0;">
                <b>א. ניתוח P/E</b> — האם המניה זולה, הוגנת, או יקרה ביחס לסקטור?<br>
                <b>ב. סנטימנט שוק</b> — קונצנזוס אנליסטים, יעד מחיר, Beta, טווח שנתי.
            </p>
        </div>
        """, unsafe_allow_html=True)

        ai_c1, ai_c2 = st.columns([3, 1])
        with ai_c1:
            if st.session_state.h_master_scan_results is not None:
                ai_ticker = st.selectbox("בחר מניה:", st.session_state.h_master_scan_results['מניה'].tolist())
            else:
                ai_ticker = st.text_input("הכנס סימול:", value="NVDA").strip().upper()
        with ai_c2:
            ai_run = st.button("🤖 הפעל AI Insight", type="primary", use_container_width=True)

        st.divider()
        if ai_run and ai_ticker:
            with st.spinner(f"מנתח {ai_ticker}..."):
                render_ai_insight(ai_ticker)
        elif not ai_run:
            st.info("בחר מניה ולחץ 'הפעל AI Insight' לקבלת ניתוח מילולי מפורט.")

    # ==========================================================
    # לשונית 3: Multi-Chart
    # ==========================================================
    with tab_multi:
        st.markdown("""
        <div class="multichart-header">
            <h2 style="color:#fff; font-size:2.6rem; margin:0; border:none; padding:0; text-align:center;">
                📊 Multi-Chart Dashboard — 4 מניות במקביל
            </h2>
            <p style="color:#a0b4d0; font-size:1.4rem; margin-top:15px; text-align:center;">
                נרות + MA20/MA50 + Volume | פריסת 2×2
            </p>
        </div>
        """, unsafe_allow_html=True)

        mc_c1, mc_c2 = st.columns([3, 1])
        with mc_c1:
            if st.session_state.h_master_scan_results is not None:
                available  = st.session_state.h_master_scan_results['מניה'].tolist()
                mc_tickers = st.multiselect(
                    "בחר עד 4 מניות:", options=available,
                    default=available[:4] if len(available) >= 4 else available,
                    max_selections=4
                )
            else:
                mc_tickers = []
        with mc_c2:
            mc_manual = st.text_input("או הכנס ידנית (פסיק):", placeholder="NVDA, TSLA, AAPL, MSFT")

        mc_final = ([s.strip().upper() for s in mc_manual.split(',') if s.strip()][:4]
                    if mc_manual.strip() else mc_tickers[:4])
        mc_btn   = st.button("🚀 הצג Multi-Chart", type="primary", use_container_width=True)
        st.divider()

        if mc_btn:
            if not mc_final:
                st.warning("אנא בחר מניות להצגה.")
            else:
                with st.spinner("טוען גרפים..."):
                    render_multi_chart(mc_final)
        elif not mc_final:
            st.info("בחר מניות מהרשימה או הכנס ידנית, ולחץ 'הצג Multi-Chart'.")

    # ==========================================================
    # לשונית 4: Portfolio Manager
    # ==========================================================
    with tab_portfolio:
        render_portfolio_manager()

    # ==========================================================
    # לשונית 5: Market Heatmap [חדש]
    # ==========================================================
    with tab_heatmap:
        render_sector_heatmap()

    # ==========================================================
    # לשונית 6: יומן מסחר
    # ==========================================================
    with tab_journal:
        st.subheader("📝 יומן מסחר אסטרטגי")
        journal_data = fetch_journal()

        if not journal_data:
            st.info("יומן המסחר ריק. סרוק מניות ושמור הזדמנויות מלשונית הסורק.")
        else:
            for ticker_j, notes_j, date_j in journal_data:
                with st.expander(f"⭐ {ticker_j} | תועד: {date_j}"):
                    jc1, jc2 = st.columns([3, 1])
                    with jc1:
                        st.write(f"**הערה:** {notes_j or 'אין הערה'}")
                    with jc2:
                        if st.button(f"🗑️ מחק {ticker_j}", key=f"del_journal_{ticker_j}"):
                            delete_from_journal(ticker_j)
                            st.rerun()

            st.divider()
            if st.button("🔄 ניתוח מחדש של כל המעקב", use_container_width=True):
                with st.spinner("מבצע ניתוח מחדש..."):
                    refreshed = []
                    for t_j, n_j, _ in journal_data:
                        res = analyze_stock(t_j)
                        if res:
                            res['הערה מקורית'] = n_j
                            refreshed.append(res)
                    if refreshed:
                        st.dataframe(pd.DataFrame(refreshed), use_container_width=True, hide_index=True)

    # ==========================================================
    # לשונית 7: קרב ביצועים
    # ==========================================================
    with tab_versus:
        st.subheader("⚔️ השוואת ביצועים ראש-בראש (Relative Strength)")
        if st.session_state.h_master_scan_results is None:
            st.warning("בצע סריקה בלשונית הסורק כדי לבחור מניות להשוואה.")
        else:
            stocks_list = st.session_state.h_master_scan_results['מניה'].tolist()
            vc1, vc2   = st.columns(2)
            with vc1:
                alpha  = st.selectbox("מניה ראשונה:", stocks_list, index=0)
            with vc2:
                beta_s = st.selectbox("מניה שנייה:", stocks_list, index=1 if len(stocks_list) > 1 else 0)
            if st.button("⚔️ בצע השוואה", type="primary", use_container_width=True):
                render_versus_chart(alpha, beta_s)


# ==============================================================================
# נקודת כניסה גלובלית — עם Auth Gate
# ==============================================================================

def main():
    """
    נקודת הכניסה הראשית — Auth Gate.
    בודק אם המשתמש מחובר:
      - לא מחובר  → מציג מסך Login/Register.
      - מחובר     → מציג Header Bar + Admin Panel (אם Admin) + run_terminal().
    """
    if not st.session_state.get('auth_user'):
        # ---- Login Wall ----
        render_auth_wall()
        return

    user = st.session_state.auth_user

    # ---- Header Bar (שם משתמש + יציאה) ----
    render_user_header()

    # Admin panel access via sidebar button (see run_terminal sidebar section)

    # ---- האפליקציה הראשית ----
    run_terminal()


if __name__ == "__main__":
    main()