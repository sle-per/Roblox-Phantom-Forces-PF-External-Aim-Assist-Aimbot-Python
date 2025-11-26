; Optimization Settings
#MaxHotkeysPerInterval 99000000
#HotkeyInterval 99000000
#KeyHistory 0
ListLines Off
Process, Priority, , A
SetBatchLines, -1
SetKeyDelay, -1, -1
SetMouseDelay, -1
SetWinDelay, -1
SetControlDelay, -1

#Persistent
#SingleInstance Force
SetTitleMatchMode, 2

; Global variables to toggle the aimbot and manage search area
global aimbotEnabled := false
global centerX := A_ScreenWidth // 2
global centerY := A_ScreenHeight // 2
global searchWidth := 400
global searchHeight := 400
global accelerationFactor := 1.5  ; Example acceleration factor
global colorTolerance := 8  ; Color tolerance for PixelSearch
global sensitivityDistance := 200  ; Distance threshold for sensitivity adjustment

; Create GUI
Gui, Add, Button, x10 y10 w100 h30 gToggleAimbot, Toggle Aimbot (`~` hotkey)
Gui, Add, Text, x10 y50 w200 h20 vStatus, Aimbot Disabled
Gui, Add, Text, x10 y80 w100 h20, Search Width:
Gui, Add, Edit, x110 y80 w50 vSearchWidth, %searchWidth%
Gui, Add, Text, x10 y110 w100 h20, Search Height:
Gui, Add, Edit, x110 y110 w50 vSearchHeight, %searchHeight%
Gui, Show, w220 h150, Color Aimbot

; Main loop
SetTimer, AimbotLoop, 10  ; Adjust timer interval as needed

return

; Toggle aimbot function
ToggleAimbot:
    aimbotEnabled := !aimbotEnabled
    GuiControl,, Status, % (aimbotEnabled ? "Aimbot Enabled" : "Aimbot Disabled")
return

; Aimbot loop function
AimbotLoop:
    if (!aimbotEnabled) {
        return
    }

    ; Update search area dimensions from GUI inputs
    GuiControlGet, searchWidth, , SearchWidth
    GuiControlGet, searchHeight, , SearchHeight

    ; Calculate new search area boundaries
    left := centerX - (searchWidth // 2)
    top := centerY - (searchHeight // 2)
    right := centerX + (searchWidth // 2)
    bottom := centerY + (searchHeight // 2)

    ; Optimized screen capture and search for color
    PixelSearch, x, y, left, top, right, bottom, 0x00E6E6, %colorTolerance%, Fast RGB ; Searching for color 0x00E6E6 with dynamic tolerance

    if (!ErrorLevel) {
        ; Calculate relative movement
        xRel := x - centerX
        yRel := y - centerY

        ; Implement mouse acceleration control
        MouseMoveAccel(xRel, yRel)

        ; Move mouse relatively using mouse_event for direct mouse control
        DllCall("mouse_event", "UInt", 0x0001, "Int", xRel, "Int", yRel, "UInt", 0, "UInt", 0)
    }
return

; Function to control mouse acceleration
MouseMoveAccel(xRel, yRel) {
    ; Apply acceleration factor to movement
    xRel := Round(xRel * accelerationFactor)
    yRel := Round(yRel * accelerationFactor)
    
    ; Return adjusted values
    return {x: xRel, y: yRel}
}
