import traceback
import sys

print("Python version:", sys.version)
print("Starting script initialization...", flush=True)

try:
    import winsound
    print("✓ winsound imported", flush=True)
    import ctypes
    print("✓ ctypes imported", flush=True)
    from ctypes import wintypes
    print("✓ ctypes.wintypes imported", flush=True)
    import numpy as np
    print("✓ numpy imported", flush=True)
    import random
    print("✓ random imported", flush=True)
    import time
    print("✓ time imported", flush=True)
    import cv2
    print("✓ cv2 imported", flush=True)
    import mss
    print("✓ mss imported", flush=True)
except Exception as e:
    print("Error importing modules:", e)
    traceback.print_exc()
    input("Press Enter to exit")
    raise SystemExit

try:
    # Win32 API wrapper using ctypes (replaces pywin32 dependency)
    print("Initializing Win32 API...")
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    print("Win32 API initialized")

    # GetAsyncKeyState: returns key state (-32768 if pressed)
    def GetAsyncKeyState(vKey):
        return user32.GetAsyncKeyState(vKey)

    # Mouse event constants (Windows API)
    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004

    # Wrapper for mouse_event using SendInput (more reliable)
    class MOUSEINPUT(ctypes.Structure):
        _fields_ = [("dx", ctypes.c_long),
                    ("dy", ctypes.c_long),
                    ("mouseData", ctypes.c_ulong),
                    ("dwFlags", ctypes.c_ulong),
                    ("time", ctypes.c_ulong),
                    ("dwExtraInfo", ctypes.c_void_p)]
    
    class INPUT(ctypes.Structure):
        _fields_ = [("type", ctypes.c_ulong),
                    ("mi", MOUSEINPUT)]
    
    def mouse_event(dwFlags, dx, dy, dwData, dwExtraInfo):
        inp = INPUT()
        inp.type = 0  # INPUT_MOUSE
        inp.mi.dx = dx
        inp.mi.dy = dy
        inp.mi.dwFlags = dwFlags
        inp.mi.mouseData = dwData
        inp.mi.dwExtraInfo = dwExtraInfo
        user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

    #Config class to store important info about program capture
    class Config:
        def __init__(self):
            
            self.width = 1920
            self.height = 1080
            self.center_x = self.width // 2
            self.center_y = self.height // 2
            self.uniformCaptureSize = 240
            self.crosshairUniform = self.uniformCaptureSize // 2
            self.capture_left = self.center_x - self.crosshairUniform
            self.capture_top = self.center_y - self.crosshairUniform
            
            self.region = {"top": self.capture_top,"left": self.capture_left,"width": self.uniformCaptureSize,"height": self.uniformCaptureSize}
            
    config = Config()
    screenCapture = mss.mss()

    template = cv2.imread(r"C:\Users\dongj\Downloads\New folder\enemyIndic3.png", cv2.IMREAD_UNCHANGED)
    if template is None:
        print("ERROR: Template image 'enemyIndic3.png' not found!")
        print("Make sure the file exists in the same directory as this script:")
        import os
        print("Current directory:", os.getcwd())
        print("Files in current directory:", os.listdir('.'))
        input("Press Enter to exit")
        raise SystemExit
    
    
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    w, h = template_gray.shape[::-1]

    #template matching will give us top left corner coords which is not what we
    #want as we must hit the center of the rhombus, so we get half of template size
    #to offset coords towards the center of template (rhombus)
    centerW = w//2
    centerH = h//2

    #copy values of these 2 vars as to make access faster (accessing attribute from fn is slower than direct variable)
    crosshairU = config.crosshairUniform
    regionC = config.region

    #change sensitivity here
    robloxSensitivity = 1
    PF_MouseSensitivity = 0.185
    PF_AimSensitivity=1

    PF_sensitivity = PF_MouseSensitivity*PF_AimSensitivity
    movementCompensation = 0.2 #keep it in 0 to 1 range
    finalComputerSensitivityMultiplier = ((robloxSensitivity*PF_sensitivity)/0.55) + movementCompensation

    print("Script started! Monitoring screen...")
    print("Press keypad 6 to exit or Ctrl+C to force exit")
    loop_count = 0
    
    while True:
        loop_count += 1
        time.sleep(0.001)
        GameFrame = np.array(screenCapture.grab(regionC))
        GameFrame = cv2.cvtColor(GameFrame, cv2.COLOR_BGRA2GRAY)

        #change to 0x12 if you wanna close program with ALT
        #cv2.waitKey(1) & 0xFF == ord('q') or 
        if GetAsyncKeyState(0x6) < 0:
                print(f"Exit key pressed! (loops: {loop_count})")
                winsound.Beep(1000, 10)
                break
            
        elif GetAsyncKeyState(0x02) < 0:
            print("Mouse click detected!")
            result = cv2.matchTemplate(GameFrame, template_gray, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            #if aim is acting out too much try 0.85 (avoid false positives)
            if max_val >= 0.40:
                print(f"Enemy found! Confidence: {max_val:.2f}")

                X=max_loc[0]+centerW
                Y=max_loc[1]+centerH
                nX = (-(crosshairU - X))*finalComputerSensitivityMultiplier
                nY = (-(crosshairU - Y))*finalComputerSensitivityMultiplier
                
                print(f"Moving mouse by: ({int(nX)}, {int(nY)})")
                    
                mouse_event(MOUSEEVENTF_MOVE, int(nX), int(nY), 0, 0)
            else:
                print(f"Match found but below threshold: {max_val:.2f}")
                
        #cv2.imshow("test", GameFrame)
    
    print("bye")
    input("Press Enter to exit")

except Exception as e:
    print("\n" + "="*60)
    print("ERROR OCCURRED!")
    print("="*60)
    traceback.print_exc()
    print("="*60)
    input("\nPress Enter to exit")