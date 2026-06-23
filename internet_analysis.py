import matplotlib.pyplot as plt
import pandas as pd

data = "/workspaces/internet_usage_analysis/INT_BAND_PER_USR.csv"

df=pd.read_csv(data)

years = df["FREQ"].unique() 
values = df["UNIT_MEASURE"].unique()

plt.plot(years,values)
plt.title("Internet Usage in South Africa")
plt.color_sequences
plt.xlabel("Freuency")
plt.ylabel("Structure_id")
plt.savefig("graph.png")

print(df.head(10))
plt.show()