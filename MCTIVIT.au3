#NoTrayIcon
#RequireAdmin
#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Icon=Tools\tvt2.ico
#AutoIt3Wrapper_UseX64=y
#AutoIt3Wrapper_Res_Description=MCTIVIT
#AutoIt3Wrapper_Res_Fileversion=2021.9.0.129
#AutoIt3Wrapper_Res_Fileversion_AutoIncrement=y
#AutoIt3Wrapper_Res_ProductVersion=2021.09
#AutoIt3Wrapper_Res_LegalCopyright=©Tivit 2021
#AutoIt3Wrapper_Res_Language=1046
#AutoIt3Wrapper_Res_Field=ProductName|MCTIVIT
#AutoIt3Wrapper_Res_Field=Made By|Isaías Pereira
#AutoIt3Wrapper_Res_Field=BuildDate|%date%
#AutoIt3Wrapper_Res_Field=AutoITVersion|%AutoItVer%
#AutoIt3Wrapper_Tidy_Stop_OnError=n
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****

;=======================================================================================================================================================
; BIBLIOTECAS USADAS
;=======================================================================================================================================================
#include ".\Tools\Process_CPUUsage.au3"
;#include <_IniController.au3>
#include <Date.au3>
#Include <GuiToolBar.au3>

Global $DIR_TEMP = "C:\Windows\DMT\MCTIVIT"
If Not FileExists ($DIR_TEMP & '\') Then DirCreate ($DIR_TEMP & '\')

Global $FileTimeStamp = @YEAR & @MON & @MDAY & '_' & StringReplace(_NowTime(), ':', '')
Global $LOGFILE = $DIR_TEMP & '\' & "MCT" & '-' & $FileTimeStamp & ".log"
Global $sHostname = @ComputerName
$itimerdiff = TimerInit()

;=======================================================================================================================================================
; VALIDA SE A EXECUÇÃO ESTÁ COM ELEVAÇÃO ADMIN
;=======================================================================================================================================================
If Not IsAdmin() Then
	Exit
Else
	_LogMsg('Processo iniciado com direitos administrativos')
EndIf
;=======================================================================================================================================================
; END
;=======================================================================================================================================================

;=======================================================================================================================================================
; VALIDA A LINGUAGEM DO SO
;=======================================================================================================================================================
$osLang = @OSLang
If $osLang = "0416" Then
	$osLang = "Pt-BR"
ElseIf $osLang = "0409" Then
	$osLang = "En-US"
EndIf

_LogMsg("(I) OS Version     = " & @OSVersion)
_LogMsg("(I) OS Build       = " & @OSBuild)
_LogMsg("(I) OS ServicePack = " & @OSServicePack)
_LogMsg("(I) OS Arch        = " & @OSArch)
_LogMsg("(I) OS Lang        = " & $osLang)
_LogMsg("(I) Computer Name  = " & @ComputerName)
_LogMsg("(I) User Name      = " & @UserName)
;=======================================================================================================================================================
; END
;=======================================================================================================================================================

;=======================================================================================================================================================
; VALIDAÇÃO SE A TAREFA EXISTE
;=======================================================================================================================================================

RunWait(@ComSpec & ' /c ' & 'SCHTASKS /QUERY /TN "TESTE" > ' & @TempDir & '\MCT\CheckTask.ini', "", @SW_HIDE)

$taskCheck = @TempDir & '\MCT\CheckTask.ini'
$readfile = FileRead($taskCheck)

Sleep(5000)

If StringInStr($readfile,"Pronto") = True Or StringInStr($readfile,"Ready") = True Then
EndIf
If FileGetSize($taskCheck) = 0 Then
	$taskCreate = RunWait(@ComSpec & ' /c ' & 'SCHTASKS /CREATE /SC DAILY /TN "TESTE" /TR cmd.exe', "", @SW_HIDE)
EndIf
If StringInStr($readfile,"Desabilitado") = True Or StringInStr($readfile,"Disable") = True Or StringInStr($readfile,"Disabled") = True  Then
	$taskDelete = RunWait(@ComSpec & ' /c ' & 'SCHTASKS /DELETE /TN TESTE /f', "", @SW_HIDE)
	$taskCreate = RunWait(@ComSpec & ' /c ' & 'SCHTASKS /CREATE /SC DAILY /TN "TESTE" /TR cmd.exe', "", @SW_HIDE)
EndIf

;=======================================================================================================================================================
; END
;=======================================================================================================================================================

;=======================================================================================================================================================
; DELETA REGISTROS ANTERIORES
;=======================================================================================================================================================
$aRegDel = RegDelete("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT")
_LogMsg('(I) ' & 'Removendo entrada de registros anteriores')
;=======================================================================================================================================================
; END
;=======================================================================================================================================================

;=======================================================================================================================================================
; EXTRAI O ARQUIVO PRINCIPAL DO APP E DEMAIS ARQUIVOS PARA O FUNCIONAMENTO
;=======================================================================================================================================================
Global $DIR_MCT = @TempDir & '\MCT'
If Not FileExists ($DIR_MCT & '\') Then DirCreate ($DIR_MCT & '\')

$rc = FileInstall (".\Binarios\MCT.exe", $DIR_MCT & '\', 1)
$rc &= FileInstall (".\Binarios\acciscocrypto.dll", $DIR_MCT & '\', 1)
$rc &= FileInstall (".\Binarios\acciscossl.dll", $DIR_MCT & '\', 1)
$rc &= FileInstall (".\Binarios\PostBBL.exe", $DIR_MCT & '\', 1)
$rc &= FileInstall (".\Binarios\GetPerformBoot.vbs", $DIR_MCT & '\', 1)
$rc &= FileInstall (".\Binarios\msedgedriver.exe", $DIR_MCT & '\', 1)
$rc &= FileInstall (".\Binarios\PostParam.ps1", $DIR_MCT & '\', 1)
$rc &= FileInstall (".\Binarios\Config.ini", $DIR_MCT & '\', 1)
$rc &= FileInstall (".\Binarios\speedtest.exe", $DIR_MCT & '\', 1)
$rc &= FileInstall (".\Binarios\trac.exe", $DIR_MCT & '\', 1)
$rc &= FileInstall (".\Binarios\TrAPI.dll", $DIR_MCT & '\', 1)
$rc &= FileInstall (".\Binarios\vpnapi.dll", $DIR_MCT & '\', 1)
$rc &= FileInstall (".\Binarios\vpncli.exe", $DIR_MCT & '\', 1)
$rc &= FileInstall (".\Binarios\vpncommon.dll", $DIR_MCT & '\', 1)
$rc &= FileInstall (".\Binarios\vpncommoncrypt.dll", $DIR_MCT & '\', 1)
$rc &= FileInstall (".\Binarios\VpnForticlient.exe", $DIR_MCT & '\', 1)
$rc &= FileInstall (".\Binarios\xerces-c_3_2.dll", $DIR_MCT & '\', 1)

_LogMsg('(I) ' & 'Arquivos extraidos com sucesso')
;=======================================================================================================================================================
; END
;=======================================================================================================================================================

;=======================================================================================================================================================
; EXECUÇÃO DO MCT
;=======================================================================================================================================================
Run(@TempDir & '\MCT\MCT.exe',"",@SW_HIDE)
_LogMsg('(I) ' & 'MCT iniciado com sucesso')
;=======================================================================================================================================================
; END
;=======================================================================================================================================================

;=======================================================================================================================================================
; VALIDAÇÃO DO CONSUMO DE PROCESSADOR
;=======================================================================================================================================================
Local $hSplash, $sSplashText
Local $sProcess, $aProcUsage, $fUsage

$sProcess = "MCT.exe"

$aProcUsage = _ProcessUsageTracker_Create($sProcess)
Sleep(250)

Do

	$sSplashText=""
	$fUsage = _ProcessUsageTracker_GetUsage($aProcUsage)
	$sSplashText &= "'"&$sProcess&"' CPU usage: " & $fUsage & " %" & @CRLF
	$timeOut = StringLeft(TimerDiff($itimerdiff)/1000,4)

	Sleep(500)

	If ($fUsage > 90) Or ($timeOut == 1200) Then

		ProcessClose($sProcess)
		Sleep(500)
		ProcessClose("speedtesst.exe")
		Sleep(500)
		ProcessClose("speedtesst.exe")
		Sleep(500)
		ProcessClose("speedtesst.exe")
		Sleep(500)
		ProcessClose("speedtesst.exe")
		Sleep(500)
		ProcessClose("MCT.exe")

		If $fUsage >= 40 = True Then
			RegWrite("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Connectivity","Log","REG_SZ","01")
			RegWrite("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Connectivity","Download","REG_SZ","N/A")
			RegWrite("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Connectivity","Upload","REG_SZ","N/A")
			RegWrite("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Connectivity","Jitter","REG_SZ","N/A")
			RegWrite("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Connectivity","PacketLoss","REG_SZ","N/A")
			RegWrite("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Connectivity","Provider","REG_SZ","N/A")
			_LogMsg('(I) Execucao finalizada por ter excedido o limite de processamento')
			Exit
		EndIf

		If $timeOut == 1200 = True Then
			RegWrite("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Connectivity","Log","REG_SZ","02")
			RegWrite("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Connectivity","Download","REG_SZ","N/A")
			RegWrite("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Connectivity","Upload","REG_SZ","N/A")
			RegWrite("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Connectivity","Jitter","REG_SZ","N/A")
			RegWrite("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Connectivity","PacketLoss","REG_SZ","N/A")
			RegWrite("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Connectivity","Provider","REG_SZ","N/A")
			_LogMsg('(I) Execucao finalizada por ter excedido o tempo limite de execução')
			Exit
		EndIf

	Endif

Until Not ProcessExists ("MCT.exe")
;=======================================================================================================================================================
; END
;=======================================================================================================================================================

;=======================================================================================================================================================
; LOG ENCERRAMENTO POR EXECUÇÃO INTERNA DO APP
;=======================================================================================================================================================
$InternalEnvironment = RegRead("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Connectivity","InternalEnvironment")
If $InternalEnvironment = "Sim" Then
	_LogMsg('(I) Execucao abortada, o equipamento está conectado dentro do ambiente corporativo')
EndIf
;=======================================================================================================================================================
; END
;=======================================================================================================================================================


;=======================================================================================================================================================
; CRIAÇÃO DE LOGS DA APLICAÇÃO PARA ENVIO NA API
;=======================================================================================================================================================
$download = RegRead("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Release","Download")
$log = RegRead("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Release","Log")

If $download = "N/A" Then
	RegWrite("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Release","Log","REG_SZ","03")
ElseIf $log = 01 Then
ElseIf $log = 02 Then
ElseIf $InternalEnvironment = "Sim" Then
	RegWrite("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Release","Log","REG_SZ","04")
Else
	RegWrite("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Release","Log","REG_SZ","00")
EndIf
;=======================================================================================================================================================
; END
;=======================================================================================================================================================

;=======================================================================================================================================================
; CRIAÇÃO DOS LOGS NO ARQUIVO PARA VALIDAÇÃO DA LEITURA DE DADOS DO PROVEDOR DE TESTES DE VELOCIDADE_
;=======================================================================================================================================================
Sleep(5000)
If $InternalEnvironment = "Sim" Then
Else
	$dw = RegRead("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Connectivity","Download")
	_LogMsg('(I) Leitura de download: ' & $dw)

	$up = RegRead("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Connectivity","Upload")
		_LogMsg('(I) Leitura de upload: ' & $up)

	$pr = RegRead("HKEY_LOCAL_MACHINE\SOFTWARE\TIVIT\MCT\Connectivity","Provider")
		_LogMsg('(I) Leitura de provedor: ' & $pr)


FileDelete($DIR_MCT)
FileDelete(@TempDir & '\bootTime.xml')
FileDelete(@TempDir & '\TmpbootTime.xml')
_LogMsg('(I) MCT finalizado com sucesso')
EndIf

;=======================================================================================================================================================
; FUNCAO DE LOG
;=======================================================================================================================================================
Func _LogMsg($msgtext)
	Local $TimeStamp = @YEAR & "-" & @MON & "-" & @MDAY & " (" & _NowTime() & ")"
	If $LOGFILE Then FileWrite($LOGFILE, $TimeStamp & ' ' & $msgtext & @CRLF)
	Return
EndFunc   ;==>_LogMsg
;=======================================================================================================================================================
; END
;=======================================================================================================================================================