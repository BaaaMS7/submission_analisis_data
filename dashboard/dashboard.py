import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_PATH = os.path.join(BASE_DIR, 'data')
DASHBOARD_PATH = os.path.join(BASE_DIR, 'dashboard')

df = pd.read_csv(os.path.join(DASHBOARD_PATH, 'main_data.csv'))
monthly_orders = pd.read_csv(os.path.join(DATA_PATH, 'monthly_orders.csv'))
monthly_revenue = pd.read_csv(os.path.join(DATA_PATH, 'monthly_revenue.csv'))
top_category = pd.read_csv(os.path.join(DATA_PATH, 'top_category.csv'))
payment_dist = pd.read_csv(os.path.join(DATA_PATH, 'payment_dist.csv'))

st.title("📊 E-Commerce Data Analysis Dashboard")

st.sidebar.header("Filter Data")

payment_filter = st.sidebar.multiselect(
    "Pilih Metode Pembayaran",
    options=df['payment_type'].unique(),
    default=df['payment_type'].unique()
)

filtered_df = df[df['payment_type'].isin(payment_filter)]

st.subheader("Key Metrics")

col1, col2 = st.columns(2)

col1.metric("Total Orders", filtered_df['order_id'].nunique())
col2.metric("Total Revenue", f"${filtered_df['price'].sum():,.0f}")

st.subheader("🏆 Top Product Categories by Revenue")

top10 = top_category.head(10)

fig1, ax1 = plt.subplots()
ax1.bar(top10['category'], top10['total_revenue'])
plt.xticks(rotation=45)
st.pyplot(fig1)

st.subheader("Monthly Orders & Revenue Trend")

fig2, ax2 = plt.subplots()

ax2.plot(monthly_orders['month'], monthly_orders['total_orders'], label='Orders')
ax2.plot(monthly_revenue['month'], monthly_revenue['total_revenue'], label='Revenue')

plt.xticks(rotation=45)
plt.legend()
st.pyplot(fig2)

st.subheader("Payment Method Distribution")

fig3, ax3 = plt.subplots()
ax3.pie(payment_dist['count'], labels=payment_dist['payment_type'], autopct='%1.1f%%')
st.pyplot(fig3)

st.subheader("Insights")

st.markdown("""
- Kategori produk tertentu mendominasi revenue.
- Tren penjualan menunjukkan fluktuasi bulanan.
- Metode pembayaran didominasi oleh credit card.
""")