import tkinter as tk
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque

# Store traffic data (last 10 readings)
traffic_data = deque(maxlen=10)
time_labels = deque(maxlen=10)
time_counter = 0  # Simulated time steps

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

# Function to update traffic light
def update_traffic_light():
    global time_counter
    car_count = read_car_count()
    emergency_detected = check_emergency()

    # Update labels
    car_count_label.config(text=f"🚗 Cars Detected: {car_count}")
    emergency_label.config(text="🚨 Emergency: Yes!" if emergency_detected else "🚨 Emergency: No")

    # Update traffic flow graph data
    traffic_data.append(car_count)
    time_labels.append(time_counter)
    time_counter += 1
    update_graph()

    # Traffic Light Logic
    if emergency_detected:
        set_light("green", "🚨 Emergency Detected!", 10)
    elif car_count > 5:  # High traffic
        set_light("green", "🟢 High Traffic", 8)
    elif car_count == 0:  # No cars
        set_light("red", "🔴 No Cars - Stopping", 5)
    else:  # Normal cars detected
        set_light("yellow", "🟡 Get Ready", 3)
        root.after(3000, lambda: set_light("green", "🟢 Cars Passing", 8))

    root.after(2000, update_traffic_light)  # Update every 2 seconds

# Function to change light color and show countdown
def set_light(color, text, duration):
    light_canvas.itemconfig(red_light, fill="red" if color == "red" else "gray")
    light_canvas.itemconfig(yellow_light, fill="yellow" if color == "yellow" else "gray")
    light_canvas.itemconfig(green_light, fill="green" if color == "green" else "gray")

    countdown_timer(text, duration, color)

# Countdown function
def countdown_timer(text, duration, color):
    if duration > 0:
        status_label.config(text=f"{text} - {duration}s", fg=color)
        root.after(1000, lambda: countdown_timer(text, duration - 1, color))
    else:
        status_label.config(text=text, fg=color)

# Function to update traffic graph
def update_graph():
    ax.clear()
    ax.plot(time_labels, traffic_data, marker="o", linestyle="-", color="blue")
    ax.set_title("Traffic Flow Over Time")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Car Count")
    ax.grid(True)
    canvas.draw()

# GUI Setup
root = tk.Tk()
root.title("🚦 Smart Traffic Light Control")
root.geometry("400x600")
root.configure(bg="white")

# Frame for traffic light with border
frame = tk.Frame(root, bg="black", bd=5, relief="ridge", padx=20, pady=20)
frame.pack(pady=10)

# Canvas for traffic light
light_canvas = tk.Canvas(frame, width=120, height=280, bg="black")
light_canvas.pack()

# Traffic light circles with padding
red_light = light_canvas.create_oval(30, 20, 90, 80, fill="red")  
yellow_light = light_canvas.create_oval(30, 100, 90, 160, fill="gray")
green_light = light_canvas.create_oval(30, 180, 90, 240, fill="gray")

# Labels with improved fonts and spacing
status_label = tk.Label(root, text="🔴 Red Light - Stop", font=("Arial", 14, "bold"), fg="red", bg="white", pady=10)
status_label.pack()

car_count_label = tk.Label(root, text="🚗 Cars Detected: 0", font=("Arial", 12), fg="blue", bg="white", pady=5)
car_count_label.pack()

emergency_label = tk.Label(root, text="🚨 Emergency: No", font=("Arial", 12, "bold"), fg="black", bg="white", pady=5)
emergency_label.pack()

# Traffic Flow Graph
fig, ax = plt.subplots(figsize=(4, 2), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Start updating traffic light
update_traffic_light()

# Run the GUI
root.mainloop()
