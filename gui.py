import tkinter as tk
import time
import car_detection  # Import car detection module

def update_traffic_lights(direction_A, direction_B):
    canvas.delete("all")  # Clear previous lights
    
    if direction_A == "green":
        canvas.create_oval(50, 50, 150, 150, fill="green", outline="black")
    else:
        canvas.create_oval(50, 50, 150, 150, fill="red", outline="black")
    
    if direction_B == "green":
        canvas.create_oval(250, 50, 350, 150, fill="green", outline="black")
    else:
        canvas.create_oval(250, 50, 350, 150, fill="red", outline="black")
    
    window.update()

def control_traffic():
    while True:
        cars_A, cars_B = car_detection.get_car_count()  # Get car counts
        
        if cars_A > cars_B:
            update_traffic_lights("green", "red")
            time.sleep(5)  # Longer green for A
        else:
            update_traffic_lights("red", "green")
            time.sleep(5)  # Longer green for B

def start_gui():
    global canvas, window
    window = tk.Tk()
    window.title("Smart Traffic Control System")
    
    canvas = tk.Canvas(window, width=400, height=200)
    canvas.pack()
    
    window.after(1000, control_traffic)  # Start traffic control loop
    window.mainloop()

start_gui()
