import sqlite3
import pandas as pd
import streamlit as st

# পেজ কনফিগারেশন
st.set_page_config(
    page_title="রাধাকৃষ্ণ কমিউনিকেশন - ক্যাটালগ",
    page_icon="📱",
    layout="wide",
)


# ডেটাবেস ইনিশিয়ালাইজেশন ফাংশন
def init_db():
  conn = sqlite3.connect("inventory.db")
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            description TEXT
        )
    """)
  conn.commit()
  conn.close()


# নতুন প্রোডাক্ট যোগ করার ফাংশন
def add_product(name, category, price, stock, description):
  conn = sqlite3.connect("inventory.db")
  cursor = conn.cursor()
  cursor.execute(
      """
        INSERT INTO products (name, category, price, stock, description)
        VALUES (?, ?, ?, ?, ?)
    """,
      (name, category, price, stock, description),
  )
  conn.commit()
  conn.close()


# প্রোডাক্ট খোঁজার ফাংশন
def fetch_products(search_term=""):
  conn = sqlite3.connect("inventory.db")
  if search_term:
    query = """
            SELECT name, category, price, stock, description 
            FROM products 
            WHERE name LIKE ? OR category LIKE ? OR description LIKE ?
        """
    param = f"%{search_term}%"
    df = pd.read_sql_query(query, conn, params=(param, param, param))
  else:
    query = """
            SELECT name, category, price, stock, description 
            FROM products
        """
    df = pd.read_sql_query(query, conn)
  conn.close()
  return df


# ডেটাবেস টেবিল তৈরি
init_db()

# --- সাইডবার: অ্যাডমিন প্যানেল ---
st.sidebar.header("🔐 অ্যাডমিন প্যানেল")
admin_password = st.sidebar.text_input("অ্যাডমিন পাসওয়ার্ড", type="password")

# ডেমো পাসওয়ার্ড: admin123 (প্রয়োজনে পরিবর্তন করে নিন)
if admin_password == "admin123":
  st.sidebar.success("লগইন সফল!")
  st.sidebar.subheader("নতুন প্রোডাক্ট যোগ করুন")

  with st.sidebar.form("add_product_form", clear_on_submit=True):
    p_name = st.text_input("প্রোডাক্টের নাম *")
    p_category = st.selectbox(
        "ক্যাটাগরি", ["মোবাইল", "অ্যাক্সেসরিজ", "ইলেকট্রনিক্স", "অন্যান্য"]
    )
    p_price = st.number_input("দাম (টাকা) *", min_value=0.0, step=10.0)
    p_stock = st.number_input("স্টক পরিমাণ *", min_value=0, step=1)
    p_desc = st.text_area("বিবরণ / কিওয়ার্ড")

    submitted = st.form_submit_button("যোগ করুন")
    if submitted:
      if p_name and p_price:
        add_product(p_name, p_category, p_price, p_stock, p_desc)
        st.sidebar.success(f"'{p_name}' সফলভাবে সংরক্ষিত হয়েছে!")
        st.rerun()
      else:
        st.sidebar.error("নাম এবং দাম দেওয়া বাধ্যতামূলক!")
elif admin_password:
  st.sidebar.error("ভুল পাসওয়ার্ড!")

# --- মূল পেজ: ক্যাটালগ ও সার্চ ---
st.title("📦 রাধাকৃষ্ণ কমিউনিকেশন এন্ড ইলেকট্রনিক্স")
st.write("আমাদের সমস্ত পণ্য ও স্টক ক্যাটালগ দেখুন:")

# সার্চ বার
search_query = st.text_input(
    "🔍 সার্চ করুন (নাম, ক্যাটাগরি বা কিওয়ার্ড দিয়ে):", ""
)

# ডেটা ফেচ ও ডিসপ্লে
df_products = fetch_products(search_query)

if not df_products.empty:
  # টেবিল কলামগুলোর বাংলা নাম দেওয়া
  df_display = df_products.rename(
      columns={
          "name": "প্রোডাক্টের নাম",
          "category": "ক্যাটাগরি",
          "price": "দাম (টাকা)",
          "stock": "স্টক",
          "description": "বিবরণ",
      }
  )

  st.dataframe(df_display, use_container_width=True)
else:
  st.info("কোনো প্রোডাক্ট পাওয়া যায়নি。")