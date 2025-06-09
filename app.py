import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import io

# --- Page Config ---
st.set_page_config(page_title="Freelancer Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- Load Data ---
df = pd.read_csv('freelancer_earnings_bd.csv')

# --- Title and Description ---
st.title("🧑‍💻 Freelancer Earnings Dashboard")
st.markdown("""
Welcome to the Freelancer Insights Dashboard.
Analyze freelance earnings, hourly rates, client ratings, and rehire trends across different platforms and experience levels.
""")

# --- Sidebar ---
st.sidebar.header("🔍 Filter Options")

# Theme Toggle
theme = st.sidebar.selectbox('🌓 Theme', ['Light', 'Dark'])
plotly_theme = 'plotly_white' if theme == 'Light' else 'plotly_dark'

# Dropdown for Region with 'Select All'
region_options = ['Select All'] + sorted(df['Client_Region'].unique())
region = st.sidebar.selectbox('🌍 Select Client Region:', region_options)

# Dropdown for Experience Level with 'Select All'
experience_options = ['Select All'] + sorted(df['Experience_Level'].unique())
experience = st.sidebar.selectbox('🧑‍💻 Select Experience Level:', experience_options)

# Filtering Logic
if region == 'Select All':
    region_filtered_df = df
else:
    region_filtered_df = df[df['Client_Region'] == region]

if experience == 'Select All':
    filtered_df = region_filtered_df
else:
    filtered_df = region_filtered_df[region_filtered_df['Experience_Level'] == experience]

# --- Download Buttons ---
st.sidebar.markdown("### 📥 Download Data")

csv = filtered_df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="Download CSV",
    data=csv,
    file_name='filtered_freelancers.csv',
    mime='text/csv',
)

# Excel download
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    filtered_df.to_excel(writer, index=False, sheet_name='Freelancers')
    
st.sidebar.download_button(
    label="Download Excel",
    data=buffer,
    file_name='filtered_freelancers.xlsx',
    mime='application/vnd.ms-excel',
)

# --- KPIs ---
st.markdown("## 📊 Key Metrics")
col1, col2, col3 = st.columns(3)

# Calculations
total_earnings = filtered_df['Earnings_USD'].sum()
avg_hourly_rate = filtered_df['Hourly_Rate'].mean()
avg_success_rate = filtered_df['Job_Success_Rate'].mean()

# Overall for delta comparison
overall_avg_hourly = df['Hourly_Rate'].mean()
delta_hourly = avg_hourly_rate - overall_avg_hourly

with col1:
    st.metric(label="💵 Total Earnings (USD)", value=f"${total_earnings:,.0f}")

with col2:
    st.metric(label="⏱️ Avg Hourly Rate (USD)", value=f"${avg_hourly_rate:.2f}", delta=f"{delta_hourly:.2f}")

with col3:
    st.metric(label="✅ Avg Success Rate (%)", value=f"{avg_success_rate:.2f}%")

# --- Visualizations ---
st.markdown("## 📈 Visual Insights")

# Two columns of charts
col4, col5 = st.columns(2)

with col4:
    st.markdown("### 🏆 Average Earnings by Platform")
    fig1 = px.bar(
        filtered_df.groupby('Platform')['Earnings_USD'].mean().reset_index(),
        x='Platform', y='Earnings_USD',
        color='Platform', template=plotly_theme, text_auto='.2s'
    )
    st.plotly_chart(fig1, use_container_width=True)

with col5:
    st.markdown("### ⏱️ Hourly Rate Distribution")
    fig2 = px.histogram(
        filtered_df, x='Hourly_Rate', nbins=20,
        color_discrete_sequence=['#636EFA'], template=plotly_theme
    )
    st.plotly_chart(fig2, use_container_width=True)

# Another row of visuals
col6, col7 = st.columns(2)

with col6:
    st.markdown("### 🌟 Client Ratings by Payment Method")
    fig3 = px.box(
        filtered_df, x='Payment_Method', y='Client_Rating',
        color='Payment_Method', template=plotly_theme
    )
    st.plotly_chart(fig3, use_container_width=True)

with col7:
    st.markdown("### 📊 Project Type Split")
    project_counts = filtered_df['Project_Type'].value_counts().reset_index()
    project_counts.columns = ['Project_Type', 'Count']
    fig4 = px.pie(
        project_counts, values='Count', names='Project_Type', hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Prism, template=plotly_theme
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# --- Top Freelancers by Earnings ---
st.markdown("## 🏅 Top 10 Freelancers by Earnings")
top_earners = filtered_df.sort_values(by='Earnings_USD', ascending=False).head(10)

# Format Total Earnings with $
top_earners_display = top_earners.copy()
top_earners_display['Earnings_USD'] = top_earners_display['Earnings_USD'].apply(lambda x: f"${x:,.0f}")

st.dataframe(top_earners_display[['Freelancer_ID', 'Platform', 'Earnings_USD', 'Job_Success_Rate']])

# --- Top Regions by Total Earnings ---
st.markdown("## 🌍 Top Regions by Total Earnings")
top_regions = (
    filtered_df.groupby('Client_Region')['Earnings_USD']
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

# Format Total Earnings with $
top_regions_display = top_regions.copy()
top_regions_display['Earnings_USD'] = top_regions_display['Earnings_USD'].apply(lambda x: f"${x:,.0f}")

st.dataframe(top_regions_display.head(10))

# --- Two Regions Comparison Section ---
st.markdown("## 🆚 Region vs Region Detailed Comparison")

# Two dropdowns for two regions
colA, colB = st.columns(2)

with colA:
    region_1 = st.selectbox('Select First Region:', df['Client_Region'].unique())

with colB:
    region_2 = st.selectbox('Select Second Region:', df['Client_Region'].unique(), index=1)

# Filter Data
compare_df = df[df['Client_Region'].isin([region_1, region_2])]

# Aggregate Metrics
compare_metrics = compare_df.groupby('Client_Region').agg(
    Total_Earnings=('Earnings_USD', 'sum'),
    Avg_Hourly_Rate=('Hourly_Rate', 'mean'),
    Avg_Success_Rate=('Job_Success_Rate', 'mean')
).reset_index()

# Sort by Total Earnings Descending
compare_metrics = compare_metrics.sort_values(by='Total_Earnings', ascending=False)

# --- Format Currency and Percentages ---
compare_metrics_display = compare_metrics.copy()
compare_metrics_display['Total_Earnings'] = compare_metrics_display['Total_Earnings'].apply(lambda x: f"${x:,.0f}")
compare_metrics_display['Avg_Hourly_Rate'] = compare_metrics_display['Avg_Hourly_Rate'].apply(lambda x: f"${x:,.2f}")
compare_metrics_display['Avg_Success_Rate'] = compare_metrics_display['Avg_Success_Rate'].apply(lambda x: f"{x:.2f}%")

# Show Formatted Table
st.dataframe(compare_metrics_display)

# Visualize the comparison
fig8 = px.bar(
    compare_metrics.melt(id_vars='Client_Region', var_name='Metric', value_name='Value'),
    x='Metric', y='Value', color='Client_Region', barmode='group',
    template=plotly_theme,
    title=f"Comparison: {region_1} vs {region_2}"
)
st.plotly_chart(fig8, use_container_width=True)

# --- Data Table Section ---
st.markdown("## 📄 Full Data Preview")
st.dataframe(filtered_df)