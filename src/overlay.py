# custom imports
from src.monitors import *

# standard imports
import tkinter as tk
from tkinter import ttk

class MonitorOverlay:
    def __init__(self, message: str, closing_button_message: str = 'Close') -> None:
        """Create fullscreen overlays on all monitors with a custom message.
        
        Args:
            message (str): Message to display on the overlays.
            closing_button_message (str, optional): Text for the closing button.
        """
        self.message = message
        self.closing_button_message = closing_button_message
        self.monitor_coordinates = get_monitor_areas()
        self.windows = [] # store references to all overlay windows
        self.create_overlays()
    
    def create_overlays(self):
        """Create overlay windows for each monitor."""
        # create a hidden root window to drive the main loop
        self.root = tk.Tk()
        self.root.withdraw()
        
        # create a Toplevel window for each monitor
        for coords in self.monitor_coordinates:
            window = tk.Toplevel(self.root)
            self.windows.append(window)
            self.create_overlay_window(window, coords)
    
    def create_overlay_window(self, window: tk.Toplevel, coords: list[int, int, int, int], title: str = 'Fullscreen Overlay'):
        """Configure a Toplevel window as a fullscreen overlay.

        Args:
            window (tk.Toplevel): The overlay window reference.
            coords (list[int, int, int, int]): Coordinates of the window.
            title (str, optional): The title of the window.
        """
        # design the main overlay, remove custom decorations
        window.title(title)
        window.configure(bg='grey20')
        window.attributes('-alpha', 0.8)
        window.attributes('-topmost', True)
        window.overrideredirect(True)
        geometry = get_geometry_string(coords)
        window.geometry(geometry)
        
        # create white popup area in the center for message and closing button
        popup_frame = tk.Frame(window, bg='white', padx=40, pady=30, highlightbackground='black', highlightthickness=1)
        popup_frame.place(relx=0.5, rely=0.5, anchor='center')
        message_label = tk.Label(popup_frame, text=self.message, bg='white', font=('Arial', 14), wraplength=400)
        message_label.pack(pady=(0, 20))
        ok_button = ttk.Button(popup_frame, text=self.closing_button_message, command=self.close_overlay)
        ok_button.pack(pady=(0, 10))
        
        # force user to interact with the overlay
        window.bind('<Button-1>', self.intercept_click)
        window.update_idletasks()
    
    def intercept_click(self, event):
        """Prevent clicks from reaching the background. Used as a callback for the overlay windows."""
        return "break"
    
    def close_overlay(self, event=None):
        """Close all overlay windows. Used as a callback for the closing button."""
        self.root.destroy()
    
    def show(self) -> True:
        """Show the overlay on all monitors."""
        self.root.mainloop()
        