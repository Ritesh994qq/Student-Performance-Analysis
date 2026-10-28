import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(page_title="Student Performance Analysis", page_icon="🎓", layout="wide")

DATA_FILE = Path(__file__).parent / "student_data.csv"
SUBJECTS = ["Maths", "Science", "English"]

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    return df

def add_metrics(df):
    df = df.copy()
    df["Total Marks"] = df[SUBJECTS].sum(axis=1)
    df["Average Marks"] = df[SUBJECTS].mean(axis=1).round(2)
    df["Percentage"] = (df[SUBJECTS].sum(axis=1) / (len(SUBJECTS) * 100) * 100).round(2)
    df["Grade"] = pd.cut(
        df["Percentage"],
        bins=[-0.01, 39.99, 49.99, 59.99, 69.99, 79.99, 100],
        labels=["F", "E", "D", "C", "B", "A"]
    )
    df["Result"] = np.where(df["Percentage"] >= 40, "Pass", "Needs Improvement")
    return df

st.title("🎓 Student Performance Analysis")
st.caption("Explore marks, attendance, study hours, and academic patterns using Python.")

df = load_data()
required = {"Student_ID", "Student_Name", "Class", "Maths", "Science", "English", "Attendance_Percent", "Study_Hours_Per_Day"}
missing = required - set(df.columns)
if missing:
    st.error("The dataset is missing required columns: " + ", ".join(sorted(missing)))
    st.stop()

df = add_metrics(df)

with st.sidebar:
    st.header("Filters")
    classes = sorted(df["Class"].dropna().unique().tolist())
    chosen_classes = st.multiselect("Select class", classes, default=classes)
    min_attendance, max_attendance = st.slider(
        "Attendance (%)", 0, 100, (0, 100)
    )
    search_name = st.text_input("Search student name")
    st.divider()
    st.caption("Sample dataset is provided. Replace student_data.csv to analyze your own data.")

filtered = df[
    df["Class"].isin(chosen_classes)
    & df["Attendance_Percent"].between(min_attendance, max_attendance)
]
if search_name.strip():
    filtered = filtered[filtered["Student_Name"].str.contains(search_name.strip(), case=False, na=False)]

if filtered.empty:
    st.warning("No students match these filters. Change the filters to see results.")
    st.stop()

total_students = len(filtered)
avg_percentage = filtered["Percentage"].mean()
avg_attendance = filtered["Attendance_Percent"].mean()
pass_rate = (filtered["Result"].eq("Pass").mean() * 100)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Students", f"{total_students}")
c2.metric("Average percentage", f"{avg_percentage:.1f}%")
c3.metric("Average attendance", f"{avg_attendance:.1f}%")
c4.metric("Pass rate", f"{pass_rate:.1f}%")

st.subheader("Student records")
display_cols = ["Student_ID", "Student_Name", "Class", *SUBJECTS, "Total Marks", "Average Marks",
                "Percentage", "Grade", "Attendance_Percent", "Study_Hours_Per_Day", "Result"]
st.dataframe(filtered[display_cols].sort_values("Percentage", ascending=False),
             use_container_width=True, hide_index=True)

csv_data = filtered[display_cols].to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download filtered analysis (CSV)", data=csv_data,
                   file_name="student_performance_analysis.csv", mime="text/csv")

left, right = st.columns(2)
with left:
    st.subheader("Average marks by subject")
    subject_means = filtered[SUBJECTS].mean()
    fig, ax = plt.subplots()
    sns.barplot(x=subject_means.index, y=subject_means.values, ax=ax)
    ax.set_ylabel("Average marks (out of 100)")
    ax.set_xlabel("Subject")
    ax.set_ylim(0, 100)
    ax.grid(axis="y", alpha=0.25)
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("Grade distribution")
    grade_counts = filtered["Grade"].value_counts().reindex(["A", "B", "C", "D", "E", "F"], fill_value=0)
    fig, ax = plt.subplots()
    ax.bar(grade_counts.index.astype(str), grade_counts.values)
    ax.set_xlabel("Grade")
    ax.set_ylabel("Number of students")
    ax.grid(axis="y", alpha=0.25)
    st.pyplot(fig)
    plt.close(fig)

left, right = st.columns(2)
with left:
    st.subheader("Attendance vs percentage")
    fig, ax = plt.subplots()
    sns.regplot(data=filtered, x="Attendance_Percent", y="Percentage", ax=ax,
                scatter_kws={"alpha": 0.7}, line_kws={"color": "red"})
    ax.set_xlabel("Attendance (%)")
    ax.set_ylabel("Overall percentage (%)")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("Study hours vs percentage")
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered, x="Study_Hours_Per_Day", y="Percentage", hue="Result", ax=ax)
    ax.set_xlabel("Study hours per day")
    ax.set_ylabel("Overall percentage (%)")
    ax.set_ylim(0, 100)
    st.pyplot(fig)
    plt.close(fig)

st.subheader("Correlation heatmap")
corr_cols = SUBJECTS + ["Attendance_Percent", "Study_Hours_Per_Day", "Percentage"]
fig, ax = plt.subplots(figsize=(9, 5))
sns.heatmap(filtered[corr_cols].corr(numeric_only=True), annot=True, cmap="coolwarm",
            vmin=-1, vmax=1, fmt=".2f", ax=ax)
st.pyplot(fig)
plt.close(fig)

st.subheader("Performance insights")
top_students = filtered.nlargest(min(3, len(filtered)), "Percentage")
needs_support = filtered[filtered["Percentage"] < 40]
weak_subject = filtered[SUBJECTS].mean().idxmin()
i1, i2 = st.columns(2)
with i1:
    st.markdown(f"**Lowest class-average subject:** {weak_subject} ({filtered[weak_subject].mean():.1f}/100)")
    st.markdown(f"**Students scoring below 40%:** {len(needs_support)}")
with i2:
    st.markdown("**Top performers in the selected data:**")
    for _, row in top_students.iterrows():
        st.write(f"- {row['Student_Name']} — {row['Percentage']:.1f}%")

if not needs_support.empty:
    st.markdown("**Students who may benefit from additional support**")
    st.dataframe(needs_support[["Student_Name", "Class", "Percentage", "Attendance_Percent", "Result"]],
                 use_container_width=True, hide_index=True)
else:
    st.success("No students in the selected data scored below 40%.")

st.info("Interpretation note: charts show associations in this dataset, not proof that attendance or study hours cause higher marks. Use student data responsibly.")
