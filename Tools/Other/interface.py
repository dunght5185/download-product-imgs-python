import tkinter as tk
from tkinter import filedialog
import threading

def browse_file():
    filename = filedialog.askopenfilename()
    # Do something with the filename
    print(f"File chosen: {filename}")

def run_script():
    # Run your script here
    print("Running script...")

def update_status():
    # Update the status of your tasks here
    print("Updating status...")

root = tk.Tk()

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack()

run_button = tk.Button(root, text="Run", command=run_script)
run_button.pack()

status_list = tk.Listbox(root)
status_list.pack()

update_button = tk.Button(root, text="Update Status", command=update_status)
update_button.pack()

root.mainloop()