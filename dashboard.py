import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="R&W Student Dashboard", layout="wide")
st.title("🎓 Red & White Skill Institutes: February 2026 Registrations")

# 2. Load the Data
@st.cache_data
def load_data():
    df = pd.read_csv("student_dummy_data.csv")
    # Ensure the date column is treated as a datetime object
    df['Registration Date'] = pd.to_datetime(df['Registration Date'])
    return df

df = load_data()

# 3. Sidebar for Interactive Filters (The "Slicers")
st.sidebar.header("Filter Data")
selected_course = st.sidebar.multiselect("Select Course(s)", df['Course'].unique(), default=df['Course'].unique())
selected_branch = st.sidebar.multiselect("Select Branch(es)", df['Branch'].unique(), default=df['Branch'].unique())

# Apply filters
filtered_df = df[(df['Course'].isin(selected_course)) & (df['Branch'].isin(selected_branch))]

# 4. Top-Level KPIs (Key Performance Indicators)
st.markdown("### Quick Stats")
col1, col2, col3 = st.columns(3)
col1.metric("Total Students Enrolled", len(filtered_df))
if not filtered_df.empty:
    col2.metric("Most Popular Course", filtered_df['Course'].mode()[0])
    col3.metric("Top Performing Branch", filtered_df['Branch'].mode()[0])
else:
    col2.metric("Most Popular Course", "N/A")
    col3.metric("Top Performing Branch", "N/A")

st.divider()

# 5. Visualizations using Plotly
if not filtered_df.empty:
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        # Donut Chart for Courses
        st.subheader("Enrollment by Course")
        fig_course = px.pie(filtered_df, names='Course', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_course, use_container_width=True)

    with col_chart2:
        # Bar Chart for Branches
        st.subheader("Enrollment by Branch")
        branch_counts = filtered_df['Branch'].value_counts().reset_index()
        branch_counts.columns = ['Branch', 'Students']
        fig_branch = px.bar(branch_counts, x='Students', y='Branch', orientation='h', color_discrete_sequence=['#4C78A8'])
        fig_branch.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_branch, use_container_width=True)

    # Line Chart for Registration Trends over Time
    st.subheader("Daily Registration Momentum")
    daily_regs = filtered_df.groupby(filtered_df['Registration Date'].dt.date).size().reset_index(name='New Students')
    fig_trend = px.line(daily_regs, x='Registration Date', y='New Students', markers=True, line_shape='spline')
    st.plotly_chart(fig_trend, use_container_width=True)

else:
    st.warning("No data matches your current filter selection.")
