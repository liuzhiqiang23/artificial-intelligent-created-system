' Autostart: silently launch Ollama + local LLM chat server (no console window)
' Called by Windows Task Scheduler on logon.
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

root = fso.GetParentFolderName(WScript.ScriptFullName)
logPath = root & "\autostart.log"

Sub LogMsg(msg)
    On Error Resume Next
    Dim f
    Set f = fso.OpenTextFile(logPath, 8, True)
    f.WriteLine Now & "  " & msg
    f.Close
    On Error GoTo 0
End Sub

LogMsg "autostart begin, root=" & root

' Force the D: model store before anything starts (Task Scheduler env may
' miss this user variable, which made ollama list show an empty library)
shell.Environment("Process")("OLLAMA_MODELS") = "D:\ollama\models"

' --- 1. Start Ollama if not running (port 11434) ---
On Error Resume Next
Set http = CreateObject("MSXML2.XMLHTTP")
http.open "GET", "http://localhost:11434/api/version", false
http.send
If http.Status <> 200 Then
    LogMsg "starting Ollama..."
    dim ollama
    ollama = shell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Ollama\ollama.exe"
    shell.Run """" & ollama & """ serve", 0, False
    WScript.Sleep 5000
Else
    LogMsg "Ollama already running"
End If
On Error GoTo 0

' --- 2. Start chat server if not running (port 5000) ---
On Error Resume Next
Set http2 = CreateObject("MSXML2.XMLHTTP")
http2.open "GET", "http://127.0.0.1:5000/", false
http2.send
If http2.Status <> 200 Then
    LogMsg "starting chat_server..."
    shell.CurrentDirectory = root
    shell.Environment("Process")("PYTHONIOENCODING") = "utf-8"
    shell.Environment("Process")("OLLAMA_MODEL") = "qwen2.5-coder:7b"
    shell.Run """" & root & "\venv\Scripts\python.exe"" -u """ & root & "\chat_server.py""", 0, False
    LogMsg "chat_server launch command sent"
Else
    LogMsg "chat_server already running"
End If
On Error GoTo 0

LogMsg "autostart done"
