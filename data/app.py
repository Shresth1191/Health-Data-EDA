import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from st_aggrid import AgGrid

# ============================== Custom Styling with CSS ==============================
st.markdown("""
    <style>
        .main { background-color: #f5f7fa; }
        .stApp { font-family: 'Segoe UI', sans-serif; }
        .block-container {
            padding-top: 1rem;
        }
        h1 {
            color: #1f77b4;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #e8f0fe;
            padding: 5px 10px;
            border-radius: 5px;
            margin-right: 5px;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #d2e3fc;
        }
        .stTabs [aria-selected="true"] {
            background-color: #1f77b4;
            color: white;
        }
        .sidebar .sidebar-content {
            background-color: #e0f7fa;
        }
        footer {
            visibility: hidden;
        }
        .footer-text {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #f0f0f0;
            text-align: center;
            font-size: 12px;
            color: #888;
            padding: 5px;
        }
    </style>
    <div class="footer-text">Diabetes EDA Dashboard © 2025 | Built with Streamlit</div>
""", unsafe_allow_html=True)

# ============================== Streamlit Config and Page Title ==============================
st.set_page_config(page_title="Interactive Diabetes EDA Dashboard", layout="wide")
st.title("Diabetes Prediction EDA Dashboard")

# ============================== Load Dataset ==============================
@st.cache_data
def load_data():
    df = pd.read_csv(r"D:\\python eda\\diabetes_prediction_dataset.csv")
    return df

df = load_data()

# ============================== Sidebar File Upload Option ==============================
uploaded_file = st.sidebar.file_uploader("Upload your own CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)

# ============================== Sidebar Help Info ==============================
# Custom Logo with Transparent Background - Visually Appealing Diabetes Icon
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4149/4149625.png", width=150)
st.sidebar.markdown("### Powered by Your Name")
st.sidebar.info("""
🔧 **Instructions**  
- Use filters to explore patterns.  
- Switch chart types and styles.  
- Download data anytime.
""")

# ============================== Sidebar Filters ==============================
st.sidebar.header("Filter Options")
gender_options = df['gender'].unique().tolist()
selected_genders = st.sidebar.multiselect("Select Gender(s):", gender_options, default=gender_options)
min_age, max_age = int(df['age'].min()), int(df['age'].max())
age_range = st.sidebar.slider("Select Age Range:", min_value=min_age, max_value=max_age, value=(min_age, max_age))
diabetes_classes = sorted(df['diabetes'].unique())
selected_classes = st.sidebar.multiselect("Select Diabetes Class:", diabetes_classes, default=diabetes_classes)

# ============================== Filter DataFrame Based on Selections ==============================
filtered_df = df[
    (df['gender'].isin(selected_genders)) &
    (df['age'].between(age_range[0], age_range[1])) &
    (df['diabetes'].isin(selected_classes))
]

# ============================== KPI Tiles Section ==============================
st.markdown("### Key Statistics")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("📊 Total Records", len(filtered_df))
kpi2.metric("🩺 % Diabetics", f"{filtered_df['diabetes'].mean()*100:.2f}%")
kpi3.metric("⚖️ Avg. BMI", f"{filtered_df['bmi'].mean():.2f}")

# ============================== Tabs for Dashboard Sections ==============================
tab1, tab2, tab3 = st.tabs(["📊 Charts", "🗃️ Data Explorer", "🧩 Custom Analysis"])

# ============================== Charts Tab ==============================
with tab1:
    st.sidebar.header("Chart Options")
    show_gender_chart = st.sidebar.checkbox("Gender vs Diabetes", True)
    show_bmi_chart = st.sidebar.checkbox("BMI vs Diabetes", True)
    show_glucose_chart = st.sidebar.checkbox("Glucose Level Distribution", True)
    show_age_chart = st.sidebar.checkbox("Age vs Diabetes", True)
    show_smoking_chart = st.sidebar.checkbox("Smoking History vs Diabetes", True)
    plot_lib = st.sidebar.radio("Plotting Library", ["Seaborn", "Plotly"])

    # ============================== Chart Style and Layout Controls ==============================
    color_theme = st.sidebar.radio("Chart Color Theme", ["Default", "Dark", "Pastel", "Colorblind"])
    color_palettes = {
        "Default": "tab10",
        "Dark": "dark",
        "Pastel": "pastel",
        "Colorblind": "colorblind"
    }
    sns.set_palette(color_palettes[color_theme])

    num_cols = st.sidebar.radio("Chart Grid Columns", [1, 2, 3], index=1)
    columns = st.columns(num_cols)

    chart_index = 0
    if show_gender_chart:
        with columns[chart_index % num_cols]:
            st.subheader("Gender vs Diabetes Count")
            if plot_lib == "Plotly":
                fig = px.histogram(filtered_df, x='gender', color='diabetes', barmode='group')
                fig.update_layout(template="plotly_dark" if color_theme=="Dark" else "plotly_white")
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig, ax = plt.subplots()
                sns.countplot(x='gender', hue='diabetes', data=filtered_df, ax=ax)
                st.pyplot(fig)
        chart_index += 1

    if show_bmi_chart:
        with columns[chart_index % num_cols]:
            st.subheader("BMI vs Diabetes")
            if plot_lib == "Plotly":
                fig = px.box(filtered_df, x='diabetes', y='bmi', color='diabetes')
                fig.update_layout(template="plotly_dark" if color_theme=="Dark" else "plotly_white")
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig, ax = plt.subplots()
                sns.boxplot(x='diabetes', y='bmi', data=filtered_df, ax=ax)
                st.pyplot(fig)
        chart_index += 1

    if show_glucose_chart:
        with columns[chart_index % num_cols]:
            st.subheader("Blood Glucose Level Distribution")
            fig = px.histogram(filtered_df, x='blood_glucose_level', marginal="box", nbins=30)
            fig.update_layout(template="plotly_dark" if color_theme=="Dark" else "plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        chart_index += 1

    if show_age_chart:
        with columns[chart_index % num_cols]:
            st.subheader("Age vs Diabetes")
            fig = px.violin(filtered_df, y='age', x='diabetes', box=True, color='diabetes')
            fig.update_layout(template="plotly_dark" if color_theme=="Dark" else "plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        chart_index += 1

    if show_smoking_chart:
        st.subheader("Smoking History vs Diabetes")
        fig = px.histogram(filtered_df, x='smoking_history', color='diabetes', barmode='group')
        fig.update_xaxes(tickangle=45)
        fig.update_layout(template="plotly_dark" if color_theme=="Dark" else "plotly_white")
        st.plotly_chart(fig, use_container_width=True)

# ============================== Data Explorer Tab ==============================
with tab2:
    if st.checkbox("Show Raw Data"):
        st.dataframe(df)
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Filtered Data", csv, "filtered_data.csv", "text/csv")
    st.subheader("Summary Statistics for Filtered Data")
    st.write(filtered_df.describe())

    st.subheader("Advanced Table (Sortable/Filterable)")
    AgGrid(filtered_df, height=300, theme="dark" if color_theme=="Dark" else "light")

# ============================== Custom Analysis Tab ==============================
with tab3:
    st.subheader("Custom Plot")
    numeric_cols = filtered_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_cols = filtered_df.select_dtypes(include='object').columns.tolist()
    x_axis = st.selectbox("X-axis (categorical):", categorical_cols)
    y_axis = st.selectbox("Y-axis (numeric):", numeric_cols, index=1)
    custom_plot_type = st.radio("Plot Type:", ['Boxplot', 'Violin', 'Scatter'])

    if custom_plot_type == 'Boxplot':
        fig = px.box(filtered_df, x=x_axis, y=y_axis, color='diabetes')
    elif custom_plot_type == 'Violin':
        fig = px.violin(filtered_df, x=x_axis, y=y_axis, color='diabetes', box=True)
    else:
        fig = px.scatter(filtered_df, x=x_axis, y=y_axis, color='diabetes')

    fig.update_layout(template="plotly_dark" if color_theme=="Dark" else "plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ============================== Optional Heatmap ==============================
if st.checkbox("Show Correlation Heatmap"):
    st.subheader("Correlation Heatmap")
    fig_corr, ax_corr = plt.subplots()
    sns.heatmap(filtered_df.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=ax_corr)
    st.pyplot(fig_corr)

# ============================== Data Insights ==============================
with st.expander("🔍 Data Insights"):
    st.write("""
    - 🧬 Higher glucose often means higher diabetes risk.
    - 🚬 Smoking history can slightly correlate with diabetes.
    - 🧑‍⚕️ Age and BMI are critical indicators.
    """)