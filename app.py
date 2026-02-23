import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(page_title="Employee Dashboard", layout="wide")

st.title("Employee Analytics Dashboard")

# ----------------------------
# Load Data
# ----------------------------
df = pd.read_json("employee_dataset.json")

# Clean column names (prevents errors)
df.columns = df.columns.str.strip().str.lower()

# Ensure salary is numeric
df['salary'] = pd.to_numeric(df['salary'], errors='coerce')

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filter Options")

healthy_filter = st.sidebar.slider(
    "Minimum Healthy Eating Score",
    int(df['healthy_eating'].min()),
    int(df['healthy_eating'].max()),
    int(df['healthy_eating'].min())
)

salary_filter = st.sidebar.slider(
    "Maximum Salary",
    int(df['salary'].min()),
    int(df['salary'].max()),
    int(df['salary'].max())
)

# Apply Filters
filtered_df = df[
    (df['healthy_eating'] >= healthy_filter) &
    (df['salary'] <= salary_filter)
]

# ----------------------------
# KPIs Section
# ----------------------------
st.subheader("Key Performance Indicators")

total_employees = filtered_df.shape[0]
avg_salary = filtered_df['salary'].mean()
avg_healthy = filtered_df['healthy_eating'].mean()
healthy_percent = (filtered_df[filtered_df['healthy_eating'] > 8].shape[0] / total_employees * 100) if total_employees > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Employees", total_employees)
col2.metric("Average Salary", f"{avg_salary:.2f}")
col3.metric("Avg Healthy Score", f"{avg_healthy:.2f}")
col4.metric("Healthy Employees % (>8)", f"{healthy_percent:.2f}%")

# ----------------------------
# Visualizations
# ----------------------------
st.subheader("Visual Analysis")

colA, colB = st.columns(2)

# Age vs Salary
with colA:
    fig1 = plt.figure(figsize=(6,4))
    sns.scatterplot(x='age', y='salary', data=filtered_df)
    plt.title("Age vs Salary")
    st.pyplot(fig1)

# Healthy vs Active Lifestyle
with colB:
    fig2 = plt.figure(figsize=(6,4))
    sns.scatterplot(x='healthy_eating', y='active_lifestyle', data=filtered_df)
    plt.title("Healthy Eating vs Active Lifestyle")
    st.pyplot(fig2)

# Salary Distribution
st.subheader("Salary Distribution")

fig3 = plt.figure(figsize=(8,4))
plt.hist(filtered_df['salary'], bins=15, edgecolor='black')
plt.xlabel("Salary")
plt.ylabel("Frequency")
plt.title("Salary Distribution")
st.pyplot(fig3)

# Groups Count Plot (if column exists)
if 'groups' in df.columns:
    st.subheader("Employee Group Distribution")
    fig4 = plt.figure(figsize=(8,4))
    sns.countplot(x='groups', data=filtered_df, edgecolor='black')
    plt.title("Groups Count")
    st.pyplot(fig4)

# ----------------------------
# Data Preview
# ----------------------------
st.subheader("Filtered Data Preview")
st.dataframe(filtered_df)