import time

try:
    import win32api  # from pywin32
    print("pywin32: installed")
except ImportError:
    print("pywin32: not installed")

try:
    import numpy
    print("numpy: installed")
except ImportError:
    print("numpy: not installed")

try:
    import cv2  # opencv-python
    print("opencv-python: installed")
except ImportError:
    print("opencv-python: not installed")

try:
    import mss
    print("mss: installed")
except ImportError:
    print("mss: not installed")

time.sleep(30)