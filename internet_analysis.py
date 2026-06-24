import matplotlib.pyplot as plt
import pandas as pd

# Loading data
data = "/workspaces/internet_usage_analysis/INT_BAND_PER_USR.csv"
df=pd.read_csv(data)

# Data Inspection of first 10 rows
print(df.head())
print("Dataset Information:\n\t",df.info())
print("Missing Values:\n\t",df.isnull().sum())
print("Missing Values:\n\t", df.duplicated().sum())

# Data Formatting: Keep the only neccessary columns for analysis
df = df[[
     "REF_AREA_LABEL",
     "TIME_PERIOD",
     "OBS_VALUE",
     "INDICATOR_LABEL"
]]

# Measure selection
measure = "OBS_VALUE"
print("Measure:\t")
print(df[measure].describe())
# Clean measure data
df = df[measure]
# ===========================
# Rename and Save to new file
# ===========================
df.to_csv("/workspaces/internet_usage_analysis/CLEAN_INT_BAND_PER_USR.csv")

# Rename columns
df.columns = [
      "Country",
      "Year",
      "InternetUsage",
      "Indicator"
]

# Ommission of missing values & duplicate rows
df.dropna()

#=================
#Ongoing Debugging
#=================
print(df.columns)
print(df.head())

# Coverting data types
df["Year"] = df["Year"].astype(int)
df["InternetUsage"] = pd.to_numeric(df["InternetUsage"])
print("SUCCESS CLEANING.............")
print(df.head())

# ========
# Analysis
# ========
print("\nAverage Inernet Usage by Country:\t")
print(df.groupby("Country")["InterneUsage"].mean().sort_values(asceding=False))

# Data filtration
sa = df[df["Country"] == "South Africa"]

# ==================
# Data Visualization
# ==================
plt.figure(figsize=(10,6))
plt.plot(sa["Year"],
         sa["InternetUsage"],
         marker="o")

plt.title("Internet Usage in South Africa")
plt.xlabel("Year",c='r')
plt.ylabel("Internet Usage",c='r')
plt.grid(True)

# Save Graph as .png for visuals
plt.savefig("graph.png")

#Display Graphs
plt.show()