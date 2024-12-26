Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

' Get the folder path of the current VBS file
currentDir = FSO.GetParentFolderName(WScript.ScriptFullName)

' Build the path to the batch file in the same directory
batFile = currentDir & "\run.bat"

' Run the batch file
WshShell.Run batFile, 0, False
