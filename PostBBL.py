import requests
import winreg as wreg
import os 
# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA LER O REGISTRO DE MAQUINA (HKEY_LOCAL_MACHINE)
# ----------------------------------------------------------------------------------------------------------------------
def RegRead_LM(param, path):
    registry_key = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, path, 0, (wreg.KEY_READ))
    value = wreg.QueryValueEx(registry_key, param)[0]     
    return value
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# ENVIO DAS INFORMAÇÕES
# ----------------------------------------------------------------------------------------------------------------------
compname = "ComputerName=" + os.environ['COMPUTERNAME']
downname = "&Download=" + RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity')
uploname = "&Upload=" + RegRead_LM("Upload", r'Software\TIVIT\MCT\Connectivity')
packname = "&PacketLoss=" + RegRead_LM("PacketLoss", r'Software\TIVIT\MCT\Connectivity')
jittname = "&Jitter=" + RegRead_LM("Jitter", r'Software\TIVIT\MCT\Connectivity')
datename = "&dateRun=" + RegRead_LM("DateRun", r'Software\TIVIT\MCT\Connectivity')
provname = "&Provider=" + RegRead_LM("Provider", r'Software\TIVIT\MCT\Connectivity')
vpnaname = "&VPN=" + RegRead_LM("VPN", r'Software\TIVIT\MCT\Connectivity')
corpname = "&CorporateID=" + RegRead_LM("CorporateID", r'Software\TIVIT\MCT\User')
username = "&UserName=" + RegRead_LM("UserName", r'Software\TIVIT\MCT\User')
versname = "&Versao=" + RegRead_LM("Version", r'Software\TIVIT\MCT\Release')
logrname = "&Log=" + RegRead_LM("Log", r'Software\TIVIT\MCT\Release')
bootname = "&bootTime=" + RegRead_LM("bootTime", r'Software\TIVIT\MCT\Hardware')
diskname = "&diskSpace=" + RegRead_LM("DiskSize", r'Software\TIVIT\MCT\Hardware')
freename = "&FreeSpace=" + RegRead_LM("FreeSpace", r'Software\TIVIT\MCT\Hardware')
stsename = "&statusEndpoint=" + RegRead_LM("Endpoint", r'Software\TIVIT\MCT\Clients')
stsaname = "&statusAV=" + RegRead_LM("Antivirus", r'Software\TIVIT\MCT\Clients')

url = "https://tamcmdb.tivit.com/mctwps/MCTAPI/new?" + compname + downname + uploname + packname + jittname + datename + provname + vpnaname + corpname + username + versname + logrname + logrname + bootname + diskname + freename + stsename + stsaname

payload={}
headers = {}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.status_code)