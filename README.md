# 🚦 Smart Traffic Control System

## 📌 Project Overview

The Smart Traffic Control System is a Python-based real-time traffic management solution that:

✅ Detects the number of cars on the road using OpenCV.
✅ Identifies emergency vehicles using color detection and siren detection.
✅ Dynamically adjusts traffic light timing based on real-time traffic flow.
✅ Provides a Tkinter GUI with a traffic light simulation and live car count updates.
✅ Displays a traffic flow graph for visualization.

___

## 🎯 Key Features

Car Detection – Counts the number of cars using OpenCV’s background subtraction and contour detection.

Emergency Detection – Identifies emergency vehicles using flashing light detection and sound analysis (PyDub).

Dynamic Traffic Light Timing – Adjusts the green light duration based on detected traffic levels.

GUI with Real-time Updates – Displays the current light status, car count, and emergency status.

Traffic Flow Graph – Visualizes car count variations over time.

___

## 🛠 Tech Stack & Libraries Used

Python (Core language)

OpenCV (Car detection)

PyDub (Siren sound detection)

Tkinter (Graphical User Interface)

Matplotlib (Traffic flow graph)

___

## 🚀 How to Run the Project

🔹 1️⃣ Setup Environment

Ensure you have Python 3.x installed. Then install dependencies using:

pip install opencv-python numpy pydub matplotlib tkinter

🔹 2️⃣ Run the Project

Run the GUI application:

python frontend.py

It will open the traffic control simulation interface.

___

## 📸 Project Workflow

1️⃣ Start the System → The program loads and initializes the GUI.2️⃣ Read Video Input → The system processes frames to detect cars.3️⃣ Check Emergency Vehicles → Detects flashing red/blue lights and sirens.4️⃣ Update Traffic Lights → Adjusts light timing dynamically based on car count & emergency status.5️⃣ GUI & Graph Updates → Displays real-time data, light changes, and traffic trends.

___

## 🖥 Project Files & Structure

📂 stcproject01
 ┣ 📜 car_detection.py  # Detects cars from video feed
 ┣ 📜 emergency_detection.py  # Detects emergency vehicles
 ┣ 📜 dynamic_timing.py  # Adjusts traffic light duration
 ┣ 📜 frontend.py  # GUI for traffic control system
 ┣ 📜 main.py  # Integrates all modules & starts the system
 ┣ 📂 videos  # Sample traffic videos for testing
 ┣ 📜 README.md  # Project Documentation

 ---

## 📊 Traffic Light Rules

Condition

Traffic Light

No cars detected

🔴 Red Light

Low traffic (1-5 cars)

🟡 Yellow Light (then Green)

High traffic (>5 cars)

🟢 Green Light

Emergency Vehicle Detected

🟢 Green Light (Priority)

___

## 📢 Future Enhancements

🔹 Add machine learning to predict congestion.🔹 Implement a web-based dashboard.🔹 Integrate IoT sensors for real-world applications.

