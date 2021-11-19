$url = 'https://tamcmdb.tivit.com/mctwps/' #atentar para a barra no fim

$b0 = $env:COMPUTERNAME
$b1 = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\TIVIT\MCT\Connectivity' -Name Download).Download
$b2 = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\TIVIT\MCT\Connectivity' -Name upload).upload
$b3 = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\TIVIT\MCT\Connectivity' -Name PacketLoss).PacketLoss
$b4 = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\TIVIT\MCT\Connectivity' -Name jitter).jitter
$b5 = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\TIVIT\MCT\Connectivity' -Name DateRun).DateRun
$b6 = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\TIVIT\MCT\Connectivity' -Name Provider).Provider
$b7 = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\TIVIT\MCT\User' -Name CorporateID).CorporateID
#$b8 = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\TIVIT' -Name Quality).Quality
$b9 = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\TIVIT\MCT\User' -Name UserName).UserName
$b10 = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\TIVIT\MCT\Connectivity' -Name VPN).VPN
$b11 = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\TIVIT\MCT\Release' -Name Version).Version
$b12 = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\TIVIT\MCT\Release' -Name Log).Log
$b13 = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\TIVIT\MCT\Hardware' -Name bootTime).bootTime
$b14 = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\TIVIT\MCT\Hardware' -Name DiskSize).DiskSize
$b15 = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\TIVIT\MCT\Clients' -Name Endpoint).Endpoint
$b16 = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\TIVIT\MCT\Clients' -Name Antivirus).Antivirus
$b17 = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\TIVIT\MCT\Hardware' -Name FreeSpace).FreeSpace

$postParams = 'ComputerName=' + $b0 + 
              '&Download=' + $b1 + 
              '&Upload=' + $b2 + 
              '&PacketLoss=' + $b3 + 
              '&Jitter=' + $b4 + 
              '&dateRun=' + $b5 + 
              '&Provider=' + $b6 + 
              '&CorporateID=' + $b7 + 
              #'&Quality=' + $b8 + 
              '&UserName=' + $b9 + 
              '&VPN=' + $b10 +
              '&Versao=' + '2021' +
              '&Log=' + '00' +
              '&bootTime=' + $b13 +
              '&diskSpace=' + $b14 +
              '&statusEndpoint=' + $b15 +
              '&statusAV=' + $b16 +
              '&FreeSpace=' + $b17

add-type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) {
            return true;
        }
    }
"@
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy

$url = $url + 'MCTAPI/New?' + $postParams 

$req = Invoke-WebRequest -Uri $url -Method Post -UseBasicParsing