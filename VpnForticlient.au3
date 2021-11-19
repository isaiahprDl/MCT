#NoTrayIcon
#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Icon=tvt2.ico
#AutoIt3Wrapper_UseX64=y
#AutoIt3Wrapper_Res_Description=VpnForticlient
#AutoIt3Wrapper_Res_Fileversion=1.10.5.1
#AutoIt3Wrapper_Res_Fileversion_AutoIncrement=y
#AutoIt3Wrapper_Res_ProductVersion=1.10.5
#AutoIt3Wrapper_Res_LegalCopyright=©Tivit 2021
#AutoIt3Wrapper_Res_Language=1046
#AutoIt3Wrapper_Res_Field=ProductName|VpnForticlient
#AutoIt3Wrapper_Res_Field=Made By|Isaías Pereira
#AutoIt3Wrapper_Res_Field=BuildDate|%date%
#AutoIt3Wrapper_Res_Field=AutoITVersion|%AutoItVer%
#AutoIt3Wrapper_Tidy_Stop_OnError=n
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****

;=======================================================================================================================================================
; BIBLIOTECAS USADAS
;=======================================================================================================================================================

#include <Date.au3>
#Include <GuiToolBar.au3>

;=======================================================================================================================================================
; EXECUTA FUNÇÃO FUNCAO VPN FORTCLIENT
;=======================================================================================================================================================

$a = ForticlientShow("forticlient")
$b = FortclientHide("forticlient")

If StringInStr($a,"conectado") = true Or StringInStr($b,"conectado") = true Then
    $vpn = RegWrite("HKEY_CURRENT_USER\SOFTWARE\TIVIT\MCT\Connectivity","VPN","REG_SZ","Sim")
Else
    $vpn = RegWrite("HKEY_CURRENT_USER\SOFTWARE\TIVIT\MCT\Connectivity","VPN","REG_SZ","Não")
EndIf

;=======================================================================================================================================================
; FUNCAO VPN FORTCLIENT --> ICONE NÃO OCULTO NO TRAYICON
;=======================================================================================================================================================

Func ForticlientShow($sToolTipTitle)

    Local $hSysTray_Handle = ControlGetHandle('[Class:Shell_TrayWnd]', '', '[Class:ToolbarWindow32;Instance:3]')

    Local $iSystray_ButCount = _GUICtrlToolbar_ButtonCount($hSysTray_Handle)

    Local $iSystray_ButtonNumber
    For $iSystray_ButtonNumber = 0 To $iSystray_ButCount - 1
        Local $sText = _GUICtrlToolbar_GetButtonText($hSysTray_Handle, $iSystray_ButtonNumber)
        If StringInStr($sText, $sToolTipTitle) = 1 Then Return $sText
    Next

    Return SetError(1, 0, "")

EndFunc

;=======================================================================================================================================================
; FUNCAO VPN FORTCLIENT --> ICONE OCULTO NO TRAYICON
;=======================================================================================================================================================

Func FortclientHide($sToolTipTitle)

    Local $hSysTray_Handle = ControlGetHandle('[Class:NotifyIconOverflowWindow]', '', '[Class:ToolbarWindow32;Instance:1]')

    Local $iSystray_ButCount = _GUICtrlToolbar_ButtonCount($hSysTray_Handle)

    Local $iSystray_ButtonNumber
    For $iSystray_ButtonNumber = 0 To $iSystray_ButCount - 1
        Local $sText = _GUICtrlToolbar_GetButtonText($hSysTray_Handle, $iSystray_ButtonNumber)
        If StringInStr($sText, $sToolTipTitle) = 1 Then Return $sText
    Next

    Return SetError(1, 0, "")

EndFunc