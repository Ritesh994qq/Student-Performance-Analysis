
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Student Performance Analysis",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = Path(__file__).parent / "student_data.csv"
SUBJECTS = ["Maths", "Science", "English"]

# --------------------------------------------------
# 2. CUSTOM CSS DESIGN
# --------------------------------------------------
st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #f5f7ff 0%, #edf3ff 100%);
    color: #172554;
}

/* Main content spacing */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1600px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071b42 0%, #102f68 100%);
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

[data-testid="stSidebar"] input {
    color: #172554 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #172554 !important;
}

/* Page title */
.hero-title {
    font-size: 2.45rem;
    font-weight: 850;
    letter-spacing: -1px;
    color: #10265c;
    margin-bottom: 0.2rem;
}

.hero-title span {
    background: linear-gradient(90deg, #1479ff, #853df2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #64748b;
    font-size: 1rem;
    margin-bottom: 1.5rem;
}

/* Metric cards */
.metric-card {
    padding: 21px 18px;
    border-radius: 18px;
    min-height: 140px;
    box-shadow: 0 5px 18px rgba(31, 57, 110, 0.07);
    border: 1px solid rgba(255,255,255,0.9);
    margin-bottom: 8px;
}

.metric-blue {
    background: linear-gradient(135deg, #e0efff, #f4f9ff);
    border-left: 5px solid #2384ff;
}

.metric-green {
    background: linear-gradient(135deg, #dcfce7, #f0fdf4);
    border-left: 5px solid #16a34a;
}

.metric-orange {
    background: linear-gradient(135deg, #fff0d7, #fffbeb);
    border-left: 5px solid #f59e0b;
}

.metric-pink {
    background: linear-gradient(135deg, #ffe4eb, #fff1f5);
    border-left: 5px solid #f43f5e;
}

.metric-label {
    color: #475569;
    font-size: 0.88rem;
    font-weight: 650;
}

.metric-value {
    font-size: 2rem;
    font-weight: 850;
    color: #10265c;
    margin-top: 8px;
}

.metric-icon {
    font-size: 1.7rem;
    margin-bottom: 5px;
}

/* Section headings */
.section-heading {
    font-size: 1.25rem;
    font-weight: 800;
    color: #10265c;
    margin: 1rem 0 0.6rem 0;
}

/* Chart containers */
div[data-testid="stPlotlyChart"],
div[data-testid="stDataFrame"] {
    border-radius: 15px;
}

/* Buttons */
.stDownloadButton button {
    background: linear-gradient(90deg, #1677ff, #5548f5);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 0.65rem 1rem;
}

.stDownloadButton button:hover {
    background: linear-gradient(90deg, #075bd4, #4338ca);
    color: white;
}

/* Data table */
[data-testid="stDataFrame"] {
    border: 1px solid #dbe5f5;
    border-radius: 12px;
}

/* Sidebar brand */
.sidebar-brand {
    font-size: 1.45rem;
    font-weight: 850;
    line-height: 1.35;
    padding: 12px 0 22px 0;
    color: #ffffff;
}

.sidebar-footer {
    margin-top: 35px;
    padding: 20px 5px;
    text-align: center;
    color: #dbeafe;
    font-size: 0.9rem;
    border-top: 1px solid rgba(255,255,255,0.2);
}

/* Responsive title */
@media (max-width: 768px) {
    .hero-title {
        font-size: 1.8rem;
    }
    .metric-value {
        font-size: 1.5rem;
    }
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 3. LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)


def prepare_data(data):
    data = data.copy()

    data[SUBJECTS] = data[SUBJECTS].apply(
        pd.to_numeric, errors="coerce"
    )
    data["Attendance_Percent"] = pd.to_numeric(
        data["Attendance_Percent"], errors="coerce"
    )
    data["Study_Hours_Per_Day"] = pd.to_numeric(
        data["Study_Hours_Per_Day"], errors="coerce"
    )

    data = data.dropna(
        subset=SUBJECTS + [
            "Attendance_Percent",
            "Study_Hours_Per_Day"
        ]
    )

    data["Total Marks"] = data[SUBJECTS].sum(axis=1)
    data["Average Marks"] = data[SUBJECTS].mean(axis=1).round(2)
    data["Percentage"] = (
        data["Total Marks"] / (len(SUBJECTS) * 100) * 100
    ).round(2)

    data["Grade"] = pd.cut(
        data["Percentage"],
        bins=[-0.01, 39.99, 49.99, 59.99, 69.99, 79.99, 100],
        labels=["F", "E", "D", "C", "B", "A"]
    )

    data["Result"] = np.where(
        data["Percentage"] >= 40,
        "Pass",
        "Needs Improvement"
    )

    return data


try:
    df = load_data()

    required_columns = [
        "Student_ID",
        "Student_Name",
        "Class",
        "Maths",
        "Science",
        "English",
        "Attendance_Percent",
        "Study_Hours_Per_Day"
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        st.error(
            "Missing columns in student_data.csv: "
            + ", ".join(missing_columns)
        )
        st.stop()

    df = prepare_data(df)

except FileNotFoundError:
    st.error(
        "student_data.csv was not found. "
        "Keep it in the same folder as app.py."
    )
    st.stop()

except Exception as error:
    st.error(f"Could not load the dataset: {error}")
    st.stop()


# --------------------------------------------------
# 4. SIDEBAR AND FILTERS
# --------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand">🎓 Student<br>'
        'Performance Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 📊 Dashboard")
    st.caption("Analyze academic performance")

    st.divider()
    st.markdown("### 🔎 Filters")

    classes = sorted(df["Class"].dropna().unique().tolist())

    selected_classes = st.multiselect(
        "Select Class",
        options=classes,
        default=classes
    )

    attendance_range = st.slider(
        "Attendance Range (%)",
        min_value=0,
        max_value=100,
        value=(0, 100)
    )

    search_name = st.text_input(
        "Search Student Name",
        placeholder="Enter name..."
    )

    reset_filters = st.button(
        "🔄 Reset Filters",
        use_container_width=True
    )

    if reset_filters:
        st.session_state.clear()
        st.rerun()

    st.markdown("""
    <div class="sidebar-footer">
        🎓<br><br>
        <b>Data Today,<br>Better Students Tomorrow</b>
        <br><br>
        Student Performance Analytics
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# 5. APPLY FILTERS
# --------------------------------------------------
filtered = df[
    df["Class"].isin(selected_classes)
    & df["Attendance_Percent"].between(
        attendance_range[0],
        attendance_range[1]
    )
]

if search_name.strip():
    filtered = filtered[
        filtered["Student_Name"].str.contains(
            search_name.strip(),
            case=False,
            na=False
        )
    ]

if filtered.empty:
    st.markdown(
        '<div class="hero-title">🎓 Student '
        '<span>Performance Analysis</span></div>',
        unsafe_allow_html=True
    )
    st.warning("No students match your filters. Please change them.")
    st.stop()


# --------------------------------------------------
# 6. DASHBOARD HEADER
# --------------------------------------------------
st.markdown(
    '<div class="hero-title">🎓 Student '
    '<span>Performance Analysis</span></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Explore marks, attendance, study hours, and academic '
    'patterns using Python.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# 7. COLOURFUL KPI CARDS
# --------------------------------------------------
total_students = len(filtered)
average_percentage = filtered["Percentage"].mean()
average_attendance = filtered["Attendance_Percent"].mean()
pass_rate = filtered["Result"].eq("Pass").mean() * 100

metrics = [
    ("👥", "Total Students", f"{total_students}", "metric-blue"),
    ("🎯", "Average Percentage", f"{average_percentage:.1f}%", "metric-green"),
    ("📅", "Average Attendance", f"{average_attendance:.1f}%", "metric-orange"),
    ("🏆", "Pass Rate", f"{pass_rate:.1f}%", "metric-pink")
]

columns = st.columns(4)

for column, (icon, label, value, css_class) in zip(columns, metrics):
    with column:
        st.markdown(
            f"""
            <div class="metric-card {css_class}">
                <div class="metric-icon">{icon}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# --------------------------------------------------
# 8. PREPARE COLOURFUL CHARTS
# --------------------------------------------------
sns.set_theme(style="whitegrid")

BLUE = "#2583ff"
GREEN = "#24c77a"
ORANGE = "#ffad32"
PINK = "#ff5c70"
PURPLE = "#8b5cf6"

st.markdown(
    '<div class="section-heading">📈 Academic Analytics</div>',
    unsafe_allow_html=True
)

# Chart row 1
chart1, chart2, chart3 = st.columns([1, 1, 1])

with chart1:
    st.markdown("**Average Marks by Subject**")

    means = filtered[SUBJECTS].mean()
    fig, ax = plt.subplots(figsize=(5, 3.5))

    bars = ax.bar(
        means.index,
        means.values,
        color=[BLUE, GREEN, PINK],
        width=0.68
    )

    ax.set_ylim(0, 110)
    ax.set_ylabel("Average Marks")
    ax.set_xlabel("Subject")
    ax.bar_label(bars, fmt="%.1f", padding=3)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.2)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with chart2:
    st.markdown("**Grade Distribution**")

    grade_order = ["A", "B", "C", "D", "E", "F"]
    grade_counts = (
        filtered["Grade"]
        .value_counts()
        .reindex(grade_order, fill_value=0)
    )
    grade_counts = grade_counts[grade_counts > 0]

    fig, ax = plt.subplots(figsize=(5, 3.5))

    grade_colors = [
        BLUE, GREEN, ORANGE, PINK, PURPLE, "#94a3b8"
    ][:len(grade_counts)]

    ax.pie(
        grade_counts.values,
        labels=grade_counts.index.astype(str),
        autopct="%1.0f%%",
        startangle=90,
        colors=grade_colors,
        wedgeprops={"width": 0.42, "edgecolor": "white"},
        pctdistance=0.78
    )

    ax.axis("equal")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with chart3:
    st.markdown("**Attendance vs Percentage**")

    fig, ax = plt.subplots(figsize=(5, 3.5))

    sns.regplot(
        data=filtered,
        x="Attendance_Percent",
        y="Percentage",
        ax=ax,
        scatter_kws={"color": BLUE, "s": 45, "alpha": 0.8},
        line_kws={"color": PINK, "linewidth": 2}
    )

    ax.set_xlabel("Attendance (%)")
    ax.set_ylabel("Percentage")
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 105)
    ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# Chart row 2
chart4, chart5 = st.columns([1, 1.5])

with chart4:
    st.markdown("**Study Hours vs Percentage**")

    fig, ax = plt.subplots(figsize=(6, 4))

    sns.scatterplot(
        data=filtered,
        x="Study_Hours_Per_Day",
        y="Percentage",
        hue="Result",
        palette={
            "Pass": GREEN,
            "Needs Improvement": PINK
        },
        s=75,
        ax=ax
    )

    ax.set_xlabel("Study Hours per Day")
    ax.set_ylabel("Percentage")
    ax.set_ylim(0, 105)
    ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with chart5:
    st.markdown("**Correlation Heatmap**")

    correlation_columns = SUBJECTS + [
        "Attendance_Percent",
        "Study_Hours_Per_Day",
        "Percentage"
    ]

    corr = filtered[correlation_columns].corr()

    corr.index = [
        "Maths", "Science", "English",
        "Attendance", "Study Hours", "Percentage"
    ]
    corr.columns = corr.index

    fig, ax = plt.subplots(figsize=(8, 4.5))

    sns.heatmap(
        corr,
        annot=True,
        cmap="RdYlBu_r",
        vmin=-1,
        vmax=1,
        center=0,
        fmt=".2f",
        linewidths=0.5,
        ax=ax,
        annot_kws={"size": 8}
    )

    ax.tick_params(axis="x", rotation=35)
    ax.tick_params(axis="y", rotation=0)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# --------------------------------------------------
# 9. PERFORMANCE INSIGHTS
# --------------------------------------------------
st.markdown(
    '<div class="section-heading">💡 Performance Insights</div>',
    unsafe_allow_html=True
)

insight1, insight2 = st.columns(2)

with insight1:
    weakest_subject = filtered[SUBJECTS].mean().idxmin()
    weakest_average = filtered[weakest_subject].mean()

    st.info(
        f"📘 Lowest class-average subject: **{weakest_subject}** "
        f"({weakest_average:.1f}/100)"
    )

    support_students = filtered[filtered["Percentage"] < 40]

    if len(support_students) > 0:
        st.warning(
            f"⚠️ {len(support_students)} student(s) scored below 40% "
            "and may benefit from additional academic support."
        )
    else:
        st.success("✅ No selected students scored below 40%.")

with insight2:
    st.markdown("**🏆 Top Performers**")

    top_students = filtered.nlargest(
        min(3, len(filtered)), "Percentage"
    )

    for _, student in top_students.iterrows():
        st.markdown(
            f"- **{student['Student_Name']}** — "
            f"{student['Percentage']:.1f}%"
        )


# --------------------------------------------------
# 10. STUDENT RECORDS TABLE
# --------------------------------------------------
st.markdown(
    '<div class="section-heading">👨‍🎓 Student Records</div>',
    unsafe_allow_html=True
)

display_columns = [
    "Student_ID",
    "Student_Name",
    "Class",
    "Maths",
    "Science",
    "English",
    "Total Marks",
    "Average Marks",
    "Percentage",
    "Grade",
    "Attendance_Percent",
    "Study_Hours_Per_Day",
    "Result"
]

table = filtered[display_columns].sort_values(
    "Percentage", ascending=False
).copy()

table = table.rename(columns={
    "Student_ID": "Student ID",
    "Student_Name": "Student Name",
    "Attendance_Percent": "Attendance (%)",
    "Study_Hours_Per_Day": "Study Hours"
})

st.dataframe(
    table,
    use_container_width=True,
    hide_index=True,
    height=390
)

csv_data = table.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data (CSV)",
    data=csv_data,
    file_name="student_performance_analysis.csv",
    mime="text/csv"
)


# --------------------------------------------------
# 11. FOOTER
# --------------------------------------------------
st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#64748b; padding:10px;">
        🎓 <b>Student Performance Analysis</b><br>
        Built with Python, Pandas, NumPy, Matplotlib, Seaborn and Streamlit.
        <br><small>Correlation shows association, not necessarily causation.</small>
    </div>
    """,
    unsafe_allow_html=True
)
