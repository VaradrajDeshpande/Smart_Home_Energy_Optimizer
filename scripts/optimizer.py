import pandas as pd

# Load data
data = pd.read_csv("../data/sample_data.csv", parse_dates=["timestamp"])

# Calculate total usage per row
data["total_usage"] = data["kitchen"] + data["ac"] + data["heater"]

# Extract hour from timestamp
data["hour"] = data["timestamp"].dt.hour

# Simple rule: suggest off-peak hours (e.g., before 9 AM or after 9 PM)
def suggest_appliance_usage(row):
    if row["total_usage"] > 1000:  # High usage
        if row["hour"] < 9 or row["hour"] >= 21:
            return "✅ Good time to run appliances"
        else:
            return "⚠️ Suggest shifting usage to off-peak hours"
    else:
        return "✔️ Usage is normal"

# Apply optimization rule
data["recommendation"] = data.apply(suggest_appliance_usage, axis=1)

# Display suggestions
print("\n🔧 Optimization Recommendations (First 10 rows):\n")
print(data[["timestamp", "total_usage", "hour", "recommendation"]].head(10))

# Save to file
data.to_csv("../data/optimized_output.csv", index=False)
print("\n📁 Saved recommendations to: data/optimized_output.csv")
