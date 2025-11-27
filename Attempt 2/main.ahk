#NoEnv
#SingleInstance Force
SetBatchLines -1

global exec := ""
global aimbotEnabled := false

Gui, Add, Button, gStartScript, Start Script
Gui, Add, Button, gStopScript, Stop Script
Gui, Add, Button, gToggleAimbot, Toggle Aimbot
Gui, Add, Text, vStatusText, Status: Stopped
Gui, Add, Text, vPythonStatus, Python Status: Missing/Error
Gui, Add, Text, , Keybinds: F5 (Toggle Aimbot), F6 (Force Shutdown)
Gui, Show, , Aimbot Control

F5::
    Gosub, ToggleAimbot
return

F6::
    if (exec != "") {
        exec.Terminate()
    }
    ExitApp
return

StartScript:
    if (exec != "") {
        MsgBox, Script is already running.
        return
    }
    pypyPath := "C:\Users\dongj\pypy\pypy3.10-v7.3.15-win64\pypy3.exe"
    scriptPath := "C:\Users\dongj\Documents\screen_capture.py"
    shell := ComObjCreate("WScript.Shell")
    exec := shell.Exec("""" . pypyPath . """ """ . scriptPath . """")
    WinWait, ahk_pid %exec.ProcessID%
    WinHide, ahk_pid %exec.ProcessID%
    GuiControl, , StatusText, Status: Running
    GuiControl, , PythonStatus, Python Status: Working
    SetTimer, ReadOutput, 10
return

StopScript:
    if (exec != "") {
        exec.Terminate()
        exec := ""
        GuiControl, , StatusText, Status: Stopped
        GuiControl, , PythonStatus, Python Status: Missing/Error
        SetTimer, ReadOutput, Off
    }
return

ToggleAimbot:
    aimbotEnabled := !aimbotEnabled
    status := aimbotEnabled ? "Enabled" : "Disabled"
    GuiControl, , StatusText, Status: Running - Aimbot %status%
return

ReadOutput:
    if (exec != "" && exec.Status == 1) {
        exec := ""
        GuiControl, , StatusText, Status: Stopped
        GuiControl, , PythonStatus, Python Status: Missing/Error
        SetTimer, ReadOutput, Off
        return
    }
    if (exec != "" && !exec.StdOut.AtEndOfStream && aimbotEnabled) {
        line := exec.StdOut.ReadLine()
        if (line != "") {
            coords := StrSplit(line, ",")
            if (coords.Length() == 2 && RegExMatch(coords[1], "^-?\d+$") && RegExMatch(coords[2], "^-?\d+$")) {
                mouseX := coords[1]
                mouseY := coords[2]
                MouseMove, %mouseX%, %mouseY%, 0, R
            }
        }
    }
return

GuiClose:
    if (exec != "") {
        exec.Terminate()
    }
    ExitApp
