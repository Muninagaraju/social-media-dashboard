import pandas as pd
import sqlalchemy
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------
# Connect to MySQL
# -------------------------------
engine = sqlalchemy.create_engine(
    "mysql+pymysql://root:Raju2003@localhost:3306/project1"
)

# -------------------------------
# Load Full Dataset (Single Query)
# -------------------------------
query = "SELECT * FROM social_media_addiction;"
df = pd.read_sql(query, engine)

# -------------------------------
# Data Cleaning (IMPORTANT)
# -------------------------------
numeric_cols = [
    "Age", "DailySocialMediaHours", "SleepHours",
    "StressLevel", "AnxietyLevel",
    "AddictionLevel", "AcademicPerformance",
    "SocialInteractionLevel"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df.fillna(0, inplace=True)

# -------------------------------
# 1. Platform Usage Analysis
# -------------------------------
platform = df["PlatformUsage"].value_counts().reset_index()
platform.columns = ["Platform", "Count"]

# Bar Chart
plt.figure(figsize=(8,5))
sns.barplot(data=platform, x="Platform", y="Count")
plt.title("Platform Usage Distribution")
plt.xlabel("Platform")
plt.ylabel("Number of Users")

# Labels
for i, val in enumerate(platform["Count"]):
    plt.text(i, val, str(val), ha='center')

plt.show()

# Pie Chart
plt.figure(figsize=(6,6))
plt.pie(platform["Count"], labels=platform["Platform"], autopct='%1.1f%%')
plt.title("Platform Usage Share")
plt.show()


# -------------------------------
# 2. Correlation Heatmap
# -------------------------------
corr = df[
    ["DailySocialMediaHours", "SleepHours",
     "StressLevel", "AnxietyLevel", "AcademicPerformance"]
].corr()

plt.figure(figsize=(8,5))
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

# -------------------------------
# 3. Mental Health Analysis
# -------------------------------
mental = df.groupby("Gender")[["StressLevel", "AnxietyLevel"]].mean()

mental.plot(kind="bar", stacked=True, figsize=(7,5))
plt.title("Stress & Anxiety by Gender")
plt.ylabel("Average Level")
plt.show()

# -------------------------------
# 4. Radar Chart
# -------------------------------
radar_vals = df[
    ["SocialInteractionLevel", "StressLevel",
     "AnxietyLevel", "AddictionLevel"]
].mean()

categories = radar_vals.index.tolist()
values = radar_vals.values

angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
values = np.concatenate((values, [values[0]]))
angles += angles[:1]

plt.figure(figsize=(6,6))
ax = plt.subplot(111, polar=True)
ax.plot(angles, values)
ax.fill(angles, values, alpha=0.2)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)
plt.title("Average Mental Health Indicators")
plt.show()

# -------------------------------
# 5. Depression Distribution
# -------------------------------
dep = df["DepressionLabel"].value_counts().reset_index()
dep.columns = ["Label", "Count"]

plt.figure(figsize=(6,4))
sns.barplot(data=dep, x="Label", y="Count")
plt.title("Depression Distribution")
plt.show()

# -------------------------------
# 6. Dataset Preview
# -------------------------------
print("\n=== Dataset Preview ===")
print(df.head())