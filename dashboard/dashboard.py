import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, 'dashboard', 'main_data.csv'))

df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

df['year'] = df['order_purchase_timestamp'].dt.year
df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

st.title("📊 E-Commerce Dashboard Analysis")

st.sidebar.header("🔎 Filter Data")

payment_filter = st.sidebar.multiselect(
    "Pilih Metode Pembayaran",
    options=df['payment_type'].unique(),
    default=df['payment_type'].unique()
)

year_filter = st.sidebar.multiselect(
    "Pilih Tahun",
    options=sorted(df['year'].unique()),
    default=sorted(df['year'].unique())
)

filtered_df = df[
    (df['payment_type'].isin(payment_filter)) &
    (df['year'].isin(year_filter))
]

st.subheader("📌 Key Metrics")

col1, col2 = st.columns(2)

col1.metric("Total Orders", filtered_df['order_id'].nunique())
col2.metric("Total Revenue", f"${filtered_df['price'].sum():,.0f}")

st.subheader("🏆 Top & Bottom Product Categories (Revenue)")

category_revenue = filtered_df.groupby('product_category_name_english')['price'] \
    .sum() \
    .sort_values(ascending=False)

top5 = category_revenue.head(5)
bottom5 = category_revenue.tail(5)

fig1, ax1 = plt.subplots()
ax1.bar(top5.index, top5.values)
plt.xticks(rotation=45)
ax1.set_title("Top 5 Categories")
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
ax2.bar(bottom5.index, bottom5.values)
plt.xticks(rotation=45)
ax2.set_title("Bottom 5 Categories")
st.pyplot(fig2)

st.subheader("📈 Monthly Orders & Revenue Trend")

monthly = filtered_df.groupby('order_month').agg({
    'order_id': 'nunique',
    'price': 'sum'
}).rename(columns={
    'order_id': 'total_orders',
    'price': 'total_revenue'
}).reset_index()

fig3, ax3 = plt.subplots()
ax3.plot(monthly['order_month'], monthly['total_orders'], label='Orders')
ax3.plot(monthly['order_month'], monthly['total_revenue'], label='Revenue')

plt.xticks(rotation=45)
plt.legend()
ax3.set_title("Monthly Trend")
st.pyplot(fig3)

st.subheader("💳 Payment Method Distribution")

payment_dist = filtered_df['payment_type'].value_counts()

fig4, ax4 = plt.subplots()
ax4.pie(payment_dist, labels=payment_dist.index, autopct='%1.1f%%')
st.pyplot(fig4)

st.subheader("📌 Insights")

st.markdown("""
- Revenue terkonsentrasi pada beberapa kategori utama
- Tren penjualan menunjukkan fluktuasi dari waktu ke waktu
- Metode pembayaran memengaruhi distribusi transaksi
""")