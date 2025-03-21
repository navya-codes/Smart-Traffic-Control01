import tkinter as tk
import time
import random

# Function to update traffic lights dynamically
def update_traffic_lights(car_count_A, car_count_B, emergency_A, emergency_B):
    canvas.delete("all")
    
    # Determine light states
    if emergency_A:
        direction_A = "green"
        direction_B = "red"
    elif emergency_B:
        direction_A = "red"
        direction_B = "green"
    else:
        direction_A = "green" if car_count_A > car_count_B else "red"
        direction_B = "green" if car_count_B > car_count_A else "red"
    
    # Draw lights for direction A
    if direction_A == "green":
        canvas.create_oval(50, 50, 150, 150, fill="green", outline="black")
    else:
        canvas.create_oval(50, 50, 150, 150, fill="red", outline="black")
    
    # Draw lights for direction B
    if direction_B == "green":
        canvas.create_oval(250, 50, 350, 150, fill="green", outline="black")
    else:
        canvas.create_oval(250, 50, 350, 150, fill="red", outline="black")
    
    # Display car counts
    canvas.create_text(100, 180, text=f"Cars A: {car_count_A}", font=("Arial", 12))
    canvas.create_text(300, 180, text=f"Cars B: {car_count_B}", font=("Arial", 12))
    
    # Display emergency vehicle status
    if emergency_A:
        canvas.create_text(100, 200, text="Emergency!", font=("Arial", 12), fill="red")
    if emergency_B:
        canvas.create_text(300, 200, text="Emergency!", font=("Arial", 12), fill="red")
    
    window.update()

# Function to simulate traffic control
def traffic_control_simulation():
    for _ in range(10):  # Simulating 10 cycles
        car_count_A = random.randint(0, 20)
        car_count_B = random.randint(0, 20)
        emergency_A = random.choice([True, False, False, False])  # Less frequent emergencies
        emergency_B = random.choice([True, False, False, False])
        
        update_traffic_lights(car_count_A, car_count_B, emergency_A, emergency_B)
        time.sleep(3)  # Pause before updating again

# Setting up the GUI
window = tk.Tk()
window.title("Smart Traffic Control System")
canvas = tk.Canvas(window, width=400, height=250)
canvas.pack()

# Start the simulation
traffic_control_simulation()

window.mainloop()
