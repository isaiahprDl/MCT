' ---------------------------------------------------------------------------
'                        Variable creation
' ---------------------------------------------------------------------------
StrComputer = "."

Set Fso = CreateObject("Scripting.FileSystemObject")
Set objShell = WScript.CreateObject("Wscript.Shell")
Set WshShell = CreateObject("WScript.Shell")
Set objWMIService = GetObject("winmgmts:\\" & StrComputer & "\root\cimv2")

Dim xmlDoc, xmlHeader, Btime, MPBtime, PBtime, BStime, MAC, MacAddr
Set xmlDoc = CreateObject("Microsoft.XMLDOM")
xmlHeader ="<?xml version='1.0' encoding='iso-8859-1'?>" ' XML Header

Set tmpFolder = Fso.GetSpecialFolder(2) ' Define Temporary Folder

' ---------------------------------------------------------------------------
'                                 BootTime
' ---------------------------------------------------------------------------
' Clean TmpOutput XML File
If Fso.FileExists(tmpFolder & "\TmpbootTime.xml") Then
 Set OutputXML  = Fso.GetFile(tmpFolder & "\TmpbootTime.xml")
 OutputXML.Delete
End If

' Clean Output XML File
If Fso.FileExists(tmpFolder & "\bootTime.xml") Then
 Set OutputXML  = Fso.GetFile(tmpFolder & "\bootTime.xml")
 OutputXML.Delete
End If

' Request Events Log, create tmp XML file

QueryWevtutil = "cmd /c %windir%\system32\wevtutil.exe qe Microsoft-Windows-Diagnostics-Performance/Operational /rd:true /f:xml /c:1 /q:" & chr(34) & "*[System[(Level=1  or Level=2 or Level=3 or Level=4 or Level=0 or Level=5) and (EventID = 100)]]" & chr(34) &" > " & tmpFolder & "\TmpbootTime.xml"

'msgbox QueryWevtutil
WshShell.run(QueryWevtutil)
wscript.sleep 2*1000 ' Pause 2s

' Read the content of the temporary File
Set TmpOutputXML = Fso.OpenTextFile(tmpFolder & "\TmpbootTime.xml", 1, True)
file = Split(TmpOutputXML.ReadAll(), vbCrLf)
TmpOutputXML.Close()
Set TmpOutputXML = Nothing

' open the final file, Add the XML Header and the content of the tmp file
Set OutputXML = Fso.OpenTextFile(tmpFolder & "\bootTime.xml", 8, True)
OutputXML.WriteLine(xmlHeader)
for i = LBound(file) to UBound(file)
     OutputXML.WriteLine(file(i))
Next
OutputXML.Close()
Set OutputXML = Nothing

wscript.sleep 1*1000 ' Pause 1s

' Read the content of the previously created XML file
xmlDoc.Async = "false"
xmlDoc.Load(tmpFolder & "\bootTime.xml") ' XML File Loaded

For Each EventElement In xmlDoc.selectNodes("Event") 'Enter into the <Event> Node
 Set EventData = EventElement.selectNodes("EventData") 'Enter into the <EventData> Node
 For Each EventDataElement In EventData
  Set DataNode = EventDataElement.selectNodes("Data")
  For Each SubElement In DataNode
   DataNodeAttr = SubElement.getAttribute("Name")
   Select Case SubElement.getAttribute("Name")
    Case "BootTime"
     Btime = ""
     Btime = SubElement.text / 1000
    Case Else
     Output = "Not Found;Not Found;Not Found;"
   End Select
  Next

' Debug Mode
' MsgBox "Boot Time : " & Btime & vbcrlf & _
'   "Main Path Boot Time: " & MPBtime & vbcrlf & _
'   "Boot Post Boot Time  : " & PBtime
 Next 'End Second loop

Next 'End first loop

Set xmlDoc = Nothing

'----------------------------------------------------------------------------
'                    DEBUG/RESULT
'----------------------------------------------------------------------------
Set WshShell = WScript.CreateObject("WScript.Shell")

WshShell.RegWrite "HKEY_LOCAL_MACHINE\SOFTWARE\","REG_SZ"
WshShell.RegWrite "HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Hardware\PerformBootTime", Btime
