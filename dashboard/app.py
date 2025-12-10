import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Page setup
st.set_page_config(page_title="Smart Home Energy Optimizer", layout="wide")

# Title and intro
st.title("🏡 Smart Home Energy Optimizer")
st.markdown("Analyze and visualize your home's energy consumption to optimize usage and save money.")

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv("data/sample_data.csv", parse_dates=["timestamp"])
    return data

data = load_data()

# Show raw data
if st.checkbox("Show Raw Data"):
    st.subheader("📄 Uploaded Energy Data")
    st.dataframe(data)

# Appliance columns
appliances = ["kitchen", "ac", "heater"]
data["total_usage"] = data[appliances].sum(axis=1)

# --- Total Energy Usage Over Time ---
st.subheader("🔌 Total Energy Usage Over Time")

fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(data["timestamp"], data["total_usage"], color='orange', marker='o')

ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.xaxis.set_major_locator(mdates.HourLocator(interval=1))
plt.xticks(rotation=45)

ax1.set_xlabel("Time of Day")
ax1.set_ylabel("Total Usage (Watts)")
ax1.set_title("🔌 Total Energy Usage Over Time")
ax1.grid(True)

plt.tight_layout()
st.pyplot(fig1)

# --- Appliance-wise Average Usage ---
st.subheader("📉 Appliance-wise Average Energy Usage")

avg_usage = data[appliances].mean()
fig2, ax2 = plt.subplots()
avg_usage.plot(kind='bar', color=['green', 'blue', 'red'], ax=ax2)

ax2.set_ylabel("Average Usage (Watts)")
ax2.set_title("📊 Average Appliance Usage")
st.pyplot(fig2)

# --- Day vs Night Usage ---
st.subheader("🌞 Day vs 🌙 Night Energy Usage")

day_data = data[data["day_night"] == "Day"]
night_data = data[data["day_night"] == "Night"]

day_total = day_data[appliances].sum().sum()
night_total = night_data[appliances].sum().sum()

col1, col2 = st.columns(2)
col1.metric("🌞 Day Usage", f"{day_total:.0f} Watts")
col2.metric("🌙 Night Usage", f"{night_total:.0f} Watts")

labels = ['Day', 'Night']
sizes = [day_total, night_total]
colors = ['gold', 'skyblue']

fig3, ax3 = plt.subplots()
ax3.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
ax3.axis('equal')
st.pyplot(fig3)

# --- Temperature vs Total Usage ---
st.subheader("🌡️ Temperature vs Energy Usage")

fig4, ax4 = plt.subplots()
ax4.plot(data["temp"], data["total_usage"], marker='o', color='purple')

ax4.set_xlabel("Temperature (°C)")
ax4.set_ylabel("Total Energy Usage (Watts)")
ax4.set_title("🌡️ Temperature vs Total Energy Usage")
ax4.grid(True)
st.pyplot(fig4)

# --- Smart Suggestion ---
st.subheader("💡 Smart Suggestions")

peak_row = data.loc[data["total_usage"].idxmax()]
peak_time = peak_row["timestamp"].strftime("%H:%M")
peak_usage = peak_row["total_usage"]

st.markdown(f"📈 Highest energy usage was **{int(peak_usage)} Watts at {peak_time}**. Try reducing appliance load during this time to save energy.")
