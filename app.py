
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(page_title="Palo Alto HR Diagnostics", page_icon="🛡️", layout="wide")

# Custom CSS to make the metrics look slightly better
st.markdown("""
    <style>
    div[data-testid="metric-container"] {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #e1e4e8;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Palo Alto Networks: HR Diagnostic Dashboard")
st.markdown("Proactive Early-Warning System for Employee Engagement and Burnout.")

# ==========================================
# 2. DATA LOADING
# ==========================================
@st.cache_data
def load_data():
    # Make sure 'Palo_Alto_Cleaned.csv' is in the same folder as this script
    return pd.read_csv('Palo_Alto_Cleaned.csv')

df = load_data()

# ==========================================
# 3. SIDEBAR CONTROLS
# ==========================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Palo_Alto_Networks_logo.svg", width=200)
st.sidebar.header("🔍 Diagnostic Filters")

selected_dept = st.sidebar.multiselect("Select Department", options=df['Department'].unique(), default=df['Department'].unique())
available_roles = df[df['Department'].isin(selected_dept)]['JobRole'].unique()
selected_role = st.sidebar.multiselect("Select Job Role", options=available_roles, default=available_roles)
overtime_filter = st.sidebar.radio("Overtime Status", options=["All", "Yes", "No"])

min_tenure, max_tenure = int(df['YearsAtCompany'].min()), int(df['YearsAtCompany'].max())
tenure_range = st.sidebar.slider("Tenure Range (Years)", min_value=min_tenure, max_value=max_tenure, value=(min_tenure, max_tenure))

engagement_threshold = st.sidebar.slider("🚨 Critical Engagement Threshold", min_value=1.0, max_value=4.0, value=2.5, step=0.1, help="Flags employees below this score")

# Apply Filters
filtered_df = df[
    (df['Department'].isin(selected_dept)) &
    (df['JobRole'].isin(selected_role)) &
    (df['YearsAtCompany'] >= tenure_range[0]) &
    (df['YearsAtCompany'] <= tenure_range[1])
    ]
if overtime_filter != "All":
    filtered_df = filtered_df[filtered_df['OverTime'] == overtime_filter]

# Identify High-Risk Pool
risk_df = filtered_df[filtered_df['EngagementIndex'] <= engagement_threshold]

# ==========================================
# 4. TOP-LEVEL METRICS (Manager Action Panel)
# ==========================================
st.markdown("### 🚨 Manager Action Panel")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Employees in View", value=len(filtered_df))
with col2:
    st.metric(label="High-Risk Employees", value=len(risk_df), delta=f"{(len(risk_df ) /len(filtered_df ) *100):.1f}% of cohort", delta_color="inverse")
with col3:
    avg_eng = round(filtered_df['EngagementIndex'].mean(), 2)
    st.metric(label="Avg Engagement Index", value=avg_eng, delta="Scale: 1-4", delta_color="off")
with col4:
    avg_burn = round(filtered_df['BurnoutRiskScore'].mean(), 2)
    st.metric(label="Avg Burnout Risk Score", value=avg_burn, delta="Higher is worse", delta_color="inverse")

st.markdown("---")

# ==========================================
# 5. DASHBOARD TABS (Organized Views)
# ==========================================
tab1, tab2, tab3 = st.tabs(["🏥 Engagement Health", "🔥 Burnout Risk", "📋 High-Risk Employee Table"])

# --- TAB 1: ENGAGEMENT HEALTH ---
with tab1:
    colA, colB = st.columns(2)

    with colA:
        st.markdown("#### Engagement Distribution")
        fig1 = px.histogram(filtered_df, x="EngagementIndex", nbins=10, color="Department",
                            title="Company-Wide Engagement Spread",
                            color_discrete_sequence=px.colors.qualitative.Pastel)
        fig1.add_vline(x=engagement_threshold, line_dash="dash", line_color="red", annotation_text="Risk Threshold")
        st.plotly_chart(fig1, use_container_width=True)

    with colB:
        st.markdown("#### Career Stage Analysis")
        # Group by Years at Company to see tenure trends
        tenure_eng = filtered_df.groupby('YearsAtCompany')['EngagementIndex'].mean().reset_index()
        fig2 = px.line(tenure_eng, x="YearsAtCompany", y="EngagementIndex", markers=True,
                       title="Engagement Trends vs. Tenure",
                       labels={"YearsAtCompany": "Years at Company", "EngagementIndex": "Average Engagement"})
        st.plotly_chart(fig2, use_container_width=True)

# --- TAB 2: BURNOUT RISK ---
with tab2:
    colC, colD = st.columns(2)

    with colC:
        st.markdown("#### Job Role Burnout Assessment")
        fig3 = px.box(filtered_df, x="JobRole", y="BurnoutRiskScore", color="Department",
                      title="Burnout Risk Score Distribution by Role")
        fig3.update_layout(xaxis={'categoryorder' :'total descending'}, xaxis_tickangle=-45)
        st.plotly_chart(fig3, use_container_width=True)

    with colD:
        st.markdown("#### Workload Stress vs Burnout")
        fig4 = px.scatter(filtered_df, x="WorkloadStress", y="BurnoutRiskScore", color="OverTime",
                          size="YearsAtCompany", hover_data=['JobRole'],
                          title="Does Workload Stress Drive Burnout?",
                          color_discrete_map={"Yes": "tomato", "No": "lightgreen"})
        st.plotly_chart(fig4, use_container_width=True)

# --- TAB 3: HIGH RISK ACTION TABLE ---
with tab3:
    st.markdown(f"### Priority Intervention List (Engagement ≤ {engagement_threshold})")
    st.write \
        ("These employees exhibit metrics mathematically identical to those who have previously left the organization due to burnout.")

    if not risk_df.empty:
        # Select only the most relevant columns for a manager to see
        display_cols = ['Department', 'JobRole', 'YearsAtCompany', 'OverTime', 'BurnoutRiskScore', 'EngagementIndex', 'MonthlyIncome']
        st.dataframe(
            risk_df[display_cols].sort_values(by='BurnoutRiskScore', ascending=False),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("Great news! No employees in the current filter match the high-risk criteria.")