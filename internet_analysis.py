import matplotlib.pyplot as plt
import pandas as pd

data = "/workspaces/internet_usage_analysis/INT_BAND_PER_USR.csv"

df=pd.read_csv(data)

#clean
df.dropna(subset=["STRUCTURE","STRUCTURE_ID","ACTION","FREQ","REF_AREA",
                        "INDICATOR","SEX","AGE","URBANISATION","UNIT_MEASURE",
                        "COMP_BREAKDOWN_1","COMP_BREAKDOWN_2","COMP_BREAKDOWN_3"], axis=0,inplace=True)

df.to_csv("/workspaces/internet_usage_analysis/CLEAN_INT_BAND_PER_USR.csv")
infor = df.describe()

ypoint = df["OBS_VALUE"]
xpoint = df["REF_AREA_LABEL"]

print(infor)
print()
print(df.info())


plt.title("Internet Usage")
#plt.color_sequences
plt.xlabel("reference area",c='r')
plt.ylabel("obs-value",c='r')

#Analysis

print(df.head(3))
plt.plot(ypoint,xpoint,marker='o',ls='--')

#Save Graph as.png for visuals
plt.savefig("graph.png")
#Display Graphs
plt.show()