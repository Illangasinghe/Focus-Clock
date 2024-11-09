"""
FocusClock: A simple alarm clock and Pomodoro timer application using Tkinter.
Features:
- Set custom alarms with sound notifications.
- Activate a 25-minute Pomodoro timer.
- Display remaining time, including negative countdown if the alarm is not dismissed.
"""

import tkinter as tk
from tkinter import simpledialog, ttk
from datetime import datetime, timedelta
import time
import threading
import pygame
import os
import sys

# Helper function to determine the base path for bundled files (PyInstaller support)
def get_resource_path(filename):
    """Get the absolute path to a resource, works for PyInstaller bundles and standalone scripts."""
    if getattr(sys, 'frozen', False):  # Check if we are running as a PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

# Function to play the alarm sound
def play_alarm_sound():
    """Plays the alarm sound when triggered."""
    pygame.mixer.init()
    sound_path = get_resource_path('cheering.wav')  # Use the correct path for the sound file
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()

# Function to display a status message in the status bar with dynamic colors
def show_status_message(message, color="green"):
    """
    Updates the status bar with a message.
    
    Args:
        message (str): The message to display.
        color (str): The color of the message text.
    """
    status_label.config(fg=color)
    status_var.set("   " + message)  # Add space for better alignment
    status_label.after(3000, lambda: status_var.set(''))  # Clear the message after 3 seconds

# Background thread function to check if it's time to trigger the alarm
def check_alarm():
    """Continuously checks if the current time matches the set alarm time and triggers the alarm if matched."""
    global alarm_triggered
    last_triggered_minute = None

    while True:
        current_time = datetime.now().strftime('%H:%M')
        current_minute = datetime.now().minute

        if alarm_time.get()[:5] == current_time and not alarm_disabled.get() and current_minute != last_triggered_minute:
            play_alarm_sound()
            root.attributes("-topmost", True)  # Bring the window to the front
            show_status_message("Alarm triggered: Time to take a break!", "green")
            last_triggered_minute = current_minute
            alarm_triggered = True

        time.sleep(1)
        update_time_remaining()

# Function to set a custom alarm time
def set_alarm():
    """Prompts the user to set a custom alarm time."""
    global alarm_triggered
    new_time = simpledialog.askstring("Set Alarm Time", "Enter time in HH:MM format:")
    if new_time:
        try:
            parsed_time = datetime.strptime(new_time, '%H:%M')
            alarm_time.set(parsed_time.strftime('%H:%M:00'))
            alarm_disabled.set(False)
            alarm_triggered = False
            show_status_message(f"Alarm set for {alarm_time.get()}")
            time_remaining_label.config(fg="green")
        except ValueError:
            show_status_message("Error: Invalid time format. Use HH:MM", "red")

# Function to activate a 25-minute Pomodoro timer
def go_pomodoro():
    """Activates a 25-minute Pomodoro timer."""
    global alarm_triggered
    work_time = datetime.now() + timedelta(minutes=25)
    alarm_time.set(work_time.strftime('%H:%M:%S'))
    alarm_disabled.set(False)
    alarm_triggered = False
    show_status_message("Pomodoro mode activated: 25 min work timer set.")
    time_remaining_label.config(fg="green")

# Function to clear the current alarm
def clear_alarm():
    """Clears the alarm and resets the UI."""
    global alarm_triggered
    alarm_disabled.set(True)
    alarm_time.set("Not set")
    time_remaining.set("00:00")
    time_remaining_label.config(fg="green")
    alarm_triggered = False
    show_status_message("Alarm cleared.", "red")

# Function to toggle the "Always on Top" state of the window
def toggle_always_on_top():
    """Toggles the 'Always on Top' state of the window."""
    root.attributes("-topmost", always_on_top.get())
    show_status_message("Always on top toggled.")

# Function to update the remaining time until the next alarm
def update_time_remaining():
    """Updates the remaining time display and handles negative countdown after the alarm is triggered."""
    global alarm_triggered
    try:
        now = datetime.now()
        if alarm_time.get() and alarm_time.get() != "Not set":
            alarm_time_obj = datetime.strptime(alarm_time.get(), '%H:%M:%S')
            alarm_datetime = now.replace(hour=alarm_time_obj.hour, minute=alarm_time_obj.minute, second=alarm_time_obj.second)

            if now >= alarm_datetime and not alarm_triggered:
                alarm_datetime += timedelta(days=1)

            remaining = alarm_datetime - now

            if remaining.total_seconds() > 0 or not alarm_triggered:
                time_remaining_label.config(fg="green")
                minutes, seconds = divmod(int(remaining.total_seconds()), 60)
                time_remaining.set(f"{minutes:02}:{seconds:02}")
            else:
                if alarm_triggered:
                    time_remaining_label.config(fg="red")
                    minutes, seconds = divmod(abs(int(remaining.total_seconds())), 60)
                    time_remaining.set(f"-{minutes:02}:{seconds:02}")
                else:
                    time_remaining.set("00:00")
        else:
            time_remaining.set("00:00")
    except ValueError:
        time_remaining.set("00:00")

# Create the main window
root = tk.Tk()
root.title("FocusClock")
root.minsize(400, 350)

# Variables for the app
alarm_time = tk.StringVar(value='Not set')
alarm_disabled = tk.BooleanVar(value=False)
pomodoro_mode = tk.BooleanVar(value=False)
always_on_top = tk.BooleanVar(value=False)
time_remaining = tk.StringVar(value='')
status_var = tk.StringVar(value='')

# Create a frame for the border
main_frame = ttk.Frame(root, padding=10, borderwidth=2, relief="solid")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# UI components
date_label = tk.Label(main_frame, text=datetime.now().strftime('%Y-%m-%d'), font=("Helvetica", 16))
date_label.pack(padx=10, pady=5)

time_display = tk.Label(main_frame, font=("Helvetica", 24))
time_display.pack(padx=10, pady=5)

next_alarm_text = tk.Label(main_frame, text="Next Alarm:", font=("Helvetica", 12), fg="gray")
next_alarm_text.pack(padx=10, pady=2)

next_alarm_label = tk.Label(main_frame, textvariable=alarm_time, font=("Helvetica", 12), fg="blue")
next_alarm_label.pack(padx=10, pady=2)

remaining_time_text = tk.Label(main_frame, text="Remaining Time:", font=("Helvetica", 12), fg="gray")
remaining_time_text.pack(padx=10, pady=2)

time_remaining_label = tk.Label(main_frame, textvariable=time_remaining, font=("Helvetica", 12), fg="green")
time_remaining_label.pack(padx=10, pady=2)

task_label = tk.Label(main_frame, text="Current Task:", font=("Helvetica", 12), fg="gray")
task_label.pack(anchor="w", padx=10, pady=2)

task_text = tk.Text(main_frame, height=3, wrap="word")
task_text.pack(fill="both", expand=True, padx=10, pady=5)

# Button frame for actions
button_frame = tk.Frame(main_frame)
button_frame.pack(padx=10, pady=5)

pomodoro_button = tk.Button(button_frame, text="Go Pomodoro", command=go_pomodoro)
pomodoro_button.pack(side='left', padx=5)

set_alarm_button = tk.Button(button_frame, text="Set Alarm Time", command=set_alarm)
set_alarm_button.pack(side='left', padx=5)

clear_alarm_button = tk.Button(button_frame, text="Clear Alarm", command=clear_alarm)
clear_alarm_button.pack(side='left', padx=5)

# "Always on Top" toggle
mode_frame = tk.Frame(main_frame)
mode_frame.pack(padx=10, pady=5)

always_on_top_button = tk.Checkbutton(mode_frame, text="Always on Top", variable=always_on_top, command=toggle_always_on_top)
always_on_top_button.pack(side='left', padx=5)

# Status bar at the bottom of the window
status_label = tk.Label(root, textvariable=status_var, font=("Helvetica", 10), anchor="w")
status_label.pack(side="bottom", fill="x")

# Function to update the current time display
def update_time():
    """Continuously updates the current time display."""
    current_time = datetime.now().strftime('%H:%M:%S')
    time_display.config(text=current_time)
    root.after(1000, update_time)

# Start a background thread for the alarm check
alarm_thread = threading.Thread(target=check_alarm, daemon=True)
alarm_thread.start()

# Start updating the current time
update_time()

# Run the main application loop
root.mainloop()
