import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("weather.csv")

print(df)

print("Average Temperature:", df["Temperature"].mean())
print("Maximum Temperature:", df["Temperature"].max())
print("Minimum Temperature:", df["Temperature"].min())

hottest = df.loc[df["Temperature"].idxmax()]
print("Hottest Day:", hottest["Date"])

plt.plot(df["Date"], df["Temperature"], marker='o')
plt.title("Daily Temperature Changes")
plt.xlabel("Date")
plt.ylabel("Temperature")
plt.show()

plt.hist(df["Temperature"], bins=5)
plt.title("Temperature Distribution")
plt.xlabel("Temperature")
plt.ylabel("Frequency")
plt.show()

plt.scatter(df["Humidity"], df["Temperature"])
plt.title("Humidity vs Temperature")
plt.xlabel("Humidity")
plt.ylabel("Temperature")
plt.show()
