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

# GUI Setup
root = tk.Tk()
root.title("Smart Traffic Light Control")

# Canvas for traffic light
light_canvas = tk.Canvas(root, width=120, height=280, bg="black")
light_canvas.pack(pady=20)

# Traffic light circles
red_light = light_canvas.create_oval(30, 20, 90, 80, fill="red")  # Red by default
yellow_light = light_canvas.create_oval(30, 100, 90, 160, fill="gray")  # Yellow
green_light = light_canvas.create_oval(30, 180, 90, 240, fill="gray")  # Green

# Labels
status_label = tk.Label(root, text="🔴 Red Light - Stop", font=("Arial", 14), fg="red")
status_label.pack()

car_count_label = tk.Label(root, text="🚗 Cars Detected: 0", font=("Arial", 14), fg="blue")
car_count_label.pack()

emergency_label = tk.Label(root, text="🚨 Emergency: No", font=("Arial", 14), fg="black")
emergency_label.pack()

# Flag to track toggling state
toggle_state = False

# Function to toggle between Yellow and Green Light
def toggle_yellow_green():
    global toggle_state

    if toggle_state:
        light_canvas.itemconfig(yellow_light, fill="gray")
        light_canvas.itemconfig(green_light, fill="green")
        status_label.config(text="🟢 Green Light - Cars can pass", fg="green")
    else:
        light_canvas.itemconfig(green_light, fill="gray")
        light_canvas.itemconfig(yellow_light, fill="yellow")
        status_label.config(text="🟡 Yellow Light - Get Ready", fg="orange")

    toggle_state = not toggle_state
    root.after(1000, toggle_yellow_green)  # Call function every second

# Function to update traffic light based on car count and emergency
def update_traffic_light():
    global toggle_state

    car_count = read_car_count()
    emergency_detected = check_emergency()

    # Debugging Prints
    print(f"Car Count: {car_count}, Emergency: {emergency_detected}")

    # Update the labels
    car_count_label.config(text=f"🚗 Cars Detected: {car_count}")
    emergency_label.config(text="🚨 Emergency: Yes!" if emergency_detected else "🚨 Emergency: No")

    # 🚨 Emergency Vehicle Detected - Priority Green
    if emergency_detected:
        print("Emergency detected! Turning GREEN for priority.")
        light_canvas.itemconfig(red_light, fill="gray")
        light_canvas.itemconfig(yellow_light, fill="gray")
        light_canvas.itemconfig(green_light, fill="green")
        status_label.config(text="🚨 Green Light - Emergency Detected!", fg="green")

    # 🚗 High Traffic Detected (> 5 cars) - Toggle Yellow & Green
    elif car_count > 5:
        print("High traffic detected! Toggling Yellow & Green.")
        light_canvas.itemconfig(red_light, fill="gray")
        toggle_yellow_green()  # Start toggling Yellow & Green

    # 🛑 No Cars - Red Light
    else:
        print("No traffic! Turning RED.")
        light_canvas.itemconfig(green_light, fill="gray")
        light_canvas.itemconfig(yellow_light, fill="gray")
        light_canvas.itemconfig(red_light, fill="red")
        status_label.config(text="🔴 Red Light - Stop", fg="red")
        toggle_state = False  # Reset toggle state

    root.after(2000, update_traffic_light)  # Check every 2 seconds

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
