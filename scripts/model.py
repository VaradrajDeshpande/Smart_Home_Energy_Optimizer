import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("../data/sample_data.csv", parse_dates=["timestamp"])
data["total_usage"] = data["kitchen"] + data["ac"] + data["heater"]

# Feature engineering: extract hour of the day
data["hour"] = data["timestamp"].dt.hour

# Prepare features and target
X = data[["kitchen", "ac", "heater", "occupancy", "temp", "hour"]]
y = data["total_usage"]

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print("✅ Model Trained Successfully")
print(f"📉 Mean Squared Error: {mse:.2f}")

# Plot actual vs predicted
plt.figure(figsize=(10, 5))
plt.plot(y_test.values, label="Actual", marker='o')
plt.plot(y_pred, label="Predicted", marker='x')
plt.title("Actual vs Predicted Energy Usage")
plt.xlabel("Sample")
plt.ylabel("Energy Usage (Watts)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
