import tkinter as tk
import time
import math
from datetime import datetime, timedelta, timezone

# Function to update the clock
def update_clock():
    # Clear all clock hands
    canvas.delete("hands")

    if display_mode.get() == "Local":
        update_local_clock()
    elif display_mode.get() == "New York":
        update_new_york_clock()
    elif display_mode.get() == "Tokyo":
        update_tokyo_clock()

    root.after(1000, update_clock)

# Function to update local time clock hands
def update_local_clock():
    current_time = time.localtime()
    seconds = current_time.tm_sec
    minutes = current_time.tm_min
    hours = current_time.tm_hour % 12  # Use 12-hour format

    if time_format.get() == 24:
        hours = current_time.tm_hour  # Use 24-hour format

    local_second_angle = 360 - (seconds * 6 - 90)  # Adjust for 12 o'clock start
    local_minute_angle = 360 - (minutes * 6 + seconds * 0.1 - 90)  # Adjust for 12 o'clock start
    local_hour_angle = 360 - (hours * 30 + minutes * 0.5 - 90)  # Adjust for 12 o'clock start

    # Update the local time clock hands
    draw_clock_hand(local_second_angle, 90, hand_color("red"))
    draw_clock_hand(local_minute_angle, 70, hand_color("blue"))
    draw_clock_hand(local_hour_angle, 50, hand_color("blue"))

    current_time_str = time.strftime("%I:%M:%S %p" if time_format.get() == 12 else "%H:%M:%S")
    time_label.config(text=f"Local Time: {current_time_str}")

# Function to update New York time clock hands
def update_new_york_clock():
    ny_time = datetime.now(timezone(timedelta(hours=-5)))
    ny_seconds = ny_time.second
    ny_minutes = ny_time.minute
    ny_hours = ny_time.hour % 12 if time_format.get() == 12 else ny_time.hour

    ny_second_angle = 360 - (ny_seconds * 6 - 90)  # Adjust for 12 o'clock start
    ny_minute_angle = 360 - (ny_minutes * 6 + ny_seconds * 0.1 - 90)  # Adjust for 12 o'clock start
    ny_hour_angle = 360 - (ny_hours * 30 + ny_minutes * 0.5 - 90)  # Adjust for 12 o'clock start

    # Update the New York time clock hands
    draw_clock_hand(ny_second_angle, 90, hand_color("red"))
    draw_clock_hand(ny_minute_angle, 70, hand_color("blue"))
    draw_clock_hand(ny_hour_angle, 50, hand_color("blue"))

    ny_time_str = ny_time.strftime("%I:%M:%S %p" if time_format.get() == 12 else "%H:%M:%S")
    time_label.config(text=f"New York Time: {ny_time_str}")

# Function to update Tokyo time clock hands
def update_tokyo_clock():
    tokyo_time = datetime.now(timezone(timedelta(hours=9)))
    tokyo_seconds = tokyo_time.second
    tokyo_minutes = tokyo_time.minute
    tokyo_hours = tokyo_time.hour % 12 if time_format.get() == 12 else tokyo_time.hour

    tokyo_second_angle = 360 - (tokyo_seconds * 6 - 90)  # Adjust for 12 o'clock start
    tokyo_minute_angle = 360 - (tokyo_minutes * 6 + tokyo_seconds * 0.1 - 90)  # Adjust for 12 o'clock start
    tokyo_hour_angle = 360 - (tokyo_hours * 30 + tokyo_minutes * 0.5 - 90)  # Adjust for 12 o'clock start

    # Update the Tokyo time clock hands
    draw_clock_hand(tokyo_second_angle, 90, hand_color("red"))
    draw_clock_hand(tokyo_minute_angle, 70, hand_color("blue"))
    draw_clock_hand(tokyo_hour_angle, 50, hand_color("blue"))

    tokyo_time_str = tokyo_time.strftime("%I:%M:%S %p" if time_format.get() == 12 else "%H:%M:%S")
    time_label.config(text=f"Tokyo Time: {tokyo_time_str}")

# Function to check if it's night
def is_night():
    current_time = time.localtime()
    return 19 <= current_time.tm_hour <= 6  # Assuming night is from 7 PM to 6 AM

# Function to switch display mode
def switch_display_mode(mode):
    display_mode.set(mode)

# Function to draw clock numbers
def draw_clock_numbers():
    for i in range(1, 13):
        angle_deg = 360 - i * 30 + 90  # Adjust for 12 o'clock start
        angle_rad = math.radians(angle_deg)
        x = 100 + 80 * math.cos(angle_rad)  # Adjust position for numbers
        y = 100 - 80 * math.sin(angle_rad)
        canvas.create_text(x, y, text=str(i), font=("Helvetica", 12, "bold"), fill=hand_color("blue"))

# Function to draw clock hands with color based on day/night
def draw_clock_hand(angle, length, color):
    angle_rad = math.radians(angle)
    x_center = 100
    y_center = 100
    x_tip = x_center + length * math.cos(angle_rad)
    y_tip = y_center - length * math.sin(angle_rad)
    canvas.create_line(x_center, y_center, x_tip, y_tip, fill=color, width=2, tag="hands")

# Function to determine hand color based on day/night and dark mode
def hand_color(color):
    return "white" if is_night() and dark_mode.get() else color

# Function to toggle between dark and light mode
def toggle_dark_mode():
    current_bg = canvas.cget("bg")
    new_bg = "black" if current_bg == "white" else "white"
    canvas.configure(bg=new_bg)

    # Update clock elements when toggling dark mode
    draw_clock_numbers()
    update_clock()

# Create the main window
root = tk.Tk()
root.title("Analog World Clock")

# Create a canvas for the clock face
canvas = tk.Canvas(root, width=200, height=200, bg="white")
canvas.pack()

# Draw a circular border around the clock
canvas.create_oval(10, 10, 190, 190, outline="blue", width=4)

# Draw clock numbers
draw_clock_numbers()

# Create a label to display the current time
time_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"))
time_label.pack()

# Create radio buttons for selecting time format
time_format_label = tk.Label(root, text="Select Time Format:", font=("Helvetica", 12))
time_format_label.pack()
time_format = tk.IntVar(value=12)
format_12_hour = tk.Radiobutton(root, text="12-Hour Format", variable=time_format, value=12, font=("Helvetica", 10))
format_12_hour.pack()
format_24_hour = tk.Radiobutton(root, text="24-Hour Format", variable=time_format, value=24, font=("Helvetica", 10))
format_24_hour.pack()

# Create buttons to switch between time zones
local_button = tk.Button(root, text="Local Time", command=lambda: switch_display_mode("Local"))
local_button.pack(side="left", padx=5)

ny_button = tk.Button(root, text="New York Time", command=lambda: switch_display_mode("New York"))
ny_button.pack(side="left", padx=5)

tokyo_button = tk.Button(root, text="Tokyo Time", command=lambda: switch_display_mode("Tokyo"))
tokyo_button.pack(side="left", padx=5)

# Create a button to toggle dark mode
dark_mode = tk.BooleanVar()
dark_mode.set(False)
dark_mode_button = tk.Button(root, text="Toggle Dark Mode", command=toggle_dark_mode)
dark_mode_button.pack(side="left", padx=5)

# Initialize display_mode variable
display_mode = tk.StringVar()
display_mode.set("Local")

# Start the clock update
update_clock()

root.mainloop()