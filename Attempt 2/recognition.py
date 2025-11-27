import sys
import os

# 1. Detect if running under PyPy, else re-exec self with PyPy
if "__pypy__" not in sys.builtin_module_names:
    print("Not running under PyPy. Relaunching with PyPy...", flush=True)
    # Path to your PyPy executable - adjust as needed
    pypy_path = r"C:\Users\dongj\pypy\pypy3.10-v7.3.15-win64\pypy3.exe"
    if not os.path.isfile(pypy_path):
        print(f"PyPy executable not found at {pypy_path}")
        sys.exit(1)
    # Relaunch self with all command line arguments
    os.execv(pypy_path, [pypy_path] + sys.argv)
    # execv replaces the current process; lines after this won't run

# If here, guaranteed running under PyPy
print("✓ Running under PyPy", flush=True)

# --- (rest of your import & main logic here) ---
import traceback

try:
    import winsound; print("✓ winsound imported", flush=True)
    import ctypes; print("✓ ctypes imported", flush=True)
    from ctypes import wintypes; print("✓ ctypes.wintypes imported", flush=True)
    import numpy as np; print("✓ numpy imported", flush=True)
    import random; print("✓ random imported", flush=True)
    import time; print("✓ time imported", flush=True)
    import cv2; print("✓ cv2 imported", flush=True)
    import mss; print("✓ mss imported", flush=True)
except Exception as e:
    print("Error importing modules:", e)
    traceback.print_exc()
    input("Press Enter to exit")
    raise SystemExit

width = 240
center_x = 1920 // 2
center_y = 1080 // 2
crosshairU = width // 2
region = {"top": center_y - crosshairU, "left": center_x - crosshairU, "width": width, "height": width}

# Load template
script_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(script_dir, "enemyIndic3.png")
template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
if template is None:
    print("error:template not found")
    sys.exit(1)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
w, h = template_gray.shape[::-1]
centerW, centerH = w // 2, h // 2

# Target color in RGB (from hex #ffffb3, colour picked from enemyIndic3.png)
target_color = (255, 255, 179)

# Real-time loop
while True:
    with mss.mss() as sct:
        frame_bgra = np.array(sct.grab(region))
    frame_rgb = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2RGB)
    frame_gray = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2GRAY)
    result = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= 0.60:
        # Check color at match location
        pixel = frame_rgb[max_loc[1], max_loc[0]]
        if np.allclose(pixel, target_color, atol=5):  # tolerance for slight variations
            X = max_loc[0] + centerW
            Y = max_loc[1] + centerH
            nX = -(crosshairU - X)
            nY = -(crosshairU - Y)
            print(f"{nX},{nY}", flush=True)
        else:
            print("", flush=True)  # color doesn't match
    else:
        print("", flush=True)  # print nothing (no move)
    time.sleep(0.010)  #to minimise CPU usage
