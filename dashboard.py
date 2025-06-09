import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import io

# --- Page Config ---
st.set_page_config(page_title="Freelance Earnings Intelligence Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- Load Data ---
df = pd.read_csv('freelancer_earnings_bd.csv')

# --- Brand Colors ---
PRIMARY_COLOR = '#0D47A1'  # Blue
SECONDARY_COLOR = '#000000'  # Black
BACKGROUND_COLOR = '#FFFFFF'  # White

# --- Auto Theme Detection ---
# (Streamlit does this by default in user settings)

# --- Dashboard Title and Description ---
st.title("\U0001F4BC Freelance Earnings Intelligence Dashboard")
st.markdown("""
Gain deep insights into freelance earnings, success rates, and platform performance to drive smarter business decisions.
""")

# --- Sidebar ---
st.sidebar.header("\U0001F50D Filter Options")

# Theme Toggle (if manual needed)
theme = st.sidebar.selectbox('\U0001F319 Theme', ['Auto', 'Light', 'Dark'])
plotly_theme = 'plotly_white' if theme == 'Light' else ('plotly_dark' if theme == 'Dark' else 'plotly')

# Region and Experience Filters
region_options = ['Select All'] + sorted(df['Client_Region'].unique())
region = st.sidebar.selectbox('\U0001F30D Select Client Region:', region_options)

experience_options = ['Select All'] + sorted(df['Experience_Level'].unique())
experience = st.sidebar.selectbox('\U0001F4BC Select Experience Level:', experience_options)

if region == 'Select All':
    region_filtered_df = df
else:
    region_filtered_df = df[df['Client_Region'] == region]

if experience == 'Select All':
    filtered_df = region_filtered_df
else:
    filtered_df = region_filtered_df[region_filtered_df['Experience_Level'] == experience]

# --- Data Download ---
st.sidebar.header("\U0001F4E5 Download Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("Download CSV", csv, "freelancers_filtered.csv", "text/csv", key="download_csv")

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    filtered_df.to_excel(writer, index=False, sheet_name='Freelancers')

st.sidebar.download_button("Download Excel", buffer, "freelancers_filtered.xlsx", "application/vnd.ms-excel", key="download_excel")

# --- Tabs Layout ---
tabs = st.tabs(["Overview", "Regional Insights", "Platform Insights", "Freelancer Leaderboard", "Download"])

# --- Overview Tab ---
with tabs[0]:
    st.subheader("\U0001F4CA Key Metrics Overview")

    col1, col2, col3 = st.columns(3)

    total_earnings = filtered_df['Earnings_USD'].sum()
    avg_hourly_rate = filtered_df['Hourly_Rate'].mean()
    avg_success_rate = filtered_df['Job_Success_Rate'].mean()

    overall_avg_hourly = df['Hourly_Rate'].mean()
    delta_hourly = avg_hourly_rate - overall_avg_hourly

    with col1:
        st.metric("\U0001F4B5 Total Earnings", f"${total_earnings:,.0f}")

    with col2:
        st.metric("\u23F1\uFE0F Avg Hourly Rate", f"${avg_hourly_rate:.2f}", delta=f"{delta_hourly:.2f}")

    with col3:
        st.metric("\u2705 Avg Success Rate", f"{avg_success_rate:.2f}%")

    st.markdown("---")

# --- Regional Insights Tab ---
with tabs[1]:
    st.subheader("\U0001F30F Top Regions by Earnings")

    top_regions = filtered_df.groupby('Client_Region')['Earnings_USD'].sum().sort_values(ascending=False).reset_index()
    top_regions_display = top_regions.copy()
    top_regions_display['Earnings_USD'] = top_regions_display['Earnings_USD'].apply(lambda x: f"${x:,.0f}")

    top_n_region = st.slider("Select Top N Regions:", 5, 20, 10)
    st.dataframe(top_regions_display.head(top_n_region))

    # Pie or Bar Chart Toggle
    chart_type = st.radio("Chart Type:", ['Pie Chart', 'Bar Chart'])
    if chart_type == 'Pie Chart':
        fig = px.pie(top_regions.head(top_n_region), values='Earnings_USD', names='Client_Region', template=plotly_theme, color_discrete_sequence=[PRIMARY_COLOR])
    else:
        fig = px.bar(top_regions.head(top_n_region), x='Client_Region', y='Earnings_USD', template=plotly_theme, color='Client_Region', color_discrete_sequence=[PRIMARY_COLOR])
        fig.update_yaxes(tickprefix="$")
    st.plotly_chart(fig, use_container_width=True)

# --- Platform Insights Tab ---
with tabs[2]:
    st.subheader("\U0001F4F0 Platform Performance")

    platform_stats = filtered_df.groupby('Platform').agg(
        Total_Earnings=('Earnings_USD', 'sum'),
        Avg_Hourly_Rate=('Hourly_Rate', 'mean'),
        Avg_Success_Rate=('Job_Success_Rate', 'mean')
    ).reset_index()

    metric = st.selectbox("Metric to Compare:", ['Total_Earnings', 'Avg_Hourly_Rate', 'Avg_Success_Rate'])
    fig2 = px.bar(platform_stats.sort_values(by=metric, ascending=False),
                  x='Platform', y=metric, template=plotly_theme, color='Platform', color_discrete_sequence=[PRIMARY_COLOR])
    if metric == 'Total_Earnings' or metric == 'Avg_Hourly_Rate':
        fig2.update_yaxes(tickprefix="$")
    st.plotly_chart(fig2, use_container_width=True)

# --- Freelancer Leaderboard Tab ---
with tabs[3]:
    st.subheader("\U0001F947 Top Freelancers by Earnings")

    top_freelancers = filtered_df.sort_values(by='Earnings_USD', ascending=False).head(10)
    top_freelancers_display = top_freelancers.copy()
    top_freelancers_display['Earnings_USD'] = top_freelancers_display['Earnings_USD'].apply(lambda x: f"${x:,.0f}")

    # Add badges for top 3
    medals = ['🥇', '🥈', '🥉'] + [''] * 7
    top_freelancers_display.insert(0, 'Medal', medals)

    st.dataframe(top_freelancers_display[['Medal', 'Freelancer_ID', 'Platform', 'Earnings_USD', 'Job_Success_Rate']])

# --- Download Section ---
with tabs[4]:
    st.subheader("\U0001F4E5 Download Your Data")
    st.download_button("Download CSV", csv, "freelancers_filtered.csv", "text/csv")
    st.download_button("Download Excel", buffer, "freelancers_filtered.xlsx", "application/vnd.ms-excel")

# --- Auto Insights ---
st.markdown("---")
st.subheader("\U0001F4DD Executive Summary")
total_freelancers = len(filtered_df)
top_region = top_regions.iloc[0]['Client_Region'] if not top_regions.empty else 'N/A'
summary_text = f"""
- The total freelance earnings captured is **${total_earnings:,.0f}**.
- The average hourly rate stands at **${avg_hourly_rate:.2f}**, compared to the global average.
- **{top_region}** leads in client spending.
- There are **{total_freelancers}** freelancers under the selected filters.
"""
st.markdown(summary_text)
