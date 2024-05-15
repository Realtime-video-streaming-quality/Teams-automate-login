import tkinter as tk
import threading
from time import sleep

class InfoWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Information Window")

        self.jsons_label = tk.Label(self.root, text="Number of jsons catched: 0")
        self.jsons_label.pack(padx=10, pady=5)

        self.participants_label = tk.Label(self.root, text="Number of participants: 0")
        self.participants_label.pack(padx=10, pady=5)

        self.cameras_label = tk.Label(self.root, text="Number of cameras: 0")
        self.cameras_label.pack(padx=10, pady=5)

        self.mics_label = tk.Label(self.root, text="Number of mics: 0")
        self.mics_label.pack(padx=10, pady=5)

        self.sharing_label = tk.Label(self.root, text="Is sharing: False")
        self.sharing_label.pack(padx=10, pady=5)

        self.close_button = tk.Button(self.root, text="Close", command=self.close_window)
        self.close_button.pack(pady=10)

    def update_info(self, jsons, participants, cameras, mics, sharing):
        self.jsons_label.config(text=f"Number of jsons catched: {jsons}")
        self.participants_label.config(text=f"Number of participants: {participants}")
        self.cameras_label.config(text=f"Number of cameras: {cameras}")
        self.mics_label.config(text=f"Number of mics: {mics}")
        self.sharing_label.config(text=f"Is sharing: {sharing}")

    def close_window(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

# Function to update information
def update_information(window):
    jsons = 10
    participants = 5
    cameras = 3
    mics = 2
    sharing = True
    window.update_info(jsons, participants, cameras, mics, sharing)

# Create the Tkinter window
window = InfoWindow()

# Create a thread to update information
thread = threading.Thread(target=update_information, args=(window,))
thread.start()

# Run the Tkinter window
window.run()
