import pandas as pd

df = pd.read_csv(
    r"C:\Users\HP\OneDrive\Desktop\Projects\Project-1 Social Media Addiction\data.txt",
    sep=r"\s+",   # regex: split on any whitespace
    header=None
)

# Assign column names
df.columns = [
    "Age","Gender","DailySocialMediaHours","PlatformUsage","SleepHours","ScreenTimeBeforeSleep","AcademicPerformance","PhysicalActivity","SocialInteractionLevel","StressLevel","AnxietyLevel","AddictionLevel","DepressionLabel"
]
# Generate SQL insert statements
# Generate SQL insert statements
with open("insert_statements.sql", "w") as f:
    for _, row in df.iterrows():
        values = []
        for val in row:
            if isinstance(val, str):
                values.append(f"'{val}'")   # wrap text in quotes
            else:
                values.append(str(val))
        sql = (
            "INSERT INTO Social_Media_Addiction "
            "(Age, Gender, DailySocialMediaHours, PlatformUsage, SleepHours, "
            "ScreenTimeBeforeSleep, AcademicPerformance, PhysicalActivity, "
            "SocialInteractionLevel, StressLevel, AnxietyLevel, AddictionLevel, DepressionLabel) "
            f"VALUES ({', '.join(values)});\n"
        )
        f.write(sql)
