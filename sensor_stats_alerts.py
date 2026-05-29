import numpy as np

n = int(input("Enter the number of sensors: "))
r = int(input("Enter the number of readings per sensor: ")) # Ek baar r pucha taki array shape sahi rahe
s = []

# STEP 1: Data Collection (Loop sirf yahan tak hona chahiye)
for i in range(n):
    data = []
    print(f"\nENTER DETAILS FOR SENSOR {i+1}")
    for j in range(r):
        hr = int(input(f"Enter the reading for hour {j+1}: "))
        data.append(hr)
    s.append(data)

# STEP 2: Conversion to NumPy Array (Loop ke bahar)
arr = np.array(s)
print("\nReadings Matrix:\n", arr)

# STEP 3: Statistical Analysis [8, 9]
avg = np.mean(arr, axis=1) # Row-wise average
print(f"\nSensor Averages: {avg}")

# STEP 4: Deviation with Broadcasting [10, 11]
try:
    reshaped_avg = avg.reshape(n, 1) # (n,) ko (n,1) banaya taki stretch ho sake
    dev = arr - reshaped_avg # FIX: arr use kiya r ki jagah
    print(f"Deviation Matrix:\n{dev}")
except ValueError as e:
    print(f"Deviation calculation failed: {e}")

# STEP 5: Finding Alerts [12]
try:
    alert_sensors, alert_hours = np.where(np.abs(dev) > 10)
    print("\n_____ALERTS TRIGGERED______\n")
    if len(alert_sensors) > 0:
        for s_idx, h_idx in zip(alert_sensors, alert_hours):
            # s_idx aur h_idx use kiya shadowing se bachne ke liye
            print(f"Sensor {s_idx} at hour {h_idx}, deviation was: {dev[s_idx, h_idx]:.2f}")
    else:
        print("No alerts triggered.")
except Exception as e:
    print("Error in checking alerts.")
