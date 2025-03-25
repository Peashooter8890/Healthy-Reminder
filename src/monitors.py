import ctypes
from ctypes import wintypes
        
def get_geometry_string(coordinates: list[int, int, int, int]) -> str:
    """Calculate the geometry string to use with tkinter for a window based on the provided coordinates.

    Args:
        coordinates (list[int, int, int, int]): Coordinates of the window.

    Returns:
        str: The geometry string for the window for tkinter. Ex. tk.Tk().window.geometry("geometry string goes here").
    """
    x1, y1, x2, y2 = coordinates
    width = x2 - x1
    height = y2 - y1
    return f'{width}x{height}+{x1}+{y1}'

def get_monitor_areas() -> list[list[int, int, int, int]]:
    """Get the coordinates of all monitors on the system.

    Returns:
        list[list[int, int, int, int]]: A list of monitor coordinates.
    """
    monitors = []
    
    # define RECT for Windows API
    class RECT(ctypes.Structure):
        _fields_ = [
            ("left", wintypes.LONG),
            ("top", wintypes.LONG),
            ("right", wintypes.LONG),
            ("bottom", wintypes.LONG),
        ]
    
    # define MONITORINFO for Windows API
    class MONITORINFO(ctypes.Structure):
        _fields_ = [
            ("cbSize", wintypes.DWORD),
            ("rcMonitor", RECT),
            ("rcWork", RECT),
            ("dwFlags", wintypes.DWORD),
        ]
    
    # callback function for EnumDisplayMonitors
    def monitor_enum_proc(hMonitor, hdcMonitor, lprcMonitor, lParam):
        monitor_info = MONITORINFO()
        monitor_info.cbSize = ctypes.sizeof(MONITORINFO)
        ctypes.windll.user32.GetMonitorInfoW(hMonitor, ctypes.byref(monitor_info))
        
        # extract monitor coordinates and append to list
        rect = monitor_info.rcMonitor
        monitors.append([rect.left, rect.top, rect.right, rect.bottom])
        return 1
    
    # create callable function pointer for the callback
    MONITORENUMPROC = ctypes.WINFUNCTYPE(
        wintypes.BOOL, wintypes.HMONITOR, wintypes.HDC, wintypes.LPRECT, wintypes.LPARAM
    )
    
    # call Windows API to enumerate monitors
    ctypes.windll.user32.EnumDisplayMonitors(
        None, None, MONITORENUMPROC(monitor_enum_proc), 0
    )
    
    return monitors
