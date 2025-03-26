import tkinter as tk
import time

# Function to read car count from file
def read_car_count():
    try:
        with open("car_count.txt", "r") as f:
            return int(f.read().strip())
    except:
        return 0  # Default to 0 if file not found

# Function to check emergency vehicle status
def check_emergency():
    try:
        with open("emergency_detected.txt", "r") as f:
            return f.read().strip() == "1"
    except:
        return False  # Default to False if file not found

# Function to update traffic light based on car count and emergency status
def update_traffic_light():
    car_count = read_car_count()
    emergency_detected = check_emergency()

    if emergency_detected:
        light_canvas.itemconfig(red_light, fill="gray")
        light_canvas.itemconfig(green_light, fill="green")
        status_label.config(text="Green Light - Emergency Vehicle!", fg="green")
    elif car_count > 0:
        light_canvas.itemconfig(red_light, fill="gray")
        light_canvas.itemconfig(green_light, fill="green")
        status_label.config(text="Green Light - Cars can pass", fg="green")
    else:
        light_canvas.itemconfig(red_light, fill="red")
        light_canvas.itemconfig(green_light, fill="gray")
        status_label.config(text="Red Light - Stop", fg="red")

    root.after(1000, update_traffic_light)  # Update every second

# GUI Setup
root = tk.Tk()
root.title("Traffic Light Control")

# Canvas for traffic light
light_canvas = tk.Canvas(root, width=100, height=200, bg="black")
light_canvas.pack(pady=20)

# Traffic light circles
red_light = light_canvas.create_oval(30, 20, 70, 60, fill="red")   # Red by default
green_light = light_canvas.create_oval(30, 140, 70, 180, fill="gray")

# Label for status
status_label = tk.Label(root, text="Red Light - Stop", font=("Arial", 14), fg="red")
status_label.pack()

# Start updating traffic light
update_traffic_light()

# Run the GUI
root.mainloop()













# import tkinter as tk
# from tkinter import Label
# import random

# # Global variables for car count and emergency status
# car_count = 0
# emergency_detected = False
# traffic_light_state = "Red"

# # Function to update the traffic light and car count
# def update_traffic_light():
#     global car_count, emergency_detected, traffic_light_state

#     # Simulate car detection (replace with real detection later)
#     car_count = random.randint(5, 30)  # Simulated count

#     # Simulate emergency detection (replace with real detection later)
#     emergency_detected = random.choice([True, False])

#     if emergency_detected:
#         traffic_light_state = "Green (Emergency)"
#         light_canvas.config(bg="green")
#         emergency_label.config(text="🚨 Emergency Vehicle Detected!", fg="red")
#     else:
#         traffic_light_state = "Green" if car_count > 15 else "Red"
#         light_canvas.config(bg="green" if traffic_light_state == "Green" else "red")
#         emergency_label.config(text="No Emergency", fg="black")

#     # Update labels
#     car_count_label.config(text=f"Car Count: {car_count}")
#     light_status_label.config(text=f"Traffic Light: {traffic_light_state}")

#     # Call the function again after 3 seconds
#     root.after(3000, update_traffic_light)

# # Create main window
# root = tk.Tk()
# root.title("Smart Traffic Control GUI")
# root.geometry("400x400")

# # Traffic light display
# light_canvas = tk.Canvas(root, width=100, height=100, bg="red")
# light_canvas.pack(pady=20)

# # Labels for car count and traffic light status
# car_count_label = Label(root, text="Car Count: 0", font=("Arial", 14))
# car_count_label.pack()

# light_status_label = Label(root, text="Traffic Light: Red", font=("Arial", 14))
# light_status_label.pack()

# # Emergency vehicle status
# emergency_label = Label(root, text="No Emergency", font=("Arial", 14))
# emergency_label.pack()

# # Start updating the GUI
# update_traffic_light()

# # Run the Tkinter event loop
# root.mainloop()
