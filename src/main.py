# custom imports
from src.overlay import MonitorOverlay

# standard imports
import time
import schedule
import pystray
from PIL import Image
import threading

def show_overlay():
    overlay = MonitorOverlay('Exercise, stretch, drink water, pray, and take a break for the next 5 minutes.')
    overlay.show()

def exit_app(icon):
    icon.stop()
    global running
    running = False

def main():
    global overlay_active
    overlay_active = False
    
    global running
    running = True
    
    # schedule the task to run at xx:55 every hour
    schedule.every().hour.at(':55').do(show_overlay)
    
    # create and run the system tray icon
    icon_image = Image.open('src/assets/daemon.ico')
    icon = pystray.Icon('daemon', icon_image, 'Python Daemon', menu=pystray.Menu(
        pystray.MenuItem('Exit', exit_app)
    ))
    
    # start the icon in a separate thread
    icon_thread = threading.Thread(target=icon.run)
    icon_thread.daemon = True
    icon_thread.start()
    
    # main loop to run the daemon
    while running:
        schedule.run_pending()
        time.sleep(1) # check every second

if __name__ == '__main__':
    main()
